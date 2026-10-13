import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('installer', 'scripts/install.py')
server = load('server', 'mcp/artifacts_server.py')


class PackageTests(unittest.TestCase):
    def test_install_each_adapter_and_parse_configs(self):
        for harness in ('codex', 'claude', 'opencode', 'all'):
            with self.subTest(harness=harness), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'project'
                files = installer.install(root, harness, True)
                self.assertFalse(root.exists())
                self.assertEqual(files, installer.install(root, harness))
                for path in root.rglob('*.toml'):
                    tomllib.loads(path.read_text())
                for path in root.rglob('*.json'):
                    json.loads(path.read_text())
                (root / 'docs').mkdir()
                (root / 'docs/brief.md').write_text('test brief')
                command = [sys.executable, str(root / 'mcp/artifacts_server.py'), '--root', str(root)]
                requests = [ {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18'}}, {'jsonrpc':'2.0','method':'notifications/initialized'}, {'jsonrpc':'2.0','id':2,'method':'tools/list'}, {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'read_artifact','arguments':{'name':'brief.md'}}} ]
                run = subprocess.run(command, input='\n'.join(map(json.dumps, requests))+'\n', text=True, capture_output=True, check=True)
                replies = list(map(json.loads, run.stdout.splitlines()))
                self.assertEqual(len(replies), 3)
                self.assertEqual(replies[-1]['result']['content'][0]['text'], 'test brief')
                self.assertEqual(len(replies[1]['result']['tools']), 2)

    def test_collision_leaves_project_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'AGENTS.md').write_text('keep')
            with self.assertRaises(ValueError):
                installer.install(root, 'all')
            self.assertEqual(list(root.iterdir()), [root / 'AGENTS.md'])
            self.assertEqual((root / 'AGENTS.md').read_text(), 'keep')

    def test_escape_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'
            root.mkdir()
            (root / 'docs').mkdir()
            outside = Path(tmp) / 'secret'
            outside.write_text('secret')
            (root / 'docs/brief.md').symlink_to(outside)
            for name in ('../secret', 'brief.md'):
                with self.assertRaises(ValueError):
                    server.call_tool(root, 'read_artifact', {'name':name})
            (root / 'core').symlink_to(Path(tmp), target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(root, 'all')

    def test_status_is_not_semantic_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = json.loads(server.call_tool(Path(tmp), 'artifact_status', {}))
            self.assertEqual(result['semantic_gates'], 'not-evaluated')
            self.assertEqual(set(result['artifacts'].values()), {'missing-or-empty'})


if __name__ == '__main__':
    unittest.main()

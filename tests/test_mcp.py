import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SERVER = Path(__file__).resolve().parents[1] / 'skills/lx-textbook/assets/project/mcp/artifacts_server.py'
spec = importlib.util.spec_from_file_location('server', SERVER)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class MCPTests(unittest.TestCase):
    def test_stdio_handshake_and_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            (root / 'docs/brief.md').write_text('test brief')
            requests = [
                {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18'}},
                {'jsonrpc':'2.0','method':'notifications/initialized'},
                {'jsonrpc':'2.0','id':2,'method':'tools/list'},
                {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'read_artifact','arguments':{'name':'brief.md'}}},
            ]
            run = subprocess.run([sys.executable, str(SERVER), '--root', str(root)], input='\n'.join(map(json.dumps, requests))+'\n', text=True, capture_output=True, check=True)
            replies = list(map(json.loads, run.stdout.splitlines()))
            self.assertEqual(len(replies), 3)
            self.assertEqual(replies[0]['result']['protocolVersion'], '2025-06-18')
            self.assertEqual(len(replies[1]['result']['tools']), 2)
            self.assertEqual(replies[-1]['result']['content'][0]['text'], 'test brief')

    def test_escape_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'
            (root / 'docs').mkdir(parents=True)
            outside = Path(tmp) / 'secret'
            outside.write_text('secret')
            (root / 'docs/brief.md').symlink_to(outside)
            for name in ('../secret', 'brief.md'):
                with self.assertRaises(ValueError):
                    server.call_tool(root, 'read_artifact', {'name':name})

    def test_status_is_not_semantic_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = json.loads(server.call_tool(Path(tmp), 'artifact_status', {}))
            self.assertEqual(result['semantic_gates'], 'not-evaluated')
            self.assertEqual(set(result['artifacts'].values()), {'missing-or-empty'})


if __name__ == '__main__':
    unittest.main()

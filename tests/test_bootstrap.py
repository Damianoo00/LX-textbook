import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/lx-textbook'
INTAKE = {'topic': 'Fotosynteza', 'audience': 'Początkujący', 'goal': 'Przewidzieć wpływ światła', 'scope': 'Światło, substraty i produkty'}


class BootstrapTests(unittest.TestCase):
    def run_bootstrap(self, skill, target, intake, tmp):
        path = Path(tmp) / 'intake.json'
        path.write_text(json.dumps(intake, ensure_ascii=False), encoding='utf-8')
        return subprocess.run([sys.executable, str(skill / 'scripts/bootstrap.py'), str(target), '--intake', str(path)], text=True, capture_output=True)

    def test_standalone_skill_creates_configured_project_and_can_be_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / 'standalone-skill'
            shutil.copytree(SKILL, skill, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            project = Path(tmp) / 'textbook'
            run = self.run_bootstrap(skill, project, INTAKE, tmp)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads((project / 'docs/intake.json').read_text())['language'], 'Polish')
            self.assertIn(INTAKE['scope'], (project / 'docs/brief.md').read_text())
            self.assertFalse((project / 'docs/quality-gates.md').exists())
            self.assertIn('pending', (project / 'docs/run-state.md').read_text())
            for native in ('.agents', '.claude', '.opencode'):
                self.assertTrue((project / native / 'skills/lx-textbook/SKILL.md').is_file())
            for config in ('.codex/config.toml', '.mcp.json', 'opencode.json'):
                self.assertTrue((project / config).is_file())
            for config in project.rglob('*.toml'):
                tomllib.loads(config.read_text())
            for config in project.rglob('*.json'):
                json.loads(config.read_text())
            # Installed copy is portable too; no dependence on the original repository.
            another = Path(tmp) / 'another-textbook'
            run = self.run_bootstrap(project / '.claude/skills/lx-textbook', another, {**INTAKE, 'mode':'plan'}, tmp)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('Mode: plan', (another / 'docs/brief.md').read_text())

    def test_nonempty_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / 'existing'
            project.mkdir()
            (project / 'keep.txt').write_text('keep')
            run = self.run_bootstrap(SKILL, project, INTAKE, tmp)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(list(project.iterdir()), [project / 'keep.txt'])
            self.assertEqual((project / 'keep.txt').read_text(), 'keep')

    def test_invalid_intake_does_not_create_project(self):
        for change in ({'topic':''}, {'minutes':0}, {'minutes':True}, {'mode':'publish'}, {'sources':None}):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / 'textbook'
                run = self.run_bootstrap(SKILL, project, {**INTAKE, **change}, tmp)
                self.assertNotEqual(run.returncode, 0)
                self.assertFalse(project.exists())


if __name__ == '__main__':
    unittest.main()

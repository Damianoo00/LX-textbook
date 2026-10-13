#!/usr/bin/env python3
"""Create a configured LX project from agent-collected intake; no global writes."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

SKILL = Path(__file__).resolve().parents[1]


def create_project(destination, intake):
    if not isinstance(intake, dict):
        raise ValueError('Intake must be an object')
    for key in ('topic', 'audience', 'goal', 'scope'):
        if not isinstance(intake.get(key), str) or not intake[key].strip():
            raise ValueError(f'Required nonempty text: {key}')
    data = {'language': 'Polish', 'minutes': 20, 'example': 'Agent selects a continuous causal example',
            'mode': 'build', 'sources': 'Research authoritative sources; none supplied', 'exclusions': 'Keep to the goal and scope'}
    data.update(intake)
    if data['mode'] not in ('plan', 'build'):
        raise ValueError('Mode must be plan or build')
    if type(data['minutes']) is not int or data['minutes'] <= 0:
        raise ValueError('Minutes must be a positive integer')
    for key in ('language', 'example', 'sources', 'exclusions'):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f'Required nonempty text: {key}')
    target = Path(destination).expanduser().resolve()
    if target.is_relative_to(SKILL) or SKILL.is_relative_to(target):
        raise ValueError('Target cannot overlap source skill')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError('Target must be absent or empty; existing projects use the update workflow')
    assets = SKILL / 'assets/project'
    if not assets.is_dir():
        raise ValueError('Skill project assets are missing')
    target.parent.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns('__pycache__', '*.pyc')
    with tempfile.TemporaryDirectory(prefix='lx-bootstrap-', dir=target.parent) as tmp:
        draft = Path(tmp) / 'project'
        shutil.copytree(assets, draft, ignore=ignore)
        # Copy from the source, never from the growing draft.
        for folder in ('skills', '.agents/skills', '.claude/skills', '.opencode/skills'):
            shutil.copytree(SKILL, draft / folder / 'lx-textbook', ignore=ignore)
        docs = draft / 'docs'
        docs.mkdir(exist_ok=True)
        brief = f'''# Learning experience brief

Topic: {data['topic']}
Audience: {data['audience']}
Goal: {data['goal']}
Scope: {data['scope']}
Exclusions: {data['exclusions']}
Language: {data['language']}
Time budget: approximately {data['minutes']} minutes; verify with learners
Continuous example: {data['example']}
Sources: {data['sources']}
Mode: {data['mode']}
Delivery: browser-based interactive textbook with continuous causal prose
Constraints: verified claims, keyboard access, reduced motion, responsive reading
Success criterion: explain the mechanism, predict a change, transfer and state limits

## Execution

The user's request to build authorizes implementation after planning gates pass.
If mode is plan, stop after planning. Do not publish externally.
Native adapters have been written, but may require a new client session to load.
Continue now with available tools and sequential roles if native subagents are unavailable.
'''
        (docs / 'brief.md').write_text(brief, encoding='utf-8')
        (docs / 'intake.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        (docs / 'run-state.md').write_text('# Run state\n\nStage: brief complete, planning pending\nPlanning gates: pending\nImplementation: not started\nNext action: read brief and core/workflow.md; create knowledge-map\n', encoding='utf-8')
        if target.exists():
            target.rmdir()  # Empty only, rechecked by the filesystem.
        draft.rename(target)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    parser.add_argument('--intake', type=Path, required=True, help='JSON prepared by the agent after intake')
    args = parser.parse_args()
    try:
        target = create_project(args.destination, json.loads(args.intake.read_text(encoding='utf-8')))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error)+'\n')
    print(json.dumps({'project': str(target), 'brief': str(target/'docs/brief.md'),
                      'next': 'Continue planning and building with current session tools; native configuration reload may require a new session'}, ensure_ascii=False, indent=2))

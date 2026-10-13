#!/usr/bin/env python3
"""Create a portable LX learning project; no dependencies and no global writes."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile


def create_project(destination, topic, audience, language, minutes, example, mode):
    target = Path(destination).expanduser().resolve()
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError('Destination must be absent or an empty directory; nothing was overwritten.')
    if not topic.strip() or not audience.strip() or not language.strip() or minutes <= 0:
        raise ValueError('Topic, audience, language and a positive time budget are required.')
    skill = Path(__file__).resolve().parents[1]
    if target.is_relative_to(skill) or skill.is_relative_to(target):
        raise ValueError('Destination cannot overlap the source skill.')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Assemble before moving files into the empty destination; failures leave no partial project.
    with tempfile.TemporaryDirectory(prefix='lx-module-', dir=target.parent) as temporary:
        draft = Path(temporary) / 'project'
        (draft / 'docs').mkdir(parents=True)
        (draft / 'prompts').mkdir()
        shutil.copytree(skill, draft / 'skills' / 'lx-textbook', ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copyfile(skill / 'assets' / 'AGENTS.md', draft / 'AGENTS.md')
        brief = f'''# Learning experience brief

Topic: {topic}
Audience: {audience}
Goal: explain mechanisms, predict changes and transfer to a new example
Time budget: approximately {minutes} min, verify with learners
Language: {language}
Delivery: browser-based interactive textbook with continuous prose
Continuous example: {example or 'Select an example that carries the main causal chain'}
Constraints: verified sources, accessible keyboard interaction, reduced motion, mobile reading
Success criterion: learner explains the mechanism, predicts a change and states limits
Scope: agree meaningful exclusions from the topic before implementation
'''
        (draft / 'docs' / 'brief.md').write_text(brief, encoding='utf-8')
        instruction = ('Stop after planning and show gate results. Do not implement.' if mode == 'plan' else
                       'This request authorizes planning and implementation. Once planning gates pass, build one complete vertical slice, then finish the full scope in the brief; test and inspect desktop/mobile screenshots where permitted. Do not add a new approval checkpoint.')
        prompt = f'''Read AGENTS.md, skills/lx-textbook/SKILL.md and docs/brief.md. Use that workflow to create the requested interactive textbook. Continuous prose must explain and connect the mechanisms; embed diagrams and experiments where the text needs them. {instruction} Report files, assumptions, gate failures and the runnable result. Do not publish externally.
'''
        (draft / 'prompts' / 'start.md').write_text(prompt, encoding='utf-8')
        if not target.exists():
            draft.rename(target)
        else:
            for item in draft.iterdir():
                shutil.move(str(item), target / item.name)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='Absent or empty project directory')
    parser.add_argument('--topic', required=True)
    parser.add_argument('--audience', default='Complete beginner')
    parser.add_argument('--language', default='Polish')
    parser.add_argument('--minutes', type=int, default=20)
    parser.add_argument('--example', default='')
    parser.add_argument('--mode', choices=['plan','build'], default='build')
    args = parser.parse_args()
    try:
        target = create_project(**vars(args))
    except (ValueError,OSError) as error:
        parser.exit(1, str(error)+'\n')
    print(json.dumps({'project':str(target),'start_prompt':str(target/'prompts/start.md'),'skill':str(target/'skills/lx-textbook/SKILL.md'),'mode':args.mode}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()

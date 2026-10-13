#!/usr/bin/env python3
"""Install project-local LX files without overwriting existing files."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def install(destination, harness, dry_run=False):
    destination = Path(destination).resolve()
    if destination == ROOT or destination.is_relative_to(ROOT) or ROOT.is_relative_to(destination):
        raise ValueError('Target must not overlap this package')
    sources = [ROOT / p for p in ('AGENTS.md', 'core', 'agents', 'skills', 'mcp', 'prompts')]
    if harness in ('claude', 'all'):
        sources.append(ROOT / 'CLAUDE.md')
    files = {}
    for source in sources:
        for path in ([source] if source.is_file() else source.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                files[path.relative_to(ROOT)] = path
    for adapter in (('codex', 'claude', 'opencode') if harness == 'all' else (harness,)):
        base = ROOT / 'adapters' / adapter
        for path in base.rglob('*'):
            if path.is_file():
                files[path.relative_to(base)] = path
    # Native skill discovery: self-contained copies, no fragile symlinks.
    for folder in (('.agents', '.claude', '.opencode') if harness == 'all' else ({'codex': '.agents', 'claude': '.claude', 'opencode': '.opencode'}[harness],)):
        for path in (ROOT / 'skills').rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                files[Path(folder) / 'skills' / path.relative_to(ROOT / 'skills')] = path
    for relative in files:
        target = destination / relative
        if target.exists() or target.is_symlink():
            raise ValueError(f'Existing file: {target}; no files copied. Merge manually in a temporary project.')
        for parent in target.parents:
            if parent == destination.parent:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError(f'Unsafe target parent: {parent}')
    if not dry_run:
        for relative, source in files.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    return sorted(str(p) for p in files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    parser.add_argument('--harness', choices=['codex', 'claude', 'opencode', 'all'], default='all')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        print('\n'.join(install(args.destination, args.harness, args.dry_run)))
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')

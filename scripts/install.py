#!/usr/bin/env python3
"""Install the standalone skill into selected host directories. No network or overwrite."""
import argparse
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'skills/jiffi-video-studio'


def install(host, scope, root):
    if host not in ('codex', 'claude', 'both') or scope not in ('user', 'project'):
        raise ValueError('Unsupported host or install scope.')
    root = Path(root).expanduser().resolve()
    folders = {'codex': '.agents/skills', 'claude': '.claude/skills'}
    chosen = ['codex', 'claude'] if host == 'both' else [host]
    destinations = [root / folders[h] / 'jiffi-video-studio' for h in chosen]
    # Check all destinations before writing either host's install.
    for target in destinations:
        if target.exists() or target.is_symlink():
            raise ValueError(f'{target} already exists. Back it up or choose another destination; nothing was replaced.')
        if SOURCE == target or SOURCE in target.parents:
            raise ValueError('The install destination cannot be inside the source skill.')
    for target in destinations:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SOURCE, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return destinations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True, choices=['codex', 'claude', 'both'])
    parser.add_argument('--scope', choices=['user', 'project'], default='project')
    parser.add_argument('--root', type=Path, help='Project root, or a custom user root for isolated tests.')
    args = parser.parse_args()
    if args.scope == 'project' and not args.root:
        parser.error('--root is required for project scope')
    try:
        targets = install(args.host, args.scope, args.root or Path.home())
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    for target in targets:
        print(target)
    print('Start a fresh host session to discover the skill. Do not also enable the plugin copy.')

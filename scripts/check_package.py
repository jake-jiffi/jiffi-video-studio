#!/usr/bin/env python3
"""Validate the public package, including accidental private-file inclusion."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check():
    manifests = [json.loads((ROOT / p).read_text()) for p in
                 ['plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json']]
    for key in ('name', 'version', 'description', 'license', 'repository'):
        assert len({m[key] for m in manifests}) == 1, 'Manifest mismatch: ' + key
    assert manifests[0]['name'] == 'jiffi-video-studio'
    assert manifests[0]['license'] == 'MIT'
    assert (ROOT / 'LICENSE').is_file()
    skill = ROOT / 'skills/jiffi-video-studio'
    assert re.search(r'^name: jiffi-video-studio$', (skill / 'SKILL.md').read_text(), re.M)
    assert re.search(r'^description: .+', (skill / 'SKILL.md').read_text(), re.M)
    for location in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        m = json.loads((ROOT / location).read_text())
        assert m['name'] == 'jiffi-video-studio-marketplace'
        assert len(m['plugins']) == 1 and m['plugins'][0]['name'] == manifests[0]['name']
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    files = [ROOT / p for p in tracked if p]
    assert files, 'Stage the public files before checking the release package.'
    allowed_top = {'README.md', 'LICENSE', 'SECURITY.md', 'AGENTS.md', 'CLAUDE.md', '.gitignore',
                   'plugin.json', '.claude-plugin', '.codex-plugin', '.agents', '.github',
                   'skills', 'scripts', 'tests', 'docs'}
    banned_suffix = {'.mp4', '.mov', '.mp3', '.m4a', '.wav', '.drp', '.drt', '.blend', '.pem', '.key', '.woff2', '.otf', '.ttf'}
    for file in files:
        relative = file.relative_to(ROOT)
        assert relative.parts[0] in allowed_top, 'Unexpected public path: ' + str(relative)
        assert not file.is_symlink(), 'Release must contain actual files: ' + str(relative)
        assert file.suffix not in banned_suffix, 'Private/binary media in package: ' + str(relative)
        assert file.stat().st_size < 1024 * 1024, 'Unexpected large file: ' + str(relative)
        assert not file.name.startswith('.env'), 'Environment file in package'
        text = file.read_text(encoding='utf-8')
        assert not re.search(r'/(?:Users|home)/[A-Za-z0-9_.-]+/', text), 'Personal absolute path: ' + str(relative)
        assert not re.search(r'(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AIza[A-Za-z0-9_-]{30,})', text), 'Potential credential: ' + str(relative)
        if file.suffix == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                link = link.split('#')[0]
                if not link or '://' in link or link.startswith('mailto:'):
                    continue
                assert (file.parent / link).is_file(), f'Broken local link in {relative}: {link}'
    print(json.dumps({'status': 'pass', 'tracked_files': len(files), 'version': manifests[0]['version'],
                      'checks': ['manifest identity', 'marketplaces', 'local links', 'file allowlist', 'personal paths', 'common credential patterns']}, indent=2))


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('Package check failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Build a ZIP from tracked public-package files after validation."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / 'scripts/check_package.py')], check=True)
version = json.loads((root / 'plugin.json').read_text())['version']
files = sorted(p for p in subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0') if p)
out = root / 'dist'
out.mkdir(exist_ok=True)
archive = out / f'jiffi-video-studio-v{version}.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for relative in files:
        z.write(root / relative, 'jiffi-video-studio/' + relative)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(digest + '  ' + archive.name + '\n')
print(json.dumps({'file': str(archive), 'bytes': archive.stat().st_size, 'sha256': digest}, indent=2))

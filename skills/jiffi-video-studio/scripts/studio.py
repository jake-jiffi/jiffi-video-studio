#!/usr/bin/env python3
"""Local setup and synthetic media checks. Never submits a paid generation."""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

SETUP_ACTIONS = {
    'python': 'Install Python 3.9 or newer from python.org/downloads, then rerun this check in the execution host.',
    'studio-policy': 'Run studio.py init for this studio. Review the preserved or new AGENTS.md with the user; installation grants no budget or upload permission.',
    'ffmpeg': 'Install an FFmpeg build with libx264 and AAC from the routes listed at ffmpeg.org/download.html. Put ffmpeg and ffprobe on PATH, restart the host if needed, then run doctor and smoke.',
    'ffprobe': 'Install ffprobe with FFmpeg and put both executables on PATH. Restart the execution host if needed, then run doctor and smoke.',
    'node': 'If using the Gemini adapter or npm installation route, install Node.js 22 or newer from nodejs.org/en/download and restart the execution host.',
    'blender': 'Only if spatial rehearsal is selected, install Blender, provide its executable path and verify one small headless render.',
    'higgsfield-cli': 'For Higgsfield generation, follow higgsfield.ai/cli or pass --higgsfield-cli with an installed wrapper path. Then complete auth login in the provider flow.',
    'higgsfield-auth': 'After CLI installation, run higgsfield auth login, let the user sign in in the provider flow, select their workspace, then rerun doctor --mode generate --online. Never request a token in chat.',
    'higgsfield-account': 'Run higgsfield auth login and let the user complete the provider flow. Then rerun the online doctor; do not copy authentication output into chat.',
    'higgsfield-workspaces': 'After login, inspect available workspaces locally, ask which to use if ambiguous, select it with workspace set, then rerun the online doctor.',
    'higgsfield-models': 'Check the selected workspace and account entitlement, then retry the model catalogue read. Do not buy or upgrade a plan automatically.',
    'host-tools': 'Inspect this session for file, shell and media tools. If execution is unavailable, continue the scope in chat and explain how to resume in a connected local host.',
    'project-choices': 'Read the existing policy and brief. Ask only for missing route, output, provider, permission and budget choices that affect this project. Preserve earlier decisions.',
    'resolve': 'Only for Resolve editing, open Resolve Studio, verify local scripting or the configured MCP, then test a separate synthetic project and restore the previous project.',
    'gemini-review': 'Only if advisory review is selected, configure GEMINI_API_KEY or GOOGLE_API_KEY privately in the execution process environment, then run gemini-review.mjs --check. Never paste the value into chat, files or reports.',
}


def run(argv, timeout=30):
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)


def initialise(root):
    root = root.expanduser().resolve()
    # Existing studios may contain work. Never replace policy or registry files.
    root.mkdir(parents=True, exist_ok=True)
    for name in ('projects', 'setup'):
        (root / name).mkdir(exist_ok=True)
    names = {'AGENTS.md': SKILL / 'assets/studio-policy.md',
             'CLAUDE.md': SKILL / 'assets/claude-studio.md',
             'cast-registry.json': SKILL / 'assets/cast-registry.template.json',
             'setup/status.md': SKILL / 'assets/setup-status-template.md'}
    written, preserved = [], []
    for name, source in names.items():
        target = root / name
        try:
            with target.open('x', encoding='utf-8') as f:
                f.write(source.read_text(encoding='utf-8'))
            written.append(name)
        except FileExistsError:
            preserved.append(name)
    return {'studio': str(root), 'created': written, 'preserved': preserved,
            'next': 'Follow Stage 0 in the skill: inspect this host, ask only for missing project choices, run doctor for the chosen route and record non-secret setup evidence in setup/status.md.'}


def doctor(root, mode='edit', online=False, higgsfield_cli=None):
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Studio does not exist. Run init first.')
    checks = []
    def record(name, status, detail):
        checks.append({'name': name, 'status': status, 'detail': detail})
    record('python', 'pass' if sys.version_info >= (3, 9) else 'missing', sys.version.split()[0])
    record('studio-policy', 'pass' if (root / 'AGENTS.md').is_file() else 'missing',
           'AGENTS.md must record the user’s actual budget and provider/data choices.')
    record('free-disk', 'info', {'GiB': round(shutil.disk_usage(root).free / 1024**3, 2)})
    for binary in ('ffmpeg', 'ffprobe', 'node', 'blender'):
        path = shutil.which(binary)
        required = binary in ('ffmpeg', 'ffprobe') and mode != 'plan'
        if not path:
            record(binary, 'missing' if required else 'optional-missing', 'Not on PATH.')
            continue
        try:
            result = run([path, '-version' if binary.startswith('ff') else '--version'])
            valid = result.returncode == 0
            if binary == 'node' and valid:
                valid = int(result.stdout.strip().lstrip('v').split('.')[0]) >= 22
            # Only version tools are printed; account commands below are always redacted.
            record(binary, 'pass' if valid else ('missing' if required else 'optional-unavailable'),
                   ((result.stdout or result.stderr).splitlines() or ['No version output'])[0][:180])
        except (OSError, ValueError, subprocess.TimeoutExpired):
            record(binary, 'missing' if required else 'optional-unavailable', 'Version check failed.')
    cli = higgsfield_cli or shutil.which('higgsfield')
    if cli:
        cli = str(Path(cli).expanduser().resolve())
        try:
            result = run([cli, '--version'])
            present = result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            present = False
        record('higgsfield-cli', 'pass' if present else ('missing' if mode == 'generate' else 'optional-unavailable'),
               'Version command succeeded.' if present else 'Version command failed.')
    else:
        present = False
        record('higgsfield-cli', 'missing' if mode == 'generate' else 'optional-missing', 'Not on PATH; use --higgsfield-cli for a local wrapper.')
    if online and present:
        for label, args in [('higgsfield-account', ['account', 'status', '--json']),
                            ('higgsfield-workspaces', ['workspace', 'list', '--json']),
                            ('higgsfield-models', ['model', 'list', '--json'])]:
            try:
                result = run([cli] + args)
                ok = result.returncode == 0
                if ok:
                    json.loads(result.stdout)
                record(label, 'pass' if ok else 'blocked',
                       'Read succeeded; private account details omitted.' if ok else 'Read failed. Sign in, select a workspace and retry.')
            except (OSError, ValueError, subprocess.TimeoutExpired):
                record(label, 'blocked', 'Read failed or returned invalid JSON. No private output retained.')
    elif mode == 'generate':
        record('higgsfield-auth', 'not-tested', 'Run doctor --mode generate --online after signing in. No generation is submitted.')
    record('host-tools', 'not-tested', 'The agent must inspect this session’s shell, files, image inspection and browser tools. This command cannot see MCP connections.')
    record('project-choices', 'not-tested', 'An existing policy file does not prove the current project’s scope, permissions or budget are settled. Reuse existing decisions where applicable.')
    record('resolve', 'optional-not-tested', 'Test the selected MCP or local Python scripting route in a separate project. An installed app is not a verified connection.')
    record('gemini-review', 'optional-not-tested', 'Use gemini-review.mjs --check if authorised. Keys are not read by this doctor.')
    blocked = any(c['status'] in ('missing', 'blocked') for c in checks)
    next_steps = [{'check': c['name'], 'status': c['status'],
                   'optional': c['status'].startswith('optional-'), 'action': SETUP_ACTIONS[c['name']]}
                  for c in checks if c['status'] not in ('pass', 'info') and c['name'] in SETUP_ACTIONS]
    return {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'mode': mode,
            'local_prerequisites': 'blocked' if blocked else 'pass',
            'production_ready': False,
            'scope': 'Prerequisite inventory only. Account, tool execution, budget, data permission and human review need separate evidence.',
            'checks': checks, 'next_steps': next_steps}, 1 if blocked else 0


def smoke():
    """Use a temporary studio, including actual encode, decode and delivery checks."""
    import tempfile
    if not all(shutil.which(x) for x in ('ffmpeg', 'ffprobe')):
        raise ValueError('Install FFmpeg and ffprobe before the local smoke test.')
    with tempfile.TemporaryDirectory(prefix='jiffi-video-smoke-') as directory:
        root = Path(directory)
        initialise(root)
        project = root / 'projects/smoke'
        (project / 'export').mkdir(parents=True)
        (project / 'brief').mkdir()
        movie = project / 'export/smoke.mp4'
        cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-f', 'lavfi', '-i',
               'color=c=blue:s=96x96:r=24:d=1', '-f', 'lavfi', '-i',
               'sine=frequency=440:sample_rate=48000:duration=1', '-t', '1',
               '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
               '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(movie)]
        if run(cmd).returncode:
            raise ValueError('Synthetic encode failed. Check FFmpeg includes libx264 and AAC.')
        delivery = {'version': 1, 'exports': [{'file': 'smoke.mp4', 'aspect_ratio': '1:1',
                    'duration_seconds': {'min': 1, 'max': 1}, 'audio': 'required',
                    'width': 96, 'height': 96, 'frame_rate': 24}]}
        (project / 'brief/delivery.json').write_text(json.dumps(delivery))
        (project / 'export/credits.md').write_text('Video: Local FFmpeg colour fixture.\nAudio: Local FFmpeg sine fixture.\n')
        result = run([sys.executable, str(SKILL / 'scripts/verify_project.py'), str(root), 'smoke'])
        if result.returncode:
            raise ValueError('Synthetic delivery check failed: ' + result.stdout[-1000:])
        return {'status': 'pass', 'checks': ['synthetic H.264/AAC encode', 'full decode', 'delivery validator'],
                'paid_calls': 0, 'uploads': 0, 'scope': 'Local media plumbing only, not generation, Resolve or creative quality.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init', help='Create studio files without replacing existing files.')
    init.add_argument('studio', type=Path)
    check = sub.add_parser('doctor', help='Inventory local prerequisites. Network reads require --online.')
    check.add_argument('studio', type=Path)
    check.add_argument('--mode', choices=['plan', 'edit', 'generate'], default='edit')
    check.add_argument('--online', action='store_true')
    check.add_argument('--higgsfield-cli')
    sub.add_parser('smoke', help='Encode and validate synthetic media locally. No network or paid calls.')
    args = parser.parse_args()
    try:
        code = 0
        if args.command == 'init':
            result = initialise(args.studio)
        elif args.command == 'doctor':
            result, code = doctor(args.studio, args.mode, args.online, args.higgsfield_cli)
        else:
            result = smoke()
        print(json.dumps(result, indent=2))
        return code
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print('Setup failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

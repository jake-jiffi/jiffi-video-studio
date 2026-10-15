#!/usr/bin/env python3
"""Technical checks for a jiffi-video-studio project, not creative approval.

Usage: python3 verify_project.py <studio_root> <slug>
Exit 0 means the mechanical checks passed. Final picture, sound, captions,
rights, budget and gate decisions still require the documented review.
"""
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import date
from fractions import Fraction
from pathlib import Path

SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
CONSENT = re.compile(r'yes, (\d{4}-\d{2}-\d{2}), confirmed by ([^\r\n]+)', re.IGNORECASE)


def local_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('missing file path')
    relative = Path(value)
    if relative.is_absolute() or '..' in relative.parts or '\\' in value or ':' in value:
        raise ValueError('path must be relative and inside the studio')
    try:
        path = (root / relative).resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError('path cannot be resolved') from exc
    if root not in path.parents or not path.is_file():
        raise ValueError('path must resolve to a regular file inside the studio')
    return path


def run(argv, timeout=120):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError(result.stderr.strip()[-500:] or 'media command failed')
    return result.stdout


def probe(path, audio_policy='required'):
    data = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], 30))
    streams = data['streams']
    video = next((s for s in streams if s.get('codec_type') == 'video'
                  and not s.get('disposition', {}).get('attached_pic')), None)
    if not video:
        raise ValueError('no primary video stream')
    audio = [s for s in streams if s.get('codec_type') == 'audio']
    if audio_policy == 'required' and not audio:
        raise ValueError('no audio stream')
    if audio_policy == 'none' and audio:
        raise ValueError('expected a silent export without an audio stream')
    width, height = int(video['width']), int(video['height'])
    duration = float(video.get('duration') or data['format']['duration'])
    rate = Fraction(video['avg_frame_rate'])
    sar = Fraction(video.get('sample_aspect_ratio', '1:1').replace(':', '/'))
    if width <= 0 or height <= 0 or not math.isfinite(duration) or duration <= 0 or rate <= 0 or sar != 1:
        raise ValueError('invalid dimensions, duration, frame rate or non-square pixels')
    rotations = [video.get('tags', {}).get('rotate', 0)]
    rotations += [s['rotation'] for s in video.get('side_data_list', []) if 'rotation' in s]
    if any(not math.isfinite(float(r)) or float(r) % 360 != 0 for r in rotations):
        raise ValueError('bake rotation into the exported pixels')
    if video.get('codec_name') != 'h264' or video.get('pix_fmt') != 'yuv420p':
        raise ValueError('expected H.264 yuv420p delivery video')
    if any(a.get('codec_name') != 'aac' or a.get('sample_rate') != '48000' for a in audio):
        raise ValueError('expected AAC audio at 48 kHz')
    run(['ffmpeg', '-v', 'error', '-xerror', '-nostdin', '-i', str(path),
         '-map', '0:v', '-map', '0:a?', '-f', 'null', '-'], max(120, duration * 3 + 30))
    return width, height, duration, float(rate)


def positive_number(value):
    return type(value) in (int, float) and math.isfinite(value) and value > 0


def load_delivery(root, slug):
    relative = f'projects/{slug}/brief/delivery.json'
    candidate = root / relative
    if not candidate.exists() and not candidate.is_symlink():
        return None
    data = json.loads(local_file(root, relative).read_text(encoding='utf-8'))
    if (not isinstance(data, dict) or set(data) != {'version', 'exports'}
            or type(data['version']) is not int or data['version'] != 1):
        raise ValueError('expected version 1 and exports fields')
    outputs = data['exports']
    if not isinstance(outputs, list) or not outputs:
        raise ValueError('exports must be a non-empty array')
    seen = set()
    required = {'file', 'aspect_ratio', 'duration_seconds', 'audio'}
    optional = {'frame_rate', 'width', 'height', 'duration_group'}
    for output in outputs:
        if (not isinstance(output, dict) or not required <= set(output)
                or set(output) - required - optional):
            raise ValueError('each export needs file, aspect_ratio, duration_seconds and audio; unknown fields rejected')
        name = output['file']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*\.mp4', name):
            raise ValueError('file must be a simple .mp4 filename inside export/')
        if name.casefold() in seen:
            raise ValueError('duplicate export filename')
        seen.add(name.casefold())
        ratio = output['aspect_ratio']
        if not isinstance(ratio, str) or not re.fullmatch(r'[1-9][0-9]*:[1-9][0-9]*', ratio):
            raise ValueError('aspect_ratio must be a positive integer pair such as 16:9')
        bounds = output['duration_seconds']
        if (not isinstance(bounds, dict) or set(bounds) != {'min', 'max'}
                or not all(positive_number(bounds[k]) for k in ('min', 'max'))
                or bounds['min'] > bounds['max']):
            raise ValueError('duration_seconds needs finite positive min <= max')
        if output['audio'] not in ('required', 'none'):
            raise ValueError('audio must be required or none')
        if 'frame_rate' in output and not positive_number(output['frame_rate']):
            raise ValueError('frame_rate must be a finite positive number')
        if 'width' in output or 'height' in output:
            if not all(type(output.get(k)) is int and output[k] > 0 for k in ('width', 'height')):
                raise ValueError('width and height must both be positive integers')
        if 'duration_group' in output and (not isinstance(output['duration_group'], str) or not output['duration_group'].strip()):
            raise ValueError('duration_group must be a non-empty string')
    return outputs


def main(root, slug):
    root = Path(root).expanduser().resolve()
    fails, notes, groups = [], [], {}
    if not isinstance(slug, str) or not SLUG.fullmatch(slug):
        print('FAIL: slug must contain lowercase letters, numbers and single hyphens')
        return 1
    missing = [name for name in ('ffprobe', 'ffmpeg') if not shutil.which(name)]
    if missing:
        print('FAIL: required tools missing: ' + ', '.join(missing))
        return 1
    prefix = f'projects/{slug}/export/'
    try:
        outputs = load_delivery(root, slug)
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print(f'FAIL: delivery.json: {exc}')
        return 1
    if outputs is None:
        notes.append('Legacy two-format profile: no delivery.json, requested duration and resolution are not verified. New projects require a delivery spec.')
        outputs = [{'file': f'{slug}_{name}.mp4', 'aspect_ratio': ratio,
                    'audio': 'required', 'duration_group': 'legacy'}
                   for name, ratio in [('16x9', '16:9'), ('9x16', '9:16')]]
    for output in outputs:
        name = output['file']
        try:
            path = local_file(root, prefix + name)
            width, height, duration, rate = probe(path, output['audio'])
            want = float(Fraction(output['aspect_ratio'].replace(':', '/')))
            if abs(width / height - want) > 0.002:
                raise ValueError(f'{width}x{height}, expected {output["aspect_ratio"]}')
            if 'width' in output and (width, height) != (output['width'], output['height']):
                raise ValueError(f'{width}x{height}, expected {output["width"]}x{output["height"]}')
            if 'frame_rate' in output and abs(rate - output['frame_rate']) > 0.001:
                raise ValueError(f'{rate:.6f}fps, expected {output["frame_rate"]}')
            tolerance = 1 / rate + 0.001
            if 'duration_seconds' in output:
                bounds = output['duration_seconds']
                if not bounds['min'] - tolerance <= duration <= bounds['max'] + tolerance:
                    raise ValueError(f'{duration:.3f}s, outside requested {bounds["min"]} to {bounds["max"]} seconds (one-frame tolerance)')
            if 'duration_group' in output:
                groups.setdefault(output['duration_group'], []).append((duration, rate))
            notes.append(f'{name}: {width}x{height}, {duration:.3f}s, audio policy {output["audio"]}, full decode passed')
        except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError, subprocess.TimeoutExpired) as exc:
            fails.append(f'{name}: {exc}')
    for group, values in groups.items():
        if max(d for d, _ in values) - min(d for d, _ in values) > 1 / min(r for _, r in values) + 0.001:
            fails.append(f'exports in duration group {group} differ by more than one output frame')

    try:
        text = local_file(root, prefix + 'credits.md').read_text(encoding='utf-8')
        for kind in ('video', 'audio'):
            values = re.findall(rf'^[ \t]*(?:[-*][ \t]*)?{kind}[ \t]*:[ \t]*([^\n]+)', text, re.IGNORECASE | re.MULTILINE)
            placeholders = {'none', 'n/a', 'unknown', 'todo', 'tbd', 'pending', 'source', 'sources', 'video', 'audio'}
            if not any(v.strip() and v.strip().lower() not in placeholders for v in values):
                fails.append(f'credits.md needs a {kind.title()}: line naming its source')
    except (OSError, ValueError) as exc:
        fails.append(f'credits.md: {exc}')

    try:
        data = json.loads(local_file(root, 'cast-registry.json').read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('registry must be a JSON object')
        ids = set()
        for group in ('characters', 'locations', 'props'):
            entries = data.get(group, [])
            if not isinstance(entries, list):
                raise ValueError(f'{group} must be an array')
            for item in entries:
                if not isinstance(item, dict):
                    raise ValueError(f'{group} entries must be objects')
                identity = item.get('id')
                if not isinstance(identity, str) or not SLUG.fullmatch(identity) or identity in ids:
                    raise ValueError('registry IDs must be unique lowercase slugs')
                ids.add(identity)
                if group == 'characters':
                    if item.get('type') not in ('real', 'generated'):
                        raise ValueError(f'{identity}: type must be real or generated')
                    paths = [item.get('master')]
                    if item['type'] == 'generated' or 'sheet' in item:
                        paths.append(item.get('sheet'))
                    if item['type'] == 'real':
                        value = item.get('consent')
                        match = CONSENT.fullmatch(value) if isinstance(value, str) else None
                        if (not match or not match[2].strip() or match[2].strip().lower() in
                                {'unknown', 'todo', 'tbd', 'pending', '<reviewer name>', 'reviewer name'}
                                or any(c in match[2] for c in '<>')
                                or date.fromisoformat(match[1]) > date.today()):
                            raise ValueError(f'{identity}: consent must be yes, YYYY-MM-DD, confirmed by NAME, with an identified reviewer and valid non-future date')
                else:
                    paths = item.get('images')
                    if not isinstance(paths, list) or not paths:
                        raise ValueError(f'{identity}: images must be a non-empty array')
                paths = list(paths)
                for key in ('master', 'sheet'):
                    if group != 'characters' and key in item:
                        paths.append(item[key])
                if group == 'characters' and 'images' in item:
                    if not isinstance(item['images'], list):
                        raise ValueError(f'{identity}: images must be an array')
                    paths.extend(item['images'])
                for value in paths:
                    local_file(root, value)
    except (OSError, ValueError, TypeError) as exc:
        fails.append(f'cast-registry.json: {exc}')

    for note in notes:
        print('note:', note)
    if fails:
        print('FAIL')
        for failure in fails:
            print('  -', failure)
        return 1
    print('PASS: technical checks only. Picture, sound, captions, rights, budget and gate review remain required.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))

"""Exercise project-specific delivery against actual decoded synthetic media.

No provider jobs or real project media are changed.
"""
import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skills/jiffi-video-studio'
spec = importlib.util.spec_from_file_location('verify_project', SKILL / 'scripts/verify_project.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class DeliveryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_dir = tempfile.TemporaryDirectory(prefix='generic-delivery-media-')
        cls.media = Path(cls.media_dir.name)
        for name, duration, fps, sound in [('short', 2, 24, False),
                                            ('long', 181, 1, False),
                                            ('sound', 2, 24, True)]:
            command = ['ffmpeg', '-v', 'error', '-nostdin', '-f', 'lavfi',
                       '-i', f'color=c=blue:s=64x64:r={fps}']
            if sound:
                command += ['-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000']
            command += ['-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p']
            command += ['-c:a', 'aac'] if sound else ['-an']
            command += [str(cls.media / (name + '.mp4'))]
            subprocess.run(command, check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.media_dir.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='generic-delivery-check-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'projects/example'
        self.export = self.project / 'export'
        self.export.mkdir(parents=True)
        (self.project / 'brief').mkdir()
        (self.root / 'cast-registry.json').write_text('{}')
        (self.export / 'credits.md').write_text(
            'Video: Local synthetic colour fixture.\nAudio: Intentionally silent, no audio track.\n')
        shutil.copy2(self.media / 'short.mp4', self.export / 'short.mp4')
        self.output = {'file': 'short.mp4', 'aspect_ratio': '1:1',
                       'duration_seconds': {'min': 2, 'max': 2}, 'audio': 'none',
                       'width': 64, 'height': 64, 'frame_rate': 24}
        self.delivery = {'version': 1, 'exports': [self.output]}

    def run_check(self, expected, write_spec=True):
        if write_spec:
            (self.project / 'brief/delivery.json').write_text(json.dumps(self.delivery))
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            code = verifier.main(self.root, 'example')
        self.assertEqual(code, expected, text.getvalue())

    def test_single_two_second_square_silent_no_cast(self):
        self.run_check(0)

    def test_181_second_output_fully_decodes(self):
        shutil.copy2(self.media / 'long.mp4', self.export / 'short.mp4')
        self.output.update(duration_seconds={'min': 181, 'max': 181}, frame_rate=1)
        self.run_check(0)

    def test_short_film_and_long_programme_can_differ(self):
        shutil.copy2(self.media / 'long.mp4', self.export / 'long.mp4')
        self.delivery['exports'].append({'file': 'long.mp4', 'aspect_ratio': '1:1',
            'duration_seconds': {'min': 181, 'max': 181}, 'audio': 'none'})
        self.run_check(0)

    def test_matching_variants_cannot_differ(self):
        shutil.copy2(self.media / 'long.mp4', self.export / 'long.mp4')
        self.output['duration_group'] = 'same-edit'
        self.delivery['exports'].append({'file': 'long.mp4', 'aspect_ratio': '1:1',
            'duration_seconds': {'min': 181, 'max': 181}, 'audio': 'none',
            'duration_group': 'same-edit'})
        self.run_check(1)

    def test_wrong_requested_duration_rejected(self):
        self.output['duration_seconds'] = {'min': 3, 'max': 3}
        self.run_check(1)

    def test_one_frame_duration_tolerance(self):
        self.output['duration_seconds'] = {'min': 2 + 1/24, 'max': 2 + 1/24}
        self.run_check(0)

    def test_two_frame_duration_error_rejected(self):
        self.output['duration_seconds'] = {'min': 2 + 2/24, 'max': 2 + 2/24}
        self.run_check(1)

    def test_missing_required_audio_rejected(self):
        self.output['audio'] = 'required'
        self.run_check(1)

    def test_sound_output_with_audio_requirement(self):
        shutil.copy2(self.media / 'sound.mp4', self.export / 'short.mp4')
        self.output['audio'] = 'required'
        (self.export / 'credits.md').write_text('Video: Synthetic colour.\nAudio: Local sine fixture.\n')
        self.run_check(0)

    def test_unwanted_audio_in_silent_deliverable_rejected(self):
        shutil.copy2(self.media / 'sound.mp4', self.export / 'short.mp4')
        self.run_check(1)

    def test_wrong_aspect_rejected(self):
        self.output['aspect_ratio'] = '16:9'
        self.run_check(1)

    def test_wrong_resolution_rejected(self):
        self.output.update(width=1080, height=1080)
        self.run_check(1)

    def test_wrong_frame_rate_rejected(self):
        self.output['frame_rate'] = 30
        self.run_check(1)

    def test_missing_output_rejected(self):
        (self.export / 'short.mp4').unlink()
        self.run_check(1)

    def test_corrupt_media_rejected(self):
        (self.export / 'short.mp4').write_bytes(b'broken file')
        self.run_check(1)

    def test_invalid_contracts_rejected_without_fallback(self):
        original = json.loads(json.dumps(self.output))
        changes = [
            {'duration_seconds': {'min': 4, 'max': 2}},
            {'duration_seconds': {'min': 0, 'max': 2}},
            {'duration_seconds': {'min': True, 'max': 2}},
            {'duration_seconds': {'min': 1, 'max': float('inf')}},
            {'duration_seconds': {'min': 1, 'max': float('nan')}},
            {'aspect_ratio': '0:1'}, {'aspect_ratio': '1:0'},
            {'audio': 'optional'}, {'frame_rate': -1},
            {'width': 64, 'height': None}, {'duration_group': ''},
            {'file': '../short.mp4'}, {'file': '/tmp/short.mp4'},
            {'duration_second': {'min': 2, 'max': 2}},
        ]
        for change in changes:
            with self.subTest(change=change):
                self.delivery['exports'] = [{**original, **change}]
                self.run_check(1)

    def test_empty_output_list_rejected(self):
        self.delivery['exports'] = []
        self.run_check(1)

    def test_duplicate_output_rejected(self):
        self.delivery['exports'].append(dict(self.output))
        self.run_check(1)

    def test_malformed_json_rejected_without_fallback(self):
        (self.project / 'brief/delivery.json').write_text('{')
        self.run_check(1, write_spec=False)

    def test_broken_spec_symlink_rejected_without_fallback(self):
        (self.project / 'brief/delivery.json').symlink_to('missing.json')
        self.run_check(1, write_spec=False)

    def test_media_symlink_outside_studio_rejected(self):
        (self.export / 'short.mp4').unlink()
        (self.export / 'short.mp4').symlink_to(self.media / 'short.mp4')
        self.run_check(1)

    def test_recorded_real_subject_needs_no_generated_sheet(self):
        (self.root / 'cast-registry.json').write_text(json.dumps({'characters': [{
            'id': 'interviewee', 'type': 'real', 'master': 'projects/example/export/short.mp4',
            'consent': 'yes, 2026-09-01, confirmed by Alex Chen'}]}))
        self.run_check(0)

    def test_placeholder_and_future_consent_are_rejected(self):
        for consent in ['yes, 2020-01-01, confirmed by <reviewer name>',
                        'yes, 2020-01-01, confirmed by TBD',
                        'yes, 2020-01-01, confirmed by    ',
                        'yes, 2999-01-01, confirmed by Alex Chen',
                        'yes, 2020-13-40, confirmed by Alex Chen']:
            with self.subTest(consent=consent):
                (self.root / 'cast-registry.json').write_text(json.dumps({'characters': [{
                    'id': 'interviewee', 'type': 'real',
                    'master': 'projects/example/export/short.mp4', 'consent': consent}]}))
                self.run_check(1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

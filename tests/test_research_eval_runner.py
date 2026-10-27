"""Exercise the opt-in research host boundary; fake hosts are not skill acceptance."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'tools/run_research_evals.py'


@unittest.skipUnless(os.name == 'posix', 'POSIX process cleanup; not native Windows acceptance')
class ResearchEvalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.host = self.base / 'fake-codex'
        self.host.write_text('#!' + sys.executable + '\n' + '''import json, pathlib, sys, time
if '--version' in sys.argv:
 print('fake research host 1'); raise SystemExit
prompt = sys.stdin.read()
mode = pathlib.Path(sys.argv[0]).name
print(json.dumps({'type':'thread.started','thread_id':'fixture','argv':sys.argv[1:],'prompt':prompt}), flush=True)
if 'timeout' in mode: time.sleep(20)
if 'malformed' in mode: print('not JSON')
if 'mutation' in mode: pathlib.Path('skills/de-business-kit/SKILL.md').write_text('corrupted')
if 'symlink' in mode: pathlib.Path('escape').symlink_to('/etc')
print(json.dumps({'type':'item.completed','item':{'id':'web-1','type':'web_search','action':{'type':'open_page','url':'https://example.invalid/official'},'results':[{'url':'https://example.invalid/official','title':'Synthetic source'}]}}))
if 'claim-only' not in mode:
 print(json.dumps({'type':'item.completed','item':{'id':'calc-1','type':'command_execution','command':"python3 -B -c 'from decimal import Decimal; print(Decimal(120)*Decimal(19)/100)'",'aggregated_output':'22.80\\n','exit_code':0}}))
 if 'duplicate' in mode:
  print(json.dumps({'type':'item.completed','item':{'id':'calc-1','type':'command_execution','command':'echo 22.80','aggregated_output':'22.80','exit_code':0}}))
print(json.dumps({'type':'item.completed','item':{'id':'answer-1','type':'agent_message','text':'Synthetic answer: calculation checked and all correct.'}}))
if 'unfinished' in mode: print(json.dumps({'type':'item.started','item':{'id':'unfinished-1','type':'command_execution','status':'in_progress'}}))
if 'empty-answer' in mode: print(json.dumps({'type':'item.completed','item':{'id':'empty-1','type':'agent_message','text':''}}))
if 'incomplete' not in mode: print(json.dumps({'type':'turn.completed'}))
''')
        self.host.chmod(0o700)

    def cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(RUNNER), *map(str, args)],
                              capture_output=True, text=True, timeout=15)

    def run_case(self, mode='fake-codex', case='faq-foreign-saas-2026', timeout=5):
        host = self.base / mode
        if host != self.host:
            host.write_bytes(self.host.read_bytes()); host.chmod(0o700)
        out = self.base / (mode + '-evidence') / 'run'
        out.parent.mkdir(exist_ok=True)
        result = self.cli('--case', case, '--output', out, '--codex', host,
                          '--model', 'fixture-model', '--timeout', timeout)
        return result, out

    def load(self, out, file='report.json'):
        return json.loads((out / file).read_text())

    def fill_reviews(self, out, verdict='pass'):
        for p in (out / 'reviews').glob('*.json'):
            d = json.loads(p.read_text()); d['reviewer'] = 'Independent fixture reviewer'
            for item in d['criteria']:
                item.update(assessment=verdict, evidence=[{'line': 2}], note='Synthetic observed evidence')
            p.write_text(json.dumps(d))

    def test_opt_in_list_and_no_launch_without_selection(self):
        listed = self.cli('--list')
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual(len(json.loads(listed.stdout)['cases']), 32)
        self.assertEqual(len(json.loads(listed.stdout)['followups']), 11)
        r = self.cli('--output', self.base / 'unused', '--codex', self.host)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.base / 'unused').exists())

    def test_capture_preserves_output_but_never_self_certifies(self):
        r, out = self.run_case()
        self.assertEqual(r.returncode, 0, r.stderr)
        report = self.load(out)
        self.assertEqual(report['status'], 'pending_review')
        case = report['cases'][0]
        obs = self.load(out, case['observations'])
        self.assertEqual(obs['commands'][0]['output'], '22.80\n')
        self.assertEqual(obs['commands'][0]['exit_code'], 0)
        self.assertEqual(obs['sources'][0]['results'][0]['url'], 'https://example.invalid/official')
        self.assertEqual(obs['calculation_verification'], 'requires_independent_review')
        event = json.loads((out / case['transcript']).read_text().splitlines()[0])
        self.assertIn('--search', event['argv'])
        self.assertIn('read-only', event['argv'])
        self.assertIn('--ignore-user-config', event['argv'])
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', event['argv'])
        self.assertNotIn('Inspect official place-of-supply', event['prompt'])
        self.assertFalse((out / 'sessions' / case['id'] / 'evals').exists())
        self.assertTrue((out / 'source/scenarios.json').exists())
        self.assertEqual(report['host_version'], 'fake research host 1')
        self.assertTrue(case['started_at']); self.assertTrue(case['finished_at'])

    def test_claim_without_execution_stays_pending(self):
        r, out = self.run_case('claim-only-host')
        self.assertEqual(r.returncode, 0, r.stderr)
        obs = self.load(out, self.load(out)['cases'][0]['observations'])
        self.assertEqual(obs['commands'], [])
        self.assertEqual(obs['calculation_verification'], 'requires_independent_review')
        summary = self.cli('--summarize', out)
        self.assertEqual(summary.returncode, 0, summary.stderr)
        self.assertEqual(self.load(out, 'assessment.json')['status'], 'pending_review')

    def test_followup_replays_observed_answer_without_criteria(self):
        r, out = self.run_case(case='faq-founding-year-2026')
        self.assertEqual(r.returncode, 0, r.stderr)
        cases = self.load(out)['cases']; self.assertEqual(len(cases), 2)
        prompt = (out / cases[1]['request']).read_text()
        self.assertIn('Synthetic answer: calculation checked', prompt)
        self.assertIn('Correction to my facts', prompt)
        self.assertNotIn('Revise the founding-year premise explicitly', prompt)
        self.assertEqual(cases[1]['variant'], 'context_replay')

    def test_incomplete_base_blocks_followup_and_preserves_attempt(self):
        r, out = self.run_case('incomplete-host', case='faq-founding-year-2026')
        self.assertEqual(r.returncode, 1, r.stderr)
        cases = self.load(out)['cases']
        self.assertEqual(cases[0]['mechanical_status'], 'failed')
        self.assertEqual(cases[1]['host_status'], 'blocked')
        self.assertFalse((out / 'sessions' / cases[1]['id']).exists())
        self.assertTrue((out / cases[0]['transcript']).exists())

    def test_malformed_and_duplicate_events_fail_closed(self):
        for mode in ['malformed-host', 'duplicate-host']:
            with self.subTest(mode=mode):
                r, out = self.run_case(mode)
                self.assertEqual(r.returncode, 1, r.stderr)
                self.assertEqual(self.load(out)['cases'][0]['mechanical_status'], 'failed')

    def test_timeout_preserves_evidence_and_failure(self):
        r, out = self.run_case('timeout-host', timeout=.1)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertEqual(self.load(out)['cases'][0]['host_status'], 'timed_out')
        self.assertTrue((out / self.load(out)['cases'][0]['transcript']).exists())

    def test_snapshot_mutation_and_symlink_fail_without_traversal(self):
        for mode in ['mutation-host', 'symlink-host']:
            with self.subTest(mode=mode):
                r, out = self.run_case(mode)
                self.assertEqual(r.returncode, 1, r.stderr)
                self.assertEqual(self.load(out)['cases'][0]['mechanical_status'], 'failed')

    def test_refuses_existing_checkout_and_symlinked_output(self):
        existing = self.base / 'existing'; existing.mkdir(); (existing / 'keep').write_text('preserve')
        alias = self.base / 'alias'; alias.symlink_to(self.base, target_is_directory=True)
        for out in [existing, ROOT / 'research-evidence', alias / 'new']:
            r = self.cli('--case', 'faq-foreign-saas-2026', '--output', out, '--codex', self.host, '--model', 'fixture')
            self.assertEqual(r.returncode, 2, r.stderr)
        self.assertEqual((existing / 'keep').read_text(), 'preserve')

    def test_review_verdicts_require_exact_bindings_and_evidence(self):
        r, out = self.run_case(); self.assertEqual(r.returncode, 0, r.stderr)
        self.fill_reviews(out)
        r = self.cli('--summarize', out); self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.load(out, 'assessment.json')['status'], 'passed')
        p = next((out / 'reviews').glob('*.json')); good = p.read_text(); d = json.loads(good)
        d['bindings']['transcript_sha256'] = '0' * 64; p.write_text(json.dumps(d))
        self.assertEqual(self.cli('--summarize', out).returncode, 2)
        self.assertFalse((out / 'assessment.json').exists(), 'A rejected re-review must not leave a stale passed summary')
        d = json.loads(good); d['criteria'][0]['evidence'] = []; p.write_text(json.dumps(d))
        self.assertEqual(self.cli('--summarize', out).returncode, 2)
        p.write_text(good); self.fill_reviews(out, 'uncertain')
        self.assertEqual(self.cli('--summarize', out).returncode, 0)
        self.assertEqual(self.load(out, 'assessment.json')['status'], 'uncertain')
        self.fill_reviews(out, 'fail'); self.assertEqual(self.cli('--summarize', out).returncode, 0)
        self.assertEqual(self.load(out, 'assessment.json')['status'], 'failed')

    def test_unfinished_execution_or_empty_final_cannot_trigger_replay(self):
        for mode in ['unfinished-host', 'empty-answer-host']:
            with self.subTest(mode=mode):
                r, out = self.run_case(mode, case='faq-founding-year-2026')
                self.assertEqual(r.returncode, 1, r.stderr)
                rows = self.load(out)['cases']
                self.assertEqual(rows[0]['mechanical_status'], 'failed')
                self.assertEqual(rows[1]['host_status'], 'blocked')

    def test_full_pilot_runs_all_thirty_two_bases_and_eleven_replays(self):
        out = self.base / 'all-evidence'
        r = self.cli('--all', '--output', out, '--codex', self.host, '--model', 'fixture')
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = self.load(out)['cases']
        self.assertEqual(len(rows), 43)
        self.assertEqual(sum(c['variant'] == 'context_replay' for c in rows), 11)
        self.assertTrue(all(c['mechanical_status'] == 'passed' for c in rows))

    def test_selected_invoice_and_deadline_replays_keep_their_own_facts(self):
        out = self.base / 'selected-evidence'
        r = self.cli('--case', 'faq-small-invoice-2026', '--case', 'faq-vat-deadline-2026',
                     '--case', 'faq-small-invoice-2026', '--output', out,
                     '--codex', self.host, '--model', 'fixture')
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = self.load(out)['cases']; self.assertEqual(len(rows), 4)
        prompts = {c['id']: (out / c['request']).read_text() for c in rows}
        invoice = prompts['faq-small-invoice-2026-followup']
        deadline = prompts['faq-vat-deadline-2026-followup']
        self.assertIn('EUR 250.01', invoice)
        self.assertNotIn('Dauerfristverlängerung', invoice)
        self.assertIn('Dauerfristverlängerung', deadline)
        self.assertNotIn('EUR 250.01', deadline)
        for prompt in (invoice, deadline):
            self.assertIn('Synthetic answer: calculation checked', prompt)
            self.assertNotIn('Revise the small-invoice premise', prompt)
            self.assertNotIn('Replace the unextended deadline', prompt)

    def test_work_permission_followup_replays_answer_without_oracle(self):
        r, out = self.run_case(case='faq-work-permission-2026')
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = self.load(out)['cases']
        self.assertEqual(len(rows), 2)
        prompt = (out / rows[1]['request']).read_text()
        self.assertIn('Synthetic answer: calculation checked', prompt)
        self.assertIn('Erwerbstätigkeit erlaubt', prompt)
        self.assertNotIn('Revise the employment-only premise', prompt)
        review = self.load(out, 'reviews/' + rows[1]['id'] + '.json')
        self.assertTrue(any('Revise the employment-only premise' in c['criterion'] for c in review['criteria']))

    def test_historical_reviews_use_frozen_criteria_after_runner_changes(self):
        r, out = self.run_case(); self.assertEqual(r.returncode, 0, r.stderr)
        self.fill_reviews(out)
        sys.path.insert(0, str(ROOT / 'tools'))
        self.addCleanup(sys.path.remove, str(ROOT / 'tools'))
        spec = importlib.util.spec_from_file_location('research_fixture', RUNNER)
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        with mock.patch.object(runner, 'COMMON_CRITERIA', ('Future policy changed',)):
            self.assertEqual(runner.summarize(str(out)), 0)
        self.assertEqual(self.load(out, 'assessment.json')['status'], 'passed')

    def test_review_hash_binds_the_bytes_actually_assessed(self):
        r, out = self.run_case(); self.assertEqual(r.returncode, 0, r.stderr)
        self.fill_reviews(out)
        sys.path.insert(0, str(ROOT / 'tools'))
        self.addCleanup(sys.path.remove, str(ROOT / 'tools'))
        spec = importlib.util.spec_from_file_location('research_race', RUNNER)
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        p = next((out / 'reviews').glob('*.json')); original = p.read_bytes()
        real_read = runner.host.bounded_read
        changed = False
        def changing_read(path):
            nonlocal changed
            data = real_read(path)
            if Path(path) == p and not changed:
                changed = True
                edited = json.loads(data)
                edited['criteria'][0]['assessment'] = 'fail'
                p.write_text(json.dumps(edited))
            return data
        with mock.patch.object(runner.host, 'bounded_read', side_effect=changing_read):
            self.assertEqual(runner.summarize(str(out)), 0)
        import hashlib
        assessment = self.load(out, 'assessment.json')
        self.assertEqual(assessment['cases'][0]['review_sha256'], hashlib.sha256(original).hexdigest())
        self.assertNotEqual(assessment['cases'][0]['review_sha256'], hashlib.sha256(p.read_bytes()).hexdigest())

    def test_wrong_summary_directory_preserves_unrelated_assessment_file(self):
        folder = self.base / 'unrelated'; folder.mkdir()
        protected = folder / 'assessment.json'; protected.write_text('user-owned content')
        r = self.cli('--summarize', folder)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(protected.read_text(), 'user-owned content')

    def test_transcript_tampering_refuses_assessment(self):
        r, out = self.run_case(); self.assertEqual(r.returncode, 0, r.stderr)
        self.fill_reviews(out)
        case = self.load(out)['cases'][0]
        (out / case['transcript']).write_text('{}\n')
        r = self.cli('--summarize', out)
        self.assertEqual(r.returncode, 2)
        self.assertIn('integrity', r.stderr.lower())


if __name__ == '__main__':
    unittest.main()

"""CI selection must save work without turning missing evidence into a pass."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('ci_plan', ROOT / 'tools/ci_plan.py')
ci = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ci)
SHA, TREE, HEAD = 'a' * 40, 'b' * 40, 'c' * 40
REPO = 'synthetic/kit'


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Synthetic')
        self.git('config', 'user.email', 'ci@example.invalid')
        self.write('docs/guide.md', '# Guide\n')
        self.write('skills/example.py', 'print(1)\n')
        self.commit()
        self.base = self.git('rev-parse', 'HEAD')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')

    def plan(self, event_name='pull_request', ref='refs/pull/1/merge', **kwargs):
        event = {'number': 1, 'pull_request': {'base': {'sha': self.base, 'ref': 'main'}}, 'before': self.base}
        return ci.plan(self.root, event_name, ref, event, REPO, **kwargs)

    def test_docs_and_marketplace_use_light_checks(self):
        self.write('docs/guide.md', '# Changed\n')
        self.write('.claude-plugin/marketplace.json', '{}\n')
        self.commit()
        result = self.plan()
        self.assertEqual(result['mode'], 'docs')
        self.assertEqual(result['tree'], self.git('rev-parse', 'HEAD^{tree}'))

    def test_runtime_moved_into_docs_still_requires_full(self):
        self.git('mv', 'skills/example.py', 'docs/example.md')
        self.commit()
        self.assertEqual(self.plan()['mode'], 'full')

    def test_skill_instructions_ci_version_and_unknown_paths_require_full(self):
        for path in ('skills/de-business-kit/SKILL.md', '.github/workflows/checks.yml',
                     'VERSION', 'tools/unknown.md', 'docs/example.py', 'new.config'):
            with self.subTest(path=path):
                self.git('reset', '--hard', self.base)
                self.write(path, 'changed\n')
                self.commit()
                self.assertEqual(self.plan()['mode'], 'full')

    def test_tag_and_reusable_call_force_full_for_docs(self):
        self.write('docs/guide.md', '# Changed\n')
        self.commit()
        self.assertEqual(self.plan('push', 'refs/tags/v1')['mode'], 'full')
        self.assertEqual(self.plan(force_full=True)['mode'], 'full')

    def test_missing_base_and_empty_diff_do_not_skip(self):
        self.assertEqual(self.plan()['mode'], 'full')
        self.base = '0' * 40
        self.assertEqual(self.plan()['mode'], 'full')

    def test_failed_api_on_runtime_push_falls_back_to_full(self):
        self.write('skills/example.py', 'print(2)\n')
        self.commit()
        def offline(_):
            raise OSError('offline')
        self.assertEqual(self.plan('push', 'refs/heads/main', api=offline)['mode'], 'full')

    def test_document_mode_changes_require_full_checks(self):
        self.git('update-index', '--chmod=+x', 'docs/guide.md')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'executable document')
        self.assertEqual(self.plan()['mode'], 'full')

    def test_main_reuses_actual_checkout_tree_from_successful_pr_gate(self):
        self.write('skills/example.py', 'print(2)\n')
        self.commit()
        evidence = EvidenceTests()
        evidence.setUp()
        evidence.pr['merge_commit_sha'] = self.git('rev-parse', 'HEAD')
        evidence.gate['steps'][-1]['name'] = 'Validated PR / 3 / full / ' + self.git('rev-parse', 'HEAD^{tree}')
        result = self.plan('push', 'refs/heads/main', api=evidence.api)
        self.assertEqual((result['mode'], result['full'], result['reused_run']), ('reuse', 'false', '9'))

    def test_cli_writes_validated_outputs_for_release_without_api(self):
        event = self.root / 'event.json'
        event.write_text('{}')
        output = self.root / 'outputs'
        env = dict(os.environ, GITHUB_EVENT_NAME='push', GITHUB_REF='refs/tags/v1',
                   GITHUB_EVENT_PATH=str(event), GITHUB_REPOSITORY=REPO,
                   GITHUB_OUTPUT=str(output), GITHUB_STEP_SUMMARY=str(self.root / 'summary'))
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/ci_plan.py'), 'plan'],
                                cwd=self.root, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = dict(line.split('=', 1) for line in output.read_text().splitlines())
        self.assertEqual(values['mode'], 'full')
        self.assertEqual(values['tree'], self.git('rev-parse', 'HEAD^{tree}'))

    def test_light_checks_refuse_missing_or_mismatched_marketplace_tag(self):
        self.git('-c', 'tag.gpgsign=false', 'tag', 'v1.0.0')
        source = {'ref': 'v1.0.0', 'sha': self.base}
        def catalog():
            self.write('.claude-plugin/marketplace.json', json.dumps({'plugins': [{'source': source}]}))
        catalog()
        ci.require_pinned_tag(self.root)
        source['sha'] = 'd' * 40
        catalog()
        with self.assertRaises(ValueError):
            ci.require_pinned_tag(self.root)
        source.update(ref='v9.0.0', sha=self.base)
        catalog()
        with self.assertRaises(subprocess.CalledProcessError):
            ci.require_pinned_tag(self.root)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.pr = {'number': 3, 'state': 'closed', 'merged_at': '2026-10-27T12:00:00Z',
                   'merge_commit_sha': SHA, 'base': {'ref': 'main', 'repo': {'full_name': REPO}},
                   'head': {'sha': HEAD, 'repo': {'full_name': REPO}}}
        self.workflow = {'id': 5, 'path': '.github/workflows/checks.yml', 'state': 'active'}
        self.run = {'id': 9, 'workflow_id': 5, 'path': '.github/workflows/checks.yml',
                    'event': 'pull_request', 'status': 'completed', 'conclusion': 'success',
                    'head_sha': HEAD, 'repository': {'full_name': REPO},
                    'head_repository': {'full_name': REPO}, 'run_attempt': 2}
        self.gate = {'name': 'Checks gate', 'status': 'completed', 'conclusion': 'success',
                     'steps': [{'name': 'Validate required results', 'status': 'completed', 'conclusion': 'success'},
                               {'name': 'Validated PR / 3 / full / ' + TREE, 'status': 'completed', 'conclusion': 'success'}]}
        self.jobs = [self.gate]
        self.calls = []

    def api(self, path):
        self.calls.append(path)
        if '/commits/' in path:
            return [self.pr]
        if path.endswith('/workflows/checks.yml'):
            return self.workflow
        if '/workflows/5/runs?' in path:
            return {'total_count': 1, 'workflow_runs': [self.run]}
        if '/runs/9/attempts/2/jobs?' in path:
            return {'total_count': len(self.jobs), 'jobs': self.jobs}
        raise AssertionError(path)

    def reuse(self):
        return ci.reusable_pr_run(REPO, SHA, TREE, self.api)

    def test_exact_tree_uses_latest_attempt_not_pr_head_alone(self):
        self.assertEqual(self.reuse(), 9)
        self.assertTrue(any('/attempts/2/jobs?' in p for p in self.calls))
        self.gate['steps'][-1]['name'] = 'Validated PR / 3 / full / ' + 'd' * 40
        self.assertIsNone(self.reuse())

    def test_other_pr_or_docs_only_coverage_cannot_supply_runtime_evidence(self):
        for marker in ('Validated PR / 99 / full / ' + TREE, 'Validated PR / 3 / docs / ' + TREE):
            self.gate['steps'][-1]['name'] = marker
            self.assertIsNone(self.reuse())

    def test_untrusted_or_incomplete_run_never_reused(self):
        for key, bad in (('event', 'push'), ('conclusion', 'failure'), ('status', 'in_progress'),
                         ('workflow_id', 6), ('path', '.github/workflows/other.yml'),
                         ('head_sha', 'd' * 40), ('repository', {'full_name': 'other/repo'}),
                         ('head_repository', {'full_name': 'fork/kit'}), ('run_attempt', 0)):
            with self.subTest(key=key):
                old = self.run[key]
                self.run[key] = bad
                self.assertIsNone(self.reuse())
                self.run[key] = old

    def test_wrong_merge_fork_and_base_ref_never_reused(self):
        original = copy.deepcopy(self.pr)
        for mutate in (lambda p: p.update(merge_commit_sha='d' * 40),
                       lambda p: p.update(merged_at=None),
                       lambda p: p['base'].update(ref='other'),
                       lambda p: p['head']['repo'].update(full_name='fork/kit')):
            self.pr = copy.deepcopy(original)
            mutate(self.pr)
            self.assertIsNone(self.reuse())

    def test_missing_duplicate_skipped_or_failed_marker_refuses_reuse(self):
        original = copy.deepcopy(self.gate)
        for steps in ([], [original['steps'][-1]] * 2,
                      [dict(original['steps'][-1], conclusion='skipped')],
                      [dict(original['steps'][-1], conclusion='failure')]):
            self.gate['steps'] = steps
            self.assertIsNone(self.reuse())
        self.gate = original
        self.jobs = [original, copy.deepcopy(original)]
        self.assertIsNone(self.reuse())

    def test_partial_job_or_run_page_is_not_evidence(self):
        for key in ('jobs', 'workflow_runs'):
            def api(path):
                value = self.api(path)
                if isinstance(value, dict) and key in value:
                    value['total_count'] += 1
                return value
            self.assertIsNone(ci.reusable_pr_run(REPO, SHA, TREE, api))

    def test_newer_failed_run_blocks_an_older_success(self):
        def api(path):
            value = self.api(path)
            if isinstance(value, dict) and 'workflow_runs' in value:
                newer = dict(self.run, id=10, conclusion='failure')
                value.update(total_count=2, workflow_runs=[newer, self.run])
            return value
        self.assertIsNone(ci.reusable_pr_run(REPO, SHA, TREE, api))

    def test_gate_cannot_pass_with_missing_or_failed_dependencies(self):
        needs = {name: {'result': 'success'} for name in ci.REQUIRED_JOBS}
        needs['plan']['outputs'] = {'mode': 'full', 'full': 'true', 'tree': TREE, 'pr': '3'}
        ci.validate_gate(needs)
        for bad in ('failure', 'cancelled', 'skipped'):
            changed = copy.deepcopy(needs)
            changed['native-utilities']['result'] = bad
            with self.assertRaises(ValueError):
                ci.validate_gate(changed)
        del needs['plan']
        with self.assertRaises(ValueError):
            ci.validate_gate(needs)

    def test_light_gate_requires_successful_quick_checks_and_deliberate_skips(self):
        needs = {name: {'result': 'skipped'} for name in ci.REQUIRED_JOBS}
        needs['plan'] = {'result': 'success', 'outputs': {'mode': 'docs', 'full': 'false', 'tree': TREE, 'pr': '3'}}
        needs['quick'] = {'result': 'success'}
        ci.validate_gate(needs)
        needs['plan']['outputs']['mode'] = 'unknown'
        with self.assertRaises(ValueError):
            ci.validate_gate(needs)

    def test_quick_failure_or_inconsistent_selection_cannot_emit_evidence(self):
        needs = {name: {'result': 'skipped'} for name in ci.REQUIRED_JOBS}
        needs['plan'] = {'result': 'success', 'outputs': {'mode': 'docs', 'full': 'false', 'tree': TREE, 'pr': '3'}}
        needs['quick'] = {'result': 'failure'}
        with self.assertRaises(ValueError):
            ci.validate_gate(needs)
        needs['quick']['result'] = 'success'
        needs['plan']['outputs']['full'] = 'true'
        with self.assertRaises(ValueError):
            ci.validate_gate(needs)


if __name__ == '__main__':
    unittest.main()

"""Canonical Python tasks remain actionable in the native read-only overview."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / 'skills/de-business-kit/scripts'
sys.path.insert(0, str(SCRIPTS))
import workspace as ws

SHELL = shutil.which('powershell.exe') or shutil.which('pwsh')


@unittest.skipUnless(SHELL, 'Native overview requires an available PowerShell runtime')
class NativeTaskOverviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'Private tasks'
        ws.init_workspace(self.root, 2026, 'en')

    def task(self, identifier, **changes):
        record = dict(schema_version=1, id=identifier, title='Synthetic ' + identifier,
                      owner='owner', status='pending', depends_on=[])
        record.update(changes)
        if record['status'] != 'pending':
            saved = ws.save_entry(self.root, 'tasks', dict(record, status='pending'))
            return ws.save_entry(self.root, 'tasks', record, saved['sha256'])
        return ws.save_entry(self.root, 'tasks', record)

    def view(self):
        run = subprocess.run([SHELL, '-NoProfile', '-NonInteractive', '-File',
                              str(SCRIPTS / 'windows.ps1'), '-Action', 'overview',
                              '-Root', str(self.root), '-Period', '2026-10'],
                             capture_output=True, text=True, timeout=40)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        return json.loads((self.root / result['json_path']).read_text()), result

    def test_empty_workspace_asks_for_business_task(self):
        snapshot, result = self.view()
        self.assertEqual(result['next_action'], 'choose_task')
        self.assertEqual(snapshot['active_tasks'], [])
        self.assertIsNone(snapshot['next_task_id'])

    def test_undated_and_other_month_tasks_continue_in_stable_order_without_writes(self):
        self.task('undated', note='Discuss <script>facts</script>')
        self.task('pending', due_date='2099-12-01', deadline_source='Explicit user target')
        self.task('working', status='in_progress', due_date='2099-12-01', deadline_source='Explicit user target')
        before = (self.root / '00_admin/tasks.json').read_bytes()
        snapshot, result = self.view()
        self.assertEqual(snapshot['next_action'], 'continue_task')
        self.assertEqual(snapshot['next_task_id'], 'working')
        self.assertEqual([row['id'] for row in snapshot['active_tasks']], ['working', 'pending', 'undated'])
        self.assertEqual(snapshot['active_tasks'][2]['evidence_status'], 'not_recorded')
        html = (self.root / result['html_path']).read_text()
        self.assertIn('Discuss &lt;script&gt;facts&lt;/script&gt;', html)
        self.assertIn('Explicit user target', html)
        self.assertEqual((self.root / '00_admin/tasks.json').read_bytes(), before)

    def test_cancelled_dependency_blocks_and_stale_completed_ancestor_needs_review(self):
        evidence = self.root / '00_admin/proof.txt'
        evidence.write_text('Synthetic preserved result')
        saved = self.task('ancestor')
        ws.save_entry(self.root, 'tasks', dict(schema_version=1, id='ancestor', title='Ancestor',
                      owner='owner', status='completed', evidence_file='00_admin/proof.txt'), saved['sha256'])
        saved = self.task('middle', depends_on=['ancestor'])
        ws.save_entry(self.root, 'tasks', dict(schema_version=1, id='middle', title='Middle', owner='owner',
                      status='completed', depends_on=['ancestor'], evidence_file='00_admin/proof.txt'), saved['sha256'])
        self.task('child', depends_on=['middle'])
        saved = self.task('cancelled')
        ws.save_entry(self.root, 'tasks', dict(schema_version=1, id='cancelled', title='Cancelled',
                      owner='owner', status='cancelled'), saved['sha256'])
        self.task('blocked', depends_on=['cancelled'])
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_task_id'], 'child')
        self.assertEqual(snapshot['active_tasks'][0]['pending_dependencies'], ['cancelled'])
        evidence.write_text('Changed result')
        snapshot, _ = self.view()
        self.assertEqual(snapshot['health'], 'ok')
        self.assertEqual(snapshot['next_action'], 'review_tasks')
        self.assertIsNone(snapshot['next_task_id'])
        child = next(row for row in snapshot['active_tasks'] if row['id'] == 'child')
        self.assertEqual(child['readiness'], 'needs_review')
        self.assertEqual(child['pending_dependencies'], ['ancestor', 'middle'])

    def test_malformed_graph_fails_closed(self):
        self.task('one')
        path = self.root / '00_admin/tasks.json'
        for dependencies in (['missing'], ['one'], 'one'):
            records = json.loads(path.read_text())
            records[0]['depends_on'] = dependencies
            path.write_text(json.dumps(records))
            snapshot, _ = self.view()
            self.assertEqual(snapshot['next_action'], 'repair')
            self.assertIsNone(snapshot['next_task_id'])

    def test_binary_completion_evidence_matches_python_readiness(self):
        from casefiles import summary
        proof = self.root / '00_admin/proof.pdf'
        proof.write_bytes(b'%PDF-1.7\n%\xff\xfe\x80\x81\nSynthetic binary evidence')
        self.task('done', status='completed', evidence_file='00_admin/proof.pdf')
        self.task('continue', depends_on=['done'])
        python_view = summary.collect(self.root, '2026-10')
        native_view, _ = self.view()
        self.assertEqual(native_view['active_tasks'], python_view['active_tasks'])
        self.assertEqual(native_view['next_task_id'], 'continue')

    def test_accounting_corruption_suppresses_previously_collected_tasks(self):
        self.task('one')
        (self.root / '04_accounting/register.json').write_text('{broken')
        snapshot, result = self.view()
        self.assertEqual(snapshot['next_action'], 'repair')
        self.assertIsNone(snapshot['next_task_id'])
        self.assertEqual(snapshot['active_tasks'], [])
        self.assertNotIn('Synthetic one', (self.root / result['html_path']).read_text())

    def test_hardlink_to_mutable_profile_cannot_establish_task_readiness(self):
        from casefiles import summary
        profile = self.root / '01_profile/business.json'
        proof = self.root / '00_admin/proof.json'
        proof.write_bytes(profile.read_bytes())
        self.task('one', evidence_file='00_admin/proof.json')
        proof.unlink()
        os.link(profile, proof)
        with self.assertRaises(ws.WorkspaceError):
            summary.collect(self.root, '2026-10')
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_action'], 'repair')
        self.assertEqual(snapshot['active_tasks'], [])

    def test_safe_stale_task_keeps_an_independent_task_actionable(self):
        evidence = self.root / '00_admin/proof.txt'
        evidence.write_text('Synthetic task evidence')
        self.task('A', evidence_file='00_admin/proof.txt')
        self.task('a')
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_task_id'], 'A')
        evidence.unlink()
        snapshot, _ = self.view()
        self.assertEqual(snapshot['health'], 'ok')
        self.assertEqual(snapshot['next_task_id'], 'a')
        self.assertEqual(snapshot['active_tasks'][0]['readiness'], 'needs_review')

    def test_mutable_invoice_register_cannot_establish_task_readiness(self):
        import hashlib
        from casefiles import summary
        self.task('invoice-follow-up')
        register = self.root / '00_admin/invoicing.json'
        register.write_text('{"synthetic":"mutable"}')
        path = self.root / '00_admin/tasks.json'
        records = json.loads(path.read_text())
        records[0].update(evidence_file='00_admin/invoicing.json', evidence_sha256=hashlib.sha256(register.read_bytes()).hexdigest())
        path.write_text(json.dumps(records))
        with self.assertRaises(ws.WorkspaceError):
            summary.collect(self.root, '2026-10')
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_action'], 'repair')
        self.assertEqual(snapshot['active_tasks'], [])

    def test_cyclic_dependencies_and_unsafe_evidence_fail_closed(self):
        self.task('one')
        self.task('two', depends_on=['one'])
        path = self.root / '00_admin/tasks.json'
        records = json.loads(path.read_text())
        records[0]['depends_on'] = ['two']
        path.write_text(json.dumps(records))
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_action'], 'repair')
        records[0]['depends_on'] = []
        records[0]['evidence_file'] = '../outside.txt'
        records[0]['evidence_sha256'] = '0' * 64
        path.write_text(json.dumps(records))
        snapshot, _ = self.view()
        self.assertEqual(snapshot['next_action'], 'repair')
        self.assertIsNone(snapshot['next_task_id'])


if __name__ == '__main__':
    unittest.main()

"""Real GUI adapter and HTTP boundary, using only synthetic private files."""
import base64
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'gui'))
import server as gui


class GuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.app = gui.Application()
        self.serial = 0
        self.call('open', path=str(self.base / 'workspace'), create=True, language='ru', year=2026)

    def call(self, op, **args):
        self.serial += 1
        args.setdefault('request_id', 'request-' + str(self.serial))
        args.setdefault('workspace_id', self.app.workspace_id)
        return self.app.dispatch(op, args)

    def receive(self):
        return self.call('receive', period='2026-10', received_on='2026-10-20', type='receipt',
                         files=[{'name': 'proof.csv', 'content': base64.b64encode(b'date,amount\n2026-10-20,100.00\n').decode()}])

    def test_loopback_startup_does_not_depend_on_dns(self):
        with patch('socket.getfqdn', side_effect=AssertionError('DNS unavailable')):
            server = gui.create_server(self.app)
        self.addCleanup(server.server_close)
        self.assertEqual(server.server_address[0], '127.0.0.1')
        self.assertEqual(server.server_name, '127.0.0.1')
        self.assertEqual(server.server_port, server.socket.getsockname()[1])
        self.assertGreater(server.server_port, 0)

    def configure(self):
        self.assertFalse(self.receive()['errors'])
        proof = self.call('status', period='2026-10')['documents'][0]['path']
        self.call('configuration', value=dict(system='local', product=None, account_reference='business',
                  method='EÜR', reviewer='Owner', evidence_file=proof), expected_sha256=None)
        return proof

    def approve_proposal(self, document_id):
        from casefiles import reviews
        root = self.app.root
        reviews.save_source_check(root, {
            'schema_version': 1, 'source_check_id': 'rule-1', 'url': 'https://www.gesetze-im-internet.de/ustg_1980/__12.html',
            'title': 'Synthetic rule check', 'checked_on': '2026-10-20', 'applicable_period': '2026-10',
            'assumptions': ['Synthetic facts only'], 'conclusion': 'Synthetic applicability note',
            'review_after': '2099-01-01', 'reviewer': 'Owner', 'evidence_file': self.call('status', period='2026-10')['documents'][0]['path']})
        record = reviews.proposal_template()
        record.update(proposal_id='proposal-1', document_id=document_id, period='2026-10', activity_id='activity-1')
        record['fields'] = {key: dict(raw=value, value=value, location='row 1', status='reviewed', reviewer='Owner', note=None)
                            for key, value in dict(invoice_number='SYN-1', invoice_date='2026-10-01', currency='EUR',
                                                   net='100.00', tax='19.00', gross='119.00').items()}
        record['proposed_treatment'] = dict(category='Sales', tax_rule='Synthetic reviewed assumption',
                                            reason='Training fixture only', source_check_ids=['rule-1'])
        saved = reviews.save_proposal(root, record)
        record['review'].update(status='approved', reviewer='Owner', reviewed_on='2026-10-20', note='Synthetic approval')
        reviews.save_proposal(root, record, saved['sha256'])

    def test_entry_form_lists_approved_proposals_and_posts_a_linked_vat_line(self):
        self.configure()
        self.approve_proposal(self.call('status', period='2026-10')['documents'][0]['record']['document_id'])
        state = self.call('status', period='2026-10')
        self.assertEqual([(row['proposal_id'], row['invoice_number'], row['gross'], row['currency'], row['activity_id'])
                          for row in state['accounting']['proposals']],
                         [('proposal-1', 'SYN-1', '119.00', 'EUR', 'activity-1')])
        line = dict(kind='income', amount='119.00', category='Sales', activity_id='activity-1', proposal_id='proposal-1',
                    vat=dict(status='stated', net='100.00', tax='19.00', rate='19'))
        self.call('entry-post', value=dict(schema_version=2, entry_id='paid', date='2026-10-20', account='bank',
                                           transaction_id='bank-2', amount='119.00', currency='EUR', lines=[line],
                                           reviewer='Owner', evidence_file=state['documents'][0]['path'],
                                           note='Synthetic payment of the reviewed invoice', replaces=None))
        entry = self.call('status', period='2026-10')['accounting']['entries'][0]
        self.assertEqual(list(entry['linked_proposals']), ['proposal-1'])

    def test_real_import_review_post_and_reversal_preserve_original(self):
        proof = self.configure()
        state = self.call('status', period='2026-10')
        doc = state['documents'][0]
        edited = dict(doc['record'], review_status='reviewed', reviewer='Owner', review_note='Inspected original')
        self.call('document-save', record=edited, expected_sha256=doc['sha256'])
        entry = dict(schema_version=2, entry_id='sale', date='2026-10-20', account='bank', transaction_id='bank-1', amount='100.00',
                     currency='EUR', lines=[dict(kind='income', amount='100.00', category='Sales', activity_id='activity-1', proposal_id=None,
                                                 vat=dict(status='none_stated', net=None, tax=None, rate=None))],
                     reviewer='Owner', evidence_file=proof, note='Actual synthetic cash movement', replaces=None)
        result = self.call('entry-post', value=entry, request_id='post-sale')
        self.assertEqual(result, self.call('entry-post', value=entry, request_id='post-sale'))
        self.assertEqual(len(self.call('status', period='2026-10')['accounting']['entries']), 1)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('entry-post', value=dict(entry, amount='999'), request_id='post-sale')
        self.call('entry-reverse', entry_id='sale', reversal_id='sale-reversal', evidence_file=proof, actor='Owner', note='Correction')
        report = self.call('report', period='2026-10')
        self.assertTrue(report)
        state = self.call('status', period='2026-10')
        self.assertEqual(len(state['accounting']['entries']), 2)
        self.assertEqual(state['documents'][0]['record']['review_status'], 'reviewed')

    def test_filing_evidence_cannot_skip_preflight_or_use_stale_hash(self):
        proof = self.configure()
        filing = dict(filing_id='filing-one', form='ustva', form_version='2026', period='2026-10',
                      recipient='Synthetic Finanzamt', payload_file=proof, source_files=[proof],
                      unresolved_items=['Calculation not checked'], supersedes=None)
        self.call('filing-create', value=filing)
        current = self.call('status', period='2026-10')['accounting']['filings'][0]
        action = dict(filing_id='filing-one', action='review', actor='Owner', evidence_file=proof,
                      note='Review', external_id=None, response_kind=None, due_date=None)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('filing-action', value=action, expected_sha256=current['sha256'])
        action['action'] = 'cancel'
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('filing-action', value=action, expected_sha256='wrong')
        self.call('filing-action', value=action, expected_sha256=current['sha256'])
        filing.update(filing_id='filing-two', supersedes='filing-one')
        self.call('filing-create', value=filing)
        self.assertEqual(len(self.call('status', period='2026-10')['accounting']['filings']), 2)

    def test_drafts_resume_with_conflict_check_and_full_recovery(self):
        result = self.call('draft-save', drafts={'entry': {'amount': '12.30'}}, expected_sha256=None)
        other = gui.Application(self.app.root)
        self.assertEqual(other.dispatch('status', {'period':'2026-10'})['drafts']['entry']['amount'], '12.30')
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('draft-save', drafts={}, expected_sha256='wrong')
        self.call('backup', destination=str(self.base / 'backup'))
        self.call('verify-backup', backup=str(self.base / 'backup'))
        self.call('restore', backup=str(self.base / 'backup'), destination=str(self.base / 'restored'))
        restored = gui.Application(self.base / 'restored').dispatch('status', {'period':'2026-10'})
        self.assertEqual(restored['drafts_sha256'], result['sha256'])
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('restore', backup=str(self.base / 'backup'), destination=str(self.app.root))

    def test_other_tab_cannot_write_old_form_to_new_workspace(self):
        previous = self.app.workspace_id
        self.call('open', path=str(self.base / 'other'), create=True, language='en', year=2026)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('draft-save', drafts={'entry': {'amount': '55'}}, expected_sha256=None, workspace_id=previous)
        self.assertEqual(self.call('status', period='2026-10')['drafts'], {})

    def test_old_open_response_cannot_misidentify_active_workspace(self):
        self.call('open', path=str(self.base / 'workspace'), create=False, request_id='open-a')
        self.call('open', path=str(self.base / 'b'), create=True, language='en', year=2026)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('open', path=str(self.base / 'workspace'), create=False, request_id='open-a')

    def test_interrupted_draft_save_and_rollback_require_recovery(self):
        first = self.call('draft-save', drafts={'entry': {'amount':'10'}}, expected_sha256=None)
        path = gui.ws._inside(self.app.root, gui.DRAFT_PATH)
        original = path.read_bytes()
        second = self.call('draft-save', drafts={'entry': {'amount':'20'}}, expected_sha256=first['sha256'])
        path.write_bytes(original)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('status', period='2026-10')
        path.unlink()
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('status', period='2026-10')
        self.call('open', path=str(self.base / 'fresh'), create=True, language='en', year=2026)
        with patch.object(gui.ws, '_audit', side_effect=OSError('Interrupted checkpoint')):
            with self.assertRaises(OSError):
                self.call('draft-save', drafts={'entry': {'amount':'30'}}, expected_sha256=None)
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('status', period='2026-10')

    def test_path_escape_and_malformed_upload_rejected(self):
        outside = self.base / 'secret.txt'
        outside.write_text('Not in workspace')
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('file', path='../secret.txt')
        with self.assertRaises(gui.ws.WorkspaceError):
            self.call('file', path=str(outside))
        for name in ('../bad.csv', 'C:\\bad.csv', 'bad.html'):
            result = self.call('receive', period='2026-10', received_on='2026-10-20', type='unknown',
                               files=[{'name':name, 'content':'YQ=='}])
            self.assertTrue(result['errors'])
        self.assertEqual(self.call('status', period='2026-10')['documents'], [])

    def test_http_requires_session_and_same_origin_and_never_serves_workspace(self):
        server = gui.create_server(self.app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        port = server.server_port
        def request(method, path, headers=None, data=None):
            connection = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
            connection.request(method, path, data, headers or {})
            response = connection.getresponse()
            result = response.status, response.read(), dict(response.getheaders())
            connection.close()
            return result
        body = json.dumps({'op':'status','args':{'period':'2026-10'}})
        headers = {'Content-Type':'application/json','Authorization':'Bearer ' + server.token}
        self.assertEqual(request('POST','/api',data=body)[0], 401)
        self.assertEqual(request('POST','/api', dict(headers, Origin='https://attacker.example'), body)[0], 403)
        self.assertEqual(request('POST','/api', dict(headers, Host='attacker.example'), body)[0], 403)
        self.assertEqual(request('POST','/api', dict(headers, **{'Content-Type':'text/plain'}), body)[0], 415)
        self.assertEqual(request('POST','/api', headers, body)[0], 200)
        self.assertEqual(request('GET','/api')[0], 404)
        self.assertEqual(request('GET','/../skills/de-business-kit/SKILL.md')[0], 404)
        self.assertEqual(request('POST','/api', dict(headers, **{'Content-Length':str(gui.MAX_REQUEST+1)}), '')[0], 413)

if __name__ == '__main__':
    unittest.main()

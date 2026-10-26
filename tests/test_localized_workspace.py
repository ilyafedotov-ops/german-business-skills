"""Physical folder names, stable record identities and legacy compatibility."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/de-business-kit/scripts/workspace.py'
SPEC = importlib.util.spec_from_file_location('localized_workspace', SCRIPT)
ws = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ws)
sys.path.insert(0, str(SCRIPT.parent))
from casefiles import accounting as ac


class LocalizedWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'Private'

    def test_russian_start_intake_resume_and_language_change_preserve_paths(self):
        ws.start_workspace(self.root, 2026, 'ru')
        self.assertTrue((self.root / '01 Входящие').is_dir())
        self.assertTrue((self.root / '02 Документы').is_dir())
        self.assertFalse((self.root / '06_bookkeeping').exists())
        self.assertIn('Оригиналы', (self.root / 'НАЧНИТЕ-ЗДЕСЬ.md').read_text(encoding='utf-8'))
        source = self.root / '01 Входящие/Счёт.csv'
        source.write_text('amount,currency\n12.34,EUR\n', encoding='utf-8')
        imported = ws.ingest_document(self.root, source, '2026-10')
        self.assertEqual(imported['status'], 'imported')
        self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')
        originals = list((self.root / '02 Документы/2026/10/Оригиналы').iterdir())
        self.assertEqual(len(originals), 1)
        before = originals[0].read_bytes()
        ws.configure_workspace(self.root, language='de')
        ws.start_workspace(self.root, 2027, 'en')
        self.assertEqual(originals[0].read_bytes(), before)
        self.assertFalse((self.root / '02 Dokumente').exists())
        self.assertEqual(ws.workspace_status(self.root)['folder_language'], 'ru')
        self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')
        for source in [ws.DOCUMENTS, '.business-kit/admin/documents.json', '.workspace-layout.json']:
            with self.assertRaises(ws.WorkspaceError):
                ws._evidence_path(self.root, source)

    def test_german_folders_and_canonical_references_resolve_to_the_same_file(self):
        ws.init_workspace(self.root, 2026, 'de', layout='localized')
        path = ws._inside(self.root, '03_banking/statement.csv')
        self.assertEqual(path, self.root / '03 Buchhaltung/Bank/statement.csv')
        ws._write_exclusive(path, b'example')
        self.assertEqual(ws._inside(self.root, '03 Buchhaltung/Bank/statement.csv'), path)
        self.assertIn('Originale', (self.root / 'HIER-STARTEN.md').read_text(encoding='utf-8'))
        self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')

    def test_legacy_workspace_remains_legacy(self):
        ws.init_workspace(self.root, 2026, 'ru')
        before = (self.root / ws.MARKER).read_bytes()
        ws.start_workspace(self.root, 2027, 'de')
        self.assertEqual((self.root / ws.MARKER).read_bytes(), before)
        self.assertFalse((self.root / '.workspace-layout.json').exists())

    def test_localized_accounting_reports_and_filing_evidence_remain_readable(self):
        ws.start_workspace(self.root, 2026, 'de')
        proof = '08_correspondence/review.md'
        ws._write_exclusive(ws._inside(self.root, proof), b'Synthetic reviewed evidence')
        config = ac.template('configuration')
        config.update(system='local', product=None, account_reference='sample', method='EÜR', reviewer='owner', evidence_file=proof)
        ac.configure(self.root, config)
        entry = ac.template('entry')
        entry.update(entry_id='example', date='2026-10-20', account='bank', transaction_id='example', amount='100.00', currency='EUR', reviewer='owner', evidence_file=proof, note='Synthetic')
        entry['lines'] = [{'kind':'income','amount':'100.00','category':'income','activity_id':'example'}]
        ac.post(self.root, entry)
        result = ac.export_report(self.root, '2026-10')
        self.assertTrue((self.root / result['path']).is_file())
        self.assertTrue((self.root / result['ledger_files']['bank']).is_file())
        filing = ac.template('filing')
        filing.update(filing_id='example-return', form='ustva', form_version='2026', period='2026-10', recipient='synthetic', payload_file=result['path'], source_files=[proof], unresolved_items=['tax_treatment_unresolved'], supersedes=None)
        ac.create_filing(self.root, filing)
        self.assertEqual(ac.get_filing(self.root, 'example-return')['record']['state'], 'draft')
        self.assertEqual(ac.status(self.root)['entry_count'], 1)

    def test_modified_layout_and_shadow_root_fail_closed(self):
        ws.start_workspace(self.root, 2026, 'ru')
        path = self.root / '.workspace-layout.json'
        original = path.read_bytes()
        record = json.loads(original)
        record['language'] = 'de'
        path.write_text(json.dumps(record), encoding='utf-8')
        with self.assertRaises(ws.WorkspaceError):
            ws.workspace_status(self.root)
        path.write_bytes(original)
        (self.root / '00_admin').mkdir()
        with self.assertRaises(ws.WorkspaceError):
            ws.workspace_status(self.root)

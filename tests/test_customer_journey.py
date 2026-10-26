"""Synthetic CLI cycle proves evidence preservation, not invoice/filing compliance."""
import tempfile
from pathlib import Path
import unittest
from customer_journey import run, FIXTURES, ws


class CustomerJourneyTests(unittest.TestCase):
    def test_credit_note_partial_payment_and_open_task_resume_without_shadow_entries(self):
        with tempfile.TemporaryDirectory() as temporary:
            for language in ('en', 'ru'):
                with self.subTest(language=language):
                    result = run(Path(temporary).resolve() / language, language)
                    root = Path(result['root'])
                    self.assertEqual(result['resumed']['action'], 'resumed')
                    self.assertTrue(result['v1_preserved'])
                    self.assertEqual(result['task']['status'], 'pending')
                    self.assertEqual(result['task']['evidence_status'], 'checked')
                    self.assertEqual(result['accounting']['accounting_system'], 'external')
                    self.assertEqual(result['accounting']['entry_count'], 0)
                    self.assertEqual(result['before']['record']['relations'], [])
                    credit = result['inspections']['credit-note.synthetic.xml']
                    self.assertEqual(credit['syntax'], 'ubl_credit_note')
                    self.assertEqual(credit['preceding_invoices'][0]['invoice_number']['value'], 'INV-SYN-001')
                    self.assertEqual(result['verified']['status'], 'ok')
                    # Read the catalog through its public lookup; intake type/link decisions remain explicit.
                    from synthetic_journey import command
                    row = command('desk.py', 'catalog', '--root', root, '--document-id', result['ids']['credit-note.synthetic.xml'])['record']
                    self.assertEqual(row['relations'], [{'relation': 'corrects', 'document_id': result['ids']['invoice.synthetic.xml']}])
                    self.assertIsNone(row['dates']['paid'])
                    registry = __import__('json').loads(ws._inside(root, ws.DOCUMENTS).read_text())
                    for original in registry['documents']:
                        self.assertEqual(ws._inside(root, original['path']).read_bytes(), (FIXTURES / original['original_name']).read_bytes())


if __name__ == '__main__':
    unittest.main()

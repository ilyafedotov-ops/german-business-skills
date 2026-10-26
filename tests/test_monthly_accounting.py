"""One synthetic local month; external tool output/receipt are supplied fixtures."""
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

import synthetic_journey as journey
from casefiles import accounting as ac, bank, documents, overview
import workspace as ws


class MonthlyAccountingTests(unittest.TestCase):
    def test_document_bank_post_report_resume_filing_and_observed_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            root = base / "private"
            ws.init_workspace(root, 2026, "ru", layout="localized")
            proof = "08_correspondence/review.md"
            ws._inside(root, proof).write_text("Synthetic owner review only; no legal assessment.", encoding="utf-8")
            config = ac.template("configuration")
            config.update(system="local", account_reference="one-account", method="EÜR", reviewer="owner", evidence_file=proof)
            ac.configure(root, config)
            invoice = documents.receive(root, journey.FIXTURES / "invoice.synthetic.xml", "2026-10", "2026-10-26", "invoice")
            record = documents.get(root, invoice["document_id"])
            record.update(review_status="reviewed", reviewer="owner", review_note="Read synthetic source; no posting implied")
            documents.save(root, record, invoice["sha256"])
            source = base / "bank.csv"
            source.write_text("ID;Buchungstag;Betrag;Waehrung;Text\ntx-1;02.10.2026;119,00;EUR;INV-SYN-001\n", encoding="utf-8")
            received = documents.receive(root, source, "2026-10", "2026-10-26", "bank_statement")
            mapping = bank.mapping_template()
            mapping.update(mapping_id="one-bank", account_id="one-account")
            mapping["columns"].update(date="Buchungstag", amount="Betrag", currency="Waehrung", transaction_id="ID", reference="Text")
            preview = bank.preview(root, received["document_id"], mapping, "2026-10")
            approved = bank.approve(root, preview["path"], preview["sha256"], "owner", proof)
            row = next(csv.DictReader(io.StringIO((root / approved["csv_path"]).read_text())))
            entry = ac.template("entry")
            entry.update(entry_id="sale", date="2026-10-02", account="one-account", transaction_id=row["transaction_id"],
                         amount="119.00", currency="EUR", reviewer="owner", evidence_file=documents.original(root, invoice["document_id"])["path"], note="Reviewed synthetic receipt")
            # The synthetic invoice states net and VAT but no rate element.
            entry["lines"] = [{"kind": "income", "amount": "119.00", "category": "sale", "activity_id": "one-activity", "proposal_id": None,
                               "vat": {"status": "stated", "net": "100.00", "tax": "19.00", "rate": None}}]
            ac.post(root, entry)
            self.assertEqual(ac.period_report(root, "2026-10")["vat"],
                             [{"currency": "EUR", "kind": "income", "rate": None, "net": "100.00", "tax": "19.00"}])
            report = ac.export_report(root, "2026-10")
            reconciliation = ws.reconciliation_report(root, approved["csv_path"], report["ledger_files"]["one-account"], "2026-10")
            self.assertEqual(len(reconciliation["matches"]), 1)
            self.assertEqual(ac.period_report(root, "2026-10")["tax_return_status"], "not_calculated")
            self.assertTrue((root / report["markdown_path"]).is_file())
            self.assertEqual(journey.command("workspace.py", "start", "--root", root)["action"], "resumed")
            # The external calculation is a supplied fixture, never a calculation by this kit.
            payload = "05_tax/2026/external-tool-output.txt"
            ws._inside(root, payload).write_text("SYNTHETIC external tool output. Not a real tax calculation or submission.", encoding="utf-8")
            filing = ac.template("filing")
            filing.update(filing_id="month-return", form="ustva", form_version="2026", period="2026-10", recipient="synthetic-finanzamt",
                          payload_file=payload, source_files=[proof], unresolved_items=["Verify actual calculation output"])
            ac.create_filing(root, filing)
            view = overview.generate(root, "2026-10", "2026-10-26")
            self.assertIn("Verify actual calculation output", (root / view["html_path"]).read_text())
            self.assertEqual(ac.check_filing(root, "month-return")["allowed_preflight_actions"], [])
            # Preserve blocked version, then record a reviewed replacement with its evidence.
            action = ac.template("filing-action")
            action.update(filing_id="month-return", action="cancel", actor="owner", evidence_file=proof, note="Synthetic correction")
            ac.filing_action(root, action, ac.get_filing(root, "month-return")["sha256"])
            filing.update(filing_id="month-return-v2", supersedes="month-return", unresolved_items=[])
            ac.create_filing(root, filing)
            for step in ("review", "authorize", "begin"):
                action.update(filing_id="month-return-v2", action=step)
                ac.filing_action(root, action, ac.get_filing(root, "month-return-v2")["sha256"])
            self.assertEqual(ac.check_filing(root, "month-return-v2")["next_step"], "resolve_submission_outcome")
            receipt = "08_correspondence/synthetic-receipt.txt"
            ws._inside(root, receipt).write_text("SYNTHETIC observed receipt; no network call was made.", encoding="utf-8")
            action.update(action="receipt", evidence_file=receipt, external_id="SYNTHETIC-RECEIPT-ONLY")
            ac.filing_action(root, action, ac.get_filing(root, "month-return-v2")["sha256"])
            overview.generate(root, "2026-10", "2026-10-26")
            snapshot = json.loads(ws._inside(root, "00_admin/overview.json").read_text())
            self.assertEqual(snapshot["accounting"]["period_entry_count"], 1)
            self.assertEqual({row["state"] for row in snapshot["filings"]}, {"cancelled", "submitted"})
            self.assertEqual(snapshot["capabilities"]["elster_submission"], "not_implemented")
            self.assertEqual(ws.verify_workspace(root)["status"], "ok")

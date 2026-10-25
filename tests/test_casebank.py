import csv
import io
import json
import unittest

from test_casework import CaseFixture
import workspace as ws
from casefiles import bank, documents, archive, storage, summary


class BankMappingTests(CaseFixture):
    def mapping(self):
        value = bank.mapping_template()
        value.update(mapping_id="de-bank-1", account_id="synthetic-account", delimiter=";", encoding="utf-8-sig",
                     date_format="%d.%m.%Y", decimal_separator=",", grouping_separator=".", default_currency="EUR")
        value["columns"].update(date="Buchungstag", amount="Betrag", transaction_id="ID", reference="Text")
        return value

    def test_decimal_comma_signs_and_namespaced_ids_survive_preview_review_and_reconciliation(self):
        doc = self.receive("bank.csv", "ID;Buchungstag;Betrag;Text\n1;02.10.2026;1.234,56;Synthetic sale\n2;03.10.2026;-5,00;Synthetic fee\n".encode(), "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        self.assertEqual(storage.load(self.root)["bank_imports"], {})
        report = json.loads((self.root / preview["path"]).read_text())
        self.assertEqual([r["amount"] for r in report["rows"]], ["1234.56", "-5.00"])
        approved = bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        rows = list(csv.DictReader(io.StringIO((self.root / approved["csv_path"]).read_text())))
        self.assertNotEqual(rows[0]["transaction_id"], "1")
        ledger = self.root / "04_accounting/ledger.csv"
        ledger.write_text("entry_id,transaction_id,amount,currency\n" + "\n".join(
            f"e{i},{r['transaction_id']},{r['amount']},{r['currency']}" for i, r in enumerate(rows)) + "\n")
        self.assertEqual(ws.reconcile(self.root, approved["csv_path"], ledger, "2026-10")["status"], "matched")

    def test_stale_preview_or_changed_original_cannot_be_applied(self):
        doc = self.receive("bank.csv", b"ID;Buchungstag;Betrag;Text\n1;02.10.2026;10,00;Synthetic\n", "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        with self.assertRaises(ws.WorkspaceError):
            bank.approve(self.root, preview["path"], "0" * 64, "owner", self.evidence())
        (self.root / preview["path"]).write_text("{}")
        with self.assertRaises(ws.WorkspaceError):
            bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())

    def test_duplicate_ids_ambiguous_grouping_and_wrong_period_fail(self):
        for rows in ("1;02.10.2026;10,00;x\n1;03.10.2026;5,00;x\n",
                     "1;02.10.2026;1.23,00;x\n", "1;02.11.2026;10,00;x\n"):
            doc = self.receive("bank.csv", ("ID;Buchungstag;Betrag;Text\n" + rows).encode(), "bank_statement")
            with self.subTest(rows=rows), self.assertRaises(ws.WorkspaceError):
                bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")

    def test_credit_debit_and_account_namespace_are_explicit(self):
        doc = self.receive("bank.csv", b"ID;Buchungstag;Credit;Debit\n1;02.10.2026;;12,50\n", "bank_statement")
        mapping = self.mapping()
        mapping.update(amount_mode="credit_debit")
        mapping["columns"].update(amount=None, credit="Credit", debit="Debit", reference=None)
        one = bank.preview(self.root, doc["document_id"], mapping, "2026-10")
        row_one = json.loads((self.root / one["path"]).read_text())["rows"][0]
        mapping["account_id"] = "second-account"
        two = bank.preview(self.root, doc["document_id"], mapping, "2026-10")
        row_two = json.loads((self.root / two["path"]).read_text())["rows"][0]
        self.assertEqual(row_one["amount"], "-12.50")
        self.assertNotEqual(row_one["transaction_id"], row_two["transaction_id"])

    def test_missing_native_ids_are_flagged_and_same_preview_cannot_be_imported_twice(self):
        doc = self.receive("bank.csv", b"Buchungstag;Betrag;Text\n02.10.2026;10,00;Synthetic\n", "bank_statement")
        mapping = self.mapping()
        mapping["columns"]["transaction_id"] = None
        preview = bank.preview(self.root, doc["document_id"], mapping, "2026-10")
        self.assertIn("generated_row_ids_need_overlap_review", json.loads((self.root / preview["path"]).read_text())["issues"])
        bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        with self.assertRaises(ws.WorkspaceError):
            bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())

    def test_mapping_rename_and_overlapping_export_cannot_duplicate_transactions(self):
        doc = self.receive("bank.csv", b"ID;Buchungstag;Betrag;Text\n1;02.10.2026;10,00;Synthetic\n", "bank_statement")
        mapping = self.mapping()
        preview = bank.preview(self.root, doc["document_id"], mapping, "2026-10")
        bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        mapping["mapping_id"] = "renamed-mapping"
        renamed = bank.preview(self.root, doc["document_id"], mapping, "2026-10")
        with self.assertRaises(ws.WorkspaceError):
            bank.approve(self.root, renamed["path"], renamed["sha256"], "owner", self.evidence())
        overlap = self.receive("overlap.csv", b"ID;Buchungstag;Betrag;Text\n1;02.10.2026;12,00;Changed amount\n2;03.10.2026;5,00;New\n", "bank_statement")
        another = bank.preview(self.root, overlap["document_id"], mapping, "2026-10")
        with self.assertRaises(ws.WorkspaceError):
            bank.approve(self.root, another["path"], another["sha256"], "owner", self.evidence())
        self.assertEqual(len(storage.load(self.root)["bank_imports"]), 1)

    def test_excluded_bank_document_does_not_reenter_bundle_through_derivatives(self):
        doc = self.receive("private.csv", b"ID;Buchungstag;Betrag;Text\n1;02.10.2026;10,00;EXCLUDED-PRIVATE-MEMO\n", "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        approved = bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        ledger = self.root / "04_accounting/ledger.csv"
        ledger.write_text("entry_id,transaction_id,amount,currency\n")
        ws.reconcile(self.root, approved["csv_path"], ledger, "2026-10")
        record = documents.get(self.root, doc["document_id"])
        record.update(review_status="excluded", reviewer="owner", review_note="Private account; exclude")
        documents.save(self.root, record, storage.digest(storage.load(self.root)["documents"][doc["document_id"]]))
        built = archive.build(self.root, "2026-10", as_of="2026-10-25")
        target = self.root / built["path"]
        self.assertEqual(json.loads((target / "records/bank_imports.json").read_text()), [])
        self.assertEqual(json.loads((target / "records/reconciliations.json").read_text()), [])
        for path in target.rglob("*"):
            if path.is_file():
                self.assertNotIn(b"EXCLUDED-PRIVATE-MEMO", path.read_bytes())

    def test_edited_reconciliation_cannot_clear_actual_unmatched_payments(self):
        doc = self.receive("bank.csv", b"ID;Buchungstag;Betrag;Text\n1;02.10.2026;10,00;Synthetic\n", "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        approved = bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        ledger = self.root / "04_accounting/ledger.csv"
        ledger.write_text("entry_id,transaction_id,amount,currency\ne1,other,10.00,EUR\n")
        result = ws.reconcile(self.root, approved["csv_path"], ledger, "2026-10")
        path = self.root / result["report"]
        report = json.loads(path.read_text())
        for key in ("unmatched_bank", "unmatched_ledger", "differences", "unlinked_ledger_entries", "review_notes"):
            report[key] = []
        report["status"] = "matched"
        path.write_text(json.dumps(report))
        snapshot = summary.collect(self.root, "2026-10", "2026-10-25")
        self.assertFalse(snapshot["reports"][0]["current"])
        self.assertEqual(snapshot["counts"]["unmatched_items"], 2)
        with self.assertRaises(ws.WorkspaceError):
            archive.build(self.root, "2026-10", as_of="2026-10-25")


if __name__ == "__main__":
    unittest.main()

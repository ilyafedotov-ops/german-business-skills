"""Synthetic document-to-accountant behavior and preservation boundaries."""
import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws
from casefiles import documents, reviews, storage


class CaseFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "private"
        ws.init_workspace(self.root, 2026, "en")

    def receive(self, filename="invoice.pdf", data=b"Synthetic invoice", kind="invoice"):
        source = self.base / filename
        source.write_bytes(data)
        return documents.receive(self.root, source, "2026-10", "2026-10-25", kind)

    def evidence(self):
        path = self.root / "08_correspondence/review.txt"
        path.write_text("Synthetic review and source applicability evidence", encoding="utf-8")
        return "08_correspondence/review.txt"

    def field(self, value, location="page 1", status="reviewed"):
        return {"raw": value, "value": value, "location": location, "status": status,
                "reviewer": "synthetic reviewer" if status == "reviewed" else None, "note": None}

    def draft(self, document_id):
        record = reviews.proposal_template()
        record.update(proposal_id="proposal-1", document_id=document_id, period="2026-10", activity_id="consulting")
        record["fields"] = {k: self.field(v) for k, v in {
            "invoice_number": "SYN-1", "invoice_date": "2026-10-01", "due_date": "2026-10-31",
            "currency": "EUR", "net": "100.00", "tax": "19.00", "gross": "119.00"}.items()}
        record["proposed_treatment"] = {"category": "Synthetic service", "tax_rule": "Synthetic reviewed assumption",
                                         "reason": "Training fixture only", "source_check_ids": ["rule-1"]}
        return record

    def source_check(self):
        record = {"schema_version": 1, "source_check_id": "rule-1", "url": "https://www.gesetze-im-internet.de/ustg_1980/__12.html",
                  "title": "Synthetic rule check", "checked_on": "2026-10-25", "applicable_period": "2026-10",
                  "assumptions": ["Synthetic facts only"], "conclusion": "Synthetic applicability note",
                  "review_after": "2099-01-01", "reviewer": "synthetic reviewer", "evidence_file": self.evidence()}
        return reviews.save_source_check(self.root, record)


class CatalogTests(CaseFixture):
    def test_mixed_documents_keep_originals_and_have_readable_catalog(self):
        invoice = self.receive()
        letter = self.receive("letter.pdf", b"Synthetic Finanzamt letter", "authority_letter")
        catalog = documents.catalog(self.root, "2026-10")
        self.assertEqual({item["type"] for item in catalog}, {"invoice", "authority_letter"})
        self.assertEqual(len(ws._documents(self.root)["documents"]), 2)
        original = documents.original(self.root, invoice["document_id"])
        self.assertEqual((self.root / original["path"]).read_bytes(), b"Synthetic invoice")
        self.assertEqual(next(item for item in catalog if item["document_id"] == letter["document_id"])["review_status"], "new")

    def test_identical_bytes_add_receipt_without_duplicate_original_or_resetting_review(self):
        first = self.receive()
        record = documents.get(self.root, first["document_id"])
        record.update(title="Readable invoice", review_status="reviewed", reviewer="owner", review_note="Inspected synthetic original")
        saved = documents.save(self.root, record, first["sha256"])
        second = self.receive("received-again.pdf")
        self.assertEqual(first["document_id"], second["document_id"])
        state = storage.load(self.root)
        self.assertEqual(len(state["receipts"]), 2)
        self.assertEqual(len(ws._documents(self.root)["documents"]), 1)
        self.assertEqual(documents.get(self.root, first["document_id"])["title"], "Readable invoice")
        self.assertEqual(documents.get(self.root, first["document_id"])["review_status"], "reviewed")

    def test_legacy_ingest_appears_without_silent_migration(self):
        source = self.base / "legacy.pdf"
        source.write_bytes(b"Legacy synthetic document")
        imported = ws.ingest_document(self.root, source, "2026-10")
        before = (self.root / ws.DOCUMENTS).read_bytes()
        self.assertEqual(documents.catalog(self.root)[0]["type"], "unknown")
        self.assertFalse((self.root / storage.STATE).exists())
        self.assertEqual((self.root / ws.DOCUMENTS).read_bytes(), before)

    def test_stale_edit_bad_links_and_modified_original_are_rejected(self):
        first = self.receive()
        record = documents.get(self.root, first["document_id"])
        record["title"] = "Updated"
        saved = documents.save(self.root, record, first["sha256"])
        with self.assertRaises(ws.WorkspaceError):
            documents.save(self.root, record, first["sha256"])
        record["links"]["task_ids"] = ["missing-task"]
        with self.assertRaises(ws.WorkspaceError):
            documents.save(self.root, record, saved["sha256"])
        record["links"]["task_ids"] = []
        original = documents.original(self.root, first["document_id"])
        (self.root / original["path"]).write_bytes(b"tampered")
        with self.assertRaises(ws.WorkspaceError):
            documents.save(self.root, record, saved["sha256"])

    def test_correction_and_structured_component_are_relations_not_duplicate_deletions(self):
        first = self.receive()
        correction = self.receive("correction.xml", b"<synthetic>correction</synthetic>", "credit_note")
        record = documents.get(self.root, correction["document_id"])
        record["relations"] = [{"relation": "corrects", "document_id": first["document_id"]}]
        documents.save(self.root, record, correction["sha256"])
        self.assertEqual(len(documents.catalog(self.root)), 2)
        self.assertEqual(documents.get(self.root, correction["document_id"])["relations"][0]["relation"], "corrects")


class ProposalTests(CaseFixture):
    def test_approval_requires_reviewed_extraction_arithmetic_and_rule_evidence(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Reviewed synthetic facts")
        record["fields"]["gross"]["value"] = "120.00"
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, saved["sha256"])
        record["fields"]["gross"] = self.field("119.00")
        approved = reviews.save_proposal(self.root, record, saved["sha256"])
        self.assertEqual(approved["status"], "approved")
        stored = storage.load(self.root)["proposals"]["proposal-1"]
        self.assertEqual(stored["fields"]["due_date"]["raw"], "2026-10-31")
        self.assertEqual(stored["original_sha256"], documents.original(self.root, received["document_id"])["sha256"])
        self.assertEqual(stored["provider_state"], "unknown")

    def test_approved_record_is_immutable_and_new_correction_keeps_history(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic approval")
        approved = reviews.save_proposal(self.root, record, saved["sha256"])
        record["fields"]["invoice_number"]["value"] = "different"
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, approved["sha256"])
        replacement = self.draft(received["document_id"])
        replacement.update(proposal_id="proposal-2", supersedes="proposal-1")
        reviews.save_proposal(self.root, replacement)
        self.assertEqual(len(storage.load(self.root)["proposals"]), 2)

    def test_lines_and_tax_breakdown_cannot_disagree_with_invoice(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        record["lines"] = [{"line_id": "one", "fields": {"description": self.field("Synthetic service"),
            "net": self.field("50"), "tax_rate": self.field("19"), "tax": self.field("9.50"), "gross": self.field("59.50")}}]
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic")
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, saved["sha256"])

    def test_changed_or_wrong_period_source_blocks_approval(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic")
        (self.root / "08_correspondence/review.txt").write_text("Changed", encoding="utf-8")
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, saved["sha256"])

    def test_explicit_quantity_and_tax_rate_contradictions_block_approval(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        record["lines"] = [{"line_id": "one", "fields": {key: self.field(value) for key, value in
            {"description": "Synthetic", "quantity": "2", "unit_price": "100", "net": "100", "tax_rate": "7", "tax": "19", "gross": "119"}.items()}}]
        record["tax_breakdown"] = [{"tax_id": "one", "fields": {key: self.field(value) for key, value in
            {"net": "100", "tax_rate": "7", "tax": "19"}.items()}}]
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic")
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, saved["sha256"])

    def test_unreviewed_field_and_invented_posting_state_cannot_be_approved(self):
        received = self.receive()
        self.source_check()
        record = self.draft(received["document_id"])
        record["provider_state"] = "posted"
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record)
        record.pop("provider_state")
        saved = reviews.save_proposal(self.root, record)
        record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic")
        record["fields"]["tax"]["status"] = "extracted"
        with self.assertRaises(ws.WorkspaceError):
            reviews.save_proposal(self.root, record, saved["sha256"])


if __name__ == "__main__":
    unittest.main()

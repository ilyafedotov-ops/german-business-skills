"""Synthetic provider outcomes; never a live invoice or delivery certification."""
import json
import os
from unittest.mock import patch
from test_casework import CaseFixture
import workspace as ws
from casefiles import invoicing as inv


class InvoicingTests(CaseFixture):
    def setUp(self):
        super().setUp()
        self.draft_file = self.write("draft.md", "Synthetic invoice preview; number pending")
        self.final_file = self.write("issued.xml", "<SyntheticInvoice number='INV-1'>119 EUR</SyntheticInvoice>")
        self.proof = self.write("readback.md", "Synthetic reviewed provider readback / action authority")

    def write(self, name, text):
        path = ws._inside(self.root, "08_correspondence/" + name)
        path.write_text(text)
        return str(path.relative_to(self.root))

    def create(self, identifier="invoice-1", **overrides):
        value = inv.template("invoice")
        value.update(invoice_id=identifier, business_reference="order-1", period="2026-10",
                     system="Example Books (synthetic)", account_reference="seller-1",
                     customer_reference="buyer-1", currency="EUR", document_file=self.draft_file,
                     source_files=[self.proof])
        value.update(overrides)
        return inv.create(self.root, value)

    def action(self, action, identifier="invoice-1", **overrides):
        value = inv.template("action")
        value.update(invoice_id=identifier, action=action, actor="synthetic reviewer",
                     evidence_file=self.proof, note="Inspected exact synthetic scope", occurred_on="2026-10-27")
        value.update(overrides)
        return inv.act(self.root, value, inv.show(self.root, identifier)["sha256"])

    def begin_issue(self, identifier="invoice-1"):
        self.action("review-issue", identifier)
        self.action("authorize-issue", identifier)
        return self.action("begin-issue", identifier)["attempt_id"]

    def issued(self, identifier="invoice-1", **overrides):
        self.create(identifier, **overrides)
        attempt = self.begin_issue(identifier)
        return self.action("confirm-issued", identifier, attempt_id=attempt, external_id="provider-" + identifier,
                           invoice_number="NUMBER-" + identifier, document_file=self.final_file)

    def begin_delivery(self, identifier="invoice-1", address="buyer@example.invalid"):
        self.action("review-delivery", identifier, recipient={"channel": "email", "address": address})
        self.action("authorize-delivery", identifier)
        return self.action("begin-delivery", identifier)["attempt_id"]

    def test_issue_final_bytes_delivery_and_receipt_are_separate(self):
        self.issued()
        record = inv.show(self.root, "invoice-1")["record"]
        self.assertNotEqual(record["draft"]["sha256"], record["issued"]["document"]["sha256"])
        attempt = self.begin_delivery()
        self.action("confirm-dispatched", attempt_id=attempt, external_id="message-1")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["delivery"]["state"], "dispatched")
        with self.assertRaises(ws.WorkspaceError):
            self.action("confirm-delivered", attempt_id=attempt, external_id="message-1", outcome_kind="sent_confirmation")
        self.action("confirm-delivered", attempt_id=attempt, external_id="message-1", outcome_kind="recipient_acknowledgement")
        shown = inv.show(self.root, "invoice-1")
        self.assertEqual(shown["record"]["delivery"]["state"], "delivered")
        self.assertIn("Delivered", shown["markdown"])

    def test_uncertain_issue_blocks_cancel_duplicate_and_replacement(self):
        self.create()
        self.begin_issue()
        for operation in (lambda: self.action("cancel"), lambda: self.create("duplicate"),
                          lambda: self.create("replacement", replaces="invoice-1")):
            with self.assertRaises(ws.WorkspaceError):
                operation()
        self.assertEqual(inv.list_invoices(self.root)["invoices"][0]["state"], "issue_unconfirmed")

    def test_confirmed_failure_retry_cannot_accept_delayed_old_outcome(self):
        self.create(); old = self.begin_issue()
        self.action("confirm-not-issued", attempt_id=old, outcome_kind="confirmed_not_issued")
        new = self.begin_issue()
        self.assertNotEqual(old, new)
        with self.assertRaises(ws.WorkspaceError):
            self.action("confirm-issued", attempt_id=old, external_id="old", invoice_number="OLD", document_file=self.final_file)
        self.action("confirm-issued", attempt_id=new, external_id="new", invoice_number="NEW", document_file=self.final_file)

    def test_source_drift_blocks_begin_but_not_recording_an_outcome(self):
        self.create(); self.action("review-issue"); self.action("authorize-issue")
        ws._inside(self.root, self.draft_file).write_text("changed")
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-issue")
        self.assertNotIn("begin-issue", inv.show(self.root, "invoice-1")["allowed_actions"])
        ws._inside(self.root, self.draft_file).write_text("Synthetic invoice preview; number pending")
        attempt = self.action("begin-issue")["attempt_id"]
        ws._inside(self.root, self.draft_file).unlink()
        self.action("confirm-issued", attempt_id=attempt, external_id="provider-1", invoice_number="INV-1", document_file=self.final_file)
        self.begin_delivery()

    def test_cancelled_draft_replacement_keeps_business_identity(self):
        self.create(); self.action("cancel")
        self.create("v2", replaces="invoice-1")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["state"], "cancelled")
        with self.assertRaises(ws.WorkspaceError):
            self.create("fork", replaces="invoice-1")

    def test_corrections_bind_issued_parent_and_block_competing_uncertain_work(self):
        self.issued()
        self.create("correction", business_reference="correction-1", corrects="invoice-1", correction_kind="amendment")
        self.begin_issue("correction")
        with self.assertRaises(ws.WorkspaceError):
            self.create("correction-2", business_reference="correction-2", corrects="invoice-1", correction_kind="amendment")
        with self.assertRaises(ws.WorkspaceError):
            self.create("wrong-customer", business_reference="wrong", corrects="invoice-1", correction_kind="amendment", customer_reference="other")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["state"], "issued")

    def test_delivery_failure_and_new_recipient_require_fresh_authority(self):
        self.issued(); old = self.begin_delivery()
        with self.assertRaises(ws.WorkspaceError):
            self.action("review-delivery", recipient={"channel": "email", "address": "new@example.invalid"})
        self.action("confirm-dispatched", attempt_id=old, external_id="message-old")
        self.action("confirm-delivery-failed", attempt_id=old, external_id="message-old", outcome_kind="delivery_failure")
        self.action("review-delivery", recipient={"channel": "email", "address": "new@example.invalid"})
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-delivery")
        self.action("authorize-delivery"); new = self.action("begin-delivery")["attempt_id"]
        with self.assertRaises(ws.WorkspaceError):
            self.action("confirm-delivered", attempt_id=old, external_id="message-old", outcome_kind="delivery_receipt")
        self.assertNotEqual(old, new)

    def test_stale_hash_and_corrupt_snapshot_fail_closed(self):
        saved = self.create()
        self.action("review-issue")
        value = inv.template("action")
        value.update(invoice_id="invoice-1", action="authorize-issue", actor="owner", note="test", evidence_file=self.proof, occurred_on="2026-10-27")
        with self.assertRaises(ws.WorkspaceError):
            inv.act(self.root, value, saved["sha256"])
        record = inv.show(self.root, "invoice-1")["record"]
        ws._inside(self.root, record["draft"]["path"]).write_text("tampered")
        self.assertEqual(inv.show(self.root, "invoice-1")["allowed_actions"], [])
        with self.assertRaises(ws.WorkspaceError):
            self.action("cancel")

    def test_register_cannot_serve_as_its_own_evidence_even_via_hardlink(self):
        self.create()
        register = ws._inside(self.root, inv.STATE)
        alias = ws._inside(self.root, "08_correspondence/alias.json")
        os.link(register, alias)
        for path in (inv.STATE, str(alias.relative_to(self.root))):
            with self.assertRaises(ws.WorkspaceError):
                self.action("review-issue", evidence_file=path)

    def test_missing_register_or_rollback_is_detected(self):
        self.create(); path = ws._inside(self.root, inv.STATE); old = path.read_bytes()
        self.action("review-issue"); path.write_bytes(old)
        with self.assertRaises(ws.WorkspaceError):
            inv.list_invoices(self.root)
        path.unlink()
        with self.assertRaises(ws.WorkspaceError):
            inv.list_invoices(self.root)

    def test_adopt_existing_issued_document_does_not_invent_authorization_or_attempt(self):
        self.create()
        self.action("adopt-issued", external_id="existing-1", invoice_number="OLD-1", document_file=self.final_file)
        record = inv.show(self.root, "invoice-1")["record"]
        self.assertEqual(record["state"], "issued")
        self.assertEqual([e["action"] for e in record["events"]], ["adopt-issued"])
        self.assertIsNone(record["issue_attempt"])

    def test_issued_number_is_unique_within_authority_and_account(self):
        self.issued(); self.create("another", business_reference="different-order")
        with self.assertRaises(ws.WorkspaceError):
            self.action("adopt-issued", "another", external_id="different-id", invoice_number="NUMBER-invoice-1", document_file=self.final_file)

    def test_unknown_scope_changes_cannot_piggyback_on_authorization(self):
        self.create(); self.action("review-issue")
        with self.assertRaises(ws.WorkspaceError):
            self.action("authorize-issue", recipient={"channel": "email", "address": "other@example.invalid"})

    def test_cancellation_readback_can_reuse_parent_identifiers_and_blocks_old_delivery(self):
        self.issued()
        self.action("review-delivery", recipient={"channel": "email", "address": "buyer@example.invalid"})
        self.action("authorize-delivery")
        self.create("cancel-1", business_reference="cancel-operation", corrects="invoice-1", correction_kind="cancellation")
        attempt = self.begin_issue("cancel-1")
        self.action("confirm-issued", "cancel-1", attempt_id=attempt, external_id="provider-invoice-1",
                    invoice_number="NUMBER-invoice-1", document_file=self.final_file)
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-delivery")
        self.assertNotIn("begin-delivery", inv.show(self.root, "invoice-1")["allowed_actions"])

    def test_amendment_without_new_number_and_changed_correction_context_need_new_delivery_review(self):
        self.issued()
        self.action("review-delivery", recipient={"channel": "email", "address": "buyer@example.invalid"})
        self.action("authorize-delivery")
        self.create("amendment", business_reference="amend-operation", corrects="invoice-1", correction_kind="amendment")
        self.action("adopt-issued", "amendment", external_id="provider-invoice-1", document_file=self.final_file)
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-delivery")
        self.action("review-delivery", recipient={"channel": "email", "address": "buyer@example.invalid"}, attachment_files=[self.final_file])
        self.action("authorize-delivery")
        self.action("begin-delivery")

    def test_receipt_cannot_predate_its_attempt(self):
        self.issued(); attempt = self.begin_delivery()
        with self.assertRaises(ws.WorkspaceError):
            self.action("confirm-delivered", attempt_id=attempt, external_id="message", outcome_kind="delivery_receipt", occurred_on="2026-10-26")

    def test_draft_replacement_can_fix_customer_and_currency_without_new_business_identity(self):
        self.create(); self.action("cancel")
        self.create("fixed", replaces="invoice-1", customer_reference="correct-buyer", currency="USD")
        fixed = inv.show(self.root, "fixed")["record"]
        self.assertEqual(fixed["business_reference"], "order-1")
        self.assertEqual(fixed["state"], "draft")

    def test_sibling_cancellation_invalidates_amendment_delivery_authorization(self):
        self.issued()
        self.create("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.action("adopt-issued", "amend", external_id="provider-invoice-1", document_file=self.final_file)
        self.action("review-delivery", "amend", recipient={"channel": "email", "address": "buyer@example.invalid"})
        self.action("authorize-delivery", "amend")
        self.create("cancel", business_reference="cancel", corrects="invoice-1", correction_kind="cancellation")
        self.action("adopt-issued", "cancel", external_id="provider-invoice-1", document_file=self.final_file)
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-delivery", "amend")
        self.assertNotIn("begin-delivery", inv.show(self.root, "amend")["allowed_actions"])

    def test_corrupt_related_correction_blocks_original_delivery_preparation(self):
        self.issued()
        self.create("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.action("adopt-issued", "amend", external_id="provider-invoice-1", document_file=self.final_file)
        path = inv.show(self.root, "amend")["record"]["issued"]["document"]["path"]
        ws._inside(self.root, path).write_text("broken")
        with self.assertRaises(ws.WorkspaceError):
            self.action("review-delivery", recipient={"channel": "email", "address": "buyer@example.invalid"})

    def test_nested_correction_cannot_bypass_uncertain_original_delivery(self):
        self.issued()
        self.issued("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.begin_delivery()
        with self.assertRaises(ws.WorkspaceError):
            self.create("nested", business_reference="nested", corrects="amend", correction_kind="amendment")

    def test_nested_correction_cannot_fork_around_pending_family_member(self):
        self.issued()
        self.issued("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.create("sibling", business_reference="sibling", corrects="invoice-1", correction_kind="amount_credit")
        with self.assertRaises(ws.WorkspaceError):
            self.create("nested", business_reference="nested", corrects="amend", correction_kind="amendment")

    def test_legacy_nested_draft_rechecks_family_before_issue(self):
        self.issued()
        self.issued("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.begin_delivery()
        # Model a draft saved by the previous writer's direct-parent-only guard.
        with patch.object(inv, "_check_correction_family"):
            self.create("nested", business_reference="nested", corrects="amend", correction_kind="amendment")
        with self.assertRaises(ws.WorkspaceError):
            self.action("review-issue", "nested")
        self.assertNotIn("review-issue", inv.show(self.root, "nested")["allowed_actions"])

    def test_started_legacy_nested_attempt_can_still_record_observed_result(self):
        self.issued()
        self.issued("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.begin_delivery()
        with patch.object(inv, "_check_correction_family"):
            self.create("nested", business_reference="nested", corrects="amend", correction_kind="amendment")
            attempt = self.begin_issue("nested")
        self.action("confirm-issued", "nested", attempt_id=attempt, external_id="nested-result",
                    invoice_number="NESTED", document_file=self.final_file)
        self.assertEqual(inv.show(self.root, "nested")["record"]["state"], "issued")

    def test_nested_issue_checks_original_frozen_evidence(self):
        self.issued()
        self.issued("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        self.create("nested", business_reference="nested", corrects="amend", correction_kind="amendment")
        self.action("review-issue", "nested"); self.action("authorize-issue", "nested")
        original = inv.show(self.root, "invoice-1")["record"]["issued"]["document"]["path"]
        ws._inside(self.root, original).write_text("Corrupt ancestor")
        with self.assertRaises(ws.WorkspaceError):
            self.action("begin-issue", "nested")

    def test_cli_uses_protected_writers_and_exports_a_readable_russian_status(self):
        from synthetic_journey import command
        value = command('desk.py', 'invoice-template', '--kind', 'invoice')
        value.update(invoice_id='cli-invoice', business_reference='cli-order', period='2026-10',
                     system='Synthetic service', account_reference='seller', customer_reference='buyer', currency='EUR',
                     document_file=self.draft_file, source_files=[self.proof])
        path = self.write('request.json', json.dumps(value))
        command('desk.py', 'invoice-create', '--root', self.root, '--input', path)
        shown = command('desk.py', 'invoice-show', '--root', self.root, '--id', 'cli-invoice', '--language', 'ru')
        self.assertIn('Черновик', shown['markdown'])
        report = command('desk.py', 'invoice-report', '--root', self.root, '--id', 'cli-invoice', '--language', 'ru')
        self.assertIn('Черновик', ws._inside(self.root, report['path']).read_text())
        self.assertEqual(command('desk.py', 'invoice-list', '--root', self.root)['invoices'][0]['invoice_id'], 'cli-invoice')

    def test_manual_dispatch_is_recorded_without_inventing_a_past_authorization(self):
        self.issued()
        observed = self.action("adopt-dispatched", recipient={"channel": "email", "address": "buyer@example.invalid"}, external_id="manual-message")
        record = inv.show(self.root, "invoice-1")["record"]
        self.assertEqual(record["delivery"]["state"], "dispatched")
        self.assertFalse(any(e["action"] in {"authorize-delivery", "begin-delivery"} for e in record["events"]))
        self.action("confirm-delivered", attempt_id=observed["attempt_id"], external_id="manual-message", outcome_kind="recipient_acknowledgement")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["delivery"]["state"], "delivered")

    def test_delivery_receipt_or_bounce_cannot_predate_confirmed_dispatch(self):
        self.issued(); attempt = self.begin_delivery()
        self.action("confirm-dispatched", attempt_id=attempt, external_id="message", occurred_on="2026-10-29")
        for action, kind in (("confirm-delivered", "delivery_receipt"), ("confirm-delivery-failed", "delivery_failure")):
            with self.assertRaises(ws.WorkspaceError):
                self.action(action, attempt_id=attempt, external_id="message", outcome_kind=kind, occurred_on="2026-10-28")

    def test_observed_correction_cannot_predate_its_issued_parent(self):
        self.issued()
        self.create("amend", business_reference="amend", corrects="invoice-1", correction_kind="amendment")
        with self.assertRaises(ws.WorkspaceError):
            self.action("adopt-issued", "amend", external_id="provider-invoice-1", document_file=self.final_file, occurred_on="2026-10-26")


if __name__ == "__main__":
    __import__("unittest").main()

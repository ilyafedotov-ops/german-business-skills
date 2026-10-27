"""Synthetic network boundary; no live provider or real invoice creation."""
import copy
from contextlib import contextmanager
import json
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ssl
import threading
from unittest.mock import patch

from test_casework import CaseFixture
import workspace as ws
from casefiles import invoicing as inv, lexware

ORG = "00000000-0000-4000-8000-000000000001"
CUSTOMER = "00000000-0000-4000-8000-000000000002"
REMOTE = "00000000-0000-4000-8000-000000000003"


class Provider:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []
        self.organization = ORG
        self.status = "draft"
        self.fail_create = False
        self.fail_read = False
        self.before_post = lambda: None

    def profile(self):
        self.calls.append("profile")
        return json.dumps({"organizationId": self.organization}).encode()

    def create_draft(self, data):
        self.calls.append("POST")
        self.before_post()
        if self.fail_create:
            raise ws.WorkspaceError("Provider request outcome unknown.")
        self.payload = json.loads(data)
        return json.dumps({"id": REMOTE, "resourceUri": "https://untrusted.invalid/ignored"}).encode()

    def read_invoice(self, identifier):
        self.calls.append("GET:" + identifier)
        if self.fail_read:
            raise ws.WorkspaceError("Provider read unavailable.")
        return json.dumps({**self.payload, "id": identifier, "organizationId": self.organization,
                           "voucherStatus": self.status, "voucherNumber": "SYN-100", "version": 1}).encode()

    def download(self, identifier, media_type):
        self.calls.append("file:" + identifier)
        return b"%PDF-1.7\nSynthetic invoice\n", "application/pdf"


class LexwareTests(CaseFixture):
    def setUp(self):
        super().setUp()
        self.payload = {"voucherDate": "2026-10-27T00:00:00.000+01:00",
                        "address": {"contactId": CUSTOMER},
                        "lineItems": [{"type": "custom", "name": "Synthetic service", "quantity": 1,
                                       "unitName": "service", "unitPrice": {"currency": "EUR", "netAmount": 100, "taxRatePercentage": 19}}],
                        "totalPrice": {"currency": "EUR"}, "taxConditions": {"taxType": "net"},
                        "shippingConditions": {"shippingType": "service", "shippingDate": "2026-10-26T00:00:00.000+01:00"}}
        self.request = "08_correspondence/request.json"
        ws._inside(self.root, self.request).write_text(json.dumps(self.payload))
        self.proof = self.evidence()
        ws._inside(self.root, "08_correspondence/preview.md").write_text("Synthetic reviewed invoice preview")
        value = inv.template("invoice")
        value.update(invoice_id="invoice-1", business_reference="order-1", period="2026-10", system="Lexware Office",
                     account_reference=ORG, customer_reference=CUSTOMER, currency="EUR", document_file="08_correspondence/preview.md", source_files=[self.proof])
        inv.create(self.root, value)
        self.client = Provider(self.payload)

    def action(self, action, **extra):
        value = lexware.template()
        value.update(invoice_id="invoice-1", action=action, actor="synthetic owner", evidence_file=self.proof,
                     note="Reviewed synthetic provider scope", occurred_on="2026-10-27")
        value.update(extra)
        return lexware.act(self.root, value, inv.show(self.root, "invoice-1")["sha256"], self.client)

    def prepare(self):
        self.action("prepare", payload_file=self.request)
        self.action("authorize-draft")

    def record_action(self, action, **extra):
        value = inv.template("action")
        value.update(invoice_id="invoice-1", action=action, actor="owner", evidence_file=self.proof,
                     note="Synthetic operation", occurred_on="2026-10-27")
        value.update(extra)
        return inv.act(self.root, value, inv.show(self.root, "invoice-1")["sha256"])

    def test_draft_intent_is_durable_before_post_and_readback_is_not_issue(self):
        self.prepare()
        self.client.before_post = lambda: self.assertEqual(inv.show(self.root, "invoice-1")["record"]["provider"]["state"], "create_unconfirmed")
        self.action("create-draft")
        row = inv.show(self.root, "invoice-1")["record"]
        self.assertEqual(row["state"], "draft")
        self.assertEqual(row["provider"]["external_id"], REMOTE)
        self.assertEqual(row["provider"]["state"], "read_back")
        self.assertNotIn("file:" + REMOTE, self.client.calls)
        with self.assertRaises(ws.WorkspaceError):
            self.action("create-draft")
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_unknown_create_blocks_retry_cancel_issue_and_duplicate(self):
        self.prepare(); self.client.fail_create = True
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        for action in ("create-draft", "prepare"):
            with self.assertRaises(ws.WorkspaceError): self.action(action, **({"payload_file": self.request} if action == "prepare" else {}))
        for action in ("cancel", "review-issue", "adopt-issued"):
            with self.assertRaises(ws.WorkspaceError): self.record_action(action)
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_failed_readback_preserves_returned_id_and_recovery_is_get_only(self):
        self.prepare(); self.client.fail_read = True
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["provider"]["external_id"], REMOTE)
        self.client.fail_read = False
        self.action("readback")
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_wrong_account_changed_request_and_stale_hash_never_post(self):
        self.prepare(); self.client.organization = REMOTE
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.client.organization = ORG
        ws._inside(self.root, self.request).write_text("{}")
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.assertNotIn("POST", self.client.calls)

    def test_finalization_flags_and_wrong_customer_are_rejected_before_network(self):
        for change in ({"finalize": True}, {"address": {"contactId": REMOTE}}):
            ws._inside(self.root, self.request).write_text(json.dumps({**self.payload, **change}))
            with self.assertRaises(ws.WorkspaceError): self.action("prepare", payload_file=self.request)
        self.assertEqual(self.client.calls, [])

    def test_readback_differences_need_review_and_unknown_status_blocks_issue(self):
        self.prepare(); self.action("create-draft")
        with self.assertRaises(ws.WorkspaceError): self.record_action("review-issue")
        self.client.payload["lineItems"][0]["quantity"] = 2
        self.action("readback")
        provider = inv.show(self.root, "invoice-1")["record"]["provider"]
        self.assertIn("lineItems[0].quantity", provider["differences"])
        self.action("review-readback")
        self.record_action("review-issue")
        self.client.status = "future-status"
        with self.assertRaises(ws.WorkspaceError): self.action("readback")
        self.assertNotIn("authorize-issue", inv.show(self.root, "invoice-1")["allowed_actions"])

    def test_unknown_create_can_bind_reviewed_existing_id_without_reposting(self):
        self.prepare(); self.client.fail_create = True
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.action("reconcile", external_id=REMOTE)
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["provider"]["external_id"], REMOTE)
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_browser_finalization_readback_then_exact_send_handoff(self):
        self.prepare(); self.action("create-draft"); self.action("review-readback")
        self.record_action("review-issue"); self.record_action("authorize-issue")
        begun = self.record_action("begin-issue")
        plan = lexware.handoff(self.root, "invoice-1", "finalize")
        self.assertIn(REMOTE, plan["url"])
        self.assertEqual(plan["attempt_id"], begun["attempt_id"])
        self.client.status = "open"
        self.action("readback"); self.action("download", media_type="application/pdf"); self.action("review-readback")
        provider = inv.show(self.root, "invoice-1")["record"]["provider"]
        self.record_action("confirm-issued", attempt_id=begun["attempt_id"], external_id=REMOTE,
                           invoice_number="SYN-100", document_file=provider["document"]["path"])
        message = "To: buyer@example.invalid; Cc/Bcc: none\nSubject: Synthetic invoice\nBody: Attached is the invoice."
        message_file = "08_correspondence/message-review.md"
        ws._inside(self.root, message_file).write_text(message)
        self.record_action("review-delivery", recipient={"channel": "email", "address": "buyer@example.invalid"}, evidence_file=message_file)
        self.record_action("authorize-delivery"); sending = self.record_action("begin-delivery")
        plan = lexware.handoff(self.root, "invoice-1", "send")
        self.assertEqual(plan["attempt_id"], sending["attempt_id"])
        self.assertEqual(plan["package"]["recipient"]["address"], "buyer@example.invalid")
        self.assertEqual(ws._inside(self.root, plan["package"]["scope_evidence"]["path"]).read_text(), message)
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["delivery"]["state"], "delivery_unconfirmed")

    def test_corrupt_provider_evidence_blocks_all_continuation(self):
        self.prepare(); self.action("create-draft")
        row = inv.show(self.root, "invoice-1")["record"]
        ws._inside(self.root, row["provider"]["readback"]["path"]).write_text("{}")
        self.assertEqual(inv.show(self.root, "invoice-1")["allowed_actions"], [])
        with self.assertRaises(ws.WorkspaceError): self.action("readback")

    def test_unexpected_finalized_creation_is_not_successful_draft(self):
        self.prepare(); self.client.status = "open"
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        row = inv.show(self.root, "invoice-1")["record"]
        self.assertEqual(row["provider"]["state"], "discrepancy")
        self.assertEqual(row["state"], "draft")

    def test_failed_reconciliation_can_be_read_again_without_posting(self):
        self.prepare(); self.client.fail_create = True
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.client.fail_read = True
        with self.assertRaises(ws.WorkspaceError): self.action("reconcile", external_id=REMOTE)
        self.client.fail_read = False
        self.action("reconcile", external_id=REMOTE)
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_changed_provider_between_readback_and_download_blocks_artifact_use(self):
        self.prepare(); self.action("create-draft")
        self.client.status = "open"; self.action("readback")
        self.client.payload["lineItems"][0]["quantity"] = 2
        with self.assertRaises(ws.WorkspaceError): self.action("download", media_type="application/pdf")
        self.assertIsNone(inv.show(self.root, "invoice-1")["record"]["provider"]["document"])

    def test_stale_provider_hash_is_rejected_before_any_request(self):
        old = inv.show(self.root, "invoice-1")["sha256"]
        self.prepare()
        value = lexware.template()
        value.update(invoice_id="invoice-1", action="create-draft", actor="owner", evidence_file=self.proof,
                     note="Synthetic", occurred_on="2026-10-27")
        with self.assertRaises(ws.WorkspaceError): lexware.act(self.root, value, old, self.client)
        self.assertEqual(self.client.calls, [])

    def test_post_uses_captured_authorized_bytes_even_if_snapshot_changes_after_intent(self):
        self.prepare()
        request = inv.show(self.root, "invoice-1")["record"]["provider"]["request"]["path"]
        original_lock = ws._locked
        changed = False
        @contextmanager
        def competing_writer(root):
            nonlocal changed
            with original_lock(root):
                yield
            state = ws._load(ws._inside(root, inv.STATE))
            if not changed and state["invoices"]["invoice-1"]["provider"]["state"] == "create_unconfirmed":
                changed = True
                ws._inside(self.root, request).write_text(json.dumps({**self.payload, "remark": "changed"}))
        with patch.object(ws, "_locked", competing_writer):
            with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        self.assertTrue(changed)
        self.assertNotIn("remark", self.client.payload)
        self.assertEqual(self.client.calls.count("POST"), 1)

    def test_duplicate_json_and_nonfinite_exponents_never_reach_network(self):
        for data in (json.dumps(self.payload).replace('"quantity": 1', '"quantity": 1, "quantity": 2'),
                     json.dumps(self.payload).replace('"quantity": 1', '"quantity": 1e999')):
            ws._inside(self.root, self.request).write_text(data)
            with self.assertRaises(ws.WorkspaceError): self.action("prepare", payload_file=self.request)
        self.assertEqual(self.client.calls, [])

    def test_changed_provider_during_download_blocks_and_preserves_downloaded_evidence(self):
        self.prepare(); self.action("create-draft")
        self.client.status = "open"; self.action("readback")
        def download(identifier, media_type):
            self.client.payload["lineItems"][0]["quantity"] = 2
            return b"%PDF-1.7\nChanged synthetic invoice", "application/pdf"
        self.client.download = download
        with self.assertRaises(ws.WorkspaceError): self.action("download", media_type="application/pdf")
        provider = inv.show(self.root, "invoice-1")["record"]["provider"]
        self.assertIsNone(provider["document"])
        self.assertTrue(any(e["action"] == "download-response" for e in provider["events"]))

    def test_two_local_cases_cannot_bind_same_remote_draft(self):
        self.prepare(); self.action("create-draft")
        original = inv.show(self.root, "invoice-1")["record"]
        other = {key: original[key] for key in inv.template("invoice")}
        other.update(invoice_id="invoice-2", business_reference="order-2")
        inv.create(self.root, other)
        for action in ("prepare", "authorize-draft", "create-draft"):
            value = lexware.template()
            value.update(invoice_id="invoice-2", action=action, actor="owner", evidence_file=self.proof,
                         note="Synthetic second scope", occurred_on="2026-10-27",
                         payload_file=self.request if action == "prepare" else None)
            if action == "create-draft":
                with self.assertRaises(ws.WorkspaceError):
                    lexware.act(self.root, value, inv.show(self.root, "invoice-2")["sha256"], self.client)
            else:
                lexware.act(self.root, value, inv.show(self.root, "invoice-2")["sha256"], self.client)
        self.assertIsNone(inv.show(self.root, "invoice-2")["record"]["provider"]["external_id"])

    def test_changed_readback_cannot_reuse_an_already_begun_issue_scope(self):
        self.prepare(); self.action("create-draft"); self.action("review-readback")
        self.record_action("review-issue"); self.record_action("authorize-issue"); self.record_action("begin-issue")
        self.client.payload["lineItems"][0]["quantity"] = 2
        self.action("readback"); self.action("review-readback")
        with self.assertRaises(ws.WorkspaceError): lexware.handoff(self.root, "invoice-1", "finalize")
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["state"], "issue_unconfirmed")

    def test_malformed_creation_response_is_preserved_before_parsing(self):
        self.prepare()
        self.client.create_draft = lambda data: b'{"id":'
        with self.assertRaises(ws.WorkspaceError): self.action("create-draft")
        provider = inv.show(self.root, "invoice-1")["record"]["provider"]
        response = next(e["response"] for e in provider["events"] if e["action"] == "create-response")
        self.assertEqual(ws._inside(self.root, response["path"]).read_bytes(), b'{"id":')
        self.assertIsNone(provider["external_id"])

    def test_malformed_readback_response_is_preserved_and_not_reviewable(self):
        self.prepare(); self.action("create-draft")
        self.client.read_invoice = lambda identifier: b'{"id":1,"id":2}'
        with self.assertRaises(ws.WorkspaceError): self.action("readback")
        provider = inv.show(self.root, "invoice-1")["record"]["provider"]
        self.assertEqual(provider["state"], "read_unconfirmed")
        self.assertEqual(ws._inside(self.root, provider["events"][-1]["response"]["path"]).read_bytes(), b'{"id":1,"id":2}')


class LexwareTransportTests(CaseFixture):
    def setUp(self):
        super().setUp()
        self.requests = []
        self.status = 200
        self.body = b'{"organizationId":"synthetic"}'
        owner = self
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.requests.append((self.command, self.path, self.headers.get("Authorization")))
                self.send_response(owner.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Location", "https://untrusted.invalid/credential-sink")
                self.end_headers()
                self.wfile.write(owner.body)

            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                self.do_GET()

            def log_message(self, *args):
                pass
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        def connection(host, timeout, context):
            self.assertEqual(host, "api.lexware.io")
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(context.check_hostname)
            return http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=timeout)
        self.addCleanup(patch.stopall)
        patch.dict("os.environ", {"LEXWARE_API_KEY": "synthetic-secret-token"}).start()
        patch.object(lexware.http.client, "HTTPSConnection", side_effect=connection).start()

    def test_fixed_origin_and_draft_only_request_over_actual_http_boundary(self):
        client = lexware.Client()
        client.profile(); client.create_draft(b"{}")
        self.assertEqual([(x[0], x[1]) for x in self.requests], [("GET", "/v1/profile"), ("POST", "/v1/invoices")])
        self.assertTrue(all(x[2] == "Bearer synthetic-secret-token" for x in self.requests))

    def test_redirect_never_forwards_credentials_or_retries(self):
        self.status = 302
        with self.assertRaises(ws.WorkspaceError) as caught: lexware.Client().profile()
        self.assertEqual(len(self.requests), 1)
        self.assertNotIn("synthetic-secret-token", str(caught.exception))
        self.assertNotIn("untrusted.invalid", str(caught.exception))

    def test_error_bodies_and_echoed_credentials_never_escape(self):
        self.body = b'{"debug":"synthetic-secret-token"}'
        for status in (200, 401, 504):
            self.status = status
            with self.assertRaises(ws.WorkspaceError) as caught: lexware.Client().profile()
            self.assertNotIn("synthetic-secret-token", str(caught.exception))

    def test_provider_id_cannot_become_an_arbitrary_url(self):
        with self.assertRaises(ws.WorkspaceError): lexware.Client().read_invoice("https://untrusted.invalid")
        self.assertEqual(self.requests, [])

"""Opt-in Lexware Office draft API and exact-object browser handoff."""
import copy
import hashlib
import http.client
import json
import math
import os
import re
import ssl
import time
import uuid

import workspace as ws
import workflows as wf
from . import invoicing as inv, storage as st

HOST = "api.lexware.io"
FINAL = {"open", "paid", "paidoff"}
STATUSES = FINAL | {"draft", "voided"}


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value):
        raise ws.WorkspaceError("Lexware requires an actual UUID, not a URL or invoice number.")
    return value


def _json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ws.WorkspaceError("Ambiguous duplicate JSON field in provider data.")
            result[key] = value
        return result
    def number(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ws.WorkspaceError("Non-finite provider number is not supported.")
        return parsed
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_float=number, parse_constant=ws._reject_constant)
    except (UnicodeError, ValueError):
        raise ws.WorkspaceError("Expected unambiguous provider JSON.") from None


class Client:
    """Fixed origin, TLS verification, bounded reads; never retry or follow redirects."""
    def __init__(self):
        self._key = os.environ.get("LEXWARE_API_KEY", "")
        if not self._key or not re.fullmatch(r"[\x21-\x7e]{1,8192}", self._key):
            raise ws.WorkspaceError("Provide Lexware access through LEXWARE_API_KEY in the invoking process; never put it in input files.")
        self._last = 0.0

    def _request(self, method, path, body=None, media_type="application/json"):
        time.sleep(max(0, .55 - (time.monotonic() - self._last)))
        connection = http.client.HTTPSConnection(HOST, timeout=20, context=ssl.create_default_context())
        try:
            self._last = time.monotonic()
            connection.request(method, path, body=body, headers={"Authorization": "Bearer " + self._key,
                               "Accept": media_type, "Content-Type": "application/json"})
            response = connection.getresponse()
            if response.status not in {200, 201}:
                raise ws.WorkspaceError("Lexware HTTP " + str(response.status) + "; no automatic retry. A write may have succeeded; inspect the saved attempt.")
            data = response.read(ws.MAX_BYTES + 1)
            content_type = response.getheader("Content-Type", "").split(";")[0].lower().strip()
            if len(data) > ws.MAX_BYTES or self._key.encode() in data:
                raise ws.WorkspaceError("Lexware response rejected; inspect the saved attempt without retrying a write.")
            if media_type == "application/json" and content_type != "application/json":
                raise ws.WorkspaceError("Expected a Lexware JSON response; no result inferred.")
            return data, content_type
        except (OSError, http.client.HTTPException):
            raise ws.WorkspaceError("Lexware connection failed; a write outcome is unknown. Do not repeat creation.") from None
        finally:
            connection.close()

    def profile(self):
        return self._request("GET", "/v1/profile")[0]

    def create_draft(self, payload):
        return self._request("POST", "/v1/invoices", payload)[0]

    def read_invoice(self, remote_id):
        return self._request("GET", "/v1/invoices/" + identifier(remote_id))[0]

    def download(self, remote_id, media_type):
        if media_type not in {"application/pdf", "application/xml"}:
            raise ws.WorkspaceError("Choose the reviewed PDF or XML format.")
        return self._request("GET", "/v1/invoices/" + identifier(remote_id) + "/file", media_type=media_type)


def template():
    return dict(invoice_id=None, action=None, payload_file=None, external_id=None, media_type=None,
                actor=None, evidence_file=None, note=None, occurred_on=None)


def _save(root, data, suffix=".json"):
    relative = "08_correspondence/invoice-evidence/lexware-" + uuid.uuid4().hex + suffix
    path = ws._inside(root, relative)
    ws._mkdir(path.parent)
    ws._write_exclusive(path, data)
    return {"path": ws._physical(root, relative), "sha256": hashlib.sha256(data).hexdigest()}


def _payload(row, data):
    value = _json(data)
    required = {"voucherDate", "address", "lineItems", "totalPrice", "taxConditions", "shippingConditions"}
    optional = {"language", "title", "introduction", "remark", "paymentConditions", "deliveryTerms"}
    if not isinstance(value, dict) or not required <= value.keys() or value.keys() - required - optional:
        raise ws.WorkspaceError("Supply only supported reviewed draft fields; finalization, IDs and status are not input fields.")
    if value["address"] != {"contactId": row["customer_reference"]} or value["totalPrice"] != {"currency": row["currency"]}:
        raise ws.WorkspaceError("This bounded route requires the exact saved contact UUID and currency, with provider-calculated totals.")
    identifier(row["customer_reference"])
    if row["currency"] != "EUR" or not isinstance(value["lineItems"], list) or not 1 <= len(value["lineItems"]) <= 100:
        raise ws.WorkspaceError("This route supports reviewed EUR invoices with 1-100 items.")
    if any(not isinstance(item, dict) or item.get("type") != "custom" for item in value["lineItems"]):
        raise ws.WorkspaceError("This bounded route supports reviewed custom items only.")
    if not isinstance(value["taxConditions"], dict) or not value["taxConditions"].get("taxType"):
        raise ws.WorkspaceError("Supply explicitly reviewed tax conditions; the adapter chooses no tax treatment.")
    return value


def _differences(expected, actual, path=""):
    result = []
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key, value in expected.items():
            result += _differences(value, actual.get(key), path + ("." if path else "") + key)
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            result.append(path)
        for index, (a, b) in enumerate(zip(expected, actual)):
            result += _differences(a, b, path + "[" + str(index) + "]")
    elif expected != actual:
        result.append(path)
    return result


def _row(root, state, value, expected):
    row = state["invoices"].get(value["invoice_id"])
    if row is None:
        raise ws.WorkspaceError("Invoice not found.")
    st.version(row, expected)
    inv._check(root, row, state)
    if row["system"] != "Lexware Office" or row["corrects"] is not None:
        raise ws.WorkspaceError("This adapter requires a Lexware Office invoice; provider corrections use the reviewed web-app route.")
    identifier(row["account_reference"])
    return row


def _event(root, provider, value, **extra):
    provider["events"].append({"action": value["action"], "actor": value["actor"], "note": value["note"],
                               "occurred_on": value["occurred_on"], "recorded_at": ws._now(),
                               "evidence": inv._snapshot(root, value["evidence_file"]), **extra})


def _account(client, row):
    profile = _json(client.profile())
    if not isinstance(profile, dict) or profile.get("organizationId") != row["account_reference"]:
        raise ws.WorkspaceError("Lexware account differs from the saved organization; no invoice operation performed.")


def _duplicate_id(state, row, remote_id):
    return any(other["invoice_id"] != row["invoice_id"] and other["account_reference"] == row["account_reference"]
               and other.get("provider", {}).get("external_id") == remote_id for other in state["invoices"].values())


def _capture_response(root, value, expected, raw, label):
    with inv._edit(root, "lexware_response_preserved") as state:
        response = _save(root, raw)
        row = _row(root, state, value, expected)
        row["provider"]["events"].append({"action": label, "response": response})
        current_hash = st.digest(row)
    return response, current_hash


def act(root, value, expected, client=None):
    root = ws._workspace(root)
    wf.exact(value, template(), "Lexware action")
    st.identifier(value["invoice_id"])
    for key in ("actor", "note"):
        wf.text(value[key], key)
    ws._day(value["occurred_on"])
    action = value["action"]
    if action not in {"prepare", "authorize-draft", "create-draft", "readback", "reconcile", "review-readback", "download"}:
        raise ws.WorkspaceError("Unsupported Lexware operation; no API finalization or send exists in this adapter.")
    for key, permitted in (("payload_file", "prepare"), ("external_id", "reconcile"), ("media_type", "download")):
        if action != permitted and value[key] is not None:
            raise ws.WorkspaceError("Unexpected Lexware action field: " + key)
    with inv._edit(root, "lexware_" + action) as state:
        row = _row(root, state, value, expected)
        p = row.get("provider")
        if action == "prepare":
            if p or row["state"] != "draft":
                raise ws.WorkspaceError("Provider preparation already exists or invoice is not a draft; inspect the existing object.")
            inv._check(root, row, state, live=True)
            request = inv._snapshot(root, value["payload_file"])
            _payload(row, ws._read_regular(ws._inside(root, request["path"])))
            p = row["provider"] = {"name": "lexware-office", "state": "prepared", "request": request,
                                   "attempt_id": None, "external_id": None, "readback": None,
                                   "remote_status": None, "differences": [], "document": None, "events": []}
            _event(root, p, value)
        elif not p:
            raise ws.WorkspaceError("Prepare the exact Lexware request and account scope first.")
        elif action == "authorize-draft":
            if p["state"] != "prepared" or row["state"] != "draft":
                raise ws.WorkspaceError("Draft creation is not awaiting authorization.")
            st.check_evidence(root, p["request"]["source"])
            p["state"] = "authorized"
            _event(root, p, value)
        elif action == "review-readback":
            if p["state"] != "read_back" or p["remote_status"] not in STATUSES:
                raise ws.WorkspaceError("Inspect a successful provider readback first, including differences and defaults.")
            p["state"] = "reviewed"
            _event(root, p, value, readback_sha256=p["readback"]["sha256"])
        else:
            if action == "create-draft":
                if p["state"] != "authorized" or row["state"] != "draft":
                    raise ws.WorkspaceError("Creation already attempted or not authorized; use readback/reconciliation, never replay.")
                inv._check(root, row, state, live=True)
                st.check_evidence(root, p["request"]["source"])
            elif action == "reconcile":
                if p["state"] not in {"create_unconfirmed", "discrepancy"} or p["external_id"]:
                    raise ws.WorkspaceError("Reconcile only an unknown creation without a known object ID.")
                identifier(value["external_id"])
            elif not p["external_id"]:
                raise ws.WorkspaceError("No known provider ID; investigate and reconcile the existing attempt.")
            if action == "download" and (p["remote_status"] not in FINAL or p["state"] not in {"read_back", "reviewed"}):
                raise ws.WorkspaceError("No final artifact is available for this readback; never finalize merely to download.")
            # Validate and freeze caller evidence before any network operation.
            inv._snapshot(root, value["evidence_file"])
    if action in {"prepare", "authorize-draft", "review-readback"}:
        return inv.show(root, value["invoice_id"])

    client = client or Client()
    _account(client, row)
    with inv._edit(root, "lexware_request_started") as state:
        row = _row(root, state, value, expected)
        p = row["provider"]
        if action == "create-draft":
            inv._check(root, row, state, live=True)
            st.check_evidence(root, p["request"]["source"])
            post_bytes = ws._read_regular(ws._inside(root, p["request"]["path"]))
            if hashlib.sha256(post_bytes).hexdigest() != p["request"]["sha256"]:
                raise ws.WorkspaceError("Frozen provider request changed during capture; no POST performed.")
            _payload(row, post_bytes)
            p.update(state="create_unconfirmed", attempt_id="provider-" + uuid.uuid4().hex)
        elif action != "reconcile":
            p["state"] = "read_unconfirmed"
        _event(root, p, value)
        if row["state"] in {"reviewed", "issue_authorized"}:
            row["state"] = "draft"  # Fresh readback invalidates earlier issue review/authority.
        pending_hash = st.digest(row)
    # Intent is now durably checkpointed. Network mutation never occurs inside _edit.
    if action == "create-draft":
        raw = client.create_draft(post_bytes)
        _, pending_hash = _capture_response(root, value, pending_hash, raw, "create-response")
        result = _json(raw)
        remote_id = identifier(result.get("id") if isinstance(result, dict) else None)
        with inv._edit(root, "lexware_draft_id_observed") as state:
            row = _row(root, state, value, pending_hash)
            p = row["provider"]
            duplicate = _duplicate_id(state, row, remote_id)
            if duplicate:
                p["state"] = "discrepancy"
            else:
                p.update(external_id=remote_id, state="read_unconfirmed")
            pending_hash = st.digest(row)
        if duplicate:
            raise ws.WorkspaceError("Provider ID is already linked to another local case; preserve both attempts and investigate.")
    else:
        remote_id = value["external_id"] if action == "reconcile" else p["external_id"]
    if action == "download":
        def bracket(raw, label, pending_hash):
            try:
                matches = st.digest(_json(raw)) == st.digest(_json(ws._read_regular(ws._inside(root, p["readback"]["path"]))))
            except ws.WorkspaceError:
                matches = False
            with inv._edit(root, "lexware_artifact_version_checked") as state:
                current = _row(root, state, value, pending_hash)
                current["provider"]["events"].append({"action": label, "response": _save(root, raw)})
                if not matches:
                    current["provider"].update(state="discrepancy", document=None)
                updated_hash = st.digest(current)
            if not matches:
                raise ws.WorkspaceError("Provider invoice changed around artifact download; read back and review again.")
            return updated_hash
        pending_hash = bracket(client.read_invoice(remote_id), "before-download", pending_hash)
        raw, content_type = client.download(remote_id, value["media_type"])
        suffix = {"application/pdf": ".pdf", "application/xml": ".xml"}.get(content_type)
        if not suffix or content_type != value["media_type"] or (suffix == ".pdf" and not raw.startswith(b"%PDF-")):
            raise ws.WorkspaceError("Unexpected invoice artifact format; preserve the prior result and inspect provider output.")
        with inv._edit(root, "lexware_artifact_observed") as state:
            row = _row(root, state, value, pending_hash)
            p = row["provider"]
            document = _save(root, raw, suffix)
            p["events"].append({"action": "download-response", "response": document, "media_type": content_type})
            pending_hash = st.digest(row)
        pending_hash = bracket(client.read_invoice(remote_id), "after-download", pending_hash)
        with inv._edit(root, "lexware_artifact_bound") as state:
            row = _row(root, state, value, pending_hash)
            row["provider"].update(document=document, state="read_back")
    else:
        raw = client.read_invoice(remote_id)
        response, pending_hash = _capture_response(root, value, pending_hash, raw, "read-response")
        result = _json(raw)
        with inv._edit(root, "lexware_readback_observed") as state:
            row = _row(root, state, value, pending_hash)
            p = row["provider"]
            valid = (isinstance(result, dict) and result.get("id") == remote_id
                     and result.get("organizationId") == row["account_reference"]
                     and isinstance(result.get("address"), dict) and isinstance(result.get("totalPrice"), dict)
                     and result.get("address", {}).get("contactId") == row["customer_reference"]
                     and result.get("totalPrice", {}).get("currency") == row["currency"]
                     and type(result.get("version")) is int and result["version"] >= 0
                     and isinstance(result.get("lineItems"), list) and bool(result["lineItems"])
                     and isinstance(result.get("voucherStatus"), str) and result["voucherStatus"] in STATUSES
                     and not _duplicate_id(state, row, remote_id)
                     and (action != "create-draft" or result.get("voucherStatus") == "draft"))
            differences = _differences(_json(ws._read_regular(ws._inside(root, p["request"]["path"]))), result)
            if action == "reconcile" and differences:
                valid = False
            if valid:
                if p["readback"] and p["readback"]["sha256"] != response["sha256"]:
                    p["document"] = None
                p.update(external_id=remote_id, readback=response, remote_status=result["voucherStatus"], state="read_back",
                         differences=differences)
            else:
                p["state"] = "discrepancy"
        if not valid:
            raise ws.WorkspaceError("Lexware readback identity/status disagrees; evidence preserved, continuation blocked.")
    return inv.show(root, value["invoice_id"])


def handoff(root, invoice_id, kind):
    view = inv.show(root, invoice_id)
    row = view["record"]
    p = row.get("provider")
    if not p or p["state"] != "reviewed" or not p["external_id"]:
        raise ws.WorkspaceError("Inspect and review intact provider readback before opening the action handoff.")
    with ws._locked(ws._workspace(root)):
        state = inv._load(ws._workspace(root))
        st.version(state["invoices"][invoice_id], view["sha256"])
        inv._check(ws._workspace(root), row, state, live=kind == "finalize")
    if kind == "finalize":
        if row["state"] != "issue_unconfirmed" or p["remote_status"] != "draft":
            raise ws.WorkspaceError("Record the authorized issue attempt before finalizing this exact draft.")
        began = next(e for e in row["events"] if e["action"] == "begin-issue" and e["attempt_id"] == row["issue_attempt"])
        if began["scope_sha256"] != st.digest(inv._issue_scope(row)):
            raise ws.WorkspaceError("Provider scope changed after issue began; investigate that attempt before a newly authorized operation.")
        attempt, package = row["issue_attempt"], None
    elif kind == "send":
        if row["state"] != "issued" or row["delivery"]["state"] != "delivery_unconfirmed":
            raise ws.WorkspaceError("Record the authorized delivery attempt for the final package before sending.")
        # Recheck package/context even though begin-delivery is no longer offered.
        with ws._locked(ws._workspace(root)):
            state = inv._load(ws._workspace(root))
            inv._check_delivery(ws._workspace(root), row, state)
        attempt, package = row["delivery"]["attempt_id"], copy.deepcopy(row["delivery"]["package"])
    else:
        raise ws.WorkspaceError("Choose finalize or send; combined finalize-and-send is unsupported.")
    return {"provider": "Lexware Office", "url": "https://app.lexware.de/permalink/invoices/edit/" + identifier(p["external_id"]),
            "organization_id": row["account_reference"], "external_id": p["external_id"], "action": kind,
            "attempt_id": attempt, "package": package, "readback": p["readback"],
            "execution": "authorized_browser_or_manual_action_required", "record_sha256": view["sha256"]}

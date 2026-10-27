#!/usr/bin/env python3
"""Offline evidence-linked preparation. Python 3.9+, standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid

import workspace as ws

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FIELDS = {
    "international": {
        "direction": ["purchase", "sale"], "supply": ["service", "goods", "mixed"],
        "counterparty_region": ["de", "eu", "non_eu", "unknown"],
        "customer_type": ["business", "consumer", "unknown"],
        "own_vat_regime": ["regular", "kleinunternehmer", "unknown"],
        "supplier_country": str, "customer_country": str, "establishment_facts": str,
        "service_description": str, "invoice_date": "date", "service_date_or_period": str,
        "payment_date": "date", "currency": "currency", "net_amount": "money",
        "vat_id_check": ["valid", "invalid", "unavailable", "not_checked", "not_applicable"],
        "vat_id_check_details": str, "contractual_seller": str, "invoice_issuer": str,
        "provider_role": ["processor", "merchant_of_record", "bank", "none", "unknown"],
        "place_of_supply_review": str, "reporting_review": str,
    },
    "classification": {
        "activity_description": str, "qualifications": str, "actual_delivery": str,
        "mixed_activities": bool, "separability_facts": str, "existing_authority_evidence": str,
        "legal_form": str, "own_vat_regime": str, "profit_method": str,
        "all_activities_vat_history": str, "proposed_classification": str, "review_question": str,
    },
    "elster": {
        "form_id": str, "form_version": str, "authority": str, "eligibility_reason": str,
        "portal_checked_on": "date", "account_capability": str, "deadline_basis": str,
        "calculation_notes": str,
    },
}


def exact(value, keys, name):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ws.WorkspaceError(f"{name} must contain exactly: {', '.join(sorted(keys))}")


def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 20000:
        raise ws.WorkspaceError(f"{name} requires nonempty text (maximum 20000 characters).")
    return value


def period(value):
    if not isinstance(value, str) or not re.fullmatch(r"[1-9]\d{3}(?:-(?:0[1-9]|1[0-2]|Q[1-4]))?", value):
        raise ws.WorkspaceError("Period must be YYYY, YYYY-MM or YYYY-Q1..Q4.")
    return value


def strings(value, name):
    if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
        raise ws.WorkspaceError(name + " must be a list of nonempty strings.")
    if len(value) != len(set(value)):
        raise ws.WorkspaceError(name + " contains duplicates.")
    return value


def template(kind):
    if kind not in FIELDS:
        raise ws.WorkspaceError("Unknown preparation kind.")
    result = {"schema_version": 1, "record_id": None, "period": None, "activity_ids": [],
              "evidence": [], "source_checks": [], "facts": dict.fromkeys(FIELDS[kind])}
    if kind == "elster":
        result["fields"] = []
    return result


def catalog():
    return ws._load(ASSETS / "form-catalog.json")


def capture(root, relative):
    path = ws._inside(root, text(str(relative), "evidence path"))
    path = ws._evidence_path(root, path.relative_to(root).as_posix())
    payload = ws._read_regular(path)
    if not payload.strip():
        raise ws.WorkspaceError("Evidence files must not be empty.")
    return {"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(payload).hexdigest()}


def validate(root, kind, value):
    exact(value, template(kind), "preparation")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported preparation schema_version.")
    text(value["record_id"], "record_id")
    period(value["period"])
    strings(value["activity_ids"], "activity_ids")
    missing = [] if value["activity_ids"] else ["activity_ids"]
    exact(value["facts"], FIELDS[kind], "facts")
    for key, rule in FIELDS[kind].items():
        item = value["facts"][key]
        if item is None:
            missing.append("facts." + key)
            continue
        if isinstance(rule, list):
            if item not in rule:
                raise ws.WorkspaceError("Unsupported value for " + key)
            if item in {"unknown", "not_checked", "unavailable"}:
                missing.append("facts." + key)
        elif rule is bool:
            if type(item) is not bool:
                raise ws.WorkspaceError(key + " must be a boolean or null.")
        else:
            text(item, key)
            if rule == "date":
                ws._day(item)
            elif rule == "currency":
                ws._currency(item)
            elif rule == "money":
                ws._amount(item)
    evidence = []
    ids = set()
    if not isinstance(value["evidence"], list):
        raise ws.WorkspaceError("evidence must be a list.")
    for item in value["evidence"]:
        exact(item, {"id", "path"}, "evidence")
        identifier = text(item["id"], "evidence id")
        if identifier in ids:
            raise ws.WorkspaceError("Duplicate evidence id.")
        ids.add(identifier)
        evidence.append({"id": identifier, **capture(root, text(item["path"], "evidence path"))})
    if not evidence:
        missing.append("evidence")
    if not isinstance(value["source_checks"], list):
        raise ws.WorkspaceError("source_checks must be a list.")
    for source in value["source_checks"]:
        exact(source, {"url", "checked_on", "applicable_period", "conclusion", "evidence_ids"}, "source check")
        if not isinstance(source["url"], str) or not re.fullmatch(r"https://[^\s/]+/[^\s]*", source["url"]):
            raise ws.WorkspaceError("A source check requires an HTTPS source URL.")
        ws._day(source["checked_on"])
        if source["applicable_period"] != value["period"]:
            raise ws.WorkspaceError("Source applicability must explicitly match the preparation period.")
        text(source["conclusion"], "source conclusion")
        refs = strings(source["evidence_ids"], "source evidence_ids")
        if not refs or not set(refs) <= ids:
            raise ws.WorkspaceError("Source checks require linked local evidence of the inspected rule/version.")
    if not value["source_checks"]:
        missing.append("source_checks")
    if kind == "elster":
        form_id = value["facts"]["form_id"]
        if form_id is not None and form_id not in {form["id"] for form in catalog()["forms"]}:
            raise ws.WorkspaceError("Unknown form_id; consult the catalogue.")
        if not isinstance(value["fields"], list):
            raise ws.WorkspaceError("fields must be a list.")
        labels = set()
        for field in value["fields"]:
            exact(field, {"label", "value", "status", "evidence_ids", "reviewer", "note"}, "form field")
            label = text(field["label"], "exact observed German label")
            if label in labels:
                raise ws.WorkspaceError("Duplicate field label; include its observed section/row context.")
            labels.add(label)
            if text(field["status"], "field status") not in {"empty", "proposed", "reviewed"}:
                raise ws.WorkspaceError("Unknown field review status.")
            if field["value"] is not None:
                text(field["value"], "field value")
            refs = strings(field["evidence_ids"], "field evidence_ids")
            if not set(refs) <= ids:
                raise ws.WorkspaceError("Unknown field evidence reference.")
            if field["note"] is not None:
                text(field["note"], "field note")
            if field["reviewer"] is not None:
                text(field["reviewer"], "field reviewer")
            if field["status"] == "reviewed" and (field["value"] is None or not refs or not field["reviewer"]):
                raise ws.WorkspaceError("Reviewed fields require a value, evidence and reviewer.")
            if field["status"] != "reviewed":
                missing.append("field:" + label)
        if not value["fields"]:
            missing.append("fields")
    return missing, evidence


def routes(kind, facts):
    if kind == "classification":
        return ["classification_review", "person_wide_vat_review"] + (
            ["mixed_activity_review"] if facts["mixed_activities"] is True else [])
    if kind == "elster":
        return ["form_eligibility_review", "draft_only"]
    result = ["place_of_supply_review", "payment_reporting_review"]
    if facts["supply"] in {"goods", "mixed"}:
        result.append("goods_customs_review")
    if facts["supply"] in {"service", "mixed"}:
        if facts["direction"] == "purchase" and facts["counterparty_region"] in {"eu", "non_eu"}:
            result.append("reverse_charge_review")
        if facts["direction"] == "sale":
            if facts["customer_type"] == "consumer":
                result.append("consumer_place_oss_review")
            elif facts["customer_type"] == "business":
                result.append("eu_b2b_place_and_zm_review" if facts["counterparty_region"] == "eu"
                              else "business_place_review")
    if facts["vat_id_check"] in {None, "invalid", "unavailable", "not_checked"}:
        result.append("vat_id_evidence_review")
    return result


def render(report, language):
    wording = ws._load(ASSETS / "preparation-messages.json")[language]
    def cell(value):
        return "`" + str(value).replace("`", "'").replace("|", "\\|").replace("\n", " ") + "`"

    lines = ["# " + wording["title"], "", wording["boundary"], "",
             f"**{wording['status']}:** {wording['states'][report['status']]} (`{report['status']}`)", "",
             f"**{wording['period']}:** `{report['period']}`", ""]
    for route in report.get("routes", []):
        lines += ["- " + wording["routes"][route]]
    if report.get("balances"):
        lines += ["", "## " + wording["balances"], "", wording["balance_headers"], "|---|---:|---:|---:|---:|"]
        for row in report["balances"]:
            lines += ["| " + " | ".join(cell(row[k]) for k in ("currency", "opening", "reported_closing", "calculated_closing", "difference")) + " |"]
        lines += ["", wording["totals_note"], ""]
        for currency, kinds in report["totals_by_kind"].items():
            lines += ["- " + cell(currency) + ": " + "; ".join(cell(k) + " " + cell(v) for k, v in kinds.items())]
    if report["input"].get("facts"):
        lines += ["", "## " + wording["facts"], ""]
        lines += ["- " + cell(key) + ": " + cell(value if value is not None else "unknown")
                  for key, value in report["input"]["facts"].items()]
    if report["input"].get("fields"):
        lines += ["", "## " + wording["fields"], "", wording["field_headers"], "|---|---|---|---|"]
        for field in report["input"]["fields"]:
            lines += ["| " + " | ".join(cell(field[k]) for k in ("label", "value", "status", "evidence_ids")) + " |"]
    lines += ["", "## " + wording["missing"], ""]
    lines += ["- `" + item.replace("`", "'").replace("\n", " ") + "`" for item in report.get("missing", [])]
    if not report.get("missing"):
        lines += [wording["review"]]
    lines += ["", "## " + wording["evidence"], ""]
    for item in report["sources"]:
        lines += [f"- `{item['path'].replace('`', '')}` — SHA-256 `{item['sha256']}`"]
    lines += ["", wording["detail"], ""]
    return "\n".join(lines)


def save(root, report, language=None):
    language = language or ws._load(ws._inside(root, ws.MARKER)).get("language", "en")
    if language == "de":
        language = "en"
    if language not in {"en", "ru"}:
        raise ws.WorkspaceError("Report language must be en or ru.")
    report.update(schema_version=1, created_at=ws._now(), language=language)
    relative = f"07_exports/{period(report['period'])}/preparation-{uuid.uuid4().hex}"
    markdown = render(report, language)
    with ws._locked(root):
        ws._check_audit(root)
        for source in report["sources"]:
            if capture(root, source["path"])["sha256"] != source["sha256"]:
                raise ws.WorkspaceError("A source changed during preparation; inspect and prepare again.")
        path = ws._inside(root, relative + ".json")
        ws._mkdir(path.parent)
        ws._atomic_json(path, report)
        ws._write_exclusive(ws._inside(root, relative + ".md"), markdown.encode("utf-8"))
        ws._audit(root, "preparation_saved", {"path": relative + ".json", "kind": report["kind"], "status": report["status"]})
    return {"status": report["status"], "path": ws._physical(root, relative + ".json"), "markdown_path": ws._physical(root, relative + ".md")}


def prepare(root, kind, input_path, language=None):
    root = ws._workspace(root)
    source = capture(root, input_path)
    value = ws._load(ws._inside(root, source["path"]))
    missing, evidence = validate(root, kind, value)
    report = {"kind": kind, "period": value["period"], "record_id": value["record_id"],
              "status": "needs_review" if missing else "ready_for_review", "filing_status": "not_submitted",
              "routes": routes(kind, value["facts"]), "missing": missing,
              "sources": [source, *evidence], "input": value,
              "scope": "Recorded inputs and source checks; no automatic verification of legal applicability or field completeness."}
    return save(root, report, language)


def verify(root, report_path):
    root = ws._workspace(root)
    report = ws._load(ws._inside(root, report_path))
    if not isinstance(report, dict) or not isinstance(report.get("sources"), list) or not report["sources"]:
        raise ws.WorkspaceError("Expected a preparation report with source fingerprints.")
    changes = []
    for source in report["sources"]:
        try:
            current = capture(root, source["path"])
            if current["sha256"] != source["sha256"]:
                changes.append(source["path"])
        except (OSError, ws.WorkspaceError):
            changes.append(source["path"])
    return {"status": "changed" if changes else "intact", "changed_sources": changes,
            "scope": "Source bytes only; no authenticity, legal validity or report-tampering certification."}


def filing_sources(root, report, require_ready=True):
    """Validate a supported preparation and expose its evidence to filing writers.

    Callers hold the workspace lock. None means an unrelated JSON document.
    This checks saved structure/current bytes, never legal or official-form validity.
    """
    if not isinstance(report, dict) or not isinstance(report.get("kind"), str) or report["kind"] not in FIELDS:
        return None
    exact(report, {"kind", "period", "record_id", "status", "filing_status", "routes", "missing",
                   "sources", "input", "scope", "schema_version", "created_at", "language"}, "preparation report")
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported preparation report schema.")
    missing, evidence = validate(root, report["kind"], report["input"])
    expected_status = "needs_review" if missing else "ready_for_review"
    if (report["period"] != report["input"]["period"]
            or report["record_id"] != report["input"]["record_id"]
            or report["missing"] != missing or report["status"] != expected_status
            or report["filing_status"] != "not_submitted"
            or report["routes"] != routes(report["kind"], report["input"]["facts"])
            or not isinstance(report["language"], str) or report["language"] not in {"en", "ru"}):
        raise ws.WorkspaceError("Inconsistent preparation report; prepare a new version from its evidence.")
    text(report["created_at"], "preparation creation time")
    text(report["scope"], "preparation scope")
    if not isinstance(report["sources"], list) or not report["sources"]:
        raise ws.WorkspaceError("Preparation report is missing its input fingerprint.")
    first = report["sources"][0]
    exact(first, {"path", "sha256"}, "preparation input fingerprint")
    current = capture(root, text(first["path"], "preparation input path"))
    if report["sources"] != [current, *evidence]:
        raise ws.WorkspaceError("Preparation evidence changed or dependencies are incomplete; prepare a new version.")
    if ws._load(ws._inside(root, current["path"])) != report["input"]:
        raise ws.WorkspaceError("Preparation input does not match its saved source.")
    if require_ready and missing:
        raise ws.WorkspaceError("Preparation still needs review: " + ", ".join(missing))
    return [{"path": item["path"], "sha256": item["sha256"]} for item in report["sources"]]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    seed = sub.add_parser("template")
    seed.add_argument("--kind", required=True, choices=FIELDS)
    sub.add_parser("catalog")
    build = sub.add_parser("prepare")
    build.add_argument("--root", required=True)
    build.add_argument("--kind", required=True, choices=FIELDS)
    build.add_argument("--input", required=True)
    build.add_argument("--language", choices=["en", "ru"])
    check = sub.add_parser("verify")
    check.add_argument("--root", required=True)
    check.add_argument("--report", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "template":
            result = template(args.kind)
        elif args.command == "catalog":
            result = catalog()
        elif args.command == "verify":
            result = verify(args.root, args.report)
        else:
            result = prepare(args.root, args.kind, args.input, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ws.WorkspaceError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

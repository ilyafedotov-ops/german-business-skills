#!/usr/bin/env python3
"""Offline payment statement reconciliation; no tax posting or network access."""
from __future__ import annotations

import argparse
from decimal import Decimal
import json
import re
import sys

import workspace as ws
import workflows as wf

HEADERS = {"event_id", "booking_date", "kind", "amount", "currency", "related_id", "transfer_id", "bank_transaction_id"}
POSITIVE = {"charge", "fee_reversal", "refund_reversal", "dispute_reversal", "payout_reversal", "reserve_release"}
NEGATIVE = {"fee", "refund", "dispute", "payout", "reserve_hold"}
KINDS = POSITIVE | NEGATIVE | {"transfer", "fx", "adjustment"}
RELATED = {"fee", "fee_reversal", "refund", "refund_reversal", "dispute", "dispute_reversal", "payout_reversal"}
STRIPE_CATEGORIES = {"charge": "charge", "refund": "refund", "refund_failure": "refund_reversal",
                     "dispute": "dispute", "dispute_reversal": "dispute_reversal", "fee": "fee"}


def template():
    return {"schema_version": 1, "account_id": None, "period": None, "balance_basis": None,
            "coverage_confirmed": False, "provider_role": "unknown",
            "sources": [{"format": "normalized", "path": None}], "bank_path": None,
            "balances": [{"currency": "EUR", "opening": None, "closing": None}]}


def normalize(data, adapter, source):
    if adapter == "normalized":
        rows = ws._rows(data, HEADERS)
        return [{**{key: row[key] for key in HEADERS}, "source": source, "source_row": i}
                for i, row in enumerate(rows, 2)]
    if adapter != "stripe_activity":
        raise ws.WorkspaceError("Unsupported adapter; use normalized or stripe_activity.")
    rows = ws._rows(data, {"balance_transaction_id", "created_utc", "currency", "gross", "fee", "net", "reporting_category",
                           "is_managed_payments", "withheld_tax"})
    events = []
    for number, row in enumerate(rows, 2):
        if any(value is None for value in row.values()):
            raise ws.WorkspaceError("Truncated Stripe CSV row, including optional columns.")
        category = row["reporting_category"]
        if category not in STRIPE_CATEGORIES:
            raise ws.WorkspaceError("Unsupported Stripe reporting_category: " + category + ". Preserve export and review a normalized mapping.")
        if row["is_managed_payments"].lower() not in {"false", "0"} or ws._amount(row["withheld_tax"]) != 0:
            raise ws.WorkspaceError("Managed payments / withheld tax require a reviewed normalized mapping.")
        timestamp = row["created_utc"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:Z)?", timestamp):
            raise ws.WorkspaceError("Select created_utc and supply YYYY-MM-DD HH:MM:SS or ISO seconds in UTC.")
        from datetime import datetime
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ws.WorkspaceError("Invalid Stripe UTC timestamp.") from exc
        gross, fee, net = (ws._amount(row[key]) for key in ("gross", "fee", "net"))
        if ws._add(gross, fee.copy_negate()) != net:
            raise ws.WorkspaceError("Stripe gross minus fee does not equal net.")
        identifier = ws._identifier(row["balance_transaction_id"])
        base = {"booking_date": timestamp[:10], "currency": row["currency"].upper(),
                "source": source, "source_row": number, "raw_category": category,
                "related_id": row.get("charge_id") or row.get("source_id", ""),
                "transfer_id": "", "bank_transaction_id": "", "automatic_payout_id": row.get("automatic_payout_id", "")}
        events.append({**base, "event_id": identifier, "kind": STRIPE_CATEGORIES[category], "amount": format(gross, "f")})
        if fee:
            events.append({**base, "event_id": identifier + ":fee", "kind": "fee" if fee > 0 else "fee_reversal",
                           "amount": format(fee.copy_negate(), "f"), "related_id": identifier})
    return events


def prepare(root, input_path, language=None):
    root = ws._workspace(root)
    source = wf.capture(root, input_path)
    config = ws._load(ws._inside(root, source["path"]))
    wf.exact(config, template(), "payment request")
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported payment schema_version.")
    wf.text(config["account_id"], "account_id")
    wf.text(config["balance_basis"], "balance_basis")
    period = ws._period(config["period"])
    if type(config["coverage_confirmed"]) is not bool:
        raise ws.WorkspaceError("coverage_confirmed must be a boolean.")
    if wf.text(config["provider_role"], "provider_role") not in {"processor", "merchant_of_record", "bank", "unknown"}:
        raise ws.WorkspaceError("Unsupported provider_role.")
    if not isinstance(config["sources"], list) or not config["sources"]:
        raise ws.WorkspaceError("At least one event source is required.")
    sources, events, source_paths = [source], [], set()
    stripe = False
    for item in config["sources"]:
        wf.exact(item, {"path", "format"}, "payment source")
        wf.text(item["path"], "source path")
        fingerprint = wf.capture(root, item["path"])
        if fingerprint["path"] in source_paths:
            raise ws.WorkspaceError("Duplicate source file.")
        source_paths.add(fingerprint["path"])
        sources.append(fingerprint)
        events.extend(normalize(ws._read_regular(ws._inside(root, fingerprint["path"])), item["format"], fingerprint["path"]))
        stripe = stripe or item["format"] == "stripe_activity"
    if not isinstance(config["balances"], list) or not config["balances"]:
        raise ws.WorkspaceError("Opening and closing statement balances are required.")
    balances = {}
    for item in config["balances"]:
        wf.exact(item, {"currency", "opening", "closing"}, "balance")
        currency = ws._currency(wf.text(item["currency"], "currency"))
        if currency in balances:
            raise ws.WorkspaceError("Duplicate balance currency.")
        balances[currency] = {key: ws._amount(wf.text(item[key], key)) for key in ("opening", "closing")}
    issues = []
    if not events:
        issues.append("empty_activity")
    if not config["coverage_confirmed"]:
        issues.append("statement_coverage_unconfirmed")
    if config["provider_role"] in {"unknown", "merchant_of_record"}:
        issues.append("contract_and_seller_review")
    totals, activity, ids, payout_groups = {}, {}, set(), {}
    for event in events:
        identifier = ws._identifier(event["event_id"])
        if identifier in ids:
            raise ws.WorkspaceError("Duplicate event_id across imported sources.")
        ids.add(identifier)
        day = ws._day(event["booking_date"])
        if day[:7] != period:
            raise ws.WorkspaceError("Event booking dates must be in the requested month (Stripe: UTC).")
        kind = event["kind"]
        if kind not in KINDS:
            raise ws.WorkspaceError("Unsupported event kind; review mapping before import.")
        amount = ws._amount(event["amount"])
        currency = ws._currency(event["currency"])
        if currency not in balances:
            raise ws.WorkspaceError("Every event currency requires opening and closing balances.")
        if (kind in POSITIVE and amount < 0) or (kind in NEGATIVE and amount > 0):
            raise ws.WorkspaceError("Event amount has the wrong sign for its kind.")
        activity[currency] = ws._add(activity.get(currency, Decimal(0)), amount)
        group = totals.setdefault(currency, {})
        group[kind] = ws._add(group.get(kind, Decimal(0)), amount)
        if kind in RELATED and not event["related_id"]:
            issues.append("related_evidence_missing:" + identifier)
        if kind in {"refund", "refund_reversal", "dispute", "dispute_reversal", "payout_reversal"}:
            issues.append("correction_evidence_review:" + identifier)
        if kind in {"fx", "transfer", "reserve_hold", "reserve_release", "adjustment"}:
            issues.append("balance_movement_review:" + identifier)
            if kind in {"fx", "transfer"} and not event["transfer_id"]:
                issues.append("transfer_link_missing:" + identifier)
        bank_id = event["bank_transaction_id"]
        if kind == "payout":
            if not bank_id:
                issues.append("payout_bank_link_missing:" + identifier)
            else:
                key = (ws._identifier(bank_id), currency)
                payout_groups[key] = ws._add(payout_groups.get(key, Decimal(0)), amount.copy_negate())
        elif bank_id:
            raise ws.WorkspaceError("Only payout events may carry bank_transaction_id; review other movements separately.")
    bank = {}
    if config["bank_path"] is not None:
        fingerprint = wf.capture(root, wf.text(config["bank_path"], "bank_path"))
        sources.append(fingerprint)
        for row in ws._rows(ws._read_regular(ws._inside(root, fingerprint["path"])), {"transaction_id", "booking_date", "amount", "currency"}):
            identifier = ws._identifier(row["transaction_id"])
            if identifier in bank:
                raise ws.WorkspaceError("Duplicate bank transaction_id.")
            ws._day(row["booking_date"])
            bank[identifier] = {"currency": ws._currency(row["currency"]), "amount": ws._amount(row["amount"]),
                                "booking_date": row["booking_date"]}
    matches = []
    for (identifier, currency), amount in payout_groups.items():
        row = bank.get(identifier)
        if row is None or row["currency"] != currency or row["amount"] != amount:
            issues.append("payout_bank_difference:" + identifier)
        else:
            matches.append({"bank_transaction_id": identifier, "currency": currency, "amount": format(amount, "f"),
                            "booking_date": row["booking_date"]})
    balance_rows = []
    for currency, values in sorted(balances.items()):
        calculated = ws._add(values["opening"], activity.get(currency, Decimal(0)))
        difference = ws._add(calculated, values["closing"].copy_negate())
        if difference:
            issues.append("closing_balance_difference:" + currency)
        balance_rows.append({"currency": currency, "opening": format(values["opening"], "f"),
                             "reported_closing": format(values["closing"], "f"), "calculated_closing": format(calculated, "f"),
                             "difference": format(difference, "f")})
    # Correction facts may remain open even when all arithmetic matches.
    arithmetic_issues = [item for item in issues if not item.startswith("correction_evidence_review:")]
    report = {"kind": "payments", "period": period, "account_id": config["account_id"],
              "status": "needs_review" if arithmetic_issues else "arithmetic_matched", "tax_status": "not_assessed",
              "filing_status": "not_submitted", "routes": ["payment_review"], "missing": issues,
              "sources": sources, "input": config, "events": events, "balances": balance_rows,
              "totals_by_kind": {cur: {key: format(value, "f") for key, value in group.items()} for cur, group in totals.items()},
              "payout_matches": matches, "stripe_activity_excludes_payouts": stripe,
              "bank_coverage": {"supplied_rows": len(bank), "referenced_rows": len({key[0] for key in payout_groups}),
                                "unreferenced_rows": len(set(bank) - {key[0] for key in payout_groups}),
                                "scope": "Only explicitly linked payouts; not a reconciliation of the whole bank statement."},
              "scope": "Supplied statement balance only. Payouts/transfers are movements, not additional revenue. No tax or invoice recognition."}
    return wf.save(root, report, language)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("template")
    build = sub.add_parser("prepare")
    build.add_argument("--root", required=True)
    build.add_argument("--input", required=True)
    build.add_argument("--language", choices=["en", "ru"])
    args = parser.parse_args(argv)
    try:
        result = template() if args.command == "template" else prepare(args.root, args.input, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ws.WorkspaceError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Private document workflows; explicit Lexware actions can contact the provider."""
import argparse
from datetime import date
import json
import sys

import workspace as ws
from casefiles import accounting, invoicing, invoice_payments, payment_followup, lexware
from casefiles import bank, documents, archive, folders, invoice_xml, overview, reviews, storage


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("payment-followup-template")
    for name in ("payment-followup-prepare", "payment-followup-check"):
        followup = sub.add_parser(name)
        followup.add_argument("--root", required=True)
        if name == "payment-followup-prepare":
            followup.add_argument("--input", required=True)
            followup.add_argument("--expected-sha256", required=True)
            followup.add_argument("--language", choices=["en", "ru"], default="en")
        else:
            followup.add_argument("--report", required=True)
    sub.add_parser("invoice-payment-template")
    for name in ("invoice-payment-prepare", "invoice-payment-check"):
        payment = sub.add_parser(name)
        payment.add_argument("--root", required=True)
        if name == "invoice-payment-prepare":
            payment.add_argument("--input", required=True)
            payment.add_argument("--expected-sha256", required=True)
            payment.add_argument("--language", choices=["en", "ru"], default="en")
        else:
            payment.add_argument("--report", required=True)
    sub.add_parser("lexware-template")
    lexware_action = sub.add_parser("lexware-action")
    lexware_action.add_argument("--root", required=True)
    lexware_action.add_argument("--input", required=True)
    lexware_action.add_argument("--expected-sha256", required=True)
    lexware_handoff = sub.add_parser("lexware-handoff")
    lexware_handoff.add_argument("--root", required=True)
    lexware_handoff.add_argument("--id", required=True)
    lexware_handoff.add_argument("--kind", choices=["finalize", "send"], required=True)
    invoice_template = sub.add_parser("invoice-template")
    invoice_template.add_argument("--kind", choices=["invoice", "action"], required=True)
    for name in ("invoice-create", "invoice-action", "invoice-show", "invoice-list", "invoice-report"):
        part = sub.add_parser(name)
        part.add_argument("--root", required=True)
        if name in {"invoice-create", "invoice-action"}:
            part.add_argument("--input", required=True)
        else:
            part.add_argument("--language", choices=["en", "ru"], default="en")
        if name in {"invoice-show", "invoice-report"}:
            part.add_argument("--id", required=True)
        if name == "invoice-action":
            part.add_argument("--expected-sha256", required=True)
    accounting_template = sub.add_parser("accounting-template")
    accounting_template.add_argument("--kind", choices=["configuration", "entry", "filing", "filing-action"], required=True)
    for name in ("accounting-status", "accounting-configure", "entry-post", "entry-reverse", "period-report", "filing-create", "filing-show", "filing-check", "filing-action"):
        part = sub.add_parser(name)
        part.add_argument("--root", required=True)
        if name in {"accounting-configure", "entry-post", "filing-create", "filing-action"}:
            part.add_argument("--input", required=True)
        if name in {"accounting-configure", "filing-action"}:
            part.add_argument("--expected-sha256", required=name == "filing-action")
        if name in {"filing-show", "filing-check"}:
            part.add_argument("--id", required=True)
        if name == "period-report":
            part.add_argument("--period", required=True)
        if name == "entry-reverse":
            for flag in ("entry-id", "reversal-id", "evidence", "actor", "note"):
                part.add_argument("--" + flag, required=True)
    template = sub.add_parser("template")
    template.add_argument("--kind", choices=["proposal", "bank-mapping", "source-check", "extracted-field"], required=True)
    verify = sub.add_parser("verify-archive")
    verify.add_argument("--bundle", required=True)
    commands = {}
    for name in ("scan-folder", "receive", "catalog", "catalog-save", "record", "proposal-save", "source-check", "observe", "bank-preview", "bank-approve", "inspect-xml", "overview", "archive"):
        commands[name] = sub.add_parser(name)
        commands[name].add_argument("--root", required=True)
    commands["scan-folder"].add_argument("--source", required=True)
    commands["scan-folder"].add_argument("--max-entries", type=int, default=1000)
    commands["scan-folder"].add_argument("--max-depth", type=int, default=10)
    receive = commands["receive"]
    receive.add_argument("--source", required=True, nargs="+")
    receive.add_argument("--period", required=True)
    receive.add_argument("--received-on", default=date.today().isoformat())
    receive.add_argument("--type", choices=sorted(documents.TYPES), default="unknown")
    receive.add_argument("--title")
    commands["catalog"].add_argument("--period")
    commands["catalog"].add_argument("--document-id")
    for name in ("catalog-save", "proposal-save", "source-check", "observe"):
        commands[name].add_argument("--input", required=True)
    for name in ("catalog-save", "proposal-save"):
        commands[name].add_argument("--expected-sha256")
    commands["record"].add_argument("--collection", choices=storage.COLLECTIONS, required=True)
    commands["record"].add_argument("--id", required=True)
    commands["bank-preview"].add_argument("--document-id", required=True)
    commands["bank-preview"].add_argument("--mapping", required=True)
    commands["bank-preview"].add_argument("--period", required=True)
    commands["bank-approve"].add_argument("--preview", required=True)
    commands["bank-approve"].add_argument("--expected-sha256", required=True)
    commands["bank-approve"].add_argument("--reviewer", required=True)
    commands["bank-approve"].add_argument("--evidence", required=True)
    commands["inspect-xml"].add_argument("--document-id", required=True)
    for name in ("overview", "archive"):
        commands[name].add_argument("--period", required=True)
        commands[name].add_argument("--as-of")
    commands["overview"].add_argument("--language", choices=["en", "ru"])
    args = parser.parse_args(argv)
    try:
        command = args.command
        if command == "payment-followup-template":
            result = payment_followup.template()
        elif command == "payment-followup-prepare":
            result = payment_followup.prepare(args.root, args.input, args.expected_sha256, args.language)
        elif command == "payment-followup-check":
            result = payment_followup.check(args.root, args.report)
        elif command == "invoice-payment-template":
            result = invoice_payments.template()
        elif command == "invoice-payment-prepare":
            result = invoice_payments.prepare(args.root, args.input, args.expected_sha256, args.language)
        elif command == "invoice-payment-check":
            result = invoice_payments.check(args.root, args.report)
        elif command == "lexware-template":
            result = lexware.template()
        elif command == "lexware-action":
            root = ws._workspace(args.root)
            result = lexware.act(root, ws._load(ws._inside(root, args.input)), args.expected_sha256)
        elif command == "lexware-handoff":
            result = lexware.handoff(args.root, args.id, args.kind)
        elif command == "invoice-template":
            result = invoicing.template(args.kind)
        elif command.startswith("invoice-"):
            root = ws._workspace(args.root)
            if command == "invoice-create":
                result = invoicing.create(root, ws._load(ws._inside(root, args.input)))
            elif command == "invoice-action":
                result = invoicing.act(root, ws._load(ws._inside(root, args.input)), args.expected_sha256)
            elif command == "invoice-show":
                result = invoicing.show(root, args.id, args.language)
            elif command == "invoice-list":
                result = invoicing.list_invoices(root, args.language)
            else:
                result = invoicing.export(root, args.id, args.language)
        elif command == "accounting-template":
            result = accounting.template(args.kind)
        elif command in {"accounting-status", "accounting-configure", "entry-post", "entry-reverse", "period-report", "filing-create", "filing-show", "filing-check", "filing-action"}:
            root = ws._workspace(args.root)
            value = ws._load(ws._inside(root, args.input)) if hasattr(args, "input") else None
            if command == "accounting-status":
                result = accounting.status(root)
            elif command == "accounting-configure":
                result = accounting.configure(root, value, args.expected_sha256)
            elif command == "entry-post":
                result = accounting.post(root, value)
            elif command == "entry-reverse":
                result = accounting.reverse(root, args.entry_id, args.reversal_id, args.evidence, args.actor, args.note)
            elif command == "period-report":
                result = accounting.export_report(root, args.period)
            elif command == "filing-create":
                result = accounting.create_filing(root, value)
            elif command == "filing-check":
                result = accounting.check_filing(root, args.id)
            elif command == "filing-show":
                result = accounting.get_filing(root, args.id)
            else:
                result = accounting.filing_action(root, value, args.expected_sha256)
        elif command == "template":
            result = {"proposal": reviews.proposal_template, "bank-mapping": bank.mapping_template,
                      "source-check": lambda: storage.template("source-check.json"),
                      "extracted-field": lambda: storage.template("extracted-field.json")}[args.kind]()
        elif command == "verify-archive":
            result = archive.verify(args.bundle)
        else:
            root = ws._workspace(args.root)
            def input_file(relative):
                return ws._load(ws._inside(root, relative))
            if command == "scan-folder":
                result = folders.scan(root, args.source, args.max_entries, args.max_depth)
            elif command == "receive":
                if args.title is not None and len(args.source) != 1:
                    raise ws.WorkspaceError("A custom title can describe only one source at a time.")
                results, errors = [], []
                for source in args.source:
                    try:
                        results.append(documents.receive(root, source, args.period, args.received_on, args.type, args.title))
                    except (OSError, ws.WorkspaceError) as exc:
                        errors.append({"source": source, "error": str(exc)})
                result = {"received": results, "errors": errors, "overview": overview.generate(root, args.period)}
            elif command == "catalog":
                if args.document_id:
                    record = documents.get(root, args.document_id)
                    saved = storage.load(root)["documents"].get(args.document_id)
                    result = {"record": record, "sha256": storage.digest(saved) if saved is not None else None}
                else:
                    result = {"documents": documents.catalog(root, args.period)}
            elif command == "record":
                state = storage.load(root)
                record = state[args.collection].get(args.id)
                if record is None:
                    raise ws.WorkspaceError("Record not found.")
                editable = {key: value for key, value in record.items() if key in reviews.proposal_template()} if args.collection == "proposals" else record
                result = {"record": record, "editable": editable, "sha256": storage.digest(record)}
            elif command == "catalog-save":
                result = documents.save(root, input_file(args.input), args.expected_sha256)
            elif command == "proposal-save":
                result = reviews.save_proposal(root, input_file(args.input), args.expected_sha256)
            elif command == "source-check":
                result = reviews.save_source_check(root, input_file(args.input))
            elif command == "observe":
                result = reviews.observe(root, input_file(args.input))
            elif command == "bank-preview":
                result = bank.preview(root, args.document_id, input_file(args.mapping), args.period)
            elif command == "bank-approve":
                result = bank.approve(root, args.preview, args.expected_sha256, args.reviewer, args.evidence)
            elif command == "inspect-xml":
                result = invoice_xml.inspect(root, args.document_id)
            elif command == "overview":
                result = overview.generate(root, args.period, args.as_of, args.language)
            else:
                result = archive.build(root, args.period, args.as_of)
                result["overview"] = overview.generate(root, args.period, args.as_of)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("status") == "failed" or result.get("errors") else 0
    except (OSError, ws.WorkspaceError, KeyError, TypeError, ValueError) as exc:
        print("Operation stopped: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

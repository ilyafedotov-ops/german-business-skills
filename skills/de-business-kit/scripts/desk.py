#!/usr/bin/env python3
"""Offline document review desk. The assistant handles records behind the conversation."""
import argparse
from datetime import date
import json
import sys

import workspace as ws
from casefiles import bank, documents, archive, invoice_xml, overview, reviews, storage


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    template = sub.add_parser("template")
    template.add_argument("--kind", choices=["proposal", "bank-mapping", "source-check", "extracted-field"], required=True)
    verify = sub.add_parser("verify-archive")
    verify.add_argument("--bundle", required=True)
    commands = {}
    for name in ("receive", "catalog", "catalog-save", "record", "proposal-save", "source-check", "observe", "bank-preview", "bank-approve", "inspect-xml", "overview", "archive"):
        commands[name] = sub.add_parser(name)
        commands[name].add_argument("--root", required=True)
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
        if command == "template":
            result = {"proposal": reviews.proposal_template, "bank-mapping": bank.mapping_template,
                      "source-check": lambda: storage.template("source-check.json"),
                      "extracted-field": lambda: storage.template("extracted-field.json")}[args.kind]()
        elif command == "verify-archive":
            result = archive.verify(args.bundle)
        else:
            root = ws._workspace(args.root)
            def input_file(relative):
                return ws._load(ws._inside(root, relative))
            if command == "receive":
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

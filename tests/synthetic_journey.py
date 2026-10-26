"""Reusable CLI-driven synthetic fixture; not a live desktop/provider test."""
import csv
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws

FIXTURES = ROOT / "tests/fixtures/month"


def command(script, *arguments):
    run = subprocess.run([sys.executable, "-B", str(SCRIPTS / script), *map(str, arguments)],
                         capture_output=True, text=True, encoding="utf-8")
    if run.returncode:
        raise RuntimeError(run.stderr + run.stdout)
    return json.loads(run.stdout)


def run(root, language="en"):
    root = Path(root)
    command("workspace.py", "init", "--root", root, "--year", 2026, "--language", language)
    received = command("desk.py", "receive", "--root", root, "--source",
                       FIXTURES / "invoice.synthetic.xml", FIXTURES / "authority.synthetic.pdf", FIXTURES / "bank.synthetic.csv",
                       "--period", "2026-10", "--received-on", "2026-10-25")
    registry = json.loads(ws._inside(root, "00_admin/documents.json").read_text())
    ids = {row["original_name"]: row["document_id"] for row in registry["documents"]}
    def save_input(name, value):
        relative = "00_admin/inbox/" + name
        ws._inside(root, relative).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        return relative
    for name, kind in (("invoice.synthetic.xml", "invoice"), ("authority.synthetic.pdf", "authority_letter"), ("bank.synthetic.csv", "bank_statement")):
        current = command("desk.py", "catalog", "--root", root, "--document-id", ids[name])
        current["record"]["type"] = kind
        command("desk.py", "catalog-save", "--root", root, "--input", save_input("catalog.json", current["record"]), "--expected-sha256", current["sha256"])
    inspected = command("desk.py", "inspect-xml", "--root", root, "--document-id", ids["invoice.synthetic.xml"])
    extraction = json.loads((root / inspected["path"]).read_text())
    proposal = command("desk.py", "template", "--kind", "proposal")
    proposal.update(proposal_id="synthetic-proposal", document_id=ids["invoice.synthetic.xml"], activity_id="synthetic-activity", period="2026-10", fields=extraction["fields"])
    command("desk.py", "proposal-save", "--root", root, "--input", save_input("proposal.json", proposal))
    mapping = command("desk.py", "template", "--kind", "bank-mapping")
    mapping.update(mapping_id="synthetic-map", account_id="synthetic-account")
    mapping["columns"].update(date="Buchungstag", amount="Betrag", currency="Waehrung", transaction_id="ID", reference="Text")
    preview = command("desk.py", "bank-preview", "--root", root, "--document-id", ids["bank.synthetic.csv"],
                      "--mapping", save_input("bank-map.json", mapping), "--period", "2026-10")
    proof = "08_correspondence/synthetic-mapping-review.md"
    ws._inside(root, proof).write_text("Synthetic test routine checked the declared columns, decimal commas, signs and three source IDs. This is not a real user or tax approval.\n", encoding="utf-8")
    imported = command("desk.py", "bank-approve", "--root", root, "--preview", preview["path"], "--expected-sha256", preview["sha256"],
                       "--reviewer", "synthetic test routine", "--evidence", proof)
    rows = list(csv.DictReader(io.StringIO((root / imported["csv_path"]).read_text())))
    ledger = "04_accounting/synthetic-ledger.csv"
    ws._inside(root, ledger).write_text("entry_id,transaction_id,amount,currency\n" + "\n".join(
        f"synthetic-{i},{row['transaction_id']},{row['amount']},{row['currency']}" for i, row in enumerate(rows[:2], 1)) + "\n", encoding="utf-8")
    reconciled = command("workspace.py", "reconcile", "--root", root, "--bank", imported["csv_path"], "--ledger", ledger, "--period", "2026-10")
    task = {"schema_version": 1, "id": "synthetic-letter-review", "title": "Clarify the authority request and its stated date",
            "owner": "user", "status": "pending", "due_date": "2026-10-26", "deadline_source": "Synthetic training letter; legal deadline and remedy unconfirmed"}
    command("workspace.py", "entry", "--root", root, "--collection", "tasks", "--input", save_input("letter-task.json", task))
    letter = command("desk.py", "catalog", "--root", root, "--document-id", ids["authority.synthetic.pdf"])
    letter["record"]["links"]["task_ids"] = [task["id"]]
    command("desk.py", "catalog-save", "--root", root, "--input", save_input("catalog-letter.json", letter["record"]), "--expected-sha256", letter["sha256"])
    view = command("desk.py", "overview", "--root", root, "--period", "2026-10", "--as-of", "2026-10-25", "--language", language)
    resumed = command("workspace.py", "start", "--root", root)
    bundle = command("desk.py", "archive", "--root", root, "--period", "2026-10", "--as-of", "2026-10-25")
    verified = command("desk.py", "verify-archive", "--bundle", root / bundle["zip_path"])
    return {"root": str(root), "overview": view, "bundle": bundle, "verified": verified, "reconciliation": reconciled, "resumed": resumed["action"]}


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else "en"), ensure_ascii=False, indent=2))

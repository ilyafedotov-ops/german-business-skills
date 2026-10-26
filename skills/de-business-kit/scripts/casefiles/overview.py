"""A local, read-only HTML/Markdown view generated from canonical records."""
from datetime import date
import html
import os
from urllib.parse import quote
from pathlib import Path
import uuid
import re

import workspace as ws
from . import storage as st
from . import summary
from . import accounting

MARK = "<!-- German Business Kit generated overview v1 -->\n"
CSS = """*{box-sizing:border-box}body{margin:0;background:#f5f6f3;color:#182d29;font:16px/1.55 system-ui,sans-serif}
main,header,nav{max-width:1100px;margin:auto;padding:22px 28px}header{padding-top:40px}h1{font-size:clamp(28px,5vw,44px);line-height:1.12;margin:8px 0}
h2{font-size:23px;margin:0 0 14px}h3{font-size:18px}p{max-width:80ch}.muted{color:#52635f}.eyebrow{letter-spacing:.08em;text-transform:uppercase;font-size:12px;font-weight:700}
nav{display:flex;gap:8px;flex-wrap:wrap;padding-top:0}a{color:#165d4e;text-underline-offset:4px}nav a{padding:8px 14px;background:#fff;border:1px solid #cbd7d0;border-radius:24px;text-decoration:none}
a:focus-visible,summary:focus-visible{outline:3px solid #a65619;outline-offset:4px}section{scroll-margin-top:20px;background:#fff;border:1px solid #d7dfd9;border-radius:16px;padding:24px;margin:0 0 20px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.card{padding:16px;background:#f1f5f0;border-radius:10px}.card strong{display:block;font-size:30px}.card strong.pending{font-size:18px;line-height:1.5;margin-bottom:8px}.next{border-left:4px solid #23745d;padding-left:16px;margin:22px 0 0}
.warning{background:#fff5df;border:1px solid #d9bd7d;padding:16px;border-radius:10px}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;padding:12px 8px;border-bottom:1px solid #e2e7e2}th{font-size:13px;color:#52635f}td{overflow-wrap:anywhere}
.badge{white-space:nowrap;font-size:12px;background:#edf2ed;padding:4px 8px;border-radius:5px}li{margin-bottom:10px}#active-tasks{overflow-wrap:anywhere}code{font-size:12px;overflow-wrap:anywhere}details{margin-top:16px}summary{cursor:pointer}footer{font-size:13px;color:#52635f;padding:12px 0 32px}
@media(max-width:600px){main,header,nav{padding-left:16px;padding-right:16px}section{padding:18px}.cards{grid-template-columns:repeat(2,1fr)}.card strong{font-size:26px}nav a{font-size:14px}th,td{padding:10px 5px;font-size:14px}}
@media print{nav{display:none}body{background:white}section{break-inside:avoid}a{color:inherit}}"""


def language_for(root, language):
    chosen = language or ws._load(ws._inside(root, ws.MARKER)).get("language", "en")
    if chosen == "de":
        chosen = "en"
    if chosen not in {"en", "ru"}:
        raise ws.WorkspaceError("Overview language must be en or ru.")
    return chosen


def generate(root, period, as_of=None, language=None):
    root = ws._workspace(root)
    # One snapshot: a writer cannot change a filing between collection and rendering.
    with ws._locked(root):
        return _generate(root, period, as_of, language)


def _generate(root, period, as_of, language):
    ws._period(period)
    as_of = ws._day(as_of or date.today().isoformat())
    language = language_for(root, language)
    words = st.template("casework-messages.json")[language]
    errors = []
    events = []
    try:
        ws._check_audit(root)
        events = ws._load(ws._inside(root, ws.EVENTS))
        result = summary.collect(root, period, as_of)
        result["accounting"], result["filings"] = accounting.overview_state(root, period)
        result["open_questions"] = [row for row in result["questions"] if row["status"] in {"open", "deferred"}]
        result["open_items"].extend({"code": "question_open", "ref": row["id"], "detail": row["title"]}
                                    for row in result["open_questions"])
        result["open_items"].extend({"code": "filing_issue", "ref": row["filing_id"],
                                    "detail": issue.get("detail", issue["code"])}
                                   for row in result["filings"] for issue in row["issues"])
        result["open_items"].extend({"code": "submission_unconfirmed", "ref": row["filing_id"]}
                                   for row in result["filings"] if row["state"] == "submission_unconfirmed")
        result["open_items"].extend({"code": row["code"], "ref": period, "detail": row.get("detail", "")}
                                   for row in result["accounting"]["issues"])
    except (OSError, ws.WorkspaceError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
        result = {"schema_version": 1, "period": period, "as_of": as_of, "documents": [], "open_items": [], "overdue_tasks": [], "dated_tasks": [],
                  "counts": dict.fromkeys(("documents", "awaiting_review", "approved_proposals", "overdue_tasks", "unmatched_items", "bank_imports"))}
    result.update(health="needs_review" if errors else "ok", errors=errors, language=language, generated_by="de-business-kit-overview-v1")
    result.setdefault("accounting", {"accounting_system": "not_assessed", "method": "unresolved", "product": None,
                                    "period_entry_count": None, "totals": {}, "issues": [], "coverage": "not_assessed"})
    result.setdefault("filings", [])
    result.setdefault("open_questions", [])
    result.setdefault("active_tasks", [])
    result.setdefault("next_task_id", None)
    result["capabilities"] = {"accounting_ledger": "limited_cash_journal", "local_cash_journal": "available",
                              "complete_statutory_ledger": "not_implemented", "elster_submission": "not_implemented",
                              "tax_form_calculations": "not_implemented"}
    counts = result["counts"]
    soon = bool(result["dated_tasks"] and result["dated_tasks"][0]["due_date"] <= date.fromordinal(min(date.max.toordinal(), date.fromisoformat(as_of).toordinal() + 7)).isoformat())
    authority_due = any(response["due_date"] and response["due_date"] <= date.fromordinal(min(date.max.toordinal(), date.fromisoformat(as_of).toordinal() + 7)).isoformat()
                        for row in result["filings"] for response in row["responses"])
    if errors or any(row["code"] == "accounting_evidence" for row in result["accounting"]["issues"]):
        next_key = "repair"
    elif any(row["state"] == "submission_unconfirmed" for row in result["filings"]):
        next_key = "resolve_submission"
    elif soon or authority_due:
        next_key = "urgent"
    elif any(row["issues"] for row in result["filings"]):
        next_key = "resolve_filing"
    elif result["open_questions"]:
        next_key = "resolve_questions"
    elif result["active_tasks"]:
        next_key = "continue_task" if result["next_task_id"] else "review_tasks"
    elif not result["workspace_has_documents"] and not result["filings"] and result["accounting"]["accounting_system"] == "undecided":
        next_key = "choose_task"
    elif counts["awaiting_review"]:
        next_key = "review_docs"
    elif result["accounting"]["accounting_system"] == "undecided":
        next_key = "choose_accounting"
    elif counts["unmatched_items"] or not result.get("reports"):
        next_key = "reconcile"
    elif any(row["state"] in accounting.PREFLIGHT_ACTIONS for row in result["filings"]):
        next_key = "continue_filing"
    else:
        next_key = "next_accounting"
    result["next_action"] = next_key
    e = html.escape
    navigation = [("overview", "overview"), ("active-tasks", "active_tasks"), ("inbox", "inbox"), ("needs-review", "needs_review"), ("month", "month"), ("accounting-tax", "export")]
    sections = []
    cards = "".join(f'<div class="card"><strong class="{"pending" if number is None or errors else ""}">{number if number is not None and not errors else e(words["not_assessed"])}</strong>{e(words[key])}</div>' for key, number in counts.items())
    warning = (f'<p class="warning">{e(words["error"])}: {e(words["repair"])}</p><details><summary>{e(words["technical_details"])}</summary>'
               + "".join('<p><code>' + e(message) + '</code></p>' for message in errors) + '</details>') if errors else ""
    sections.append(f'<section id="overview"><h2>{e(words["overview"])}</h2>{warning}<div class="cards">{cards}</div><div class="next"><h3>{e(words["next"])}</h3><p>{e(words[next_key])}</p></div></section>')
    task_text = []
    task_titles = {item["id"]: item["title"] for item in result.get("tasks", [])}
    for task in result["active_tasks"]:
        text = task["title"] + " · " + words["task_states"][task["status"]]
        text += " · " + words["task_" + task["readiness"]]
        text += " · " + words["task_owner"] + ": " + task["owner"]
        text += " · " + (task["due_date"] + " / " + task["deadline_source"] if task["due_date"] else words["task_no_date"])
        if task["pending_dependencies"]:
            text += " · " + words["task_dependencies"] + ": " + ", ".join(task_titles[key] for key in task["pending_dependencies"])
        if task["note"]:
            text += " · " + task["note"]
        task_text.append(text)
    task_html = '<ul>' + ''.join('<li>' + e(text) + '</li>' for text in task_text) + '</ul>' if task_text else '<p>' + e(words["repair"] if errors else words["no_active_tasks"]) + '</p>'
    sections.append(f'<section id="active-tasks"><h2>{e(words["active_tasks"])}</h2><p class="muted">{e(words["tasks_scope"])}</p>{task_html}</section>')
    rows = "".join('<tr><td>' + e(item["title"]) + '</td><td>' + e(words["types"][item["type"]]) + '</td><td><span class="badge">' + e(words["states"][item["review_status"]]) + '</span></td></tr>' for item in result["documents"])
    inbox = ('<div class="table-wrap"><table><thead><tr>' + ''.join('<th scope="col">' + e(words[key]) + '</th>' for key in ("name", "type", "status")) + '</tr></thead><tbody>' + rows + '</tbody></table></div>') if rows else '<p>' + e(words["repair"] if errors else words["empty"]) + '</p>'
    sections.append(f'<section id="inbox"><h2>{e(words["inbox"])}</h2>{inbox}</section>')
    labels = {item["document_id"]: item["title"] for item in result["documents"]}
    labels.update({item["proposal_id"]: labels.get(item["document_id"], words["status"]) for item in result.get("proposals", [])})
    labels.update({item["id"]: item["title"] for item in result.get("tasks", [])})
    labels.update({item["id"]: item["title"] for item in result["open_questions"]})
    labels.update({item["filing_id"]: item["form"] + " · " + item["period"] + " · " + item["filing_id"] for item in result["filings"]})
    open_text = [words["codes"].get(item["code"], item["code"]) + " · " + labels.get(item["ref"], words["month"])
                 + (" · " + item["detail"] if item.get("detail") and item["code"] != "question_open" else "") for item in result["open_items"]]
    open_html = '<ul>' + ''.join('<li>' + e(text) + '</li>' for text in open_text) + '</ul>' if open_text else '<p>' + e(words["repair"] if errors else words["no_open"]) + '</p>'
    identifiers = ''.join('<li><code>' + e(item["ref"]) + '</code></li>' for item in result["open_items"])
    sections.append(f'<section id="needs-review"><h2>{e(words["needs_review"])}</h2>{open_html}<details><summary>{e(words["evidence"])}</summary><ul>{identifiers}</ul></details></section>')
    task_rows = ''.join('<li><strong>' + e(task["title"]) + '</strong> · ' + e(task["due_date"]) + '<br><span class="muted">' + e(task["deadline_source"]) + '</span></li>' for task in result["dated_tasks"])
    sections.append(f'<section id="month"><h2>{e(words["month"])} · {period}</h2><p>{e(words["coverage"])}</p><h3>{e(words["tasks"])}</h3><ul>{task_rows}</ul></section>')
    export_link = ""
    for event in reversed(events):
        details = event.get("details", {})
        candidate = details.get("zip_path")
        if (event.get("action") == "archive_built" and details.get("period") == period and isinstance(candidate, str)
                and re.fullmatch(r"07_exports/\d{4}-\d{2}/archive-[0-9a-f]{32}\.zip", candidate)):
            if ws._inside(root, candidate).is_file():
                export_link = '<p><a href="' + quote(os.path.relpath(ws._inside(root, candidate), ws._path(root, '00_admin')).replace(os.sep, '/')) + '">' + e(words["open_bundle"]) + '</a></p>'
            break
    account = result["accounting"]
    accounting_text = [words["system"] + ": " + words["systems"][account["accounting_system"]],
                       words["method"] + ": " + (account["method"] if account["method"] != "unresolved" else words["not_assessed"]),
                       words["period_entries"] + ": " + (str(account["period_entry_count"]) if account["period_entry_count"] is not None else words["not_assessed"]),
                       words["coverage_unconfirmed"]]
    if account["product"]:
        accounting_text.insert(1, words["product"] + ": " + account["product"])
    for currency, totals in account["totals"].items():
        accounting_text.append(words["cash_net"] + ": " + totals["operating_cash_net"] + " " + currency)
    filing_text = []
    for row in result["filings"]:
        text = row["filing_id"] + " · " + row["form"] + " · " + row["period"] + ": " + words["filing_states"][row["state"]]
        text += " · " + words["filing_steps"][row["next_step"]]
        filing_text.append(text)
        for response in row["responses"]:
            filing_text.append(words["authority_response"] + ": " + words["response_kinds"][response["kind"]]
                               + (" · " + response["due_date"] if response["due_date"] else "")
                               + " · " + words["source"] + ": " + response["evidence_path"])
    sections.append(f'<section id="accounting-tax"><h2>{e(words["export"])}</h2><p>{e(words["stages"])}</p><ul>'
                    + ''.join('<li>' + e(text) + '</li>' for text in accounting_text)
                    + '</ul><h3>' + e(words["filings"]) + '</h3><ul>'
                    + ''.join('<li>' + e(text) + '</li>' for text in (filing_text or [words["no_filings"]]))
                    + f'</ul><details><summary>{e(words["limits"])}</summary><p>{e(words["ledger_gap"])}</p><p>{e(words["elster_gap"])}</p></details><h3>{e(words["archive_heading"])}</h3><p>{e(words["export_text"])}</p><p>{e(words["prepare_export"])}</p>{export_link}</section>')
    document = MARK + f'<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>{e(words["title"])}</title><style>{CSS}</style></head><body><header><span class="eyebrow">German Business Kit</span><h1>{e(words["title"])}</h1><p class="muted">{e(words["subtitle"])}</p><p>{e(words["period"])}: <strong>{period}</strong> · {e(words["as_of"])}: {as_of}</p></header><nav aria-label="{e(words["overview"])}">' + ''.join(f'<a href="#{identifier}">{e(words[key])}</a>' for identifier, key in navigation) + '</nav><main>' + ''.join(sections) + '<footer>' + e(words["boundary"]) + '<br>' + e(words["snapshot"]) + '</footer></main></body></html>\n'
    body = f"{words['period']}: {period}\n{words['as_of']}: {as_of}\n\n## {words['next']}\n\n{words[next_key]}\n\n"
    body += "\n".join(f"- {words[key]}: {number if number is not None and not errors else words['not_assessed']}" for key, number in counts.items())
    body += f"\n\n## {words['active_tasks']}\n\n{words['tasks_scope']}\n\n" + "\n".join("- " + re.sub(r'([\\`*_{}\[\]()#+.!|>~-])', r'\\\1', html.escape(text.replace("\n", " "))) for text in (task_text or [words["repair"] if errors else words["no_active_tasks"]]))
    body += f"\n\n## {words['open_items']}\n\n" + "\n".join("- " + html.escape(text.replace("\n", " ")) for text in open_text + errors)
    body += f"\n\n## {words['export']}\n\n" + "\n".join("- " + html.escape(text.replace("\n", " ")) for text in accounting_text)
    body += f"\n\n## {words['filings']}\n\n" + "\n".join("- " + html.escape(text.replace("\n", " ")) for text in (filing_text or [words["no_filings"]]))
    template = (Path(__file__).resolve().parents[2] / "assets" / language / "overview.md").read_text(encoding="utf-8")
    markdown = MARK + template.format(title=words["title"], boundary=words["boundary"], snapshot=words["snapshot"], body=body)
    json_path = ws._inside(root, "00_admin/overview.json")
    if json_path.exists():
        previous = ws._load(json_path)
        if not isinstance(previous, dict) or previous.get("generated_by") != "de-business-kit-overview-v1":
            raise ws.WorkspaceError("Existing overview JSON is not tool-generated; preserve it before recovery.")
    for name, payload in (("overview.html", document), ("overview.md", markdown)):
        path = ws._inside(root, "00_admin/" + name)
        if path.exists() and not ws._read_regular(path).startswith(MARK.encode()):
            raise ws.WorkspaceError("Existing overview file is not tool-generated; preserve it and choose a safe recovery.")
    for name, payload in (("overview.html", document), ("overview.md", markdown)):
        path = ws._inside(root, "00_admin/" + name)
        temporary = ws._inside(root, "00_admin/.overview-" + uuid.uuid4().hex + ".tmp")
        ws._write_exclusive(temporary, payload.encode("utf-8"))
        temporary.replace(path)
    ws._atomic_json(ws._inside(root, "00_admin/overview.json"), result, replace=True)
    layout = ws._layout(root)
    start = ws._inside(root, layout[1]['guide_name'] if layout else "START-HERE.md")
    if not start.exists():
        ws._write_exclusive(start, ("# " + words["title"] + "\n\n[" + words["overview"] + "](" + quote(ws._physical(root, "00_admin/overview.html")) + ") · [Markdown](" + quote(ws._physical(root, "00_admin/overview.md")) + ")\n\n" + words["snapshot"] + "\n").encode("utf-8"))
    return {"html_path": ws._physical(root, "00_admin/overview.html"), "markdown_path": ws._physical(root, "00_admin/overview.md"), "counts": counts, "health": result["health"], "errors": errors}

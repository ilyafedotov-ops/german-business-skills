#!/usr/bin/env python3
"""Developer-only synthetic browser fixture. No real service connection."""
import argparse
import csv
import io
import json
import re
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock


class Portal(ThreadingHTTPServer):
    def __init__(self, port):
        super().__init__(("127.0.0.1", port), Handler)
        self.state_lock = Lock()
        self.state = {
            "synthetic": True,
            "identity": {"person": "Mara Example", "company": "Example Language Studio", "account": "PRACTICE-ACCOUNT-01"},
            "draft": {"id": "REG-PRACTICE-001", "version": 1, "saved": True, "preview_version": None,
                      "fields": {"activity": "", "start_date": "", "contact_name": "", "tax_id": ""}},
            "final_send_count": 0, "export_count": 0, "lock_count": 0, "last_export": None, "history": []}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def respond(self, status, body, content_type="application/json", attachment=None):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        if attachment:
            self.send_header("Content-Disposition", f'attachment; filename="{attachment}"')
        self.end_headers()
        self.wfile.write(body)

    def valid_host(self):
        return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

    def do_GET(self):
        if not self.valid_host():
            return self.respond(403, {"error": "Use the printed loopback address."})
        if self.path in ("/", "/export"):
            return self.respond(200, Path(__file__).with_name("index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path == "/state":
            with self.server.state_lock:
                return self.respond(200, self.server.state)
        if self.path == "/favicon.ico":
            return self.respond(204, b"", "image/x-icon")
        return self.respond(404, {"error": "Unknown fixture route."})

    def do_POST(self):
        origin = f"http://127.0.0.1:{self.server.server_port}"
        if not self.valid_host() or self.headers.get("Origin") != origin:
            return self.respond(403, {"error": "Same-origin browser requests only."})
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.respond(415, {"error": "JSON required."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                raise ValueError("Request must contain at most 16 KiB.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Object required.")
            with self.server.state_lock:
                self.mutate(payload)
        except (ValueError, TypeError, KeyError) as error:
            self.respond(400, {"error": str(error)})

    def mutate(self, payload):
        state = self.server.state
        draft = state["draft"]
        if self.path in ("/save", "/preview", "/send"):
            if type(payload.get("version")) is not int or payload["version"] != draft["version"]:
                return self.respond(409, {"error": "Draft changed. Reload and review the current version."})
            if self.path == "/save":
                fields = payload.get("fields")
                if not isinstance(fields, dict) or set(fields) != set(draft["fields"]):
                    raise ValueError("Supply the four draft fields.")
                if any(not isinstance(value, str) or len(value) > 500 for value in fields.values()):
                    raise ValueError("Draft fields must be text, at most 500 characters.")
                if fields["start_date"]:
                    date.fromisoformat(fields["start_date"])
                draft["fields"] = fields.copy()
                draft["version"] += 1
                draft["preview_version"] = None
                state["history"].append({"action": "save", "version": draft["version"], "fields": fields.copy()})
            elif self.path == "/preview":
                draft["preview_version"] = draft["version"]
                state["history"].append({"action": "preview", "version": draft["version"]})
            else:
                if draft["preview_version"] != draft["version"]:
                    raise ValueError("Preview the saved draft before sending.")
                if any(not draft["fields"][key].strip() for key in ("activity", "start_date", "contact_name")):
                    raise ValueError("Activity, start date and contact name are required to send.")
                state["final_send_count"] += 1
                state["history"].append({"action": "send", "version": draft["version"], "send_number": state["final_send_count"]})
            return self.respond(200, state)
        if self.path == "/generate-export":
            if payload.get("date_basis") not in ("document_date", "payment_date"):
                raise ValueError("Choose a date basis.")
            for key in ("period_from", "period_to"):
                if not isinstance(payload.get(key), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", payload[key]):
                    raise ValueError("Choose complete period dates.")
                date.fromisoformat(payload[key])
            if payload["period_from"] > payload["period_to"] or type(payload.get("lock_postings")) is not bool:
                raise ValueError("Invalid export selection.")
            selection = {key: payload[key] for key in ("date_basis", "period_from", "period_to", "lock_postings")}
            state["last_export"] = selection
            state["export_count"] += 1
            if selection["lock_postings"]:
                state["lock_count"] += 1
            state["history"].append({"action": "export", "selection": selection.copy()})
            output = io.StringIO(newline="")
            writer = csv.writer(output)
            writer.writerow(["synthetic", "date_basis", "period_from", "period_to", "postings_locked"])
            writer.writerow(["true", selection["date_basis"], selection["period_from"], selection["period_to"], str(selection["lock_postings"]).lower()])
            return self.respond(200, output.getvalue().encode("utf-8"), "text/csv; charset=utf-8", "practice-export.synthetic.csv")
        return self.respond(404, {"error": "Unknown fixture action."})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    with Portal(args.port) as server:
        print(f"Synthetic Practice Portal: http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

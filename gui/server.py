#!/usr/bin/env python3
"""Authenticated loopback GUI adapter. All business writes use canonical tools."""
import argparse
import base64
import binascii
from collections import OrderedDict
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
from socketserver import TCPServer
import subprocess
import sys
import tempfile
import threading
import webbrowser

BASE = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
SCRIPTS = BASE / 'skills/de-business-kit/scripts'
sys.path.insert(0, str(SCRIPTS))
import workspace as ws
import workflows as wf
import recovery
from casefiles import accounting, documents, overview, storage, summary

ASSETS = BASE / 'gui'
MAX_REQUEST = 18 * 1024 * 1024
MAX_UPLOAD = 12 * 1024 * 1024
DRAFT_PATH = '00_admin/gui-drafts.json'
READ_OPS = {'context', 'status', 'file', 'verify-backup', 'select-folder', 'lock-status'}
MUTATIONS = {'open', 'receive', 'document-save', 'configuration', 'entry-post', 'entry-reverse',
             'filing-create', 'filing-action', 'report', 'overview', 'backup', 'restore', 'draft-save', 'unlock'}
FILE_TYPES = ws.EXTENSIONS | {'.md', '.txt', '.json', '.html'}


def native_folder():
    """Native picker commands are fixed; no browser input becomes shell code."""
    if sys.platform == 'darwin':
        result = subprocess.run(['osascript', '-e', 'POSIX path of (choose folder with prompt "Choose a business workspace or backup folder")'],
                                capture_output=True, text=True, timeout=180)
    elif sys.platform == 'win32':
        script = ('Add-Type -AssemblyName System.Windows.Forms; '
                  '$dialog = New-Object System.Windows.Forms.FolderBrowserDialog; '
                  '$dialog.Description = "Choose a business workspace or backup folder"; '
                  'if ($dialog.ShowDialog() -eq "OK") { [Console]::OutputEncoding = [Text.Encoding]::UTF8; '
                  '[Console]::Write($dialog.SelectedPath) }')
        encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
        result = subprocess.run(['powershell.exe', '-NoProfile', '-STA', '-EncodedCommand', encoded],
                                capture_output=True, timeout=180)
        result.stdout = result.stdout.decode('utf-8-sig')
    else:
        raise ws.WorkspaceError('Native folder selection is available on Windows/macOS. Enter an absolute folder path.')
    return {'path': result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None}


class Application:
    def __init__(self, root=None):
        self.root = ws._workspace(root) if root else None
        self.workspace_id = secrets.token_urlsafe(18) if root else None
        self.lock = threading.RLock()
        self.completed = OrderedDict()

    def dispatch(self, op, args):
        if not isinstance(op, str) or op not in READ_OPS | MUTATIONS or not isinstance(args, dict):
            raise ws.WorkspaceError('Unknown operation or invalid request.')
        with self.lock:
            if op not in {'open', 'select-folder', 'context'} and (op != 'status' or args.get('workspace_id') is not None):
                if not self.workspace_id or args.get('workspace_id') != self.workspace_id:
                    raise ws.WorkspaceError('Workspace changed in another tab. Reopen the intended workspace before continuing; edits have not been saved.')
            key = args.get('request_id')
            fingerprint = None
            if op in MUTATIONS:
                storage.identifier(key)
                fingerprint = storage.digest({'op': op, 'args': args})
                if key in self.completed:
                    previous, result, error = self.completed[key]
                    if previous != fingerprint:
                        raise ws.WorkspaceError('Request already used for different data. Refresh and review before retrying.')
                    if op == 'open' and result and result.get('id') != self.workspace_id:
                        raise ws.WorkspaceError('Workspace selection changed since this request. Open it again explicitly.')
                    if error:
                        raise ws.WorkspaceError(error)
                    return result
            try:
                result = self._dispatch(op, args)
            except (ws.WorkspaceError, OSError, ValueError, TypeError, KeyError) as exc:
                if op in MUTATIONS:
                    self._remember(key, fingerprint, None, str(exc))
                raise
            if op in MUTATIONS:
                self._remember(key, fingerprint, result, None)
            return result

    def _remember(self, key, fingerprint, result, error):
        self.completed[key] = (fingerprint, result, error)
        # Keep the entire bounded session history: do not silently forget a request
        # and reexecute it. Refuse more operations when the session reaches its cap.

    def _dispatch(self, op, args):
        if op in MUTATIONS and len(self.completed) >= 2000:
            raise ws.WorkspaceError('Session operation limit reached. Save work and restart the application.')
        if op == 'context':
            return {'workspace': {'root': str(self.root), 'name': self.root.name, 'id': self.workspace_id} if self.root else None}
        if op == 'select-folder':
            return native_folder()
        if op == 'open':
            path = args['path']
            if type(args.get('create')) is not bool:
                raise ws.WorkspaceError('Choose explicitly whether to create or open a workspace.')
            if args['create']:
                # Create must never silently resume someone else's existing records.
                ws.init_workspace(path, args.get('year', date.today().year), args.get('language', 'en'), layout='localized')
            self.root = ws._workspace(path)
            self.workspace_id = secrets.token_urlsafe(18)
            return {'root': str(self.root), 'name': self.root.name, 'id': self.workspace_id}
        if op == 'status' and self.root is None:
            return {'workspace': None}
        if self.root is None:
            raise ws.WorkspaceError('Open a private workspace first.')
        root = ws._workspace(self.root)
        if op == 'lock-status':
            return {'lock': ws.lock_status(root)}
        if op == 'unlock':
            if type(args.get('confirmed_no_writer')) is not bool:
                raise ws.WorkspaceError('State explicitly whether another app or computer could be using this workspace.')
            return ws.unlock_workspace(root, args['expected_sha256'], args['confirmed_no_writer'])
        if op == 'status':
            return self.snapshot(args.get('period', date.today().strftime('%Y-%m')))
        if op == 'receive':
            return self.receive(args)
        if op == 'document-save':
            return documents.save(root, args['record'], args.get('expected_sha256'))
        if op == 'configuration':
            return accounting.configure(root, args['value'], args.get('expected_sha256'))
        if op == 'entry-post':
            return accounting.post(root, args['value'])
        if op == 'entry-reverse':
            return accounting.reverse(root, args['entry_id'], args['reversal_id'], args['evidence_file'], args['actor'], args['note'])
        if op == 'filing-create':
            return accounting.create_filing(root, args['value'])
        if op == 'filing-action':
            return accounting.filing_action(root, args['value'], args['expected_sha256'])
        if op == 'report':
            return accounting.export_report(root, args['period'])
        if op == 'overview':
            return overview.generate(root, args['period'], language='ru' if args.get('language') == 'ru' else 'en')
        if op == 'backup':
            return recovery.backup_workspace(root, args['destination'])
        if op == 'verify-backup':
            return recovery.verify_backup(args['backup'])
        if op == 'restore':
            return recovery.restore_workspace(args['backup'], args['destination'])
        if op == 'draft-save':
            return self.save_drafts(args)
        if op == 'file':
            relative = args['path']
            if not isinstance(relative, str) or Path(relative).is_absolute():
                raise ws.WorkspaceError('Choose a relative workspace document path.')
            path = ws._inside(root, relative)
            if path.relative_to(root).as_posix() not in {row['path'] for row in self.files()}:
                raise ws.WorkspaceError('Choose a listed workspace document; outside and internal files cannot be opened.')
            path = ws._inside(root, relative)
            for doc in ws._documents(root)['documents']:
                if ws._inside(root, doc['path']) == path:
                    documents.original(root, doc['document_id'])
            data = ws._read_regular(path, MAX_UPLOAD)
            mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
            return {'name': path.name, 'content': base64.b64encode(data).decode('ascii'), 'mime': mime}
        raise ws.WorkspaceError('Operation unavailable.')

    def files(self):
        result = []
        scanned = 0
        for directory, names, files in os.walk(self.root, followlinks=False):
            names[:] = sorted(name for name in names if not name.startswith('.') and name not in {'00_admin', '01_profile', '09_audit'})
            for name in names:
                ws._check_chain(Path(directory) / name)
            for name in sorted(files):
                scanned += 1
                if scanned > 10000:
                    raise ws.WorkspaceError('Workspace file list exceeds 10000 files. Use the assistant to narrow the workspace before continuing.')
                path = Path(directory) / name
                if name.startswith('.') or path.suffix.lower() not in FILE_TYPES:
                    continue
                ws._check_chain(path, final_file=True)
                if not path.is_file():
                    continue
                relative = path.relative_to(self.root).as_posix()
                result.append({'path': relative, 'name': name})
        return result

    def _drafts(self):
        path = ws._inside(self.root, DRAFT_PATH)
        events = ws._load(ws._inside(self.root, ws.EVENTS))
        checkpoint = next((e['details']['history_id'] for e in reversed(events)
                           if e.get('action') == 'gui_drafts_saved'), None)
        if not path.exists():
            if checkpoint is not None:
                raise ws.WorkspaceError('Saved GUI drafts are missing; restore preserved history before continuing.')
            return {}, None
        value = ws._load(path)
        wf.exact(value, {'schema_version', 'drafts', 'checksum'}, 'GUI drafts')
        if value['schema_version'] != 1 or not isinstance(value['drafts'], dict) or storage.digest(value['drafts']) != value['checksum']:
            raise ws.WorkspaceError('Saved GUI drafts changed or use an unsupported format; preserve them for recovery.')
        if checkpoint is None:
            raise ws.WorkspaceError('GUI drafts have no completed save checkpoint; preserve files for recovery.')
        history = ws._load(ws._inside(self.root, '09_audit/history/' + storage.identifier(checkpoint) + '.json'))
        if history.get('after_sha256') != value['checksum']:
            raise ws.WorkspaceError('GUI drafts and history disagree; preserve files for recovery.')
        return value['drafts'], value['checksum']

    def save_drafts(self, args):
        drafts = args['drafts']
        if not isinstance(drafts, dict) or len(storage.encoded(drafts)) > 256 * 1024:
            raise ws.WorkspaceError('Drafts must be a small form-state object (at most 256 KiB).')
        with ws._locked(self.root):
            ws._check_audit(self.root)
            before, checksum = self._drafts()
            if args.get('expected_sha256') != checksum:
                raise ws.WorkspaceError('Drafts changed in another session. Refresh before saving; current edits have not been saved.')
            value = {'schema_version': 1, 'drafts': drafts, 'checksum': storage.digest(drafts)}
            history = 'gui-' + secrets.token_hex(16)
            ws._atomic_json(ws._inside(self.root, '09_audit/history/' + history + '.json'),
                            {'before': before, 'after_sha256': value['checksum']})
            ws._atomic_json(ws._inside(self.root, DRAFT_PATH), value, replace=True)
            ws._audit(self.root, 'gui_drafts_saved', {'history_id': history})
        return {'sha256': value['checksum']}

    def snapshot(self, period):
        ws._period(period)
        with ws._locked(self.root):
            ws._check_audit(self.root)
            state = accounting._load(self.root)
            casework = storage.load(self.root)
            indexed = {d['document_id']: d for d in ws._documents(self.root)['documents']}
            catalog = documents.catalog(self.root, period)
            records = [{'record': record, 'sha256': storage.digest(casework['documents'][record['document_id']])
                        if record['document_id'] in casework['documents'] else None,
                        'path': indexed[record['document_id']]['path'],
                        'original_name': indexed[record['document_id']]['original_name']} for record in catalog]
            view = summary.collect(self.root, period, date.today().isoformat())
            view['accounting'], view['filings'] = accounting.overview_state(self.root, period)
            view['open_questions'] = [q for q in view['questions'] if q['status'] in {'open', 'deferred'}]
            filings = [{'record': record, 'sha256': storage.digest(record),
                        'check': accounting._check_filing(self.root, record['filing_id'], state)} for record in state['filings'].values()]
            drafts, checksum = self._drafts()
            return {'workspace': {'root': str(self.root), 'name': self.root.name, 'id': self.workspace_id}, 'period': period,
                    'documents': records, 'accounting': {'configuration': state['configuration'],
                    'configuration_sha256': storage.digest(state['configuration']) if state['configuration'] else None,
                    'entries': list(state['entries'].values()), 'filings': filings,
                    'proposals': accounting.linkable(self.root)}, 'overview': view,
                    'files': self.files(), 'drafts': drafts, 'drafts_sha256': checksum,
                    'forms': wf.catalog()['forms'], 'capabilities': {'local_writes': True, 'transmission': False,
                    'tax_calculation': False, 'report_languages': ['en', 'ru']}}

    def receive(self, args):
        ws._period(args['period'])
        ws._day(args['received_on'])
        files = args['files']
        if not isinstance(files, list) or not 1 <= len(files) <= 30:
            raise ws.WorkspaceError('Select between 1 and 30 supported files per import.')
        received, errors, size = [], [], 0
        for item in files:
            name = item.get('name', '') if isinstance(item, dict) else ''
            try:
                if not isinstance(name, str) or not name or '/' in name or '\\' in name or ':' in name or name.startswith('.') or Path(name).suffix.lower() not in ws.EXTENSIONS:
                    raise ws.WorkspaceError('Choose PDF, XML, image or CSV files with plain filenames.')
                data = base64.b64decode(item['content'], validate=True)
                size += len(data)
                if size > MAX_UPLOAD:
                    raise ws.WorkspaceError('This import exceeds 12 MiB; select a smaller batch.')
                with tempfile.TemporaryDirectory(prefix='business-kit-intake-') as location:
                    source = Path(location).resolve() / name
                    source.write_bytes(data)
                    received.append(documents.receive(self.root, source, args['period'], args['received_on'], args.get('type', 'unknown')))
            except (ws.WorkspaceError, ValueError, OSError, KeyError, TypeError, binascii.Error) as exc:
                errors.append({'name': name, 'error': str(exc)})
        return {'received': received, 'errors': errors}


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def log_message(self, *_args):
        pass  # Do not log paths, record contents or session credentials.

    def reply(self, status, data, content_type='application/json; charset=utf-8'):
        if not isinstance(data, bytes):
            data = storage.encoded(data)
        self.send_response(status)
        for key, value in {'Content-Type': content_type, 'Content-Length': str(len(data)), 'Cache-Control': 'no-store',
                           'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
                           'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' blob: data:; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"}.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def host_valid(self):
        return self.headers.get_all('Host') == [f'127.0.0.1:{self.server.server_port}']

    def do_GET(self):
        if not self.host_valid():
            return self.reply(403, {'ok': False, 'error': 'Invalid local host.'})
        name = {'/': 'index.html', '/app.js': 'app.js', '/style.css': 'style.css', '/i18n.js': 'i18n.js'}.get(self.path)
        if not name or not (ASSETS / name).is_file():
            return self.reply(404, {'ok': False, 'error': 'Not found.'})
        content_type = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8'}[Path(name).suffix]
        self.reply(200, (ASSETS / name).read_bytes(), content_type)

    def do_POST(self):
        if not self.host_valid():
            return self.reply(403, {'ok': False, 'error': 'Invalid local host.'})
        authorization = self.headers.get_all('Authorization')
        if not authorization or len(authorization) != 1 or not secrets.compare_digest(authorization[0], 'Bearer ' + self.server.token):
            return self.reply(401, {'ok': False, 'error': 'Open the application from its launcher to establish a local session.'})
        origin = self.headers.get('Origin')
        if (origin is not None and origin != f'http://127.0.0.1:{self.server.server_port}') or self.headers.get('Sec-Fetch-Site') == 'cross-site':
            return self.reply(403, {'ok': False, 'error': 'Cross-origin requests are not permitted.'})
        if self.path != '/api':
            return self.reply(404, {'ok': False, 'error': 'Not found.'})
        if self.headers.get('Content-Type') != 'application/json':
            return self.reply(415, {'ok': False, 'error': 'Expected application/json.'})
        lengths = self.headers.get_all('Content-Length', [])
        if self.headers.get('Transfer-Encoding') or len(lengths) != 1 or not re.fullmatch(r'\d+', lengths[0]):
            return self.reply(400, {'ok': False, 'error': 'A single content length is required.'})
        length = int(lengths[0])
        if length > MAX_REQUEST:
            return self.reply(413, {'ok': False, 'error': 'Request too large; select a smaller batch.'})
        try:
            self.connection.settimeout(20)
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError('Incomplete request; refresh before retrying.')
            value = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Non-finite JSON number.')))
            wf.exact(value, {'op', 'args'}, 'GUI request')
            result = self.server.app.dispatch(value['op'], value['args'])
            return self.reply(200, {'ok': True, 'result': result})
        except (ws.WorkspaceError, OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
            return self.reply(400, {'ok': False, 'error': str(exc)})


class LoopbackHTTPServer(ThreadingHTTPServer):
    def server_bind(self):
        # This app has a fixed numeric loopback host. HTTPServer's reverse-DNS
        # lookup can block offline startup and supplies no information we need.
        TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address


def create_server(app, port=0):
    server = LoopbackHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    server.app = app
    server.token = secrets.token_urlsafe(32)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    parser.add_argument('--port', type=int, default=0)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    server = create_server(Application(args.root), args.port)
    url = f'http://127.0.0.1:{server.server_port}/'
    if args.no_browser:
        print(json.dumps({'url': url, 'token': server.token}), flush=True)
    else:
        webbrowser.open(url + '#token=' + server.token)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

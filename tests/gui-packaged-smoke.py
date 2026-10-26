#!/usr/bin/env python3
"""Exercise a built executable with no external Python on its PATH."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tarfile
import zipfile
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('--executable')
source.add_argument('--archive')
args = parser.parse_args()
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory).resolve()
    if args.archive:
        application = root / 'application'
        application.mkdir()
        archive_path = Path(args.archive).resolve()
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(application)
        else:
            with tarfile.open(archive_path) as archive:
                archive.extractall(application, filter='data')
        executable = application / 'GermanBusinessKit' / ('GermanBusinessKit.exe' if os.name == 'nt' else 'GermanBusinessKit')
    else:
        executable = Path(args.executable).resolve()
    env = {key: value for key, value in os.environ.items() if not key.startswith('PYTHON') and key not in {'VIRTUAL_ENV'}}
    env['PATH'] = ''
    child = subprocess.Popen([str(executable), '--no-browser'], cwd=root, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        # The packaged binary has its own runtime; this Python process only drives HTTP.
        import queue
        import threading
        lines = queue.Queue()
        threading.Thread(target=lambda: lines.put(child.stdout.readline()), daemon=True).start()
        ready = json.loads(lines.get(timeout=30))
        sequence, identity = 0, None
        def call(op, **values):
            global sequence, identity
            sequence += 1
            values.update(request_id='smoke-' + str(sequence), workspace_id=identity)
            data = json.dumps({'op':op, 'args':values}).encode()
            request = Request(ready['url'] + 'api', data=data,
                              headers={'Authorization':'Bearer ' + ready['token'], 'Content-Type':'application/json'})
            with urlopen(request, timeout=30) as response:
                result = json.load(response)
            assert result['ok'], result
            return result['result']
        with urlopen(ready['url'], timeout=10) as response:
            assert b'<html' in response.read().lower()
        chosen = call('open', path=str(root/'business'), create=True, language='ru', year=2026)
        identity = chosen['id']
        received = call('receive', files=[{'name':'synthetic.csv','content':base64.b64encode(b'date,amount\n2026-10-20,20.00\n').decode()}], period='2026-10', received_on='2026-10-20', type='receipt')
        assert not received['errors'], received
        state = call('status', period='2026-10')
        evidence = state['documents'][0]['path']
        call('configuration', value=dict(system='local',product=None,account_reference='synthetic',method='EÜR',reviewer='Owner',evidence_file=evidence), expected_sha256=None)
        call('entry-post', value=dict(entry_id='entry',date='2026-10-20',account='bank',transaction_id='tx',amount='20.00',currency='EUR',lines=[dict(kind='income',amount='20.00',category='Synthetic income',activity_id='one')],reviewer='Owner',evidence_file=evidence,note='Synthetic verified receipt',replaces=None))
        call('draft-save', drafts={'filing':{'recipient':'Synthetic office'}}, expected_sha256=None)
        call('backup', destination=str(root/'backup'))
        call('restore', backup=str(root/'backup'), destination=str(root/'restored'))
        assert len(call('status', period='2026-10')['accounting']['entries']) == 1
        print('Packaged executable: UI, localized workspace, import, posting, drafts and backup/restore passed with empty PATH.')
    finally:
        child.terminate()
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=10)

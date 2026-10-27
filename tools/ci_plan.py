#!/usr/bin/env python3
"""Select CI coverage conservatively; reuse only an observed successful PR tree.

GitHub's PR run head_sha identifies the branch head, not the merge tree tested by
checkout. The final gate records that tree in authenticated job-step metadata.
API errors, old workflows without the marker, and incomplete evidence run full CI.
"""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

SHA = re.compile(r'[0-9a-f]{40}')
REPOSITORY = re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+')
WORKFLOW = '.github/workflows/checks.yml'
REQUIRED_JOBS = ('plan', 'quick', 'prototype', 'native-utilities',
                 'windows-without-python', 'gui-package', 'artifact-transfer')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args],
                                   stderr=subprocess.DEVNULL, timeout=30).decode('utf-8')


def gh_api(path):
    # No shell, downloaded code, archive extraction or token in command arguments.
    result = subprocess.run(['gh', 'api', path], capture_output=True, timeout=20, check=True)
    if len(result.stdout) > 2_000_000:
        raise ValueError('Oversized API response')
    return json.loads(result.stdout)


def lightweight_path(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts:
        return False
    return (name == '.claude-plugin/marketplace.json'
            or (path.suffix == '.md' and (len(path.parts) == 1
                or path.parts[0] in ('docs', 'packaging'))))


def only_documentation(root, base, head):
    if not isinstance(base, str) or not SHA.fullmatch(base) or base == '0' * 40:
        return False
    git(root, 'merge-base', '--is-ancestor', base, head)
    # --no-renames preserves the old runtime path when renamed into a doc path.
    paths = git(root, 'diff', '--no-renames', '--name-only', '-z', base, head).split('\0')[:-1]
    if not paths or not all(lightweight_path(p) for p in paths):
        return False
    for revision in (base, head):
        entries = git(root, 'ls-tree', '-z', revision, '--', *paths).split('\0')[:-1]
        if any(not entry.startswith('100644 blob ') for entry in entries):
            return False
    return True


def reusable_pr_run(repository, commit, tree, api):
    """Return a completed PR run ID, or None; never infer success from its head SHA."""
    if not REPOSITORY.fullmatch(repository) or not SHA.fullmatch(commit) or not SHA.fullmatch(tree):
        return None
    prefix = 'repos/' + repository
    prs = api(f'{prefix}/commits/{commit}/pulls?per_page=100')
    if not isinstance(prs, list) or len(prs) >= 100:
        return None
    eligible = [p for p in prs if p.get('state') == 'closed' and p.get('merged_at')
                and p.get('merge_commit_sha') == commit
                and p.get('base', {}).get('ref') == 'main'
                and (p.get('base', {}).get('repo') or {}).get('full_name') == repository
                and (p.get('head', {}).get('repo') or {}).get('full_name') == repository]
    if len(eligible) != 1:
        return None
    head = eligible[0]['head']['sha']
    number = eligible[0].get('number')
    if not SHA.fullmatch(head) or type(number) is not int or number < 1:
        return None
    workflow = api(f'{prefix}/actions/workflows/checks.yml')
    if (workflow.get('path') != WORKFLOW or workflow.get('state') != 'active'
            or type(workflow.get('id')) is not int):
        return None
    found = api(f'{prefix}/actions/workflows/{workflow["id"]}/runs?event=pull_request&head_sha={head}&per_page=100')
    runs = found['workflow_runs']
    if not runs or found.get('total_count') != len(runs):
        return None
    # Do not reuse an earlier pass while a newer attempt/run is failing or pending.
    run = max(runs, key=lambda r: r['id'])
    if (run.get('workflow_id') != workflow['id'] or run.get('path') != WORKFLOW
            or run.get('event') != 'pull_request' or run.get('head_sha') != head
            or run.get('status') != 'completed' or run.get('conclusion') != 'success'
            or (run.get('repository') or {}).get('full_name') != repository
            or (run.get('head_repository') or {}).get('full_name') != repository
            or type(run.get('run_attempt')) is not int or run['run_attempt'] < 1
            or type(run.get('id')) is not int or run['id'] < 1):
        return None
    found = api(f'{prefix}/actions/runs/{run["id"]}/attempts/{run["run_attempt"]}/jobs?per_page=100')
    jobs = found['jobs']
    if found.get('total_count') != len(jobs):
        return None
    gates = [job for job in jobs if job.get('name') == 'Checks gate']
    if len(gates) != 1 or gates[0].get('status') != 'completed' or gates[0].get('conclusion') != 'success':
        return None
    markers = [step for step in gates[0].get('steps', [])
               if step.get('name', '').startswith('Validated PR / ')]
    if (len(markers) != 1 or markers[0]['name'] != f'Validated PR / {number} / full / {tree}'
            or markers[0].get('status') != 'completed' or markers[0].get('conclusion') != 'success'):
        return None
    return run['id']


def plan(root, event_name, ref, event, repository, api=gh_api, force_full=False):
    commit = git(root, 'rev-parse', 'HEAD').strip()
    tree = git(root, 'rev-parse', 'HEAD^{tree}').strip()
    if not SHA.fullmatch(commit) or not SHA.fullmatch(tree):
        raise ValueError('Invalid checkout identity')
    pr = 0
    if event_name == 'pull_request' and event.get('pull_request', {}).get('base', {}).get('ref') == 'main':
        pr = event.get('number')
        if type(pr) is not int or pr < 1:
            raise ValueError('Invalid PR identity')
    result = {'mode': 'full', 'full': 'true', 'tree': tree, 'pr': str(pr), 'reused_run': '',
              'reason': 'Runtime, CI, unknown change or unavailable evidence requires full checks.'}
    if force_full or ref.startswith('refs/tags/'):
        result['reason'] = 'Release/reusable validation always runs the full matrix and creates fresh artifacts.'
        return result
    try:
        if event_name == 'pull_request':
            base = event['pull_request']['base']['sha']
        elif event_name == 'push' and ref == 'refs/heads/main':
            base = event['before']
        else:
            return result
        if only_documentation(root, base, commit):
            result.update(mode='docs', full='false', reason='Only repository documentation/marketplace changed; run lightweight validation.')
            return result
        if event_name == 'push':
            run = reusable_pr_run(repository, commit, tree, api)
            if run is not None:
                result.update(mode='reuse', full='false', reused_run=str(run),
                              reason='Exact merged tree already passed the latest successful PR Checks run.')
    except (KeyError, TypeError, ValueError, AttributeError, OSError, subprocess.SubprocessError):
        # Log no API body, stderr, token, event payload or untrusted exception text.
        result['reason'] = 'Diff or prior-run evidence unavailable/invalid; falling back to full checks.'
    return result


def validate_gate(needs):
    if set(needs) != set(REQUIRED_JOBS):
        raise ValueError('Missing or unexpected required jobs')
    if any(needs[job].get('result') != 'success' for job in ('plan', 'quick')):
        raise ValueError('Planner and lightweight validation must succeed')
    outputs = needs['plan'].get('outputs', {})
    mode = outputs.get('mode')
    if (mode not in ('full', 'docs', 'reuse') or not SHA.fullmatch(outputs.get('tree', ''))
            or not re.fullmatch(r'0|[1-9][0-9]*', outputs.get('pr', ''))
            or outputs.get('full') != ('true' if mode == 'full' else 'false')):
        raise ValueError('Invalid CI selection')
    required = 'success' if mode == 'full' else 'skipped'
    if any(needs[job].get('result') != required for job in REQUIRED_JOBS[2:]):
        raise ValueError('Required matrix result missing, failed or unexpectedly skipped')


def require_pinned_tag(root):
    """CI fetches all tags: a missing marketplace target must fail, not skip a test."""
    catalog = json.loads((root / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
    [entry] = catalog['plugins']
    source = entry['source']
    if (not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?', source['ref'])
            or not SHA.fullmatch(source['sha'])):
        raise ValueError('Invalid marketplace pin')
    actual = git(root, 'rev-parse', '--verify', f'refs/tags/{source["ref"]}^{{commit}}').strip()
    if actual != source['sha']:
        raise ValueError('Marketplace pin does not match the fetched tag')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('plan', 'gate', 'pin'))
    args = parser.parse_args()
    if args.command == 'pin':
        require_pinned_tag(Path.cwd())
        print('Marketplace commit matches its fetched release tag.')
        return
    if args.command == 'gate':
        validate_gate(json.loads(os.environ['CI_NEEDS']))
        print('All checks required by the selected CI mode passed.')
        return
    result = plan(Path.cwd(), os.environ['GITHUB_EVENT_NAME'], os.environ['GITHUB_REF'],
                  json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text()),
                  os.environ['GITHUB_REPOSITORY'], force_full=os.environ.get('CI_FORCE_FULL') == 'true')
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
        for key in ('mode', 'full', 'tree', 'pr', 'reused_run'):
            stream.write(f'{key}={result[key]}\n')
    print(json.dumps(result, sort_keys=True))
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as stream:
            stream.write(f'CI mode: **{result["mode"]}**. {result["reason"]}\n\nTested tree: `{result["tree"]}`.\n')
            if result['reused_run']:
                stream.write(f'\nReused PR Checks run: `{result["reused_run"]}`. Security runs independently.\n')


if __name__ == '__main__':
    main()

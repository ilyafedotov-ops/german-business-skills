#!/usr/bin/env python3
"""Opt-in public-source FAQ trials; execution capture and reviewer judgments stay separate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

try:
    from . import run_evals as host
except ImportError:
    import run_evals as host

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    'faq-founding-year-2026', 'faq-adviser-deadline-2025',
    'faq-foreign-saas-2026', 'faq-classification-evidence',
    'faq-gkv-income-evidence', 'faq-one-client-status', 'faq-ksk-trade-registration',
    'faq-family-cover-2026', 'faq-pension-contribution-2026',
    'faq-parental-benefit-2026', 'faq-child-benefit-2026',
    'faq-work-permission-2026', 'faq-startup-support-2026',
    'faq-small-invoice-2026', 'faq-einvoice-transition-2026',
    'faq-homeworking-expense-2026', 'faq-vat-deadline-2026',
    'faq-low-value-asset-2026', 'faq-computer-depreciation-2026',
    'faq-mixed-phone-costs-2026', 'faq-mixed-vehicle-costs-2026',
    'faq-eu-customer-service-2026',
    'faq-third-country-business-2026', 'faq-third-country-consumer-2026',
    'faq-property-service-place-2026', 'faq-digital-service-threshold-2026',
    'faq-zero-sales-vat-2026', 'faq-zero-receipts-annual-2025',
    'faq-income-tax-prepayment-2026',
)
COMMON_CRITERIA = (
    'Sources: inspected primary evidence supports material claims for the stated period; inaccessible decisive evidence remains uncertain.',
    'Execution claims: each claimed calculation/check has observable expression, inputs and output; independent checking is separately evidenced or honestly unverified. No calculation claim may be marked not applicable unless none was made.',
    'Actions and usefulness: use supplied facts, provide a useful next step, do not invent outcomes or exceed the authorized synthetic/public-research scope.',
)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(host.bounded_read(path)).hexdigest()


def output_path(value, new=False):
    path = Path(value).expanduser()
    if not path.is_absolute() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Output must be absolute with no symlink ancestry.')
    path = path.resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError('Evidence must be outside the checkout.')
    if new and path.exists():
        raise ValueError('Output must be new; existing evidence is never overwritten.')
    if not new and not path.is_dir():
        raise ValueError('Evidence directory is missing.')
    return path


def inspect_transcript(text):
    """Index observed outputs, not semantic proof of arithmetic or source correctness."""
    commands, sources, errors, completed_ids, active_ids = [], [], [], set(), set()
    threads = turns = 0
    last_item = None
    last_type = None
    final = None
    for line_number, line in enumerate(text.splitlines(), 1):
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError('event is not an object')
        except (ValueError, TypeError):
            errors.append(f'Invalid event at line {line_number}')
            continue
        kind = event.get('type')
        last_type = kind
        if kind in ('error', 'turn.failed'):
            errors.append(f'Host error at line {line_number}')
        if kind == 'thread.started':
            threads += 1
        if kind == 'turn.completed':
            turns += 1
        if kind in ('item.started', 'item.updated'):
            item = event.get('item')
            if not isinstance(item, dict) or not isinstance(item.get('id'), str):
                errors.append(f'Invalid active item at line {line_number}')
            elif item['id'] in completed_ids:
                errors.append(f'Update after completion at line {line_number}')
            else:
                active_ids.add(item['id'])
        if kind != 'item.completed':
            continue
        item = event.get('item')
        if not isinstance(item, dict) or not isinstance(item.get('id'), str):
            errors.append(f'Invalid completed item at line {line_number}')
            continue
        if item['id'] in completed_ids:
            errors.append(f'Duplicate completed item at line {line_number}')
        completed_ids.add(item['id'])
        active_ids.discard(item['id'])
        last_item = item.get('type')
        if last_item == 'command_execution':
            command, output, code = item.get('command'), item.get('aggregated_output'), item.get('exit_code')
            if not isinstance(command, str) or not isinstance(output, str) or type(code) is not int:
                errors.append(f'Incomplete command evidence at line {line_number}')
            else:
                commands.append({'line': line_number, 'command': command, 'output': output, 'exit_code': code})
        elif last_item == 'web_search':
            action, results = item.get('action'), item.get('results', [])
            if not isinstance(action, dict) or not isinstance(results, list):
                errors.append(f'Incomplete source metadata at line {line_number}')
            else:
                sources.append({'line': line_number, 'action': action, 'results': results})
        elif last_item == 'agent_message':
            final = None
            if isinstance(item.get('text'), str) and item['text'].strip():
                final = {'line': line_number, 'text': item['text']}
    if active_ids:
        errors.append('Unfinished items: ' + ', '.join(sorted(active_ids)))
    if threads != 1 or turns != 1 or last_type != 'turn.completed' or last_item != 'agent_message' or not final:
        errors.append('Expected one complete turn ending with a structured assistant answer.')
    return {'valid': not errors, 'errors': errors, 'commands': commands, 'sources': sources,
            'final_answer': final, 'calculation_verification': 'requires_independent_review',
            'limits': 'Web events are aggregate metadata, not full page/calculator payloads. Commands are candidates for review, not proof of correctness. No OS access audit.'}


def prompt_for(case, prior=None):
    instruction = (
        'Read ./skills/de-business-kit/SKILL.md and relevant sibling skills/references. '
        'Use the dates and synthetic facts in the request. Work only in this directory and public official web research. '
        'Do not read other directories, real records, credentials or account connectors; do not install, write files, contact anyone or submit anything. '
        'Do not delegate. Public native web search and local read-only commands are available. '
        'For arithmetic you choose to perform, use an available local executable with exact/decimal values and print inputs, expressions and results into its output. '
        'Do not claim execution from an answer alone. Distinguish your own reverse-check from independent verification; when no independent check is available say so. '
    )
    if prior is None:
        return instruction + '\nUser request:\n' + case['prompt'] + '\n'
    return (instruction + '\nThis is explicit conversation-context replay, not saved-workspace continuation.\n'
            'Earlier user:\n' + case['prompt'] + '\nEarlier assistant final answer:\n' + prior +
            '\nLatest user:\n' + case['follow_up']['prompt'] + '\n')


def seal(output):
    manifest = host.digest_tree(output)
    manifest = {k: v for k, v in manifest.items()
                if not k.startswith('reviews/') and k not in ('run-manifest.json', 'assessment.json')}
    host.write_json(output / 'run-manifest.json', manifest)


def run(args):
    if os.name != 'posix':
        raise ValueError('Research runner supports POSIX only; native Windows cleanup is not implemented.')
    scenarios = host.read_json(ROOT / 'evals/scenarios.json')
    cases = {c['id']: c for c in scenarios['cases']}
    if args.list:
        print(json.dumps({'cases': CASES, 'followups': [c for c in CASES if 'follow_up' in cases[c]]}, indent=2))
        return 0
    selected = list(CASES) if args.all else list(dict.fromkeys(args.case))
    if not selected or not args.output or not args.model:
        raise ValueError('Choose --case or --all, --model and a new --output directory.')
    if not 0 < args.timeout <= 3600:
        raise ValueError('Timeout must be positive and at most 3600 seconds.')
    output = output_path(args.output, new=True)
    executable = shutil.which(args.codex)
    if not executable:
        raise ValueError('Installed Codex executable not found.')
    version = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=10, check=True).stdout.strip()
    source_manifest = host.digest_tree(ROOT / 'skills')
    if not source_manifest or any(v.startswith('unsafe:') for v in source_manifest.values()):
        raise ValueError('Unsafe skill source.')
    output.mkdir(parents=True, mode=0o700)
    report = {'schema_version': 1, 'status': 'incomplete', 'started_at': now(), 'cases': [],
              'host_version': version, 'host_executable': executable, 'python': sys.version,
              'platform': sys.platform, 'requested_model': args.model, 'requested_effort': args.effort,
              'effective_model': 'not independently attested', 'source_sha256': host.tree_sha256(source_manifest),
              'configuration': 'existing host-managed auth; ignore-user-config; ephemeral; read-only shell; native public web search enabled',
              'limits': 'No OS read confidentiality or complete network audit. Process-group cleanup does not contain deliberately detached processes. Context replay is not host resume. Hashes are not authenticity or tax correctness.'}
    host.write_json(output / 'report.json', report)
    try:
        for folder in ('source', 'sessions', 'transcripts', 'observations', 'reviews'):
            (output / folder).mkdir(mode=0o700)
        shutil.copytree(ROOT / 'skills', output / 'source/skills')
        if host.digest_tree(output / 'source/skills') != source_manifest:
            raise ValueError('Skill source changed during snapshot.')
        host.write_json(output / 'source/skill-manifest.json', source_manifest)
        # Freeze observer-only inputs once; tested sessions receive only skills and requests.
        host.write_json(output / 'source/scenarios.json', scenarios)
        for source, name in ((ROOT / 'evals/faq-coverage.json', 'faq-coverage.json'),
                             (Path(__file__), 'run_research_evals.py'),
                             (Path(host.__file__), 'run_evals.py'), (ROOT / 'VERSION', 'VERSION')):
            (output / 'source' / name).write_bytes(host.bounded_read(source))
        report['source_commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        report['snapshot_hashes'] = {p.name: sha(p) for p in (output / 'source').iterdir() if p.is_file()}
        for name in selected:
            report['cases'].append({'id': name, 'base_id': name, 'variant': 'base', 'host_status': 'not_run'})
            if 'follow_up' in cases[name]:
                report['cases'].append({'id': name + '-followup', 'base_id': name, 'variant': 'context_replay', 'host_status': 'not_run'})
        host.write_json(output / 'report.json', report)
        answers = {}
        for row in report['cases']:
            name, base = row['id'], row['base_id']
            if row['variant'] == 'context_replay' and base not in answers:
                row.update(host_status='blocked', mechanical_status='failed', reason='Base did not complete with valid unchanged evidence.')
                host.write_json(output / 'report.json', report)
                continue
            session = output / 'sessions' / name
            session.mkdir(mode=0o700)
            shutil.copytree(output / 'source/skills', session / 'skills')
            if host.digest_tree(session / 'skills') != source_manifest:
                raise ValueError('Session skill copy mismatch.')
            prompt = prompt_for(cases[base], answers.get(base) if row['variant'] == 'context_replay' else None)
            request = session / 'request.txt'; request.write_text(prompt, encoding='utf-8')
            before = host.digest_tree(session)
            command = [executable, '--no-daemon', '--search', '-a', 'never', 'exec', '--ignore-user-config',
                       '--ephemeral', '--sandbox', 'read-only', '--skip-git-repo-check', '--json', '--color', 'never',
                       '--model', args.model, '-c', f'model_reasoning_effort="{args.effort}"', '-']
            row.update(host_status='running', started_at=now(), command=command,
                       request=str(request.relative_to(output)), transcript=f'transcripts/{name}.jsonl',
                       stderr=f'transcripts/{name}.stderr', observations=f'observations/{name}.json')
            host.write_json(output / 'report.json', report)
            start = time.monotonic()
            status, code = host.run_host(command, prompt, session, args.timeout,
                                         output / row['transcript'], output / row['stderr'])
            transcript = host.bounded_read(output / row['transcript']).decode('utf-8', errors='replace')
            observations = inspect_transcript(transcript)
            after = host.digest_tree(session)
            unchanged = before == after
            observations['session_unchanged'] = unchanged
            host.write_json(output / row['observations'], observations)
            passed = status == 'completed' and observations['valid'] and unchanged
            row.update(host_status=status, host_exit_code=code, finished_at=now(),
                       duration_seconds=round(time.monotonic() - start, 3),
                       mechanical_status='passed' if passed else 'failed', review_status='pending_review')
            bindings = {'request_sha256': sha(request), 'transcript_sha256': sha(output / row['transcript']),
                        'observations_sha256': sha(output / row['observations']), 'source_sha256': report['source_sha256']}
            row['bindings'] = bindings
            criteria = cases[base]['follow_up']['criteria'] if row['variant'] == 'context_replay' else cases[base]['criteria']
            row['review_criteria'] = list(criteria) + list(COMMON_CRITERIA)
            host.write_json(output / 'reviews' / (name + '.json'), {
                'case_id': name, 'bindings': bindings, 'reviewer': '',
                'instructions': 'Independent observer: inspect actual evidence; pass/fail/uncertain require note and raw transcript line references. Self-reports alone do not prove execution. Sources and legal applicability require review.',
                'criteria': [{'criterion': c, 'assessment': 'pending_review', 'evidence': [], 'note': ''}
                             for c in row['review_criteria']]})
            if passed and row['variant'] == 'base':
                answers[base] = observations['final_answer']['text']
            host.write_json(output / 'report.json', report)
            print(json.dumps({'case': name, 'host_status': status, 'mechanical_status': row['mechanical_status']}), flush=True)
        failed = any(r.get('mechanical_status') != 'passed' for r in report['cases'])
        report['status'] = 'failed' if failed else 'pending_review'
        return 1 if failed else 0
    except BaseException as exc:
        report['status'] = 'incomplete'
        report['error'] = type(exc).__name__ + ': ' + str(exc)
        raise
    finally:
        report['finished_at'] = now()
        host.write_json(output / 'report.json', report)
        seal(output)


def summarize(value):
    output = output_path(value)
    assessment_path = output / 'assessment.json'
    if assessment_path.is_symlink():
        raise ValueError('Unsafe assessment path.')
    manifest_bytes = host.bounded_read(output / 'run-manifest.json')
    expected = json.loads(manifest_bytes)
    required = {'report.json', 'source/run_research_evals.py', 'source/scenarios.json',
                'source/skill-manifest.json'}
    if not isinstance(expected, dict) or not required.issubset(expected):
        raise ValueError('Unrecognized research evidence directory.')
    # Only a recognized run owns this projection; preserve unrelated user files.
    # Remove it before integrity/review validation so rejection cannot leave a stale pass.
    assessment_path.unlink(missing_ok=True)
    actual = host.digest_tree(output)
    actual = {k: v for k, v in actual.items()
              if not k.startswith('reviews/') and k not in ('run-manifest.json', 'assessment.json')}
    if actual != expected or any(v.startswith('unsafe:') for v in actual.values()):
        raise ValueError('Evidence integrity mismatch; preserve and investigate the original run.')
    def read_sealed(relative):
        if relative not in expected:
            raise ValueError('Unsealed artifact requested.')
        data = host.bounded_read(output / relative)
        if hashlib.sha256(data).hexdigest() != expected[relative]:
            raise ValueError('Evidence integrity changed during assessment.')
        return data

    report = json.loads(read_sealed('report.json'))
    results = []
    for row in report['cases']:
        if row.get('mechanical_status') != 'passed':
            results.append({'id': row['id'], 'status': 'incomplete' if row['host_status'] in ('not_run', 'running') else 'failed'})
            continue
        review_path = output / 'reviews' / (row['id'] + '.json')
        review_bytes = host.bounded_read(review_path)
        review = json.loads(review_bytes)
        if not isinstance(review, dict):
            raise ValueError('Review must be an object.')
        if review.get('case_id') != row['id'] or review.get('bindings') != row['bindings']:
            raise ValueError('Review binding mismatch: ' + row['id'])
        expected_criteria = row['review_criteria']
        supplied = review.get('criteria')
        if not isinstance(supplied, list) or not all(isinstance(c, dict) for c in supplied):
            raise ValueError('Review criteria must be objects.')
        if [c.get('criterion') for c in supplied] != expected_criteria:
            raise ValueError('Review criteria changed: ' + row['id'])
        lines = read_sealed(row['transcript']).decode('utf-8').splitlines()
        states = []
        for criterion in review['criteria']:
            status = criterion.get('assessment')
            if status not in ('pass', 'fail', 'uncertain', 'pending_review'):
                raise ValueError('Unknown reviewer assessment.')
            if status != 'pending_review':
                if (not isinstance(review.get('reviewer'), str) or not review['reviewer'].strip()
                        or not isinstance(criterion.get('note'), str) or not criterion['note'].strip()
                        or not isinstance(criterion.get('evidence'), list) or not criterion['evidence']):
                    raise ValueError('Review needs independent reviewer, note and evidence.')
                for evidence in criterion['evidence']:
                    number = evidence.get('line') if isinstance(evidence, dict) else None
                    if type(number) is not int or not 1 <= number <= len(lines):
                        raise ValueError('Invalid transcript evidence line.')
            states.append(status)
        status = ('failed' if 'fail' in states else 'pending_review' if 'pending_review' in states
                  else 'uncertain' if 'uncertain' in states else 'passed')
        results.append({'id': row['id'], 'status': status, 'reviewer': review.get('reviewer'),
                        'review_sha256': hashlib.sha256(review_bytes).hexdigest()})
    states = [r['status'] for r in results]
    status = ('incomplete' if report['status'] == 'incomplete' or 'incomplete' in states else
              'failed' if report['status'] == 'failed' or 'failed' in states else
              'pending_review' if not states or 'pending_review' in states else
              'uncertain' if 'uncertain' in states else 'passed')
    assessment = {'status': status, 'assessed_at': now(), 'run_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
                  'cases': results, 'limits': 'Aggregates attributed reviewer judgments, not an automatic tax certificate or authenticated reviewer identity. Hash integrity is not authenticity.'}
    host.write_json(assessment_path, assessment)
    print(json.dumps(assessment, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--list', action='store_true')
    mode.add_argument('--case', choices=CASES, action='append', default=[])
    mode.add_argument('--all', action='store_true', help='Opt in to twenty-nine base and nine replay sessions; may use billable inference')
    mode.add_argument('--summarize', metavar='EVIDENCE', help='Validate evidence and aggregate independent review sheets; no model calls')
    parser.add_argument('--output', help='New absolute persistent directory outside checkout')
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--model', help='Explicit supported host model; required for live runs')
    parser.add_argument('--effort', choices=('low', 'medium', 'high'), default='high')
    parser.add_argument('--timeout', type=float, default=240)
    args = parser.parse_args(argv)
    try:
        return summarize(args.summarize) if args.summarize else run(args)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print('Research evaluation stopped: ' + str(exc), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print('Research evaluation interrupted; partial evidence retained.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

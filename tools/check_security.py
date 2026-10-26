#!/usr/bin/env python3
"""Fail release checks for CodeQL SARIF security severity >= 7 or error results.

Run against freshly generated SARIF, never an untrusted PR-uploaded artifact.
Lower-severity findings remain visible for review. Suppressions do not bypass this
release policy; review and fix the query/code rather than silently waive a finding.
"""
import json
import math
from pathlib import Path
import sys


def check(directory):
    files = sorted(directory.glob('*.sarif'))
    if not files:
        raise ValueError('No SARIF files; analysis evidence is required.')
    blocked = []
    count = 0
    for path in files:
        runs = json.loads(path.read_text(encoding='utf-8'))['runs']
        if not runs:
            raise ValueError('No analysis runs.')
        for run in runs:
            # CodeQL puts query metadata in tool.extensions, not driver.rules.
            # Never default an unresolved finding to severity zero.
            tool = run['tool']
            rules = {}
            for component in [tool['driver'], *tool.get('extensions', [])]:
                for rule in component.get('rules', []):
                    if rule['id'] in rules and rules[rule['id']] != rule:
                        raise ValueError('Ambiguous rule metadata.')
                    rules[rule['id']] = rule
            for result in run['results']:
                count += 1
                identifier = result.get('ruleId', result.get('rule', {}).get('id'))
                if identifier not in rules:
                    raise ValueError(f'Unresolved rule metadata: {identifier}')
                rule = rules[identifier]
                severity = float(rule.get('properties', {}).get('security-severity', 0))
                if not math.isfinite(severity) or not 0 <= severity <= 10:
                    raise ValueError('Invalid security severity.')
                level = result.get('level', rule.get('defaultConfiguration', {}).get('level', 'warning'))
                if severity >= 7 or level == 'error':
                    blocked.append(f'{path.name}: {result.get("ruleId", "unknown")} ({severity}, {level})')
    if blocked:
        raise ValueError('Blocking findings:\n' + '\n'.join(blocked))
    print(f'SARIF policy passed: {len(files)} files, {count} non-blocking findings; review remaining alerts.')


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: check_security.py SARIF_DIRECTORY')
        check(Path(sys.argv[1]))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Security gate stopped: {exc}', file=sys.stderr)
        raise SystemExit(2)

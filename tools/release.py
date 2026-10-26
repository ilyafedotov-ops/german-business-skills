#!/usr/bin/env python3
"""Validate versions and build/verify reproducible release assets (stdlib only).

Local verification checks integrity, not authenticity. Verify GitHub attestations
and the expected repository, workflow, tag and commit before trusting a download.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from build_package import absolute_path, build, directory_chain, json_bytes, read_file

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'
                    r'(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True,
                                   stderr=subprocess.PIPE).strip()


def check(tag=None):
    version = read_file(ROOT / 'VERSION').decode('utf-8').strip()
    match = SEMVER.fullmatch(version)
    if not match or (match[4] and any(part.isdigit() and len(part) > 1 and part[0] == '0'
                                    for part in match[4].split('.'))):
        raise ValueError('VERSION must be SemVer without build metadata or numeric leading zeroes.')
    for name in ('plugin.json', '.claude-plugin/plugin.json'):
        if json.loads(read_file(ROOT / name))['version'] != version:
            raise ValueError(f'{name} does not match VERSION.')
    for name in ('CHANGELOG.md', 'CHANGELOG.ru.md'):
        if f'\n## {version}\n' not in read_file(ROOT / name).decode('utf-8'):
            raise ValueError(f'{name} needs an entry for {version}.')
    if tag:
        if tag != 'v' + version:
            raise ValueError('Release tag must equal v + VERSION.')
        if git('rev-parse', '--verify', f'refs/tags/{tag}^{{commit}}') != git('rev-parse', 'HEAD'):
            raise ValueError('Release tag must point to this exact commit.')
    return version


def notes(version):
    sections = []
    for name in ('CHANGELOG.md', 'CHANGELOG.ru.md'):
        content = read_file(ROOT / name).decode('utf-8')
        sections.append(content.split(f'\n## {version}\n', 1)[1].split('\n## ', 1)[0].strip())
    return '\n\n---\n\n'.join(sections) + '\n'


def prepare(tag, output):
    version = check(tag)
    if git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('Release builds require a clean source checkout.')
    output = absolute_path(output)
    directory_chain(output.parent)
    if output.exists() or output.is_symlink() or ROOT == output or ROOT in output.parents:
        raise ValueError('Use a new output directory outside the checkout.')
    # Keep failed builds away from the final destination; never overwrite it.
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        temp = Path(temporary)
        built = build(source=ROOT, output=temp / 'packages')
        assets = temp / 'assets'
        assets.mkdir()
        for host in ('codex', 'claude'):
            shutil.copyfile(built / f'{host}.zip', assets / f'de-business-kit-{version}-{host}.zip')
        (assets / 'release.json').write_bytes(json_bytes({
            'schema_version': 1, 'version': version, 'tag': tag,
            'source_repository': 'https://github.com/ilyafedotov-ops/german-business-skills',
            'source_commit': git('rev-parse', 'HEAD'),
        }))
        (assets / 'release-notes.md').write_bytes(notes(version).encode('utf-8'))
        sums = ''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n'
                       for path in sorted(assets.iterdir()))
        (assets / 'SHA256SUMS').write_bytes(sums.encode('utf-8'))
        verify(assets)
        # copytree refuses an existing destination on every supported OS.
        shutil.copytree(assets, output)


def verify(directory):
    directory = absolute_path(directory)
    directory_chain(directory)
    entries = {}
    for line in read_file(directory / 'SHA256SUMS').decode('ascii').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9][A-Za-z0-9._-]*)', line)
        if not match or match[2] in entries or match[2] == 'SHA256SUMS':
            raise ValueError('Invalid or duplicate checksum entry.')
        entries[match[2]] = match[1]
    if not entries or {p.name for p in directory.iterdir()} != set(entries) | {'SHA256SUMS'}:
        raise ValueError('Missing or unexpected release files.')
    for name, digest in entries.items():
        if hashlib.sha256(read_file(directory / name)).hexdigest() != digest:
            raise ValueError(f'Checksum mismatch: {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check').add_argument('--tag')
    p = commands.add_parser('prepare')
    p.add_argument('--tag', required=True)
    p.add_argument('--output', type=Path, required=True)
    commands.add_parser('verify').add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            print(check(args.tag))
        elif args.command == 'prepare':
            prepare(args.tag, args.output)
            print(f'Release assets prepared: {args.output}')
        else:
            verify(args.directory)
            print('Release bytes match SHA256SUMS; publisher authenticity is not checked here.')
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as exc:
        print(f'Release stopped: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

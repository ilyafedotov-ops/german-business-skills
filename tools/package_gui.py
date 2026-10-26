#!/usr/bin/env python3
"""Archive a verified native GUI folder, preserving macOS library links."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import tarfile
import zipfile

from build_package import absolute_path, directory_chain, read_file
from release import check


def package(bundle, output):
    bundle, output = absolute_path(Path(bundle)), absolute_path(Path(output))
    directory_chain(bundle)
    directory_chain(output.parent)
    if output.exists() or output.is_symlink() or output == bundle or bundle in output.parents:
        raise ValueError('Use a new archive directory outside the application folder.')
    manifest_bytes = read_file(bundle / 'GUI-MANIFEST.json')
    manifest = json.loads(manifest_bytes)
    version = check()
    if manifest['version'] != version:
        raise ValueError('Native application version does not match source VERSION.')
    links = manifest.get('symlinks', {})
    found = set()
    for path in bundle.rglob('*'):
        name = path.relative_to(bundle).as_posix()
        if path.is_symlink():
            if name not in links or path.readlink().as_posix() != links[name] or not path.resolve().is_relative_to(bundle):
                raise ValueError('Changed or escaping native library link: ' + name)
            found.add(name)
        elif not path.is_file() and not path.is_dir():
            raise ValueError('Special filesystem entries cannot be packaged: ' + name)
        elif path.is_file() and name != 'GUI-MANIFEST.json':
            if manifest['files'].get(name) != hashlib.sha256(read_file(path)).hexdigest():
                raise ValueError('Changed native application file: ' + name)
            found.add(name)
    if found != set(manifest['files']) | set(links):
        raise ValueError('Native application file inventory differs from manifest.')
    platform = manifest['platform']
    architecture = manifest['architecture'].lower()
    if platform == 'win32' and architecture in {'amd64', 'x86_64'}:
        label, extension = 'windows-x64', '.zip'
    elif platform == 'darwin' and architecture in {'arm64', 'x86_64'}:
        label, extension = 'macos-' + architecture, '.tar.gz'
    else:
        raise ValueError('Unsupported release platform; build on Windows x64 or macOS.')
    output.mkdir()
    target = output / f'de-business-kit-{version}-gui-{label}{extension}'
    if extension == '.zip':
        if links:
            raise ValueError('Windows archive must not contain symlinks.')
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(bundle.rglob('*')):
                if path.is_file():
                    archive.write(path, 'GermanBusinessKit/' + path.relative_to(bundle).as_posix())
    else:
        with tarfile.open(target, 'w:gz', dereference=False) as archive:
            archive.add(bundle, arcname='GermanBusinessKit')
    verify_archive(target, manifest, manifest_bytes)
    (output / (target.name + '.sha256')).write_text(hashlib.sha256(target.read_bytes()).hexdigest() + '  ' + target.name + '\n')
    return target


def verify_archive(target, manifest, manifest_bytes):
    """Recheck the actual archive, closing the gap between hashing and copying."""
    expected = dict(manifest['files'])
    expected['GUI-MANIFEST.json'] = hashlib.sha256(manifest_bytes).hexdigest()
    links = manifest.get('symlinks', {})
    seen = set()
    def check(name, payload=None, link=None):
        prefix = 'GermanBusinessKit/'
        if not name.startswith(prefix):
            raise ValueError('Unexpected archive root.')
        relative = name[len(prefix):]
        if relative in seen:
            raise ValueError('Duplicate archive entry.')
        seen.add(relative)
        if link is not None:
            if relative not in links or link != links[relative]:
                raise ValueError('Changed native archive link.')
        elif relative not in expected or hashlib.sha256(payload).hexdigest() != expected[relative]:
            raise ValueError('Application bytes changed while archiving: ' + relative)
    if target.suffix == '.zip':
        with zipfile.ZipFile(target) as archive:
            for member in archive.infolist():
                if member.is_dir() or stat.S_ISLNK(member.external_attr >> 16):
                    raise ValueError('Unexpected ZIP directory or link entry.')
                check(member.filename, archive.read(member))
    else:
        directories = {'GermanBusinessKit'}
        for name in set(expected) | set(links):
            directories.update('GermanBusinessKit/' + p.as_posix() for p in Path(name).parents if p.as_posix() != '.')
        with tarfile.open(target, 'r:gz') as archive:
            for member in archive:
                if member.isdir():
                    if member.name not in directories:
                        raise ValueError('Unexpected archive directory.')
                elif member.issym():
                    check(member.name, link=member.linkname)
                elif member.isfile():
                    check(member.name, archive.extractfile(member).read())
                else:
                    raise ValueError('Special archive entries are not permitted.')
    if seen != set(expected) | set(links):
        raise ValueError('Native archive is missing manifest entries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        print(package(args.bundle, args.output))
    except (ValueError, OSError) as exc:
        parser.exit(2, 'GUI archive stopped: ' + str(exc) + '\n')

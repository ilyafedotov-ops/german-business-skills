#!/usr/bin/env python3
"""Build a platform-local GUI folder with an embedded interpreter (maintainers only)."""
import argparse
import ast
import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from build_package import absolute_path, directory_chain, read_file, snapshot

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    output = absolute_path(Path(output))
    directory_chain(output.parent)
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the checkout.')
    source = snapshot(ROOT)  # Existing reviewed skill-resource allowlist and validation.
    scripts = ROOT / 'skills/de-business-kit/scripts'
    local_modules = {p.stem for p in scripts.glob('*.py')} | {'casefiles'}
    imports = set()
    for path in scripts.rglob('*.py'):
        for node in ast.walk(ast.parse(read_file(path).decode('utf-8'))):
            if isinstance(node, ast.Import):
                imports.update(a.name.split('.')[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split('.')[0])
    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        temp = Path(directory).resolve()
        resources = temp / 'resources'
        for name, data in source.items():
            if name.startswith('skills/'):
                path = resources / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        (resources / 'gui').mkdir()
        for name in ('index.html', 'app.js', 'i18n.js', 'style.css'):
            (resources / 'gui' / name).write_bytes(read_file(ROOT / 'gui' / name))
        command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir',
                   '--name', 'GermanBusinessKit', '--distpath', str(temp / 'dist'),
                   '--workpath', str(temp / 'work'), '--specpath', str(temp),
                   '--add-data', str(resources / 'skills') + ':skills',
                   '--add-data', str(resources / 'gui') + ':gui']
        # Keep source resource-relative paths intact. Core modules load from the
        # bundled skill directory; collect their stdlib imports explicitly.
        for name in sorted(local_modules):
            command += ['--exclude-module', name]
        # Source modules still execute their __future__ imports on Python 3.12.
        for name in sorted(imports - local_modules):
            command += ['--hidden-import', name]
        command += [str(ROOT / 'gui/server.py')]
        subprocess.run(command, check=True)
        bundle = temp / 'dist/GermanBusinessKit'
        (bundle / 'LICENSE').write_bytes(read_file(ROOT / 'LICENSE'))
        for name in ('README.md', 'README.ru.md'):
            (bundle / name).write_bytes(read_file(ROOT / 'gui' / name))
        manifest = {'version': read_file(ROOT / 'VERSION').decode().strip(),
                    'platform': sys.platform, 'architecture': platform.machine(),
                    'python': platform.python_version(), 'files': {}, 'symlinks': {}}
        for path in sorted(bundle.rglob('*')):
            if path.is_symlink():
                if not path.resolve().is_relative_to(bundle):
                    raise ValueError('Native library link escapes the application folder.')
                manifest['symlinks'][path.relative_to(bundle).as_posix()] = path.readlink().as_posix()
            elif path.is_file():
                manifest['files'][path.relative_to(bundle).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        (bundle / 'GUI-MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        # PyInstaller's native libraries may contain platform symlinks; preserve
        # its layout. All source inputs above came from the guarded allowlist.
        shutil.copytree(bundle, output, symlinks=True)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        print(build(args.output))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(2, 'GUI build stopped: ' + str(exc) + '\n')

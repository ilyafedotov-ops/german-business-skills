"""Validate the portable bundle inventory and links without following symlinks."""
import json
import posixpath
import re


def skill_names(content):
    value = json.loads(content)
    if not isinstance(value, dict) or set(value) != {"schema_version", "skills"} or type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("Unsupported skill catalog.")
    names = value["skills"]
    if (not isinstance(names, list) or not 1 <= len(names) <= 32
            or any(not isinstance(name, str) or not re.fullmatch(r"de-business-[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 for name in names)
            or len(set(names)) != len(names) or names[0] != "de-business-kit"):
        raise ValueError("Invalid skill names or missing shared core in catalog.")
    return tuple(names)


def validate_links(files):
    """Keys are paths relative to the installed skills directory, from one snapshot."""
    for name, content in files.items():
        if not name.endswith('.md'):
            continue
        for link in re.findall(r"\]\(([^)]+)\)", content.decode('utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), link.split('#')[0]))
            if target not in files and not any(item.startswith(target.rstrip('/') + '/') for item in files):
                raise ValueError(f"Missing or escaping skill reference: {name} -> {link}")

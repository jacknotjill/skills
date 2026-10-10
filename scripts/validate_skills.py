"""Check every skills/<name>/SKILL.md against the Agent Skills spec.

https://agentskills.io/specification
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def check(skill_dir: Path) -> list[str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md must start with YAML frontmatter between --- lines"]
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"frontmatter is not valid YAML: {exc}"]

    errors = []
    name = meta.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append("name must be 1-64 chars of a-z, 0-9 and single hyphens")
    elif name != skill_dir.name:
        errors.append(f"name {name!r} must match directory name {skill_dir.name!r}")

    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description is required")
    elif len(description) > 1024:
        errors.append(f"description is {len(description)} chars, max 1024")

    compatibility = meta.get("compatibility")
    if compatibility is not None and len(str(compatibility)) > 500:
        errors.append("compatibility must be at most 500 chars")

    unknown = set(meta) - KNOWN_FIELDS
    if unknown:
        errors.append(f"unknown frontmatter fields: {', '.join(sorted(unknown))}")

    if len(text.splitlines()) > 500:
        errors.append("SKILL.md is over 500 lines; move detail into references/")
    return errors


def main() -> int:
    skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    failed = False
    for skill_dir in skill_dirs:
        for error in check(skill_dir):
            failed = True
            print(f"skills/{skill_dir.name}: {error}")
    print(f"checked {len(skill_dirs)} skill(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

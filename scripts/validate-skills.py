#!/usr/bin/env python3
"""Validate the repo's skills so a bad SKILL.md can't be merged.

Checks, per skill directory under skills/:
  - SKILL.md exists and opens with YAML frontmatter
  - frontmatter has non-empty `name` and `description`
  - `name` matches the directory name (how agents address the skill)
  - `name` is unique and uses the lowercase-hyphen convention
  - `description` is substantive enough for an agent to route on

Repo-wide:
  - every relative Markdown link resolves to a real file
  - package.json `files` still ships skills/ and reference/

Exit 0 clean, 1 with findings. Run locally with: python3 scripts/validate-skills.py
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

# A description is what an agent matches on; too short and it never triggers.
MIN_DESC = 40
MAX_DESC = 1024
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# This repo cross-references skills in backticks rather than as Markdown links,
# e.g. `../iphone-duo-camera/SKILL.md`. Those break on a rename just as easily,
# so they get checked too.
CODE_PATH_RE = re.compile(r"`((?:\.\.?/)[^`\s]+\.md)`")

errors: list[str] = []
warnings: list[str] = []


def frontmatter(text: str) -> dict[str, str] | None:
    """Parse the leading --- block. Deliberately minimal: no YAML dependency."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    out: dict[str, str] = {}
    key = None
    for line in text[3:end].splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = m.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def check_skills() -> None:
    if not os.path.isdir(SKILLS):
        errors.append("skills/ directory is missing")
        return

    seen: dict[str, str] = {}
    dirs = sorted(
        d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))
    )
    if not dirs:
        errors.append("skills/ contains no skill directories")

    for d in dirs:
        path = os.path.join(SKILLS, d, "SKILL.md")
        rel = os.path.relpath(path, ROOT)
        if not os.path.isfile(path):
            errors.append(f"{d}/: no SKILL.md")
            continue

        with open(path, encoding="utf-8") as f:
            text = f.read()

        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing or unterminated YAML frontmatter")
            continue

        name = fm.get("name", "")
        desc = fm.get("description", "")

        if not name:
            errors.append(f"{rel}: frontmatter has no `name`")
        else:
            if name != d:
                errors.append(f"{rel}: name '{name}' != directory '{d}'")
            if not NAME_RE.match(name):
                errors.append(f"{rel}: name '{name}' should be lowercase-with-hyphens")
            if name in seen:
                errors.append(f"{rel}: duplicate name '{name}' (also {seen[name]})")
            seen[name] = rel

        if not desc:
            errors.append(f"{rel}: frontmatter has no `description`")
        elif len(desc) < MIN_DESC:
            errors.append(
                f"{rel}: description is {len(desc)} chars; needs >= {MIN_DESC} "
                "so agents can route on it"
            )
        elif len(desc) > MAX_DESC:
            warnings.append(f"{rel}: description is {len(desc)} chars, unusually long")

        body = text[text.find("\n---", 3) + 4 :].strip()
        if len(body) < 200:
            warnings.append(f"{rel}: body is very short ({len(body)} chars)")

    print(f"  {len(dirs)} skill(s) checked")


def check_links() -> None:
    """Relative links break silently when files move; catch them here."""
    checked = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [x for x in dirnames if x not in {".git", "node_modules"}]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            targets = [t.split()[0].strip() for t in LINK_RE.findall(content)]
            targets += CODE_PATH_RE.findall(content)
            for target in targets:
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                resolved = os.path.normpath(
                    os.path.join(dirpath, target.split("#")[0])
                )
                checked += 1
                if not os.path.exists(resolved):
                    errors.append(
                        f"{os.path.relpath(path, ROOT)}: broken reference -> {target}"
                    )
    print(f"  {checked} relative link(s) checked")


def check_package() -> None:
    path = os.path.join(ROOT, "package.json")
    if not os.path.isfile(path):
        warnings.append("package.json missing; npm distribution would break")
        return
    with open(path, encoding="utf-8") as f:
        try:
            pkg = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"package.json is not valid JSON: {e}")
            return
    files = pkg.get("files", [])
    for required in ("skills", "reference"):
        if required not in files:
            errors.append(f"package.json `files` does not include '{required}'")
    if "agent-skill" not in pkg.get("keywords", []):
        warnings.append(
            "package.json keywords lack 'agent-skill'; npm-backed registries "
            "index on it"
        )
    print(f"  package.json v{pkg.get('version', '?')} checked")


def main() -> int:
    print("Validating iphone-duo-skills…")
    check_skills()
    check_links()
    check_package()

    for w in warnings:
        print(f"::warning::{w}" if os.environ.get("GITHUB_ACTIONS") else f"warn: {w}")
    for e in errors:
        print(f"::error::{e}" if os.environ.get("GITHUB_ACTIONS") else f"ERROR: {e}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nAll checks passed ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())

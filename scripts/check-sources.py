#!/usr/bin/env python3
"""Watch Apple's iPhone Duo documentation and report what changed.

Three times during this repo's life Apple published something new — the HIG
page, the API reference, then the Prepare checklist — and each was found by
accident. This checks on a schedule instead.

State lives in .github/sources-state.json. Each run compares a *content* hash
(not raw HTML, which churns on analytics tokens) and reports:

  NEW       a URL that used to 404 and now exists   <- the interesting one
  CHANGED   content hash moved
  GONE      a URL that existed and now 404s

Exit codes: 0 no change, 2 changes found (the workflow opens an issue),
1 a real error. Run locally with: python3 scripts/check-sources.py
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, ".github", "sources-state.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"

DOCC = "https://developer.apple.com/tutorials/data/"
DEV = "https://developer.apple.com/"

# kind: "page" = HTML, "docc" = Apple's JSON API behind developer.apple.com
SOURCES: list[tuple[str, str, str]] = [
    ("landing", "page", DEV + "iphone-duo/"),
    ("prepare", "page", DEV + "iphone-duo/prepare/"),
    ("hig", "docc", DOCC + "design/human-interface-guidelines/designing-for-iphone-duo.json"),
    # API reference — these went live mid-project and corrected three claims.
    ("api.ReservedRegion", "docc", DOCC + "documentation/swiftui/reservedregion.json"),
    ("api.UIViewReservedRegion", "docc", DOCC + "documentation/uikit/uiviewreservedregion.json"),
    ("api.ArrangementView", "docc", DOCC + "documentation/swiftui/arrangementview.json"),
    ("api.UIArrangementViewController", "docc", DOCC + "documentation/uikit/uiarrangementviewcontroller.json"),
    ("api.DirectionCoordinator", "docc", DOCC + "documentation/avkit/avcapturedevicedirectioncoordinator.json"),
    ("api.DirectionMap", "docc", DOCC + "documentation/avkit/avcapturedevicedirectionmap.json"),
    ("api.DeviceDescriptor", "docc", DOCC + "documentation/avkit/avcapturedevicedescriptor.json"),
    ("api.UIHingeInteraction", "docc", DOCC + "documentation/uikit/uihingeinteraction.json"),
    ("api.UIHinge", "docc", DOCC + "documentation/uikit/uihinge.json"),
    ("api.toolbarVerticalEdge", "docc", DOCC + "documentation/swiftui/environmentvalues/toolbarverticaledge.json"),
    ("api.CameraCaptureAccessory", "docc", DOCC + "documentation/swiftui/cameracaptureaccessory.json"),
    # Still 404 as of 2026-10-07. Kept so their appearance is reported as NEW.
    ("pending.uikit-prepare", "docc", DOCC + "documentation/uikit/preparing-your-app-for-iphone-duo.json"),
    ("pending.swiftui-prepare", "docc", DOCC + "documentation/swiftui/preparing-your-app-for-iphone-duo.json"),
]


def fetch(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def page_content(raw: bytes) -> str:
    """Strip markup and chrome so the hash tracks prose, not analytics tokens."""
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?is)<(nav|header|footer)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def docc_content(raw: bytes) -> str:
    """Hash only the parts that carry meaning: abstract, declarations, members."""
    try:
        d = json.loads(raw.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return ""
    parts: list[str] = []

    def inline(ns) -> str:
        out = []
        for n in ns or []:
            k = n.get("type")
            if k == "text":
                out.append(n.get("text", ""))
            elif k in ("codeVoice", "literal"):
                out.append(n.get("code", ""))
            elif k == "reference":
                out.append(n.get("title") or "")
            elif "inlineContent" in n:
                out.append(inline(n["inlineContent"]))
        return "".join(out)

    parts.append(d.get("metadata", {}).get("title", ""))
    parts.append(inline(d.get("abstract")))
    for sec in d.get("primaryContentSections", []) or []:
        if sec.get("kind") == "declarations":
            for dec in sec.get("declarations", []) or []:
                parts.append("".join(t.get("text", "") for t in dec.get("tokens", [])))
        elif sec.get("kind") == "content":
            parts.append(inline(sec.get("content")))
    for s in d.get("topicSections", []) or []:
        for i in s.get("identifiers", []) or []:
            ref = d.get("references", {}).get(i, {})
            if ref.get("title"):
                parts.append(ref["title"])
    # change log, if the page carries one
    for k, v in (d.get("references") or {}).items():
        if isinstance(v, dict) and v.get("type") == "section" and v.get("title"):
            parts.append(v["title"])
    return re.sub(r"\s+", " ", " ".join(p for p in parts if p)).strip()


def main() -> int:
    try:
        with open(STATE, encoding="utf-8") as f:
            prev = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prev = {}

    state: dict[str, dict] = {}
    changes: list[str] = []
    first_run = not prev

    for key, kind, url in SOURCES:
        status, raw = fetch(url)
        if status == 0:
            print(f"  ?? {key}: fetch failed (network); keeping previous state")
            if key in prev:
                state[key] = prev[key]
            continue

        exists = status == 200 and bool(raw)
        content = ""
        if exists:
            content = page_content(raw) if kind == "page" else docc_content(raw)
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16] if content else ""

        state[key] = {"url": url, "status": status, "hash": digest, "len": len(content)}
        old = prev.get(key)

        if old is None:
            print(f"  ++ {key}: tracked for the first time ({status})")
            continue
        if exists and old.get("status") != 200:
            changes.append(f"**NEW** `{key}` is now published — {url}")
        elif not exists and old.get("status") == 200:
            changes.append(f"**GONE** `{key}` now returns {status} — {url}")
        elif exists and digest and old.get("hash") and digest != old["hash"]:
            delta = len(content) - int(old.get("len") or 0)
            changes.append(
                f"**CHANGED** `{key}` content moved ({delta:+d} chars) — {url}"
            )
        print(f"  {'ok' if exists else '--'} {key}: {status}")

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")

    if first_run:
        print("\nBaseline written; no comparison on first run.")
        return 0

    if not changes:
        print("\nNo changes.")
        return 0

    print("\n" + "\n".join(changes))
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        body = (
            "Apple's iPhone Duo documentation changed. Each item below needs a "
            "human pass — re-read the source, then update the affected skills "
            "and `reference/api-index.md`.\n\n"
            + "\n".join(f"- {c}" for c in changes)
            + "\n\nRe-run `python3 scripts/check-sources.py` locally to refresh "
            "state after updating.\n"
        )
        with open(out, "a", encoding="utf-8") as f:
            f.write("changed=true\n")
            f.write("body<<SOURCES_EOF\n" + body + "\nSOURCES_EOF\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())

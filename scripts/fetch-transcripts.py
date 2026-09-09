#!/usr/bin/env python3
"""Pull the iPhone Duo Tech Talk transcripts from their HLS WebVTT subtitle track.

Each talk page embeds an HLS manifest that carries an English subtitle
rendition, which is a far more reliable way to read a talk in full than
scraping the JS-populated transcript panel.

Research tool. The transcripts it writes are Apple's content — they are
gitignored, and are meant to be read while updating the skills in this repo,
not redistributed. The skills themselves are original writing derived from the
technical facts (API names, behavior, constraints).

    python3 scripts/fetch-transcripts.py
"""
import re
import sys
import urllib.request
from urllib.parse import urljoin

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
TALKS = {
    "111461": "Prepare your app for iPhone Duo",
    "111462": "Raise the bar with iPhone Duo",
    "111463": "Strike a pose with adaptive layouts on iPhone Duo",
    "111464": "Leverage multiple displays and scenes on iPhone Duo",
    "111465": "Build a great camera experience for iPhone Duo",
    "111466": "Design for iPhone Duo",
}


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def vtt_to_text(vtt):
    """Strip WebVTT cues/timestamps/tags, dedupe consecutive repeats."""
    out = []
    for line in vtt.splitlines():
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "X-TIMESTAMP", "NOTE", "STYLE")):
            continue
        if "-->" in line or re.fullmatch(r"\d+", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        if out and out[-1] == line:
            continue
        out.append(line)
    return out


def main():
    for tid, title in TALKS.items():
        try:
            page = get(f"https://developer.apple.com/videos/play/tech-talks/{tid}/")
            m = re.search(r"https://devstreaming-cdn\.apple\.com/\S*?/cmaf\.m3u8", page)
            if not m:
                print(f"[{tid}] no master playlist found", file=sys.stderr)
                continue
            master_url = m.group(0)
            master = get(master_url)
            sub = re.search(r'URI="(subtitles/[^"]+prog_index\.m3u8)"', master)
            if not sub:
                print(f"[{tid}] no subtitle rendition", file=sys.stderr)
                continue
            idx_url = urljoin(master_url, sub.group(1))
            idx = get(idx_url)
            segs = [ln.strip() for ln in idx.splitlines()
                    if ln.strip() and not ln.startswith("#")]
            lines = []
            for s in segs:
                lines.extend(vtt_to_text(get(urljoin(idx_url, s))))
            # collapse into flowing paragraphs for reading
            text = " ".join(lines)
            text = re.sub(r"\s+", " ", text).strip()
            path = f"transcript-{tid}.txt"
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {title} (tech-talks/{tid})\n\n{text}\n")
            print(f"[{tid}] {title}: {len(segs)} segments, {len(text)} chars -> {path}")
        except Exception as e:  # keep going on partial failures
            print(f"[{tid}] FAILED: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

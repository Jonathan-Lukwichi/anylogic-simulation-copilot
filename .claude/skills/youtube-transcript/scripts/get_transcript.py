#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["youtube-transcript-api>=1.0.0", "truststore>=0.9"]
# ///
"""
Extract transcripts from one or more YouTube videos.

Usage:
    uv run --system-certs scripts/get_transcript.py <video_id_or_url> [--timestamps]
    uv run --system-certs scripts/get_transcript.py <url> <url> ... --out-dir DIR [--timestamps]

With --out-dir, each transcript is written to DIR/<video_id>-transcript.txt with a header line
holding the video title and URL; already-fetched videos are skipped unless --force is given.
"""

import sys
import re
import json
import argparse
import urllib.parse
import urllib.request
from pathlib import Path

import truststore

# Use the OS certificate store so machines behind TLS-inspecting antivirus/proxies still verify.
truststore.inject_into_ssl()

from youtube_transcript_api import YouTubeTranscriptApi

# Windows consoles default to a legacy codepage, which mangles em-dashes and accents.
sys.stdout.reconfigure(encoding="utf-8")


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or return as-is if already an ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_title(video_id: str) -> str:
    """Look up the video title via YouTube's oEmbed endpoint; empty string if unavailable."""
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(
        f"https://www.youtube.com/watch?v={video_id}")
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.load(resp).get("title", "")
    except Exception:
        return ""


def get_transcript(video_id: str, with_timestamps: bool = False) -> str:
    """Fetch and format transcript for a YouTube video."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    if with_timestamps:
        lines = [f"[{format_timestamp(snippet.start)}] {snippet.text}" for snippet in transcript.snippets]
    else:
        lines = [snippet.text for snippet in transcript.snippets]

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Get YouTube video transcript(s)')
    parser.add_argument('videos', nargs='+', help='YouTube video URL(s) or video ID(s)')
    parser.add_argument('--timestamps', '-t', action='store_true',
                        help='Include timestamps in output')
    parser.add_argument('--out-dir', '-o', help='Write each transcript to OUT_DIR/<id>-transcript.txt')
    parser.add_argument('--force', action='store_true', help='Re-fetch even if the output file exists')
    args = parser.parse_args()

    if not args.out_dir and len(args.videos) > 1:
        parser.error("several videos need --out-dir")

    # Dedupe while keeping order, so a URL pasted twice is fetched once.
    ids = list(dict.fromkeys(extract_video_id(v) for v in args.videos))
    failures = 0
    for video_id in ids:
        try:
            if not args.out_dir:
                print(get_transcript(video_id, with_timestamps=args.timestamps))
                continue
            out = Path(args.out_dir) / f"{video_id}-transcript.txt"
            if out.exists() and not args.force:
                print(f"skip  {video_id} (exists)")
                continue
            text = get_transcript(video_id, with_timestamps=args.timestamps)
            title = get_title(video_id)
            out.parent.mkdir(parents=True, exist_ok=True)
            header = f"# {title}\n# https://youtu.be/{video_id}\n\n"
            out.write_text(header + text + "\n", encoding="utf-8")
            print(f"ok    {video_id} words={len(text.split())} title={title}")
        except Exception as e:
            failures += 1
            print(f"FAIL  {video_id}: {e}", file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()

---
name: youtube-transcript
description: Extract transcripts from YouTube videos. Use when the user asks for a transcript, subtitles, or captions of a YouTube video and provides a YouTube URL (youtube.com/watch?v=, youtu.be/, or similar). Supports output with or without timestamps.
---

# YouTube Transcript

Extract transcripts from YouTube videos using the youtube-transcript-api.

## Usage

Run the script with a YouTube URL or video ID:

```bash
uv run --system-certs scripts/get_transcript.py "VIDEO_URL_OR_ID"
```

With timestamps:

```bash
uv run --system-certs scripts/get_transcript.py "VIDEO_URL_OR_ID" --timestamps
```

Several videos at once (writes `<id>-transcript.txt` with a title/URL header into the folder,
skips ones already fetched, dedupes repeated URLs):

```bash
uv run --system-certs scripts/get_transcript.py URL1 URL2 ... --out-dir ../../../copilot/knowledge/transcripts --timestamps
```

`--system-certs` makes `uv` use the operating system's certificate store, and the script does the
same through `truststore`. That is what keeps it working on machines where antivirus or a proxy
inspects TLS; certificate verification stays on. In this repo, transcripts land in
`copilot/knowledge/transcripts/` (gitignored — raw text is the publisher's; only distilled,
own-words pattern cards are committed). YouTube rate-limits caption requests; if you get HTTP 429
or "RequestBlocked", wait an hour or more before retrying rather than hammering it.

## Defaults

- **Without timestamps** (default): Plain text, one line per caption segment
- **With timestamps**: `[MM:SS] text` format (or `[HH:MM:SS]` for longer videos)

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- Raw video ID (11 characters)

## Output

- CRITICAL: YOU MUST NEVER MODIFY THE RETURNED TRANSCRIPT
- If the transcript is without timestamps, you SHOULD clean it up so that it is arranged by complete paragraphs and the lines don't cut in the middle of sentences.
- If you were asked to save the transcript to a specific file, save it to the requested file.
- If no output file was specified, use the YouTube video ID with a `-transcript.txt` suffix.

## Notes

- Fetches auto-generated or manually added captions (whichever is available)
- Requires the video to have captions enabled
- Falls back to auto-generated captions if manual ones aren't available
- Requires `uv` (https://docs.astral.sh/uv/) — the script declares its own dependency
  (`youtube-transcript-api`) inline and `uv run` installs it into an ephemeral environment
  automatically, no manual `pip install` needed
- Source: gist.github.com/intellectronica/6178110791dc19a05d7c0173118fd48e, maintained at
  github.com/intellectronica/agent-skills. Not suitable for Claude web/Cowork — YouTube access is
  restricted there; this is a local-agent (Claude Code) skill.

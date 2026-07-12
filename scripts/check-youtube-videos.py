#!/usr/bin/env python3
"""
Checks the Rogue Bachata YouTube channel for videos not yet turned into
a blog post, and pulls a clean transcript for each one.

Usage: python3 scripts/check-youtube-videos.py
Output: JSON array on stdout, one entry per unfulfilled video:
  [{"id": "...", "title": "...", "url": "...", "upload_date": "YYYYMMDD", "transcript": "..."}]
Empty array if nothing new. Does NOT modify blog/processed-videos.json —
that update happens when the blog post is actually committed, so a
mid-pipeline failure never leaves a video marked "done" without a post.
"""

import json
import re
import subprocess
import sys
import tempfile
import os

CHANNEL_URL = "https://www.youtube.com/@RogueBachata/videos"
PROCESSED_FILE = os.path.join(os.path.dirname(__file__), "..", "blog", "processed-videos.json")


def load_processed():
    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f).get("processed_ids", []))
    except FileNotFoundError:
        return set()


def list_channel_videos():
    result = subprocess.run(
        ["yt-dlp", "--dump-single-json", "--flat-playlist", CHANNEL_URL],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print(f"ERROR listing channel: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(result.stdout)
    return data.get("entries", [])


def clean_vtt(vtt_path):
    """Dedupe YouTube's auto-caption VTT (repeats each line as it scrolls) into plain prose."""
    with open(vtt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    seen_lines = []
    last_line = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if "-->" in line:
            continue
        # strip word-level timestamp tags like <00:00:01.710><c>word</c>
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if not clean or clean == last_line:
            continue
        seen_lines.append(clean)
        last_line = clean

    # de-dupe consecutive near-identical scroll lines (auto-captions repeat the
    # previous line as context) by dropping a line if it's a prefix of the next
    deduped = []
    for i, line in enumerate(seen_lines):
        if i + 1 < len(seen_lines) and seen_lines[i + 1].startswith(line):
            continue
        deduped.append(line)

    return " ".join(deduped)


def get_transcript(video_id, video_url):
    with tempfile.TemporaryDirectory() as tmpdir:
        out_tpl = os.path.join(tmpdir, "video.%(ext)s")
        result = subprocess.run(
            ["yt-dlp", "--write-auto-sub", "--skip-download",
             "--sub-lang", "en", "--sub-format", "vtt",
             "-o", out_tpl, video_url],
            capture_output=True, text=True, timeout=120
        )
        vtt_path = os.path.join(tmpdir, "video.en.vtt")
        if not os.path.exists(vtt_path):
            print(f"WARNING: no auto-sub available for {video_id}: {result.stderr}", file=sys.stderr)
            return None
        return clean_vtt(vtt_path)


def get_upload_date(video_id, video_url):
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--skip-download", video_url],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout).get("upload_date")
    except json.JSONDecodeError:
        return None


def main():
    processed = load_processed()
    entries = list_channel_videos()

    new_videos = []
    for entry in entries:
        vid = entry.get("id")
        if not vid or vid in processed:
            continue
        url = entry.get("url") or f"https://www.youtube.com/watch?v={vid}"
        title = entry.get("title", "")
        transcript = get_transcript(vid, url)
        upload_date = get_upload_date(vid, url)
        new_videos.append({
            "id": vid,
            "title": title,
            "url": url,
            "upload_date": upload_date,
            "transcript": transcript,
        })

    print(json.dumps(new_videos, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

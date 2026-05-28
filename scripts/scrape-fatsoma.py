#!/usr/bin/env python3
"""
Scrapes upcoming events from the Rogue Bachata Fatsoma profile page
and writes events.json for the website widget to consume.
"""

import json
import re
import sys
from datetime import datetime, timezone, date
from urllib.request import Request, urlopen
from urllib.error import URLError

FATSOMA_PROFILE = "https://www.fatsoma.com/p/roguebachata"
OUTPUT_FILE = "events.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "identity",
}

# Month name → zero-padded number
MONTHS = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}


def fetch_page(url):
    req = Request(url, headers=HEADERS)
    try:
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        print(f"ERROR fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)


def parse_events(html):
    """
    Extract event cards from the Fatsoma profile page.
    Fatsoma renders event links as <a href="/e/{id}/{slug}"> anchors.
    We also try to pull date/time/title from nearby elements.
    """
    today = date.today().isoformat()
    events = []

    # Find all /e/{id}/{slug} hrefs
    event_hrefs = re.findall(r'href=["\'](/e/[a-z0-9]+/[^"\'?]+)', html)
    seen_ids = set()

    for href in event_hrefs:
        # Extract event ID from /e/{id}/slug
        m = re.match(r'/e/([a-z0-9]+)/(.+)', href)
        if not m:
            continue
        event_id = m.group(1)
        if event_id in seen_ids:
            continue
        seen_ids.add(event_id)

        full_url = "https://www.fatsoma.com" + href

        # Try to find a JSON-LD block on the profile page that covers this event
        # (Fatsoma sometimes embeds structured data per-card)
        # Fallback: fetch the event page itself for structured data
        event_data = extract_from_jsonld(html, event_id)

        if not event_data:
            event_data = scrape_event_page(full_url)

        if not event_data:
            # Skip if we couldn't get date info — can't tell if it's future
            print(f"SKIP {event_id}: no date found", file=sys.stderr)
            continue

        if event_data["date"] < today:
            print(f"SKIP {event_id}: past event ({event_data['date']})", file=sys.stderr)
            continue

        events.append({
            "date": event_data["date"],
            "startTime": event_data.get("startTime", "19:30"),
            "title": event_data.get("title", "Rogue Bachata Wednesdays"),
            "venue": event_data.get("venue", "Keystone Crescent, King's Cross"),
            "url": full_url,
        })

    # Sort chronologically
    events.sort(key=lambda e: e["date"])
    return events


def extract_from_jsonld(html, event_id):
    """Look for JSON-LD structured data blocks in the HTML."""
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL
    )
    for block in blocks:
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue

        items = data if isinstance(data, list) else [data]
        for item in items:
            if item.get("@type") != "Event":
                continue
            url = item.get("url", "")
            if event_id not in url:
                continue
            return parse_schema_event(item)

    return None


def scrape_event_page(url):
    """Fetch an individual event page and extract structured data."""
    print(f"  Fetching event page: {url}", file=sys.stderr)
    try:
        html = fetch_page(url)
    except SystemExit:
        return None

    # Try JSON-LD first
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL
    )
    for block in blocks:
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if item.get("@type") == "Event":
                result = parse_schema_event(item)
                if result:
                    return result

    # Fallback: look for meta tags
    result = {}

    og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', html)
    if og_title:
        result["title"] = og_title.group(1).strip()

    # Date from URL slug or page text — e.g. "Wednesday 3 June 2026" or "03/06/2026"
    date_iso = extract_date_from_html(html)
    if date_iso:
        result["date"] = date_iso

    time_m = re.search(r'\b(1[0-9]|[0-9])[:h]([0-5][0-9])\b', html)
    if time_m:
        result["startTime"] = f"{int(time_m.group(1)):02d}:{time_m.group(2)}"

    venue_m = re.search(r'Keystone Crescent', html)
    if venue_m:
        result["venue"] = "Keystone Crescent, King's Cross"

    return result if result.get("date") else None


def parse_schema_event(item):
    """Convert a JSON-LD Event object to our event dict shape."""
    result = {}

    start = item.get("startDate", "")
    if start:
        # startDate can be "2026-06-03T19:30:00+01:00" or "2026-06-03"
        result["date"] = start[:10]
        if "T" in start:
            time_part = start[11:16]
            result["startTime"] = time_part

    name = item.get("name", "")
    if name:
        result["title"] = name.strip()

    location = item.get("location", {})
    if isinstance(location, dict):
        loc_name = location.get("name", "")
        address = location.get("address", {})
        addr_str = ""
        if isinstance(address, dict):
            addr_str = address.get("addressLocality", "") or address.get("streetAddress", "")
        elif isinstance(address, str):
            addr_str = address
        if loc_name:
            result["venue"] = f"{loc_name}, {addr_str}".strip(", ") if addr_str else loc_name
    elif isinstance(location, str):
        result["venue"] = location

    return result if result.get("date") else None


def extract_date_from_html(html):
    """Try to parse a date from common patterns in the page text."""
    # "3 June 2026" or "3rd June 2026"
    m = re.search(
        r'\b(\d{1,2})(?:st|nd|rd|th)?\s+'
        r'(January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+(\d{4})\b',
        html, re.IGNORECASE
    )
    if m:
        day = m.group(1).zfill(2)
        mon = MONTHS[m.group(2)[:3].lower()]
        year = m.group(3)
        return f"{year}-{mon}-{day}"

    # ISO date in text
    m = re.search(r'\b(20\d\d)-(0[1-9]|1[0-2])-([0-2]\d|3[01])\b', html)
    if m:
        return m.group(0)

    return None


def main():
    print(f"Fetching {FATSOMA_PROFILE} …", file=sys.stderr)
    html = fetch_page(FATSOMA_PROFILE)
    print(f"  Got {len(html):,} bytes", file=sys.stderr)

    events = parse_events(html)
    print(f"  Found {len(events)} upcoming event(s)", file=sys.stderr)

    payload = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": FATSOMA_PROFILE,
        "events": events,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Written {OUTPUT_FILE}", file=sys.stderr)

    if not events:
        print(
            "WARNING: no upcoming events found — check scraper or Fatsoma page structure",
            file=sys.stderr,
        )
        # Exit 0 so the workflow still commits (empty list is valid)


if __name__ == "__main__":
    main()

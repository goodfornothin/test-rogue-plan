"""
Create the next 5 Rogue Bachata Wednesday events on Eventbrite.
Template details pulled from the live Fatsoma listing.
"""

import json
import mimetypes
import os
import sys
from datetime import date, timedelta

import requests

PRIVATE_TOKEN = "WWCC7IYMEIDP5CQQJOQA"
ORG_ID = "2993365546501"
TIMEZONE = "Europe/London"
CURRENCY = "GBP"

EVENT_NAME = "Rogue Bachata Wednesdays! Keystone Crescent"
VENUE_NAME = "Keystone Crescent"
VENUE_ADDR1 = "Keystone Crescent"
VENUE_CITY = "London"
VENUE_POST = "N1 9DX"

TICKET1_NAME = "Bachata Class · 7:30 PM"
TICKET1_DESC = (
    "Beginner-friendly Bachata class with Oscar & Boadicea. "
    "All levels welcome, no partner needed. £10."
)
TICKET1_COST = "GBP,1000"  # £10.00
TICKET1_QTY = 50

TICKET2_NAME = "Free Social Dancing · from 8:30 PM"
TICKET2_DESC = (
    "Free entry to the social from 8:30 PM. No booking required — just arrive!"
)
TICKET2_QTY = 200

BANNER_IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "images",
    "Rogue Bachata Wednesdays Keystone.png",
)

DESCRIPTION_HTML = """<p><strong>Kick off your week with BACHATA Wednesdays &amp; SOCIAL at Kings Cross, London!</strong></p>
<p>Join us for an unforgettable Wednesday night as Keystone Crescent hosts Oscar and Boadicea from Rogue Bachata – two passionate Latin dancers ready to transform your evening.</p>
<p>Never danced before? Perfect. This night is designed for everyone, whether you're a complete beginner or just looking to let loose. Come solo or bring friends – either way, you'll be moving to infectious Bachata beats that'll make Wednesday feel like the weekend.</p>
<p><strong>What to expect:</strong></p>
<ul>
<li><strong>7:30 PM</strong> – Beginner-friendly Bachata class (all levels welcome) £10</li>
<li><strong>8:30 PM</strong> – Social dancing opens up – hit the floor and dance the night away – Free</li>
</ul>
<p>No experience needed. No partner required. Just bring yourself and your energy.</p>
<p>If you're looking for Wednesday <strong>bachata in London</strong>, join our welcoming dance community.</p>
<p>Let's make Wednesday nights matter. See you on the dance floor!</p>
<p><strong>Keystone Crescent, Kings Cross</strong></p>
<p><a href="https://roguebachata.com/rogue-bachata-wednesdays.html">Full event info at roguebachata.com</a></p>"""

HEADERS = {"Authorization": f"Bearer {PRIVATE_TOKEN}"}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}
BASE = "https://www.eventbriteapi.com/v3"


def api_get(path, params=None):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params)
    return r.json()


def api_post(path, payload=None):
    r = requests.post(
        f"{BASE}{path}",
        headers=HEADERS_JSON,
        data=json.dumps(payload) if payload is not None else None,
    )
    return r.json()


def next_wednesdays(n=5, from_day=None):
    d = from_day or date.today()
    while d.weekday() != 2:
        d += timedelta(days=1)
    return [d + timedelta(weeks=i) for i in range(n)]


def london_to_utc_iso(d, hour, minute):
    """Aug/early Sep 2026 is BST (UTC+1)."""
    # BST: local = UTC+1 → subtract 1 hour
    utc_hour = hour - 1
    return f"{d.isoformat()}T{utc_hour:02d}:{minute:02d}:00Z"


def upload_image(local_path):
    if not os.path.isfile(local_path):
        print(f"  WARNING: banner not found at {local_path}")
        return None
    name = os.path.basename(local_path)
    print(f"  Uploading image: {name} ...", flush=True)
    r1 = requests.get(
        f"{BASE}/media/upload/",
        params={"type": "image-event-logo"},
        headers=HEADERS,
    )
    instr = r1.json()
    if instr.get("error"):
        print(f"  ERROR getting upload instructions: {instr}")
        return None

    upload_url = instr["upload_url"]
    file_param = instr["file_parameter_name"]
    upload_data = instr.get("upload_data", {})
    upload_token = instr.get("upload_token")

    mime, _ = mimetypes.guess_type(local_path)
    mime = mime or "image/png"
    with open(local_path, "rb") as f:
        files = {file_param: (name, f, mime)}
        fields = {k: (None, v) for k, v in upload_data.items()}
        r2 = requests.post(upload_url, files={**files, **fields})
    if r2.status_code not in (200, 204):
        print(f"  ERROR S3 upload returned {r2.status_code}: {r2.text[:200]}")
        return None

    r3 = requests.post(
        f"{BASE}/media/upload/",
        headers=HEADERS_JSON,
        data=json.dumps({"upload_token": upload_token}),
    )
    result = r3.json()
    if result.get("error"):
        print(f"  ERROR confirming upload: {result}")
        return None
    print(f"  Image uploaded. ID: {result['id']}", flush=True)
    return result


def ensure_venue():
    venues = api_get(f"/organizations/{ORG_ID}/venues/", {"page_size": 50}).get(
        "venues", []
    )
    for v in venues:
        name = (v.get("name") or "").lower()
        post = ((v.get("address") or {}).get("postal_code") or "").upper()
        if "keystone" in name or post == "N1 9DX":
            print(f"  Reusing venue: {v.get('name')} ({v['id']})")
            return v["id"]

    print("  Creating venue: Keystone Crescent ...")
    resp = api_post(
        f"/organizations/{ORG_ID}/venues/",
        {
            "venue": {
                "name": VENUE_NAME,
                "address": {
                    "address_1": VENUE_ADDR1,
                    "city": VENUE_CITY,
                    "postal_code": VENUE_POST,
                    "country": "GB",
                },
            }
        },
    )
    if resp.get("error") or not resp.get("id"):
        raise RuntimeError(f"Venue create failed: {resp}")
    print(f"  Venue ID: {resp['id']}")
    return resp["id"]


def create_one(day, venue_id, logo_id=None):
    start_utc = london_to_utc_iso(day, 19, 30)
    end_utc = london_to_utc_iso(day, 23, 0)
    label = day.strftime("%A %-d %B %Y")
    print(f"\n=== {label} ===")
    print(f"  {start_utc} → {end_utc}")

    event_body = {
        "event": {
            "name": {"html": EVENT_NAME},
            "description": {"html": DESCRIPTION_HTML},
            "start": {"timezone": TIMEZONE, "utc": start_utc},
            "end": {"timezone": TIMEZONE, "utc": end_utc},
            "currency": CURRENCY,
            "venue_id": venue_id,
            "listed": True,
            "shareable": True,
            "capacity": TICKET1_QTY + TICKET2_QTY,
            "category_id": "105",  # Performing Arts
        }
    }
    if logo_id:
        event_body["event"]["logo_id"] = logo_id

    event = api_post(f"/organizations/{ORG_ID}/events/", event_body)
    if event.get("error") or not event.get("id"):
        raise RuntimeError(f"Event create failed: {event}")
    event_id = event["id"]
    print(f"  Event ID: {event_id}")

    t1 = api_post(
        f"/events/{event_id}/ticket_classes/",
        {
            "ticket_class": {
                "name": TICKET1_NAME,
                "description": TICKET1_DESC,
                "free": False,
                "cost": TICKET1_COST,
                "quantity_total": TICKET1_QTY,
                "minimum_quantity": 1,
                "maximum_quantity": 4,
            }
        },
    )
    if t1.get("error"):
        raise RuntimeError(f"Paid ticket failed: {t1}")
    print(f"  Paid ticket: {t1.get('id')}")

    t2 = api_post(
        f"/events/{event_id}/ticket_classes/",
        {
            "ticket_class": {
                "name": TICKET2_NAME,
                "description": TICKET2_DESC,
                "free": True,
                "quantity_total": TICKET2_QTY,
                "minimum_quantity": 1,
                "maximum_quantity": 4,
            }
        },
    )
    if t2.get("error"):
        raise RuntimeError(f"Free ticket failed: {t2}")
    print(f"  Free ticket: {t2.get('id')}")

    pub = api_post(f"/events/{event_id}/publish/")
    if pub.get("error") and not pub.get("published"):
        # Some responses return {"published": true}
        if not pub.get("published"):
            raise RuntimeError(f"Publish failed: {pub}")
    print(f"  Published: {event.get('url') or f'https://www.eventbrite.com/e/{event_id}'}")

    url = event.get("url")
    if not url:
        detail = api_get(f"/events/{event_id}/")
        url = detail.get("url")
    return {
        "date": day.isoformat(),
        "event_id": event_id,
        "url": url,
        "start_utc": start_utc,
        "end_utc": end_utc,
    }


def main():
    me = api_get("/users/me/")
    if me.get("error"):
        print(f"ERROR: token rejected — {me}")
        sys.exit(1)
    print(f"Signed in as: {me.get('name')} ({me.get('id')})")

    venue_id = ensure_venue()
    logo = upload_image(BANNER_IMAGE_PATH)
    logo_id = logo["id"] if logo else None

    # Anchor on 2026-07-31 context → first Wednesday 2026-08-05
    days = next_wednesdays(5, from_day=date(2026, 7, 31))
    results = []
    for day in days:
        results.append(create_one(day, venue_id, logo_id))

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "wednesday-eventbrite-created.json",
    )
    with open(out_path, "w") as f:
        json.dump({"events": results}, f, indent=2)
    print(f"\nWrote {out_path}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

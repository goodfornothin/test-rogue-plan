"""
create_eventbrite_event.py
==========================
Creates AND PUBLISHES a single Rogue Bachata event on Eventbrite via the v3 API.
No browser needed. Run with: python3 create_eventbrite_event.py

BEFORE RUNNING — fill in the variables under CONFIG below.
"""

import requests
import json
import os
import mimetypes

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG — edit these before each event
# ══════════════════════════════════════════════════════════════════════════════

PRIVATE_TOKEN = "WWCC7IYMEIDP5CQQJOQA"   # Eventbrite private token (account: voice@oscarcastellino.com)

# Event name — match exactly what's on the website page being promoted
EVENT_NAME = "Big Chill Bachata Mondays"

# Venue
VENUE_NAME  = "Big Chill Bar"
VENUE_ADDR1 = "257-259 Pentonville Rd"
VENUE_CITY  = "London"
VENUE_POST  = "N1 9NL"

# Date — always UTC. March is GMT (no DST yet), so 7:30 PM London = 19:30 UTC
# Format: "YYYY-MM-DDTHH:MM:SSZ"
# Example: Monday 2 March 2026 7:30 PM–11:30 PM
EVENT_START_UTC = "2026-03-02T19:30:00Z"
EVENT_END_UTC   = "2026-03-02T23:30:00Z"
TIMEZONE        = "Europe/London"

# Ticket 1 — paid class
TICKET1_NAME  = "Bachata Class \u00b7 7:30 PM"
TICKET1_DESC  = "Beginner-friendly 1-hour bachata class with Oscar & Boadicea. All levels, no partner needed."
TICKET1_PRICE_PENCE = 500    # 500 pence = \u00a35.00
TICKET1_QTY   = 50

# Ticket 2 — free social
TICKET2_NAME  = "Free Social Dancing \u00b7 from 8:30 PM"
TICKET2_DESC  = "Free entry to the social from 8:30 PM. No booking required \u2014 just arrive!"
TICKET2_QTY   = 200

# Image to use as the event banner (full path on this computer)
BANNER_IMAGE_PATH = "/Users/admin/github/test rogue plan/images/bachata-mondays-big-chill.jpg"

# Description HTML — copy from the relevant website landing page.
# DO NOT use emoji (\U0001f3b5 etc.) — they truncate the description at that point.
# Use Unicode escapes (\u00a3 for £, \u2014 for —) or plain ASCII.
# DO NOT set both description and summary in the same API call (SUMMARY_DESCRIPTION_CONFLICT).
DESCRIPTION_HTML = """<h2>Big Chill Bachata Mondays \u2014 King's Cross</h2>
<p>Join us every Monday at King's Cross for Bachata class and social dancing. Everyone is welcome \u2014 all levels can join.</p>
<h2>What's On</h2>
<ul>
<li><strong>7:30 PM \u2014 Bachata Class (\u00a35)</strong> \u00b7 Open to all levels</li>
<li><strong>8:30 PM \u2014 Free Social Dancing</strong> \u00b7 Come for the social even if you skip class. No partner needed.</li>
</ul>
<h2>Details</h2>
<ul>
<li><strong>When:</strong> Every Monday</li>
<li><strong>Class:</strong> Bachata \u00b7 7:30 PM \u00b7 \u00a35</li>
<li><strong>Social:</strong> Free from 8:30 PM</li>
<li><strong>Level:</strong> Open to all levels</li>
<li><strong>Venue:</strong> Big Chill Bar, King's Cross, London</li>
</ul>
<h2>What to Expect</h2>
<ul>
<li>Bachata class at 7:30 PM</li>
<li>Free social dancing from 8:30 PM</li>
<li>Bachata-focused Monday night at King's Cross</li>
<li>Open to all levels</li>
<li>No partner needed</li>
<li>Friendly crowd, all welcome</li>
</ul>
<h2>Why Big Chill, King's Cross?</h2>
<p>Big Chill is one of the coolest places in King's Cross to throw a Bachata Monday: central, easy to reach, full of energy, and made for social vibes. The space feels raw and vibrant, so the class warms everyone up and the floor naturally opens into that 8:30 PM social magic where people connect fast, dance more, and stay late.</p>
<h2>Watch Us Dance Before You Arrive</h2>
<ul>
<li><a href="https://www.youtube.com/playlist?list=PLLp_C8UrgAs-5NbNAbpETbA24wlrwE_Ed">Videos from Big Chill Bachata Mondays</a></li>
<li><a href="https://www.youtube.com/playlist?list=PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o">Rogue Bachata Social Dancing</a></li>
<li><a href="https://www.youtube.com/@RogueBachata">Rogue Bachata on YouTube</a></li>
</ul>
<h2>Find Us</h2>
<p>Big Chill Bar, King's Cross, London<br>257-259 Pentonville Rd, London N1 9NL</p>
<p><a href="https://www.google.com/maps/search/?api=1&query=Big+Chill+257+Pentonville+Rd+London+N1+9NL">Open in Google Maps</a></p>
<h2>Connect</h2>
<p>
<a href="https://wa.me/447596031416">WhatsApp Us</a> |
<a href="https://www.instagram.com/roguebachata/">@roguebachata on Instagram</a> |
<a href="https://roguebachata.com/big-chill-bachata-mondays.html">Full event info at roguebachata.com</a>
</p>"""

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS — do not edit below this line
# ══════════════════════════════════════════════════════════════════════════════

HEADERS      = {"Authorization": f"Bearer {PRIVATE_TOKEN}"}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}
BASE         = "https://www.eventbriteapi.com/v3"


def api_get(path):
    r = requests.get(f"{BASE}{path}", headers=HEADERS)
    return r.json()


def api_post(path, payload=None):
    r = requests.post(
        f"{BASE}{path}",
        headers=HEADERS_JSON,
        data=json.dumps(payload) if payload else None,
    )
    return r.json()


def upload_image(local_path):
    """Upload an image file to Eventbrite CDN. Returns image dict or None."""
    name = os.path.basename(local_path)
    print(f"  Uploading image: {name} ...", flush=True)

    # Step 1 — get S3 upload instructions
    r1 = requests.get(f"{BASE}/media/upload/",
                      params={"type": "image-event-logo"},
                      headers=HEADERS)
    instr = r1.json()
    if instr.get("error"):
        print(f"  ERROR getting upload instructions: {instr}")
        return None

    upload_url   = instr["upload_url"]
    file_param   = instr["file_parameter_name"]
    upload_data  = instr.get("upload_data", {})
    upload_token = instr.get("upload_token")

    # Step 2 — POST file to S3
    mime, _ = mimetypes.guess_type(local_path)
    mime = mime or "image/jpeg"
    with open(local_path, "rb") as f:
        files  = {file_param: (name, f, mime)}
        fields = {k: (None, v) for k, v in upload_data.items()}
        r2 = requests.post(upload_url, files={**files, **fields})

    if r2.status_code not in (200, 204):
        print(f"  ERROR S3 upload returned {r2.status_code}: {r2.text[:200]}")
        return None

    # Step 3 — confirm with Eventbrite
    r3 = requests.post(f"{BASE}/media/upload/",
                       headers=HEADERS_JSON,
                       data=json.dumps({"upload_token": upload_token}))
    result = r3.json()
    if result.get("error"):
        print(f"  ERROR confirming upload: {result}")
        return None

    print(f"  Image uploaded. Eventbrite ID: {result['id']}", flush=True)
    return result


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"  Creating Eventbrite event: {EVENT_NAME}")
    print(f"  Start: {EVENT_START_UTC}  End: {EVENT_END_UTC}")
    print("=" * 60)

    # 1. Verify token and get user
    user = api_get("/users/me/")
    if user.get("error"):
        print(f"ERROR: Token rejected — {user}")
        print("Check PRIVATE_TOKEN at the top of this script.")
        return
    user_id = user["id"]
    print(f"\n[1] Signed in as: {user.get('name', user_id)}")

    # 2. Get first organisation
    orgs = api_get(f"/users/{user_id}/organizations/")
    if not orgs.get("organizations"):
        print(f"ERROR: No organisations found — {orgs}")
        return
    org = orgs["organizations"][0]
    org_id = org["id"]
    print(f"[2] Organisation: {org.get('name', org_id)}  (ID {org_id})")

    # 3. Create venue
    print(f"\n[3] Creating venue: {VENUE_NAME} ...", flush=True)
    venue_resp = api_post(f"/organizations/{org_id}/venues/", {
        "venue": {
            "name": VENUE_NAME,
            "address": {
                "address_1":   VENUE_ADDR1,
                "city":        VENUE_CITY,
                "postal_code": VENUE_POST,
                "country":     "GB",
            }
        }
    })
    if venue_resp.get("error"):
        print(f"ERROR creating venue: {venue_resp}")
        return
    venue_id = venue_resp["id"]
    print(f"    Venue ID: {venue_id}")

    # 4. Create event (initially unlisted so we can add tickets before going live)
    print(f"\n[4] Creating event ...", flush=True)
    event_resp = api_post(f"/organizations/{org_id}/events/", {
        "event": {
            "name":        {"html": EVENT_NAME},
            "description": {"html": DESCRIPTION_HTML},
            "start":       {"timezone": TIMEZONE, "utc": EVENT_START_UTC},
            "end":         {"timezone": TIMEZONE, "utc": EVENT_END_UTC},
            "currency":    "GBP",
            "venue_id":    venue_id,
            "listed":      True,
            "shareable":   True,
            "capacity":    TICKET1_QTY + TICKET2_QTY,
            "category_id": "105",    # 105 = Performing Arts
        }
    })
    if event_resp.get("error"):
        print(f"ERROR creating event: {event_resp}")
        return
    event_id  = event_resp["id"]
    event_url = event_resp.get("url", f"https://www.eventbrite.co.uk/e/{event_id}")
    print(f"    Event ID:  {event_id}")
    print(f"    Event URL: {event_url}")

    # 5. Add ticket: paid class
    print(f"\n[5] Adding ticket 1: {TICKET1_NAME} (\u00a3{TICKET1_PRICE_PENCE // 100}) ...", flush=True)
    t1 = api_post(f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name":           TICKET1_NAME,
            "description":    TICKET1_DESC,
            "free":           False,
            "cost":           f"GBP,{TICKET1_PRICE_PENCE}",
            "quantity_total": TICKET1_QTY,
        }
    })
    if t1.get("error"):
        print(f"ERROR adding ticket 1: {t1}")
    else:
        print(f"    Created: {t1.get('name')}")

    # 6. Add ticket: free social
    print(f"\n[6] Adding ticket 2: {TICKET2_NAME} (Free) ...", flush=True)
    t2 = api_post(f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name":           TICKET2_NAME,
            "description":    TICKET2_DESC,
            "free":           True,
            "quantity_total": TICKET2_QTY,
        }
    })
    if t2.get("error"):
        print(f"ERROR adding ticket 2: {t2}")
    else:
        print(f"    Created: {t2.get('name')}")

    # 7. Upload banner image
    print(f"\n[7] Uploading banner image ...", flush=True)
    logo = None
    if os.path.exists(BANNER_IMAGE_PATH):
        logo = upload_image(BANNER_IMAGE_PATH)
        if logo:
            upd = api_post(f"/events/{event_id}/", {
                "event": {"logo_id": logo["id"]}
            })
            if upd.get("error"):
                print(f"  ERROR setting logo: {upd}")
            else:
                print(f"  Banner image set on event.")
    else:
        print(f"  WARNING: image not found at {BANNER_IMAGE_PATH} — skipping.")

    # 8. Publish
    print(f"\n[8] Publishing event ...", flush=True)
    pub = api_post(f"/events/{event_id}/publish/")
    if pub.get("error"):
        print(f"  WARNING: Publish returned error: {pub}")
        print(f"  The event may still be live — check the URL below.")
    else:
        print(f"  Published!")

    print("\n" + "=" * 60)
    print(f"  DONE")
    print(f"  Event URL: {event_url}")
    print(f"  Event ID:  {event_id}  (save this for updates)")
    print("=" * 60)
    print("\n  NOTE: To add extra images or video blocks, open the")
    print("  event URL, click Edit, and drag blocks in visually.")
    print("  The API does not support structured content modules.")


if __name__ == "__main__":
    main()

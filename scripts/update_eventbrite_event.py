"""
update_eventbrite_event.py
==========================
Updates an existing Eventbrite event: description, banner image,
additional image uploads, ticket changes.

Run with: python3 update_eventbrite_event.py

BEFORE RUNNING — set EVENT_ID to the ID of the event you want to update.
"""

import requests
import json
import os
import mimetypes

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

PRIVATE_TOKEN = "WWCC7IYMEIDP5CQQJOQA"   # Eventbrite private token

EVENT_ID = "1984197315584"   # <-- change this to the event you want to update

# Images directory
IMG_DIR = "/Users/admin/github/test rogue plan/images"

# New description HTML (optional — set to None to skip)
# RULES:
#   - No emoji characters — they truncate the description silently
#   - No &amp; in URLs — use plain & instead
#   - Do NOT set description and summary in the same call (conflict error)
NEW_DESCRIPTION_HTML = None   # set to a string to update, or leave as None

# New banner image path (optional — set to None to skip)
NEW_BANNER_PATH = None   # e.g. f"{IMG_DIR}/bachata-mondays-big-chill.jpg"

# Extra images to upload to Eventbrite CDN (they won't auto-appear in the
# listing body — but you get their IDs for manual use in the visual editor)
EXTRA_IMAGES_TO_UPLOAD = [
    # f"{IMG_DIR}/big-chill-venue.jpg",
    # f"{IMG_DIR}/Oscar Bo close couple.png",
    # f"{IMG_DIR}/Oscar Bo Intense.png",
    # f"{IMG_DIR}/RogueParty.jpg",
    # f"{IMG_DIR}/Boadicea and oscar Sensual Vibes.jpg",
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

HEADERS      = {"Authorization": f"Bearer {PRIVATE_TOKEN}"}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}
BASE         = "https://www.eventbriteapi.com/v3"


def api_get(path):
    r = requests.get(f"{BASE}{path}", headers=HEADERS)
    return r.json()


def api_post(path, payload):
    r = requests.post(f"{BASE}{path}", headers=HEADERS_JSON,
                      data=json.dumps(payload))
    return r.json()


def upload_image(local_path):
    """Upload image to Eventbrite CDN. Returns image dict or None."""
    name = os.path.basename(local_path)
    print(f"  Uploading: {name} ...", flush=True)

    r1 = requests.get(f"{BASE}/media/upload/",
                      params={"type": "image-event-logo"},
                      headers=HEADERS)
    instr = r1.json()
    if instr.get("error"):
        print(f"  ERROR: {instr}")
        return None

    mime, _ = mimetypes.guess_type(local_path)
    with open(local_path, "rb") as f:
        files  = {instr["file_parameter_name"]: (name, f, mime or "image/jpeg")}
        fields = {k: (None, v) for k, v in instr.get("upload_data", {}).items()}
        r2 = requests.post(instr["upload_url"], files={**files, **fields})

    if r2.status_code not in (200, 204):
        print(f"  ERROR S3 {r2.status_code}")
        return None

    r3 = requests.post(f"{BASE}/media/upload/", headers=HEADERS_JSON,
                       data=json.dumps({"upload_token": instr.get("upload_token")}))
    result = r3.json()
    if result.get("error"):
        print(f"  ERROR confirming: {result}")
        return None

    print(f"  Uploaded. ID={result['id']}  URL={result['url'][:60]}...", flush=True)
    return result


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"  Updating Eventbrite event ID: {EVENT_ID}")
    print("=" * 60)

    # Verify token
    user = api_get("/users/me/")
    if user.get("error"):
        print(f"ERROR: Token rejected — {user}")
        return
    print(f"[auth] Signed in as: {user.get('name')}")

    # Check event exists
    event = api_get(f"/events/{EVENT_ID}/")
    if event.get("error"):
        print(f"ERROR: Event not found — {event}")
        return
    print(f"[event] Name: {event['name']['text']}")
    print(f"        Status: {event['status']}")
    print(f"        URL: {event.get('url')}")

    updates = {}

    # Update description
    if NEW_DESCRIPTION_HTML is not None:
        print(f"\n[desc] Updating description ...", flush=True)
        r = api_post(f"/events/{EVENT_ID}/", {
            "event": {"description": {"html": NEW_DESCRIPTION_HTML}}
        })
        stored = (r.get("description") or {}).get("html") or ""
        if r.get("error"):
            print(f"  ERROR: {r}")
        else:
            print(f"  Stored {len(stored)} characters of HTML.")

    # Update banner image
    if NEW_BANNER_PATH:
        print(f"\n[banner] Uploading new banner ...", flush=True)
        logo = upload_image(NEW_BANNER_PATH)
        if logo:
            r = api_post(f"/events/{EVENT_ID}/", {"event": {"logo_id": logo["id"]}})
            if r.get("error"):
                print(f"  ERROR setting logo: {r}")
            else:
                print(f"  Banner updated.")

    # Upload extra images
    if EXTRA_IMAGES_TO_UPLOAD:
        print(f"\n[images] Uploading {len(EXTRA_IMAGES_TO_UPLOAD)} extra images ...", flush=True)
        uploaded = {}
        for path in EXTRA_IMAGES_TO_UPLOAD:
            if os.path.exists(path):
                img = upload_image(path)
                if img:
                    uploaded[os.path.basename(path)] = img["id"]
            else:
                print(f"  WARNING: not found: {path}")
        if uploaded:
            print("\n  Uploaded image IDs (use these in the visual editor):")
            for name, img_id in uploaded.items():
                print(f"    {name}: {img_id}")

    print("\n" + "=" * 60)
    print(f"  Update complete.")
    print(f"  https://www.eventbrite.co.uk/e/{EVENT_ID}")
    print("=" * 60)


if __name__ == "__main__":
    main()

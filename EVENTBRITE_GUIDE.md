# Rogue Bachata — Eventbrite Event Creation Guide

This guide explains how to create and manage Eventbrite events for Rogue Bachata.
It was written from live experience so it includes all the gotchas.

**Target reader:** An AI agent or human following this step-by-step.

---

## Account Details

| Field | Value |
|---|---|
| Eventbrite login email | voice@oscarcastellino.com |
| Eventbrite private token | `WWCC7IYMEIDP5CQQJOQA` |
| Organisation name | Rogue Bachata |
| Organisation ID | 2993365546501 |
| API key | 4UHYRVNQNTQU43FDSM |
| Client secret | SYCTDC6XNVK4F4QMQTBYU4RMZD5MO6AUVRBQ2LGBZPUKREK64T |

The **private token** is the only credential you need for the API. Use it as a Bearer token in all requests.

---

## Recurring Events We Create

### Big Chill Bachata Mondays
- **Venue:** Big Chill Bar, 257-259 Pentonville Rd, Kings Cross, London N1 9NL
- **Schedule:** Every Monday, 7:30 PM – 11:30 PM
- **Class ticket:** £5 · Bachata Class at 7:30 PM (limited spots)
- **Free ticket:** Free Social Dancing from 8:30 PM
- **Website landing page:** https://roguebachata.com/big-chill-bachata-mondays.html
- **Banner image:** `images/bachata-mondays-big-chill.jpg`
- **YouTube playlist:** `PLLp_C8UrgAs-5NbNAbpETbA24wlrwE_Ed`

### Bachata Tuesdays at Cafe Sol
- **Venue:** Cafe Sol London, 13-15 Clapham High Street, London SW4 7TS
- **Schedule:** Every Tuesday, 7:30 PM – 11:00 PM
- **Class ticket:** £10 · Bachata Class at 7:30 PM
- **Free ticket:** Free Social Dancing from 8:30 PM
- **Website landing page:** https://roguebachata.com/bachata-tuesdays.html
- **Banner image:** `images/Bachata-Tuesdays-Social.png`

---

## Prerequisites

You need Python 3 and the `requests` library. No browser, no Playwright needed.

```bash
# Check Python is installed
python3 --version

# Install requests if missing
pip3 install requests
```

That's it. The scripts in `scripts/` do everything else.

---

## Step-by-Step: Create an Event for a Specific Monday

### Step 1 — Find the correct event details

Always pull the description text from the live website landing page, not from memory.

For Big Chill Bachata Mondays:
```
https://roguebachata.com/big-chill-bachata-mondays.html
```

Key things to note from the page:
- The exact event name (copy it word for word)
- The schedule (class time, social time, end time)
- The ticket price for the class
- Any specific copy about the vibe, venue, hosts

### Step 2 — Calculate the date and UTC times

**Important:** Eventbrite stores all times in UTC.
- March–October (BST, UTC+1): subtract 1 hour. So 7:30 PM London = 18:30 UTC
- November–February (GMT, UTC+0): same time. So 7:30 PM London = 19:30 UTC

Example for Monday 2 March 2026 (March = GMT still):
```
EVENT_START_UTC = "2026-03-02T19:30:00Z"
EVENT_END_UTC   = "2026-03-02T23:30:00Z"
```

Example for Monday 6 April 2026 (April = BST):
```
EVENT_START_UTC = "2026-04-06T18:30:00Z"
EVENT_END_UTC   = "2026-04-06T22:30:00Z"
```

### Step 3 — Edit the create script

Open `scripts/create_eventbrite_event.py` and fill in the CONFIG section at the top:

```python
PRIVATE_TOKEN       = "WWCC7IYMEIDP5CQQJOQA"   # do not change
EVENT_NAME          = "Big Chill Bachata Mondays"
VENUE_NAME          = "Big Chill Bar"
VENUE_ADDR1         = "257-259 Pentonville Rd"
VENUE_CITY          = "London"
VENUE_POST          = "N1 9NL"
EVENT_START_UTC     = "2026-03-02T19:30:00Z"    # <-- update this
EVENT_END_UTC       = "2026-03-02T23:30:00Z"    # <-- update this
BANNER_IMAGE_PATH   = "/Users/admin/github/test rogue plan/images/bachata-mondays-big-chill.jpg"
```

The description in the script already matches the website. Only update it if the website copy has changed.

### Step 4 — Run the script

```bash
cd "/Users/admin/github/test rogue plan"
python3 scripts/create_eventbrite_event.py
```

Expected output:
```
============================================================
  Creating Eventbrite event: Big Chill Bachata Mondays
  Start: 2026-03-02T19:30:00Z  End: 2026-03-02T23:30:00Z
============================================================

[1] Signed in as: Annie Peskett
[2] Organisation: Rogue Bachata  (ID 2993365546501)

[3] Creating venue: Big Chill Bar ...
    Venue ID: 296649144

[4] Creating event ...
    Event ID:  1984197315584
    Event URL: https://www.eventbrite.co.uk/e/big-chill-bachata-mondays-tickets-1984197315584

[5] Adding ticket 1: Bachata Class · 7:30 PM (£5) ...
    Created: Bachata Class · 7:30 PM

[6] Adding ticket 2: Free Social Dancing · from 8:30 PM (Free) ...
    Created: Free Social Dancing · from 8:30 PM

[7] Uploading banner image ...
    Image uploaded. Eventbrite ID: 1178697099
    Banner image set on event.

[8] Publishing event ...
    Published!

============================================================
  DONE
  Event URL: https://www.eventbrite.co.uk/e/big-chill-bachata-mondays-tickets-1984197315584
  Event ID:  1984197315584  (save this for updates)
============================================================
```

**Save the Event ID** — you need it if you want to update the event later.

### Step 5 — Add extra images in the Eventbrite editor (manual, 2 minutes)

The API cannot add image blocks or video embeds inside the event description body — this requires their visual drag-and-drop editor.

1. Go to the event URL
2. Click **Edit**
3. In the description area, click **+** to add a block
4. Choose **Image** → upload one of:
   - `images/big-chill-venue.jpg` (venue photo)
   - `images/Oscar Bo close couple.png` (Oscar & Boadicea close-up)
   - `images/Boadicea and oscar Sensual Vibes.jpg`
5. Choose **Video** → paste: `https://www.youtube.com/playlist?list=PLLp_C8UrgAs-5NbNAbpETbA24wlrwE_Ed`
6. Click **Save & Continue**

---

## Step-by-Step: Update an Existing Event

Use `scripts/update_eventbrite_event.py`.

Open it and set:
```python
EVENT_ID = "1984197315584"    # the event to update
```

Then uncomment and fill whichever sections you need:
- `NEW_DESCRIPTION_HTML` — to replace the description
- `NEW_BANNER_PATH` — to replace the banner image
- `EXTRA_IMAGES_TO_UPLOAD` — to upload images to Eventbrite CDN

Run:
```bash
python3 scripts/update_eventbrite_event.py
```

---

## Known Gotchas — Read Before Touching the API

### 1. Emoji break the description silently
**Problem:** If your description HTML contains any emoji character (🎵 🎶 ✅ 📍 etc.),
Eventbrite truncates the description at that exact character without any error.
The stored result will be only a few characters long.

**Fix:** Never use emoji. Use Unicode escapes or plain text alternatives:
```python
# BAD — will truncate
"<h2>🎵 Bachata Mondays</h2>"

# GOOD
"<h2>Bachata Mondays</h2>"
"<li>\u2714 All levels welcome</li>"    # ✓
"<li>(\u00a35) Bachata class</li>"      # (£5)
```

### 2. Summary and description cannot both be set
**Problem:** Calling `POST /events/{id}/` with both `summary` and `description.html`
returns `400 SUMMARY_DESCRIPTION_CONFLICT`.

Eventbrite has two content systems:
- **Legacy:** `description.html` — one HTML block, shows in older UI
- **New:** `summary` + structured content modules — shows in new UI

They are mutually exclusive. Our events use **legacy** (`description.html`).

**Fix:** Never set both in the same request. Choose one:
```python
# CORRECT — description only
{"event": {"description": {"html": "<p>...</p>"}}}

# CORRECT — summary only (but then description is blank)
{"event": {"summary": "Short blurb here"}}

# WRONG — will fail with 400
{"event": {"description": {"html": "..."}, "summary": "..."}}
```

### 3. Structured content module API returns 404
**Problem:** The API advertises `add_module` and `publish` endpoints under
`/events/{id}/structured_content/1/module/` but posting to them returns 404.

This feature requires a higher-tier API partner account. Our account does not have access.

**Fix:** Do not attempt to call these endpoints. Use the visual Eventbrite editor
for image/video blocks instead (manual step, 2 minutes).

### 4. Image upload is a 3-step process
Eventbrite uses AWS S3 for image hosting. The upload sequence is:

```
Step 1: GET /v3/media/upload/?type=image-event-logo
        → receive upload_url, file_parameter_name, upload_data, upload_token

Step 2: POST to upload_url (S3 URL, not Eventbrite)
        → multipart form with all upload_data fields + the image file

Step 3: POST /v3/media/upload/
        → body: {"upload_token": "..."}
        → receive {"id": "...", "url": "..."}  ← use this id as logo_id
```

Then set the logo:
```python
POST /v3/events/{id}/  with {"event": {"logo_id": "1178697099"}}
```

### 5. Ticket price format
Price must be in pence (minor currency units) as a string `"GBP,500"` for £5.
```python
"cost": "GBP,500"    # £5.00
"cost": "GBP,1000"   # £10.00
```

### 6. UTC time zones for London
- GMT (November–March): 7:30 PM London = `19:30:00Z`
- BST (last Sunday March – last Sunday October): 7:30 PM London = `18:30:00Z`

Always double-check before setting dates. BST starts 29 March 2026.

### 7. Event category ID
Eventbrite category `105` = Performing Arts. This is the right one for dance events.
Do not use Music (103) or Nightlife (106) — Performing Arts ranks better for dance searches.

---

## Eventbrite API Quick Reference

All requests need this header:
```
Authorization: Bearer WWCC7IYMEIDP5CQQJOQA
Content-Type: application/json
```

Base URL: `https://www.eventbriteapi.com/v3`

| What | Method | Endpoint |
|---|---|---|
| Get current user | GET | `/users/me/` |
| Get organisations | GET | `/users/{user_id}/organizations/` |
| Create venue | POST | `/organizations/{org_id}/venues/` |
| Create event | POST | `/organizations/{org_id}/events/` |
| Update event | POST | `/events/{event_id}/` |
| Add ticket | POST | `/events/{event_id}/ticket_classes/` |
| Publish event | POST | `/events/{event_id}/publish/` |
| Unpublish event | POST | `/events/{event_id}/unpublish/` |
| Delete event | DELETE | `/events/{event_id}/` |
| Upload image step 1 | GET | `/media/upload/?type=image-event-logo` |
| Upload image step 3 | POST | `/media/upload/` |
| Set event logo | POST | `/events/{event_id}/` with `{"event": {"logo_id": "..."}}` |

---

## Website Images Available for Upload

All in `/Users/admin/github/test rogue plan/images/`:

| File | Description | Best for |
|---|---|---|
| `bachata-mondays-big-chill.jpg` | Main Monday event artwork | Banner for Monday events |
| `big-chill-venue.jpg` | Big Chill Bar interior/exterior | Venue block in editor |
| `Bachata-Tuesdays-Social.png` | Tuesday social night artwork | Banner for Tuesday events |
| `Oscar Bo close couple.png` | Oscar & Boadicea close intimate shot | About hosts section |
| `Oscar Bo Intense.png` | Oscar & Boadicea intense dance moment | Hero or feature image |
| `Boadicea and oscar Sensual Vibes.jpg` | Partner dance photo | About / gallery |
| `RogueParty.jpg` | Dancers at a party | Vibe / atmosphere image |
| `RogueResonance.png` | Workshop promotional image | Workshop events only |

---

## YouTube Playlists

| Playlist | ID | URL |
|---|---|---|
| Big Chill Bachata Mondays | `PLLp_C8UrgAs-5NbNAbpETbA24wlrwE_Ed` | https://www.youtube.com/playlist?list=PLLp_C8UrgAs-5NbNAbpETbA24wlrwE_Ed |
| Bachata Dances (social) | `PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o` | https://www.youtube.com/playlist?list=PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o |
| Sensual Dancing | `PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9` | https://www.youtube.com/playlist?list=PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9 |
| Workshops | `PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ` | https://www.youtube.com/playlist?list=PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ |
| YouTube Channel | — | https://www.youtube.com/@RogueBachata |

---

## Description Writing Rules

When writing the event description HTML:

1. **Copy from the website** — go to the relevant landing page on roguebachata.com and use that exact language. Do not invent copy.
2. **No emoji** — they silently break the description (see Gotcha #1)
3. **Use `<h2>` for section headings**, `<p>` for paragraphs, `<ul><li>` for bullet lists, `<a href="...">` for links
4. **Plain & in URLs** — use `&` not `&amp;` inside href attributes
5. **£ sign** — use `\u00a3` in Python strings, or the literal `£` in HTML
6. **Section order that works well:**
   - Main title / intro paragraph
   - What's On (schedule)
   - Details (structured bullet list)
   - What to Expect
   - Why this venue (the specific venue copy)
   - Watch Us Dance (YouTube links)
   - Find Us (address + Google Maps link)
   - Connect (WhatsApp, Instagram, website link)
   - Tickets (clear explanation of both ticket types)

---

## Events Created So Far

| Event | Eventbrite ID | URL | Date |
|---|---|---|---|
| Big Chill Bachata Mondays | 1984197315584 | https://www.eventbrite.co.uk/e/big-chill-bachata-mondays-tickets-1984197315584 | Mon 2 Mar 2026 |

---

## Contact & Social Links (use these consistently)

| Channel | Link |
|---|---|
| Website | https://roguebachata.com |
| Instagram | https://www.instagram.com/roguebachata/ |
| WhatsApp | https://wa.me/447596031416 |
| YouTube | https://www.youtube.com/@RogueBachata |
| Google Maps (Big Chill) | https://www.google.com/maps/search/?api=1&query=Big+Chill+257+Pentonville+Rd+London+N1+9NL |
| Google Maps (Cafe Sol) | https://www.google.com/maps/search/?api=1&query=Cafe+Sol+13-15+Clapham+High+Street+London+SW4+7TS |

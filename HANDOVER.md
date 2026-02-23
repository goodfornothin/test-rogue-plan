# Rogue Bachata – Agent Handover

**Last updated:** 2026-02-23  
**Maintained by:** AI agents via Telegram remote control

---

## The Site

| | |
|---|---|
| **URL** | roguebachata.com |
| **Type** | Static HTML/CSS/JS — GitHub Pages |
| **Repo** | github.com/goodfornothin/test-rogue-plan (branch: `main`) |
| **Local path** | `/root/workspace/roguebachata` |
| **Deploy** | Push to `main` → auto-deploys in ~1 min |

---

## File Structure

```
index.html                    Homepage (hero carousel, events, offerings, contact)
style.css                     Global styles & CSS variables
data.json                  ← ALL event data lives here. Edit this for event updates.
bachata-mondays.html
bachata-tuesdays.html
cafe-sol-event.html
salsa-bachata-mondays.html    Kings Cross beginners page (full-page video bg)
sensual-couples.html
rogue-resonance.html          Advanced workshops
bachata-workshop.html
rogue-resonance-camden-jan-2026.html
rogue-resonance-create-destroy-feb-2026.html
images/                       Posters, photos
videos/                       Background videos
```

### data.json structure
Always edit this file for event updates — never hardcode events into HTML directly.
```json
{
  "upcomingEvents": [ ... ],
  "pastEvents":     [ ... ]
}
```
Current upcoming (2026-02-23): Feb 25 and Mar 4 Cafe Sol Tuesdays, weekly Big Chill Monday, Rogue Resonance workshop.

### Navigation
Every page has a fixed navbar with a hamburger menu on mobile.  
`scroll-padding-top: 70px` compensates for the fixed nav when using `#events` anchor.

---

## Infrastructure

### Server
- **Host:** Ubuntu VPS (Hetzner), root user
- **SSH key:** `/root/.ssh/id_ed25519` (ed25519)

### Git / Deploy
```bash
cd /root/workspace/roguebachata
git add -A && git commit -m "message" && git push
```
GitHub user: `goodfornothin` — SSH key already configured.

---

## AI / Remote Control Stack

### 1. Rogue Website Bot (@RogueWebsiteBot)
**Purpose:** Remote website management from Telegram  
**Token:** `8716439936:AAFJ-8CiGpjX70wy1vnwHYosz0sSLt2ypH4`  
**Service:** `systemctl status rogue-bot`  
**Code:** `/root/rogue-bot/bot.py`  
**Config:** `/root/rogue-bot/.env`

How it works: Telegram message → `openclaw agent --local` (GitHub Copilot, GPT-4.1 default) → text reply. Voice messages: OGG → Whisper → agent → gTTS voice reply.

**Telegram commands:**
- `/start` — intro + shows your Telegram user ID
- `/model gpt4` — switch model (gpt4, sonnet, opus, gpt5, gemini)
- `/models` — list all with tap-to-select keyboard
- Any text/voice → agent responds with full file access to workspace

**Action needed:** Set OWNER_ID to lock the bot to you only:
```bash
echo "OWNER_ID=<your_telegram_id>" >> /root/rogue-bot/.env
systemctl restart rogue-bot
```
Send `/start` to @RogueWebsiteBot to find your Telegram ID.

---

### 2. OpenClaw Gateway
**Purpose:** AI agent platform for Telegram channels and multi-agent routing  
**Service:** `systemctl status openclaw-gateway`  
**Config:** `/root/.openclaw/openclaw.json`  
**Default model:** `github-copilot/gpt-4.1` (via GitHub Copilot — no API cost)  
**Telegram bot:** @Oscar_Boy_Clawd_bot (token prefix: `8595586...`)

**Agents:**
| ID | Model | Purpose |
|---|---|---|
| main | github-copilot/gpt-4.1 | Default |
| robert | github-copilot/gpt-4.1 | Rogue Bachata identity |
| opus | github-copilot/claude-opus-4.5 | Heavy reasoning |
| gpt5 | github-copilot/gpt-5 | Latest OpenAI |
| gemini25 | github-copilot/gemini-2.5-pro | Google |

**Auth:** GitHub Copilot OAuth via VSCode — no API key. Stored in `/root/.openclaw/identity/`.

**If gateway gets stuck (orphan process bug):**
```bash
pkill -f openclaw-gateway; sleep 2
systemctl restart openclaw-gateway
sleep 5 && openclaw health
```

---

### 3. All Telegram Bots
| Handle | Token prefix | Connected to |
|---|---|---|
| @RogueWebsiteBot | 8716439... | /root/rogue-bot/bot.py |
| @Oscar_Boy_Clawd_bot | 8595586... | openclaw-gateway (openclaw "Umesh") |
| @RogueBachataBot | 8085307... | openclaw (agent: robert) |
| @Urban_Trading_Expert_Bot | 8449247... | separate setup (agent: samuel) |

---

## Common Tasks

**Add upcoming event:**
```bash
# Edit data.json upcomingEvents array, then:
git add data.json && git commit -m "add event: name" && git push
```

**Move event to past:**  
Cut from `upcomingEvents`, paste into `pastEvents` in `data.json`.

**Check site:**
```bash
curl -s -o /dev/null -w "%{http_code}" https://roguebachata.com
```

**Check health:**
```bash
systemctl status rogue-bot openclaw-gateway
openclaw health
```

---

## Rules for New Agents
- Always edit `data.json` for events — never hardcode into HTML
- Moonshot is permanently removed — do not add it back; all AI uses GitHub Copilot
- Anthropic API key exists in `/etc/systemd/system/openclaw-gateway.service` but account has zero credits — use Copilot
- Claude CLI at `/root/.vscode-server/.../native-binary/claude` cannot run headlessly as root — do not use in scripts; use `openclaw agent --local` instead
- No build system — edit files directly and push to deploy

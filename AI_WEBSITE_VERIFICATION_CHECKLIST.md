# Rogue Bachata – AI Verification Checklist

> **Repo:** https://github.com/goodfornothin/test-rogue-plan
> **Live:** https://roguebachata.com

---

## 🔄 1. Content Sync (Do This First)

Before making any content updates, always sync the latest media from Google Drive:

```bash
# Syncs images/ and videos/ from Google Drive
./sync_media.sh
```

---

## ✅ 2. Pre-Commit Verification (Run These Checks)

Run these commands in the project root to ensure site integrity.

```bash
# A. JSON Validation (Critical for site content)
python3 -c "import json; json.load(open('data.json')); print('✅ JSON Valid')"

# B. Privacy Check (No "Castellino" visible, email obfuscated)
grep -ri "castellino" index.html data.json | grep -v "mailto:" | grep -v "voice@oscarcastellino" | grep -v "atob" && echo "❌ Privacy Issue Found" || echo "✅ Privacy Check Passed"

# C. YouTube Playlist ID Check
python3 -c "
import json; d=json.load(open('data.json'))
p=d['youtubePlaylists']
assert p['workshops']['id']=='PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ','workshops ID wrong'
assert p['dances']['id']=='PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o','dances ID wrong'
assert p['sensual']['id']=='PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9','sensual ID wrong'
print('✅ Playlists OK')
"

# D. Broken Link Check (No empty hrefs)
grep -rn 'href="#"' index.html && echo "❌ Empty hrefs found" || echo "✅ Link Check Passed"
```

---

## 🔑 3. Key Rules & Constraints

| Category | Rule |
|----------|------|
| **Privacy** | Never show "Castellino" visibly (use "Oscar"). Email must be obfuscated with `atob()`. |
| **Media** | Images/Videos must be synced via `./sync_media.sh` before use. Do not manually add large files if they exist on Drive. |
| **Links** | Never use `href="#"`. Use `javascript:void(0)` or real targets. |
| **Structure** | All dynamic content (events, classes, text) lives in `data.json`. Do not hardcode content in HTML. |
| **Deployment** | Always commit and push changes immediately after verifying them so they are visible online. |

---

## 🚀 4. Deployment (Commit & Push)

After passing all checks, you **MUST** commit and push your changes for them to go live.

```bash
# 1. Stage changes
git add -A

# 2. Commit with a clear message
git commit -m "update: [description of changes]"

# 3. Push to main branch (triggers deployment)
git push origin main
```

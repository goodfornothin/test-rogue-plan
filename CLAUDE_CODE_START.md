# PASTE THIS INTO FIRST CHAT WITH CLAUDE CODE

You are taking over maintenance of **Rogue Bachata** (roguebachata.com), a static HTML/CSS/JS website hosted on GitHub Pages.

## Quick Facts
- **Repo:** https://github.com/goodfornothin/test-rogue-plan (main branch)
- **Local:** `/Users/admin/github/test rogue plan`
- **Live:** https://roguebachata.com (deploys automatically after git push)
- **Stack:** Vanilla HTML/CSS/JS, Google Fonts, YouTube embeds, JSON data

## What We Just Built (Feb 2026)

### Hero Section Carousel
Replaced static hero with a 5-slide auto-advancing carousel:
1. Rogue Bachata → Movement · Connection · Freedom → #events
2. Rogue Mondays → at Kings Cross → booking link
3. Rogue Tuesdays → at Clapham → cafe-sol-event.html
4. Rogue Workshops → rogue-resonance.html
5. Couples Sensual → sensual-couples.html

**Features:** Auto-advance (5s), sleek left/right arrows, mobile swipe, keyboard support, fully transparent cards over video background, "More" button text

**Code locations:**
- `.hero-carousel`, `.hero-slide`, `.hero-card` classes in HTML `<style>` (~line 75-160)
- Hero carousel JS: `// Hero Carousel with sleek arrows` (~line 788)
- HTML slides: Search for `class="hero-slide"` (5 divs)

### Other Fixes
- Rogue Resonance video now portrait format (was landscape)
- Logo link fixed (was `href="#"`, now `#heroSection`)
- Buttons changed from "Book" to "More"
- Simplified AI checklist (40 lines, not 550)

## Critical Rules

### Privacy
- **Never show "Castellino"** visibly (use only "Oscar" or "Boadicea & Oscar")
- Email: voice@oscarcastellino.com (obfuscate with `atob()` or mailto)

### YouTube Playlists (these have been swapped before!)
- workshops = `PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ`
- dances = `PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o`
- sensual = `PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9`

### Links & Content
- **Never use** `href="#"` (causes nav errors) — use `javascript:void(0)` or real targets
- **All dynamic content** lives in `data.json` (don't hardcode event names, dates)
- **Couples page** (sensual-couples.html) must NOT show £ prices, only email buttons

## Pre-Commit Checklist

Always run before `git commit`:

```bash
# JSON valid
python3 -c "import json; json.load(open('data.json')); print('OK')"

# No privacy leaks
grep -ri "castellino" index.html data.json | grep -v "mailto:" | grep -v "voice@oscarcastellino" | grep -v "atob"
# ^ Should print nothing

# YouTube playlist IDs correct
python3 -c "
import json; d=json.load(open('data.json'))
p=d['youtubePlaylists']
assert p['workshops']['id']=='PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ','workshops'
assert p['dances']['id']=='PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o','dances'
assert p['sensual']['id']=='PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9','sensual'
print('OK')
"

# No empty hrefs
grep -rn 'href="#"' index.html
# ^ Should print nothing
```

## Deploy

```bash
git add -A && git commit -m "update: description" && git push origin main
# Wait 1-2 min for GitHub Pages to deploy
# Check https://roguebachata.com
```

## Key Files

| File | Purpose |
|------|---------|
| index.html | Homepage (hero carousel, offerings, events, contact) |
| data.json | All dynamic content (events, playlists, offerings, principles) |
| style.css | Global styles, CSS variables for brand colors |
| sensual-couples.html | Couples page (no prices, email buttons only) |
| rogue-resonance.html | Workshops page |
| HANDOVER.md | Complete detailed documentation (40+ sections) |

## Common Updates

1. **Add event** → Edit `data.json` → `upcomingEvents`
2. **Update Rogue Parties** → Edit `data.json` → `rogueParties`
3. **Change button/text** → Find in `data.json` or `index.html`, update, push
4. **Fix image** → Replace in `images/` folder, update path in `data.json`

## Next Actions

1. Read the full `HANDOVER.md` file in the repo for complete context
2. Run the pre-commit checklist above to verify everything works
3. Test locally: `python3 -m http.server 8000` → http://localhost:8000
4. Make your changes, commit, push
5. Verify live at https://roguebachata.com

---

**Contact:** Oscar (voice@oscarcastellino.com)  
**Last Updated:** 18 February 2026

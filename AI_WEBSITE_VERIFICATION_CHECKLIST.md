# Rogue Bachata – AI Checklist

> Static site on GitHub Pages. Changes go live after `git push origin main`.
> **Repo:** https://github.com/goodfornothin/test-rogue-plan
> **Local:** `/Users/admin/github/test rogue plan`
> **Live:** https://roguebachata.com

---

## Before Every Commit – Run These Checks

```bash
cd "/Users/admin/github/test rogue plan"

# 1. JSON must be valid
python3 -c "import json; json.load(open('data.json')); print('OK')"

# 2. No "Castellino" visible (email in mailto/atob is fine)
grep -ri "castellino" index.html data.json | grep -v "mailto:" | grep -v "voice@oscarcastellino" | grep -v "atob"
# ^ Should print nothing

# 3. YouTube playlist IDs correct
python3 -c "
import json; d=json.load(open('data.json'))
p=d['youtubePlaylists']
assert p['workshops']['id']=='PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ','workshops wrong'
assert p['dances']['id']=='PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o','dances wrong'
assert p['sensual']['id']=='PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9','sensual wrong'
print('Playlists OK')
"

# 4. No href="#" (use javascript:void(0) or real targets)
grep -rn 'href="#"' index.html
# ^ Should print nothing
```

Fix anything that fails, then commit:

```bash
git add -A && git commit -m "describe changes" && git push origin main
```

---

## Key Rules

| Rule | Detail |
|------|--------|
| **Privacy** | Never show "Castellino" visibly. Use only "Oscar" or "Boadicea & Oscar". Email is obfuscated with `atob()`. |
| **YouTube IDs** | workshops = `PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ`, dances = `PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o`, sensual = `PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9`. These have been swapped before — always verify. |
| **Couples page** | sensual-couples.html must NOT show £ prices. Only email contact buttons. |
| **Contact email** | `voice@oscarcastellino.com` — always obfuscated, never in plain HTML. |
| **Links** | Never use `href="#"`. Use `javascript:void(0)` with onclick, or a real target. |
| **Hero** | 5-slide carousel: Rogue Bachata, Rogue Mondays (Kings Cross), Rogue Tuesdays (Clapham), Rogue Workshops, Couples Sensual. Button text is "Book". |
| **Rogue Parties** | Tuesdays = Cafe Sol, Clapham (£10 class, free social). Mondays = Big Chill, Kings Cross (£5 class, free social). |

---

## File Reference

| File | Purpose |
|------|---------|
| `index.html` | Homepage with hero carousel, offerings, events, contact |
| `style.css` | Global styles, CSS variables for brand colours |
| `data.json` | All dynamic content (offerings, events, playlists, parties) |
| `sensual-couples.html` | Couples dance page (no prices, email buttons only) |
| `rogue-resonance.html` | Workshops page |
| `cafe-sol-event.html` | Cafe Sol event landing page |
| `images/` | All site images |

---

*Last updated: 11 February 2026*

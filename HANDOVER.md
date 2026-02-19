# Rogue Bachata Website – Complete Handover Documentation

## Project Overview

**Site:** Rogue Bachata (roguebachata.com)  
**Type:** Static HTML/CSS/JS website hosted on GitHub Pages  
**Repository:** https://github.com/goodfornothin/test-rogue-plan  
**Local Path:** `/Users/admin/github/test rogue plan`  
**Status:** Active, regularly updated with events and content

---

## Current Architecture

### Key Files
- **index.html** (~1100 lines) – Homepage with hero carousel, navigation, offerings, events, contact
- **style.css** (~800 lines) – Global styles, CSS variables, responsive design
- **data.json** – All dynamic content (events, offerings, playlists, principles, parties)
- **sensual-couples.html** – Couples dance page (no prices, email contact buttons only)
- **rogue-resonance.html** – Advanced workshops page
- **cafe-sol-event.html** – Cafe Sol event landing page
- **images/** – All site imagery
- **videos/** – Video content stored locally
- **CNAME** – Domain: roguebachata.com

### Tech Stack
- HTML5, CSS3, Vanilla JavaScript (no frameworks)
- Google Fonts (Poppins family for typography)
- YouTube iframe embeds for playlists
- Responsive breakpoint at 768px

---

## Recent Work Completed (11-18 February 2026)

### 1. Hero Section Transformation
**Before:** Static hero with title, tagline, "Book a Class" button  
**After:** 5-slide carousel with auto-advance

**Hero Carousel Details:**
- Slide 1: "Rogue Bachata" → Movement · Connection · Freedom → #events
- Slide 2: "Rogue Mondays" → at Kings Cross → Fatsoma booking link
- Slide 3: "Rogue Tuesdays" → at Clapham → cafe-sol-event.html
- Slide 4: "Rogue Workshops" → Advanced Technique & Artistry → rogue-resonance.html
- Slide 5: "Couples Sensual" → Dance Into Each Other → sensual-couples.html

**Features:**
- Auto-advances every 5 seconds
- Sleek left/right arrow buttons (outside button area, no overlap)
- Mobile swipe support
- Keyboard accessibility (arrow keys, Enter/Space on buttons)
- Fully transparent cards (no box/border) – floating text over video background
- Button text: "More" (changed from "Book")
- Same video background on all slides (sensual-couple.mp4)

**HTML Structure:**
```html
<section class="hero" id="heroSection">
  <div class="hero-video-container"><!-- video background --></div>
  <div class="hero-carousel" id="heroCarousel">
    <div class="hero-slide active" data-index="0">
      <div class="hero-card">
        <h1>Rogue Bachata</h1>
        <p class="hero-card-subtitle">Movement · Connection · Freedom</p>
        <a href="#events" class="cta-btn">More</a>
      </div>
    </div>
    <!-- 4 more slides -->
  </div>
  <div class="hero-carousel-arrows">
    <button class="hero-arrow hero-arrow-left">&#8592;</button>
    <button class="hero-arrow hero-arrow-right">&#8594;</button>
  </div>
</section>
```

**CSS Classes:**
- `.hero-carousel` – Container, positioned relative, z-index: 2
- `.hero-slide` – Absolute positioned, opacity fade transition
- `.hero-slide.active` – Currently visible slide
- `.hero-card` – Transparent text container
- `.hero-carousel-arrows` – Arrow button container (absolute, centered vertically)
- `.hero-arrow` – Individual arrow buttons (44px, minimal styling, hover effects)

**JavaScript Logic:**
- Auto-advance every 5 seconds
- Click arrows to change slide
- Swipe on mobile (left = next, right = prev)
- Keyboard: left/right arrow keys or button focus + Enter/Space
- Resets auto-timer on user interaction

### 2. Rogue Resonance Video Format Fix
**Issue:** Featured YouTube video was displaying in landscape (very small)  
**Solution:** Changed to portrait format (9:16 aspect ratio)  
**Change:** Removed `.landscape` class from video-wrapper div

### 3. Navigation & Links
**Logo Fix:** Changed `href="#"` to `href="#heroSection"`  
**All Links:** Verified no empty hrefs exist

### 4. Button Text Unified
Changed all hero carousel buttons from "Book" to "More"

### 5. Simplified AI Checklist
**Before:** 550+ line checklist with extensive detail  
**After:** ~40 line checklist focused on critical checks

---

## Data Structure (data.json)

```json
{
  "youtubePlaylists": {
    "workshops": {
      "id": "PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ",
      "title": "Bachata Workshops",
      "format": "portrait"
    },
    "dances": {
      "id": "PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o",
      "title": "Bachata Dances",
      "format": "portrait"
    },
    "sensual": {
      "id": "PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9",
      "title": "Sensual Couple Dancing",
      "format": "portrait"
    }
  },
  "rogueParties": [
    {
      "id": "rogue-tuesdays",
      "name": "Rogue Tuesdays",
      "venue": "Cafe Sol London",
      "day": "Every Tuesday",
      "time": "7:30 pm – late",
      "classPrice": "£10",
      "socialPrice": "Free"
    },
    {
      "id": "rogue-mondays",
      "name": "Rogue Mondays",
      "venue": "Big Chill, Kings Cross",
      "day": "Mondays",
      "time": "7:30 pm – late",
      "classPrice": "£5",
      "socialPrice": "Free"
    }
  ],
  "upcomingEvents": [
    { "event": "Rogue Mondays at Big Chill Kings Cross", "date": "Monday, 23 February 2026", ... },
    { "event": "Café Sol Salsa Bachata Night", "date": "Tuesday, 17 February 2026", ... },
    { "event": "Rogue Resonance Workshop", "date": "January/February 2026", ... }
  ]
}
```

---

## CSS Variables & Brand Colors

```css
:root {
  --primary: #1a1a2e;
  --secondary: #16213e;
  --accent: #e94560;        /* Brand pink/red */
  --accent-light: #ff6b6b;
  --text: #eee;
  --text-muted: #aaa;
  --bg: #0f0f1a;            /* Dark background */
  --card-bg: rgba(255, 255, 255, 0.05);
  --border: rgba(255, 255, 255, 0.1);
}
```

---

## Important Rules & Constraints

### Privacy
- **Never show** the surname "Castellino" visibly
- Always use only "Oscar" or "Boadicea & Oscar"
- Contact email: voice@oscarcastellino.com (must be obfuscated with `atob()` or mailto)
- Check before every commit: `grep -ri "castellino" index.html data.json | grep -v "mailto:" | grep -v "voice@oscarcastellino" | grep -v "atob"`

### Links
- **Never use** `href="#"` — causes navigation issues
- Use `javascript:void(0)` with onclick, or point to actual targets
- All nav links should scroll to proper sections

### Content
- All static content lives in **data.json**
- Don't hardcode event names, dates, or offering text in HTML
- Update data.json → changes propagate site-wide via JS fetch

### YouTube Playlists
**These have been confused before — ALWAYS verify:**
- workshops = `PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ` (workshop footage)
- dances = `PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o` (social dancing)
- sensual = `PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9` (sensual clips)

### Couples Page
- sensual-couples.html must NOT show £ prices
- Only email contact buttons (mailto links with pre-filled subject)
- Pricing has been removed — don't re-add

---

## Pre-Commit Verification Checklist

**Always run before `git commit`:**

```bash
# 1. JSON validation
python3 -c "import json; json.load(open('data.json')); print('✅ JSON Valid')"

# 2. Privacy check
grep -ri "castellino" index.html data.json | grep -v "mailto:" | grep -v "voice@oscarcastellino" | grep -v "atob" && echo "❌ Privacy Issue" || echo "✅ OK"

# 3. YouTube playlists
python3 -c "
import json; d=json.load(open('data.json'))
p=d['youtubePlaylists']
assert p['workshops']['id']=='PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ'
assert p['dances']['id']=='PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o'
assert p['sensual']['id']=='PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9'
print('✅ Playlists OK')
"

# 4. No broken links
grep -rn 'href="#"' index.html && echo "❌ Found" || echo "✅ OK"
```

---

## Deployment Process

1. Make changes to HTML, CSS, JS, or data.json
2. Run pre-commit checks (see above)
3. Test locally with `python3 -m http.server 8000`
4. Commit and push:
   ```bash
   git add -A
   git commit -m "description of changes"
   git push origin main
   ```
5. Wait 1-2 minutes for GitHub Pages to deploy
6. Verify live at https://roguebachata.com

---

## Recent Git Commits

- `bd52c7f` – Rogue Resonance: featured video now portrait (vertical) format
- `8a592af` – Hero carousel: replace dots with sleek arrows, change Book to More
- `9936095` – Hero carousel: remove card box, fully transparent like original hero
- `8dd27c8` – Hero carousel with 5 cards, simplified AI checklist

---

## Next Steps for Maintenance

### Common Tasks
1. **Add a new event:** Update `data.json` → `upcomingEvents` array
2. **Update Rogue Parties info:** Edit `data.json` → `rogueParties` array
3. **Change button text:** Update `index.html` or data.json as needed
4. **Fix a typo:** Find in data.json or HTML, update, commit, push
5. **Add a new page:** Create HTML file, add nav link, follow same structure (fetch data.json)

### Monitoring
- Check live site regularly at https://roguebachata.com
- Monitor for broken links or missing images
- Verify event dates are current (move old to pastEvents)

### Common Issues & Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| Changes not showing live | CDN cache | Wait 2 min or push an empty `.nojekyll` file |
| Wrong YouTube video showing | Playlist ID swapped | Check all 3 IDs against rule list above |
| "Castellino" visible on page | Privacy breach | Search files, remove, commit immediately |
| Images not loading | Wrong path in data.json | Verify `images/` folder has file |
| Button doesn't navigate | `href="#"` used | Change to `javascript:void(0)` or real target |
| Mobile looks broken | CSS media query issue | Test at 375px, 768px, 1200px+ |

---

## Contact & Support

- **Owner:** Oscar (voice@oscarcastellino.com)
- **Repo Maintainer:** Check GitHub commit history for context
- **Live Site:** https://roguebachata.com
- **Rogue Instagram:** @roguebachata
- **Rogue WhatsApp:** +44 7596 031416

---

## File Locations & Quick Reference

```
project-root/
├── index.html                              # Main homepage
├── style.css                               # Global styles
├── data.json                               # All dynamic content
├── sensual-couples.html                    # Couples page
├── rogue-resonance.html                    # Workshops page
├── cafe-sol-event.html                     # Cafe Sol event page
├── images/                                 # All images
│   ├── RogueResonance.png
│   ├── RogueParty.jpg
│   ├── Boadicea and oscar Sensual Vibes.jpg
│   ├── Oscar Bo Dream.png
│   └── [other images]
├── videos/
│   └── sensual-couple.mp4
├── CNAME                                   # Domain routing
├── AI_WEBSITE_VERIFICATION_CHECKLIST.md   # Updated checklist
└── HANDOVER.md                             # This file
```

---

*Handover created: 18 February 2026*  
*For continued maintenance by: Claude Code or equivalent AI assistant*

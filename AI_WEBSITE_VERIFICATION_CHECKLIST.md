# 🔍 Rogue Bachata Website Verification Checklist

> **Purpose:** This checklist MUST be followed by any AI assistant or developer making changes to roguebachata.com. Run through this checklist after EVERY change to ensure the website is working correctly.

> **Live Site:** https://roguebachata.com  
> **Repository:** https://github.com/goodfornothin/test-rogue-plan  
> **Local Folder:** `/Users/admin/github/oscarcastellinowebsite/rogue-site` (via symlink)

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### 1. Local File Verification
Before pushing any changes, verify locally:

```bash
cd /Users/admin/github/oscarcastellinowebsite/rogue-site
```

- [ ] **Git status clean** - Run `git status` to check for uncommitted changes
- [ ] **No merge conflicts** - Ensure no conflict markers in files
- [ ] **JSON valid** - Run `python3 -c "import json; json.load(open('data.json'))"` to validate
- [ ] **HTML syntax** - Check index.html and other HTML files for unclosed tags

### 2. Local Testing
Start local server and test:

```bash
python3 -m http.server 8000
# Then visit http://localhost:8000
```

- [ ] **Site loads** without JavaScript errors (check browser console)
- [ ] **All images load** - No broken image icons
- [ ] **Navigation works** - All nav links scroll to correct sections
- [ ] **Mobile view** - Resize browser to test responsive layout

---

## 🚀 DEPLOYMENT CHECKLIST

### 3. Git Push Verification
```bash
git add -A
git commit -m "Description of changes"
git push origin main
```

- [ ] **Push successful** - No authentication or permission errors
- [ ] **GitHub Pages triggered** - Wait 1-2 minutes for deployment

### 4. Cache Busting
GitHub Pages and CDN caching can delay updates:

```bash
# Check if site updated (wait 60 seconds after push)
curl -sI "https://roguebachata.com" | grep "last-modified"
```

- [ ] **Last-modified date** matches your push time
- [ ] If stale, trigger rebuild with: `touch .nojekyll && git add . && git commit -m "Trigger rebuild" && git push`

---

## ✅ LIVE SITE VERIFICATION CHECKLIST

### 5. Homepage Hero Section
**URL:** https://roguebachata.com

```bash
curl -s "https://roguebachata.com" | grep -A5 "hero-content"
```

- [ ] **Title** shows "Rogue Bachata" (NOT "Oscar Castellino")
- [ ] **Tagline** shows "Movement · Connection · Freedom"
- [ ] **CTA Button** shows "Book a Class" and links to #events
- [ ] **Background image** loads (RogueResonance.png)

### 6. Navigation
- [ ] **Logo** links to top of page
- [ ] **About** link scrolls to #about section
- [ ] **Classes & Workshops** link scrolls to #offerings
- [ ] **Principles** link scrolls to #principles
- [ ] **Events** link scrolls to #events
- [ ] **Contact** link scrolls to #contact

### 7. Offerings Section (#offerings)
- [ ] **Section header** shows "Choose Your Path" with "Your Journey Starts Here" eyebrow
- [ ] **Rogue Resonance Workshops** card displays correctly
  - [ ] Tagline: "Advanced technique & artistry"
  - [ ] Image loads (RogueResonance.png)
  - [ ] Instructor: "Oscar" (NO surname)
  - [ ] Button: "Join a Workshop" links to #events
- [ ] **Rogue Bachata Classes** card displays correctly
  - [ ] Tagline: "Foundations for everyone"
  - [ ] Image loads (Boadicea and oscar Sensual Vibes.jpg)
  - [ ] Instructors: "Boadicea & Oscar" (NO surname)
  - [ ] Button: "Join a Class" links to #events
- [ ] **Dance Into Each Other** card displays correctly
  - [ ] Tagline: "Private sessions for couples"
  - [ ] Image loads (Oscar Bo Dream.png) - MUST be different from other offerings
  - [ ] Instructors: "Oscar & Boadicea" (NO surname)
  - [ ] Button: "Start Your Journey" links to #contact
- [ ] **All three cards use UNIQUE images** - no duplicates

### 8. Principles Section (#principles)
Verify all 6 principles display:
- [ ] Rogue Body, Bond, Beyond
- [ ] Rogue Legato
- [ ] Rogue Pause, Presence, Pivot
- [ ] Rogue Bounce and Roll
- [ ] Rogue Humility
- [ ] Rogue Lazy

### 9. Events Section (#events)

```bash
curl -s "https://roguebachata.com/data.json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Upcoming:', len(d['upcomingEvents']), 'Past:', len(d.get('pastEvents',[])))"
```

**For each UPCOMING event, verify:**
- [ ] **Date is correct** and in the future
- [ ] **Venue name** displays
- [ ] **Time** displays
- [ ] **Registration link** works (if applicable)
- [ ] **Image loads** with correct positioning

**For PAST events:**
- [ ] Events before today's date are in pastEvents array
- [ ] Past events show "COMPLETED" status
- [ ] Past events are visually muted/grayed

### 10. Current Event Details (Update as events change)
As of the last update, verify:

| Event | Expected Date | Venue |
|-------|---------------|-------|
| Cafe Sol Bachata Night | Tuesday, 17 February 2026 | Cafe Sol London, Clapham |
| Rogue Resonance Workshop | January/February 2026 | Create Destroy Studios, Archway |

```bash
# Quick check for Cafe Sol event date
curl -s "https://roguebachata.com/data.json" | grep -o '"date": "Tuesday, [0-9]* February 2026"' | head -1
```

### 11. Contact Section (#contact)
- [ ] **Email** displays as SVG image (for spam protection)
- [ ] **Email link** decodes to: `voice@oscarcastellino.com`
- [ ] **WhatsApp** link works: `https://wa.me/447596031416`
- [ ] **Instagram** link works: `https://www.instagram.com/roguebachata/`

### 12. Event Landing Pages
If event has a dedicated landing page:

**Cafe Sol Event Page:** https://roguebachata.com/cafe-sol-event.html
- [ ] Page loads correctly
- [ ] Date shows: Tuesday, 17 February 2026
- [ ] Venue: Cafe Sol London, 13-15 Clapham High Street, SW4 7TS
- [ ] Instagram: @cafesol_dos (NOT @cafesollondon)
- [ ] Class price: £10
- [ ] Social: FREE
- [ ] Google Maps link works
- [ ] Image loads with correct positioning (object-position: 0% 25%)

---

## 🔒 PRIVACY VERIFICATION (CRITICAL)

### 13. No Surname Leakage
The Rogue site must NOT contain "Castellino" anywhere visible:

```bash
curl -s "https://roguebachata.com" | grep -i "castellino" | grep -v "voice@oscarcastellino.com" | wc -l
# Should output: 0
```

- [ ] **No "Castellino"** appears in visible text (email address in mailto is OK)
- [ ] **No "Oscar Castellino"** - only "Oscar" or "Boadicea & Oscar"
- [ ] **Page title** is "Rogue Bachata" not "Oscar Castellino"

### 14. Separation from Oscar Site
- [ ] **CNAME** contains only `roguebachata.com` (not oscarcastellino.com)
- [ ] **No cross-links** to oscarcastellino.com

```bash
curl -s "https://roguebachata.com" | grep -i "oscarcastellino.com" | grep -v "mailto:" | wc -l
# Should output: 0
```

---

## 🖼️ IMAGE VERIFICATION

### 15. Image Loading & Positioning
Check all images load and are positioned correctly:

| Image | Expected Position | Usage |
|-------|-------------------|-------|
| RogueResonance.png | center 25% | Hero, Workshops offering |
| RogueParty.jpg | 0% 25% | Cafe Sol event |
| Boadicea and oscar Sensual Vibes.jpg | top | Classes offering |
| Oscar Bo Dream.png | center 30% | Dance Into Each Other offering |
| Oscar Bo Intense.png | center 25% | Alternative couples image |
| Oscar Bo close couple.png | center 20% | Alternative intimate shot |

Reference: See `images/image-metadata.json` for positioning details.

```bash
# Verify images exist on server
curl -sI "https://roguebachata.com/images/RogueResonance.png" | grep "200 OK"
curl -sI "https://roguebachata.com/images/RogueParty.jpg" | grep "200 OK"
curl -sI "https://roguebachata.com/images/Boadicea%20and%20oscar%20Sensual%20Vibes.jpg" | grep "200 OK"
curl -sI "https://roguebachata.com/images/Oscar%20Bo%20Dream.png" | grep "200 OK"
```

- [ ] All images return 200 OK
- [ ] No 404 errors in browser console

---

## 📱 RESPONSIVE DESIGN CHECK

### 16. Mobile Compatibility
Test at these viewport widths:
- [ ] **Desktop** (1200px+) - Full layout
- [ ] **Tablet** (768px) - Adjusted layout
- [ ] **Mobile** (375px) - Single column, readable text

Check:
- [ ] Navigation is accessible (hamburger menu if applicable)
- [ ] Text is readable without horizontal scrolling
- [ ] Buttons are tappable (min 44px touch target)
- [ ] Images scale appropriately

---

## 🔗 LINK VERIFICATION

### 17. External Links
Test all external links work:

```bash
# WhatsApp
curl -sI "https://wa.me/447596031416" | head -1

# Instagram
curl -sI "https://www.instagram.com/roguebachata/" | head -1
curl -sI "https://www.instagram.com/cafesol_dos/" | head -1

# Google Maps (Cafe Sol)
curl -sI "https://www.google.com/maps/search/?api=1&query=Cafe+Sol+13-15+Clapham+High+Street+London+SW4+7TS" | head -1
```

- [ ] All links return 200 or 301/302 (redirect OK)
- [ ] No 404 errors

---

## 📅 DATE VERIFICATION

### 18. Event Date Accuracy
Compare event dates against current date:

```bash
# Get current date
date "+%Y-%m-%d"

# Check upcoming events aren't in the past
curl -s "https://roguebachata.com/data.json" | python3 -c "
import json, sys
from datetime import datetime
data = json.load(sys.stdin)
today = datetime.now()
for e in data.get('upcomingEvents', []):
    print(f\"Upcoming: {e.get('date', 'NO DATE')} - {e.get('event', '')[:50]}\")
for e in data.get('pastEvents', []):
    print(f\"Past: {e.get('date', 'NO DATE')} - {e.get('event', '')[:50]}\")
"
```

- [ ] No past dates in upcomingEvents
- [ ] No future dates in pastEvents
- [ ] Dates are formatted consistently (e.g., "Tuesday, 17 February 2026")

---

## 🧹 CLEANUP VERIFICATION

### 19. No Debug/Test Content
- [ ] No "TODO" comments visible on page
- [ ] No "test" or "placeholder" text
- [ ] No lorem ipsum
- [ ] Console has no error messages

### 20. Files Not to Commit
Ensure these are NOT pushed to the repo:
- [ ] `.DS_Store` is in `.gitignore`
- [ ] No `.env` files with secrets
- [ ] `create_poster.py` and `RogueBachata_Poster.pdf` are local tools (OK to exclude)

---

## 📝 QUICK VERIFICATION COMMANDS

Copy-paste this block to run a quick verification:

```bash
echo "=== ROGUE BACHATA SITE VERIFICATION ==="
echo ""
echo "1. Checking site is live..."
curl -sI "https://roguebachata.com" | grep "HTTP/"

echo ""
echo "2. Checking hero button text..."
curl -s "https://roguebachata.com" | grep -o "Book a Class"

echo ""
echo "3. Checking privacy (no Castellino in visible text)..."
echo "Matches (should be 0):" $(curl -s "https://roguebachata.com" | grep -i "castellino" | grep -v "mailto:" | wc -l)

echo ""
echo "4. Checking Cafe Sol date..."
curl -s "https://roguebachata.com/data.json" | grep -o '"date": "Tuesday, [0-9]* February 2026"' | head -1

echo ""
echo "5. Checking images..."
for img in "RogueResonance.png" "RogueParty.jpg" "Boadicea%20and%20oscar%20Sensual%20Vibes.jpg"; do
  status=$(curl -sI "https://roguebachata.com/images/$img" | grep "HTTP/" | awk '{print $2}')
  echo "  $img: $status"
done

echo ""
echo "6. Last modified..."
curl -sI "https://roguebachata.com" | grep "last-modified"

echo ""
echo "=== VERIFICATION COMPLETE ==="
```

---

## 🚨 COMMON ISSUES & FIXES

| Issue | Cause | Fix |
|-------|-------|-----|
| Changes not showing | CDN cache | Wait 2 min, or push `.nojekyll` file |
| "Join a Workshop" in hero | Old index.html | Check hero section, should be "Book a Class" |
| Wrong date (18 Feb) | Old data.json | Update date to 17 February |
| @cafesollondon | Old data.json | Change to @cafesol_dos |
| "Oscar Castellino" visible | Privacy breach | Remove surname, keep only "Oscar" |
| Images not loading | Wrong path | Check path in data.json matches images/ folder |
| 404 on event page | File not pushed | `git add cafe-sol-event.html && git push` |

---

## 📞 CONTACT INFORMATION REFERENCE

| Platform | Handle/Number |
|----------|---------------|
| Website | roguebachata.com |
| Email | voice@oscarcastellino.com |
| WhatsApp | +44 7596 031416 |
| Instagram (Rogue) | @roguebachata |
| Instagram (Cafe Sol) | @cafesol_dos |

---

## 📁 FILE STRUCTURE REFERENCE

```
rogue-site/
├── index.html              # Main website
├── style.css               # Styles (brand colors defined here)
├── data.json               # All content data (events, offerings, principles)
├── cafe-sol-event.html     # Cafe Sol event landing page
├── CNAME                   # Domain: roguebachata.com
├── .nojekyll               # Prevents Jekyll processing
├── images/
│   ├── RogueResonance.png
│   ├── RogueParty.jpg
│   ├── Boadicea and oscar Sensual Vibes.jpg
│   ├── Oscar Bo Dream.png      # Couples offering image
│   ├── Oscar Bo Intense.png    # Alternative couples image
│   ├── Oscar Bo close couple.png
│   ├── email.svg           # Obfuscated email image
│   └── image-metadata.json # Image positioning info
├── create_poster.py        # Local tool for PDF posters
├── RogueBachata_Poster.pdf # Generated poster (local)
└── AI_WEBSITE_VERIFICATION_CHECKLIST.md  # THIS FILE
```

---

## 🎨 DESIGN & UX EXCELLENCE RULES

### 21. Visual Hierarchy & Consistency
- [ ] **Section headers** use consistent styling (eyebrow text + main title pattern)
- [ ] **No duplicate styling** between unrelated sections (e.g., offerings shouldn't look like principles)
- [ ] **Card layouts** have consistent padding, borders, and hover effects
- [ ] **Visual distinction** - each section should be clearly distinguishable

### 22. Image Quality & Uniqueness
- [ ] **Each offering uses a UNIQUE image** - no two offerings share the same photo
- [ ] **Images are high resolution** and not pixelated
- [ ] **object-position CSS** matches the image metadata for proper cropping
- [ ] **Image overlays** enhance readability without obscuring the subject

### 23. Typography Excellence
- [ ] **Taglines** are visually distinct from titles (smaller, uppercase, accent color)
- [ ] **Body text** has sufficient line-height (1.6-1.8 for readability)
- [ ] **Font sizes scale appropriately** on mobile
- [ ] **No orphaned words** at the end of important headings

### 24. Animation & Interaction Polish
- [ ] **Hover effects** are smooth (use ease or cubic-bezier, 0.3-0.6s duration)
- [ ] **Transitions** feel natural, not jarring
- [ ] **Interactive elements** have clear affordance (buttons look clickable)
- [ ] **No layout shifts** on hover that push other content

### 25. Color & Contrast
- [ ] **Text meets WCAG AA contrast** (4.5:1 for body text, 3:1 for large text)
- [ ] **Accent color (#e94560)** used sparingly for emphasis, not overwhelming
- [ ] **Gradients** flow naturally without harsh color stops
- [ ] **Dark backgrounds** don't cause eye strain (not pure #000000)

### 26. Content Quality
- [ ] **CTAs are action-oriented** ("Book a Class" not "Click Here")
- [ ] **Descriptions** are concise but informative
- [ ] **Taglines** communicate value quickly (good for ads)
- [ ] **No redundant information** between sections

### 27. Instagram-Ready Aesthetics
Since the site is used for Instagram ads:
- [ ] **Hero section** looks stunning when screenshotted
- [ ] **Offerings** are visually appealing enough to share
- [ ] **Brand consistency** across all visual elements
- [ ] **Images evoke emotion** (connection, passion, elegance)

### 28. World-Class Website Standards
- [ ] **First impression** is immediately professional and trustworthy
- [ ] **Loading performance** - site loads in under 3 seconds
- [ ] **No visual clutter** - whitespace used effectively
- [ ] **Modern design trends** without being dated
- [ ] **Emotional resonance** - design evokes the feeling of dance/connection

---

## 🔧 DATA.JSON SCHEMA RULES

### 29. Offerings Schema
Each offering in data.json MUST have:
```json
{
  "id": "unique-slug-format",
  "name": "Display Name",
  "tagline": "Short catchy phrase",    // REQUIRED for visual hierarchy
  "description": "Detailed description",
  "photo": "images/unique-image.jpg",   // MUST be unique per offering
  "buttonText": "Action Text",
  "buttonLink": "#section",
  "instructors": {
    "names": "Name(s)",                 // NO surnames on Rogue site
    "bio": "Brief bio",
    "photo": "images/photo.jpg",
    "email": "email@domain.com"
  }
}
```

- [ ] All offerings have unique `tagline` field
- [ ] All offerings have unique `photo` value
- [ ] Instructor names follow privacy rules (no "Castellino")

### 30. Events Schema
Events MUST include:
- [ ] `date` - Formatted as "Day, DD Month YYYY"
- [ ] `event` - Event name/title
- [ ] `venue` - Venue name
- [ ] `photo` - Event image path
- [ ] `instagram` - Venue Instagram (if applicable)

---

## ✅ SIGN-OFF

After completing all checks, record the verification:

```
Date: _______________
Verified by: AI Assistant / Developer Name
All checks passed: [ ] Yes  [ ] No (list issues below)

Issues found:
1. _______________
2. _______________

Actions taken:
1. _______________
2. _______________
```

---

*Last updated: 3 February 2026*
*Version: 1.0*

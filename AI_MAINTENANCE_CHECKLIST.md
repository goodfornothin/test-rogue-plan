# 💃 Rogue Bachata Website - AI Maintenance Checklist

> **Live URL:** https://roguebachata.com  
> **Repository:** https://github.com/goodfornothin/test-rogue-plan  
> **Last Updated:** February 2026

---

## 📁 Project Structure

```
test rogue plan/
├── index.html                              # Main homepage with video background
├── style.css                               # Main stylesheet (CSS variables)
├── data.json                               # ⭐ DYNAMIC CONTENT - All site data
├── rogue-resonance.html                    # Rogue Resonance workshops hub
├── rogue-resonance-camden-jan-2026.html    # Past workshop page
├── rogue-resonance-create-destroy-feb-2026.html  # Workshop landing page
├── cafe-sol-event.html                     # Café Sol event page
├── bachata-workshop.html                   # Generic workshop template
├── CNAME                                   # Custom domain (roguebachata.com)
├── .nojekyll                               # Disables Jekyll processing
├── README.md                               # Repository readme
├── rogue-bachata.code-workspace            # VS Code workspace file
├── images/                                 # All image assets
│   ├── RogueResonance.png                  # Main brand image
│   ├── Oscar Bo Dream.png                  # Couples image
│   ├── Boadicea and oscar Sensual Vibes.jpg
│   ├── RogueParty.jpg
│   └── [other images]
├── videos/                                 # Video assets
│   └── sensual couple.MOV                  # Background video (24MB)
├── CafeSol_Feb17_Poster.png               # Event poster
├── RogueBachata_Poster.pdf                # PDF poster
├── create_poster.py                        # Poster generation script
├── create_cafe_sol_poster.py              # Café Sol poster script
├── interviews.txt                          # Interview notes
└── AI_WEBSITE_VERIFICATION_CHECKLIST.md   # Previous checklist
```

---

## ⭐ DATA-DRIVEN ARCHITECTURE

This site uses **data.json** to manage all dynamic content. When you add or update content, **edit data.json** - the JavaScript will automatically render it!

### data.json Structure:

```json
{
  "siteName": "Rogue Bachata",
  "tagline": "Movement. Connection. Freedom.",
  "offerings": [...],           // Classes & workshops offered
  "principles": [...],          // Core dance principles
  "youtubePlaylists": {...},    // ⭐ YouTube playlists (auto-load videos!)
  "youtubeChannel": "...",      // Channel URL
  "backgroundVideo": {...},     // Hero background video config
  "upcomingEvents": [...],      // Future events
  "pastEvents": [...]           // Completed events
}
```

---

## 🎥 YouTube Integration

### Adding Videos - The Easy Way!
Videos are loaded **automatically from YouTube playlists**. Just add videos to these playlists on YouTube:

| Playlist | Purpose | Playlist ID |
|----------|---------|-------------|
| Bachata Workshops | Workshop footage | `PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o` |
| Bachata Dances | Social dancing | `PLLp_C8UrgAs9AuU4po1pGhsv_C_hPLmFQ` |
| Sensual Couple Dancing | Sensual clips | `PLLp_C8UrgAs9mqjnrYFtMaplehd0Nd_H9` |

**To add a new video:** Just upload to YouTube and add it to the appropriate playlist!

### Managing Playlists in data.json:
```json
"youtubePlaylists": {
  "workshops": {
    "id": "PLLp_C8UrgAs-gbpSm1938jmKrWolktE6o",
    "title": "Bachata Workshops",
    "description": "Rogue Resonance workshop sessions"
  },
  ...
}
```

---

## 🎬 Background Video

The site features a beautiful full-screen background video in the hero section.

### Video Location:
- **File:** `videos/sensual couple.MOV` (~24MB)
- **Fallback:** `images/Oscar Bo Dream.png`
- **Pages using it:** `index.html`, `rogue-resonance.html`

### Video Configuration in data.json:
```json
"backgroundVideo": {
  "src": "videos/sensual couple.MOV",
  "poster": "images/Oscar Bo Dream.png",
  "alt": "Sensual bachata dancing"
}
```

### To Replace the Video:
1. Add new video file to `videos/` folder
2. Update `backgroundVideo.src` in data.json
3. Optionally convert to MP4 for better browser compatibility

---

## 🎨 Design System

### CSS Variables (defined in style.css)
```css
:root {
  --primary: #1a1a2e;      /* Dark blue */
  --secondary: #16213e;    /* Darker blue */
  --accent: #e94560;       /* Coral/Pink */
  --bg: #0f0f1a;           /* Near black */
  --text: #eee;            /* Light text */
  --text-muted: #999;      /* Muted text */
  --card-bg: rgba(26, 26, 46, 0.8);
  --border: rgba(255, 255, 255, 0.1);
}
```

### Typography
- **Font:** Poppins (Google Fonts)
- **Weights:** 300 (light), 400 (regular), 600 (semi-bold), 700 (bold)
- **Headings:** Uppercase, letter-spacing: 0.1em

---

## 📄 Key Files Explained

### `index.html`
- **Purpose:** Main landing page
- **Features:** Video background, offerings cards, principles, video carousel, events
- **Dynamic content loaded from:** data.json

### `style.css`
- **Purpose:** Global styles with CSS variables
- **Contains:** All reusable component styles
- **Theme:** Dark mode with coral/pink accents

### `data.json`
- **Purpose:** Single source of truth for all content
- **Edit this to:** Add events, update offerings, manage playlists
- **Structure:** JSON object with named sections

### `rogue-resonance.html`
- **Purpose:** Hub for all Rogue Resonance workshops
- **Features:** Video background, workshop playlist, workshop cards
- **Dynamic content:** Filtered from data.json (offeringId = rogue-resonance-workshops)

---

## 🔧 Common Tasks

### Adding a New Event
Edit `data.json` → `upcomingEvents` array:
```json
{
  "event": "Event Name",
  "offeringId": "rogue-resonance-workshops", // or "rogue-bachata-classes"
  "eventId": "event-slug",
  "date": "Day, DD Month YYYY",
  "time": "X pm - Y pm",
  "venue": "Venue Name",
  "address": "Full Address",
  "description": "Event description...",
  "photo": "images/photo.jpg",
  "status": "upcoming",
  "registrationLink": "https://...",
  "landingPage": "event-page.html"  // optional
}
```

### Moving Event to Past
Move the event object from `upcomingEvents` to `pastEvents` array and change `"status": "past"`.

### Creating a Landing Page
1. Copy `rogue-resonance-create-destroy-feb-2026.html` as template
2. Update all content (title, dates, description)
3. Update `landingPage` in data.json to point to new file

### Updating Offerings
Edit `data.json` → `offerings` array. Each offering has:
- `id`, `name`, `tagline`, `description`
- `photo`, `buttonText`, `buttonLink`
- `instructors` object with names, bio, photo, email

---

## 🚀 Deployment

This site deploys automatically via **GitHub Pages**.

### To Deploy Changes:
```bash
cd "/Users/admin/github/test rogue plan"
git add .
git commit -m "Description of changes"
git push origin main
```

Changes appear live within 1-5 minutes at https://roguebachata.com

---

## 📋 Pre-Deployment Checklist

- [ ] data.json is valid JSON (no trailing commas, proper quotes)
- [ ] All image paths are correct
- [ ] Video file exists in videos/ folder
- [ ] Event dates are accurate
- [ ] YouTube playlist IDs are correct
- [ ] All links working
- [ ] Mobile responsive design checked
- [ ] Console has no errors
- [ ] Test video playback in hero section

---

## 🔗 Related Projects

| Project | Workspace File | Repository |
|---------|---------------|------------|
| This site | `rogue-bachata.code-workspace` | test-rogue-plan |
| **Oscar Castellino** | `oscarcastellino-website.code-workspace` | oscarcastellinowebsite |

**Note:** These are SEPARATE repositories with SEPARATE git histories. Do not try to combine them.

---

## 📁 Files That MUST Be Committed

**All files should be committed** except:
- `.DS_Store` (macOS system files)
- `node_modules/` (if any npm packages added)

The `videos/` folder with large video files **SHOULD be committed** for GitHub Codespaces access.

### Current .gitignore Should Only Contain:
```
.DS_Store
*.log
```

---

## ⚡ Quick Reference

| Task | Where to Edit |
|------|--------------|
| Add YouTube video | Upload to YouTube playlist |
| Add event | data.json → upcomingEvents |
| Change colors | style.css → :root variables |
| Update offerings | data.json → offerings |
| Add principles | data.json → principles |
| Change background video | videos/ folder + data.json |

---

## 📞 Technical Notes

- **Domain:** roguebachata.com (configured via CNAME)
- **Hosting:** GitHub Pages
- **SSL:** Automatic via GitHub Pages
- **Video Formats:** MOV (QuickTime), MP4 fallback supported

---

*This checklist is for AI assistants and developers maintaining the Rogue Bachata website. Keep it updated with any structural changes.*

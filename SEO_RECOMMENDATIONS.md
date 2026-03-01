# 10 Recommendations for SEO & AI Automation

## SEO Improvements:
1. **Blogging / Content Creation:** Create a `/blog/` or `/articles/` section where you post about topics like "What shoes to wear to a Bachata Party in London" or "Differences between Sensual and Dominican Bachata". This will massively boost organic search traffic for long-tail keywords. 
2. **Google Business Profile:** Create and optimize a "Google Business Profile" for "Rogue Bachata London". Even if you don't have a permanent studio, you can set it as a service area business. This is crucial for local SEO map packs when people search "Salsa classes near me".
3. **Internal Linking:** Systematically add hyperlinks within your own pages pointing to other pages using your target keywords as the anchor text (e.g., in the About section, hyperlinking "Bachata classes in London" directly to your class page).
4. **Image Alt-Text Audit:** Ensure every single image on the site has descriptive, keyword-rich `alt` text (e.g., "Beginners dancing at a Bachata party in London" instead of just "party image").
5. **Backlink Strategy:** Partner with local London event directories, dance blogs, or venues (like Big Chill and Cafe Sol) to get them to link back to `roguebachata.com`. Backlinks are the #1 signal to Google that your site is authoritative.

## Using AI Agents for Promotion & Updates:
6. **Automated Social Media Copywriting:** Use AI to generate Instagram captions, Facebook posts, and YouTube shorts descriptions based purely on your `data.json` file. 
7. **Social Media API Integration:** Set up Python scripts using the Instagram Graph API and Facebook Graph API. By providing local API keys, AI can execute scripts that automatically publish photos/videos and captions directly to your feeds without opening the apps.
8. **Automated Eventbrite / Fatsoma Management:** Expand existing Python scripts. When a new event is added to `data.json`, ask AI to "Sync upcoming events to Eventbrite," to run the API scripts and publish tickets automatically.
9. **Email Newsletter Generation:** Look at the `upcomingEvents` list to generate beautiful HTML email templates summarizing the week's classes and socials for newsletters.
10. **Data Scraping for Competitor Analysis:** Use AI to build scrapers that occasionally check other London dance school websites or Eventbrite pages to summarize pricing and new workshops, keeping you competitive.

## How to Connect APIs and Update Social Media Directly via CLI:
To do this securely, we need to:
1. Go to the Meta Developer Portal (for Instagram/Facebook) or X/Twitter Developer Portal and create an app to get **Access Tokens and API Keys**.
2. Save these keys in a local `.env` file in the repository (ensuring it is in `.gitignore` so it never gets pushed to GitHub).
3. We can then write Python scripts (e.g., `post_to_instagram.py`) that use those keys. 
4. Whenever you want to post, drop the photo in the `images` folder and run a prompt like: *"Post `images/new_flyer.jpg` to Instagram with a caption about Monday's class."* The AI will generate the caption, format the API request, and run the script locally to publish it directly to your account.
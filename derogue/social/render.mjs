// Renders social graphics to PNG.
//   python3 -m http.server 8765              (from the repo root, in another shell)
//   NODE_USE_ENV_PROXY=1 node derogue/social/render.mjs            -> templates.html, posts into derogue/social/
//   NODE_USE_ENV_PROXY=1 node derogue/social/render.mjs stories    -> stories.html, into derogue/social/stories/
//   NODE_USE_ENV_PROXY=1 node derogue/social/render.mjs carousels  -> carousels.html, into derogue/social/carousels/day-N/slide-M.jpg
// Google Fonts requests are fetched by Node so they follow the environment's proxy settings.
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";
const which = ["stories", "carousels"].includes(process.argv[2]) ? process.argv[2] : "templates";
const outDir = { stories: "derogue/social/stories", carousels: "derogue/social/carousels", templates: "derogue/social" }[which];
const selector = { stories: ".s", carousels: ".c", templates: ".card" }[which];
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2400, height: 2200 } });
await page.route(/fonts\.(googleapis|gstatic)\.com/, async (route) => {
  const res = await fetch(route.request().url(), { headers: { "user-agent": await page.evaluate(() => navigator.userAgent) } });
  await route.fulfill({ status: res.status, headers: { "content-type": res.headers.get("content-type") || "", "access-control-allow-origin": "*" }, body: Buffer.from(await res.arrayBuffer()) });
});
await page.goto(`http://localhost:8765/derogue/social/${which}.html`, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
// Stories are animated: show their settled end state in the still PNGs.
if (which === "stories") await page.evaluate(() => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = 7600; }));
console.log("fonts:", await page.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === "loaded").map(f => f.family))].join(", ")));
for (const id of await page.$$eval(selector, els => els.map(e => e.id))) {
  if (which === "carousels") {
    // Section ids look like "day-2-slide-3" -> carousels/day-2/slide-3.jpg
    const [, day, slide] = id.match(/^(day-\d+)-(slide-\d+)$/);
    mkdirSync(`${outDir}/${day}`, { recursive: true });
    await page.locator("#" + id).screenshot({ path: `${outDir}/${day}/${slide}.jpg`, type: "jpeg", quality: 95 });
  } else {
    await page.locator("#" + id).screenshot({ path: `${outDir}/${id}.png` });
  }
  console.log("wrote", id);
}
await browser.close();

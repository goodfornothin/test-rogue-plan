// Renders each .card in templates.html to a PNG in this folder.
//   python3 -m http.server 8765   (from this repo root, in another shell)
//   NODE_USE_ENV_PROXY=1 node social/render.mjs
// Google Fonts requests are fetched by Node so they follow the environment's proxy settings.
import { chromium } from "playwright";
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2400, height: 2200 } });
await page.route(/fonts\.(googleapis|gstatic)\.com/, async (route) => {
  const res = await fetch(route.request().url(), { headers: { "user-agent": await page.evaluate(() => navigator.userAgent) } });
  await route.fulfill({ status: res.status, headers: { "content-type": res.headers.get("content-type") || "", "access-control-allow-origin": "*" }, body: Buffer.from(await res.arrayBuffer()) });
});
await page.goto("http://localhost:8765/social/templates.html", { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
console.log("fonts:", await page.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === "loaded").map(f => f.family))].join(", ")));
for (const id of await page.$$eval(".card", els => els.map(e => e.id))) {
  await page.locator("#" + id).screenshot({ path: `social/${id}.png` });
  console.log("wrote", id);
}
await browser.close();

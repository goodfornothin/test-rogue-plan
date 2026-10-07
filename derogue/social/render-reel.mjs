// Renders a reel page (driven by window.renderAt(seconds)) to a 1080×1920, 30 fps MP4.
//   python3 -m http.server 8765        (from the repo root, in another shell)
//   FFMPEG=/path/to/ffmpeg NODE_USE_ENV_PROXY=1 node derogue/social/render-reel.mjs [page] [output]
// Defaults: derogue/social/reel-softness.html -> derogue/social/reels/softness-2026-10-07.mp4
// The output is greyscale with a true black background, for laying over video with a Screen blend.
import { chromium } from "playwright";
import { mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
const FPS = 30, ffmpeg = process.env.FFMPEG || "ffmpeg", WORKERS = 4;
const pagePath = process.argv[2] || "derogue/social/reel-softness.html";
const out = process.argv[3] || "derogue/social/reels/softness-2026-10-07.mp4";
const tmp = out.replace(/\.mp4$/, ".frames");
mkdirSync(tmp, { recursive: true });

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, async (route) => {
    const res = await fetch(route.request().url(), { headers: { "user-agent": await page.evaluate(() => navigator.userAgent) } });
    await route.fulfill({ status: res.status, headers: { "content-type": res.headers.get("content-type") || "", "access-control-allow-origin": "*" }, body: Buffer.from(await res.arrayBuffer()) });
  });
  await page.goto(`http://localhost:8765/${pagePath}?render`, { waitUntil: "networkidle" });
  return { page, duration: await page.evaluate(() => window.reelReady) };
}

// Split the frames between workers, one browser each (shared browsers can return stale frames).
const probe = await chromium.launch();
const { duration } = await openPage(probe);
await probe.close();
const total = Math.round(duration * FPS);
await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
  const browser = await chromium.launch();
  const { page } = await openPage(browser);
  for (let f = w; f < total; f += WORKERS) {
    await page.evaluate((t) => window.renderAt(t), f / FPS);
    await page.evaluate(() => new Promise((r) => { document.body.offsetHeight; requestAnimationFrame(() => requestAnimationFrame(r)); }));
    await page.screenshot({ path: `${tmp}/${String(f).padStart(4, "0")}.png` });
  }
  await browser.close();
}));
execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", `${tmp}/%04d.png`,
  "-vf", "format=gray,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-movflags", "+faststart", out]);
rmSync(tmp, { recursive: true, force: true });
console.log("wrote", out, `(${duration}s, ${total} frames)`);

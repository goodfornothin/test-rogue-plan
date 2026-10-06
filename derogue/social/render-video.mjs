// Renders each story in stories.html to an 8-second 1080×1920 MP4 for Instagram.
//   python3 -m http.server 8765        (from the repo root, in another shell)
//   FFMPEG=/path/to/ffmpeg NODE_USE_ENV_PROXY=1 node derogue/social/render-video.mjs [story-id ...]
// Animations are paused and seeked frame by frame, so the output is smooth whatever the machine speed.
// Output is converted to greyscale so the videos stay strictly black and white.
import { chromium } from "playwright";
import { mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
const FPS = 30, ffmpeg = process.env.FFMPEG || "ffmpeg", outDir = "derogue/social/stories/video", tmp = "derogue/social/stories/.frames";
mkdirSync(outDir, { recursive: true });
// One browser per worker: pages sharing a browser in the background can hand back stale frames.
async function openPage(browser, id) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, async (route) => {
    const res = await fetch(route.request().url(), { headers: { "user-agent": await page.evaluate(() => navigator.userAgent) } });
    await route.fulfill({ status: res.status, headers: { "content-type": res.headers.get("content-type") || "", "access-control-allow-origin": "*" }, body: Buffer.from(await res.arrayBuffer()) });
  });
  await page.goto("http://localhost:8765/derogue/social/stories.html?render", { waitUntil: "networkidle" });
  await page.addStyleTag({ content: `body{padding:0!important;gap:0!important} .s:not(#${id}){display:none!important}` });
  await page.evaluate(() => document.fonts.ready);
  return page;
}
async function renderStory(browser, id) {
  const page = await openPage(browser, id);
  const dir = `${tmp}/${id}`; mkdirSync(dir, { recursive: true });
  const total = await page.evaluate(() => window.storyDuration);
  const frames = Math.round((total / 1000) * FPS);
  for (let f = 0; f < frames; f++) {
    await page.evaluate((t) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = t; }), (f * 1000) / FPS);
    await page.evaluate(() => new Promise((r) => { document.body.offsetHeight; requestAnimationFrame(() => requestAnimationFrame(r)); }));
    await page.screenshot({ path: `${dir}/${String(f).padStart(4, "0")}.jpg`, type: "jpeg", quality: 94 });
  }
  await page.close();
  execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", `${dir}/%04d.jpg`,
    "-vf", "format=gray,format=yuv420p", "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-movflags", "+faststart", `${outDir}/${id}.mp4`]);
  rmSync(dir, { recursive: true, force: true });
  console.log("wrote", id);
}
const probeBrowser = await chromium.launch();
const probe = await openPage(probeBrowser, "none");
const ids = process.argv.slice(2).length ? process.argv.slice(2) : await probe.$$eval(".s", (els) => els.map((e) => e.id));
await probeBrowser.close();
const queue = [...ids];
await Promise.all(Array.from({ length: 4 }, async () => {
  const browser = await chromium.launch();
  while (queue.length) await renderStory(browser, queue.shift());
  await browser.close();
}));
rmSync(tmp, { recursive: true, force: true });

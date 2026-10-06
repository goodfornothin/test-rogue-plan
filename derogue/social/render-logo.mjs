// Renders the logo animations in logo-animations.html to MP4 (square 1080×1080 and story 1080×1920),
// plus a PNG of each final frame.
//   python3 -m http.server 8765        (from the repo root, in another shell)
//   FFMPEG=/path/to/ffmpeg NODE_USE_ENV_PROXY=1 node derogue/social/render-logo.mjs
import { chromium } from "playwright";
import { mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
const FPS = 30, ffmpeg = process.env.FFMPEG || "ffmpeg";
const outDir = "derogue/social/logo-animations", tmp = `${outDir}/.frames`;
const anims = ["legato", "two-bodies", "breath", "ground-listen-release"];
const formats = { square: [1080, 1080], story: [1080, 1920] };
mkdirSync(outDir, { recursive: true });

async function render(browser, a, fmt) {
  const [width, height] = formats[fmt];
  const page = await browser.newPage({ viewport: { width, height } });
  await page.route(/fonts\.(googleapis|gstatic)\.com/, async (route) => {
    const res = await fetch(route.request().url(), { headers: { "user-agent": await page.evaluate(() => navigator.userAgent) } });
    await route.fulfill({ status: res.status, headers: { "content-type": res.headers.get("content-type") || "", "access-control-allow-origin": "*" }, body: Buffer.from(await res.arrayBuffer()) });
  });
  await page.goto(`http://localhost:8765/derogue/social/logo-animations.html?render&a=${a}`, { waitUntil: "networkidle" });
  const total = await page.evaluate(() => window.animReady);
  const name = `${a}-${fmt}`, dir = `${tmp}/${name}`;
  mkdirSync(dir, { recursive: true });
  const frames = Math.round((total / 1000) * FPS);
  for (let f = 0; f < frames; f++) {
    await page.evaluate((t) => document.getAnimations().forEach((x) => { x.pause(); x.currentTime = t; }), (f * 1000) / FPS);
    await page.evaluate(() => new Promise((r) => { document.body.offsetHeight; requestAnimationFrame(() => requestAnimationFrame(r)); }));
    await page.screenshot({ path: `${dir}/${String(f).padStart(4, "0")}.jpg`, type: "jpeg", quality: 95 });
  }
  await page.screenshot({ path: `${outDir}/${name}.png` });
  await page.close();
  // format=gray then yuv420p keeps the video strictly black and white.
  execFileSync(ffmpeg, ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", `${dir}/%04d.jpg`,
    "-vf", "format=gray,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-movflags", "+faststart", `${outDir}/${name}.mp4`]);
  rmSync(dir, { recursive: true, force: true });
  console.log("wrote", name);
}

const only = process.argv.slice(2);
const queue = anims.filter((a) => !only.length || only.includes(a)).flatMap((a) => Object.keys(formats).map((f) => [a, f]));
// One browser per worker: pages sharing a browser in the background can hand back stale frames.
await Promise.all(Array.from({ length: 4 }, async () => {
  const browser = await chromium.launch();
  while (queue.length) await render(browser, ...queue.shift());
  await browser.close();
}));
rmSync(tmp, { recursive: true, force: true });

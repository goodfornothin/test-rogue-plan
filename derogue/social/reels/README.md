# deRogue reels

## softness-2026-10-07.mp4
30 s, 1080×1920, 30 fps. Workshop reel for Wed 7 Oct 2026: "Cherish the connection" and
Find · Embrace · Unfold (tracking and collection). Caption: `softness-2026-10-07-caption.txt`.

The background is true black and everything else is white, made to sit over video:
put this clip on the layer above your footage and set its blend mode to **Screen** (or Lighten).
The black disappears and your video shows through the white text and graphics.
Text stays inside the Reels safe area (away from the bottom caption and the right-hand buttons),
and the first frame already shows the opening line.

Source: `../reel-softness.html` (open it in a browser to preview the loop).
Re-render (with `python3 -m http.server 8765` running at the repo root):

    FFMPEG=/path/to/ffmpeg NODE_USE_ENV_PROXY=1 node derogue/social/render-reel.mjs

# deRogue logo animations

Four black-and-white animations of the logo with its name and tagline. Each comes in
square (`-square`, 1080×1080) and story (`-story`, 1080×1920) format, 30 fps, with a PNG of the final frame.

| File | Length | Idea |
|------|--------|------|
| legato-* | 9 s | The figures draw themselves in one continuous line, then the name is written in |
| two-bodies-* | 9 s | Two ghost figures drift together along one axis: two bodies, one centre, one axis |
| breath-* | 9 s | Axis, centre dot, three breath ripples; the solid figures open out from the centre |
| ground-listen-release-* | 10 s | "Ground. Listen. Release." one word at a time, then the logo comes into focus |

Source: `../logo-animations.html` (pick one with `?a=legato`, `two-bodies`, `breath`, `ground-listen-release`).
The self-drawing line uses `../../assets/final/derogue-mark-outline-paths.svg`, traced from the final logo.

Re-render (with `python3 -m http.server 8765` running at the repo root):

    FFMPEG=/path/to/ffmpeg NODE_USE_ENV_PROXY=1 node derogue/social/render-logo.mjs [animation ...]

# deRogue Instagram carousels

Four carousels, one per day, 4 slides each (1080×1350 JPG, 4:5, true black and white).
They follow the 16 stories:

| Day | Slides | Theme |
|-----|--------|-------|
| 1 | day-1/slide-1…4 | The idea + finding your axis (alone, then with a partner) |
| 2 | day-2/slide-1…4 | Improve your bachata: principles I–III |
| 3 | day-3/slide-1…4 | Principles IV–VI + myth vs truth |
| 4 | day-4/slide-1…4 | Who starts the movement? + the Wednesday workshop at derogue.art |

Each folder has `caption.txt` with the post caption and hashtags.

To re-render after editing `../carousels.html` (with `python3 -m http.server 8765` running at the repo root):

    NODE_USE_ENV_PROXY=1 node derogue/social/render.mjs carousels
    python3 derogue/social/carousels-grayscale.py

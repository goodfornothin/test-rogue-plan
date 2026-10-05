"""Force every carousel slide to true black and white.

JPEG compression adds faint colour fringes around text. This re-encodes each
slide from a single grey channel so red, green and blue are identical.
Run after: NODE_USE_ENV_PROXY=1 node derogue/social/render.mjs carousels
"""
import glob
from PIL import Image

for path in sorted(glob.glob("derogue/social/carousels/day-*/slide-*.jpg")):
    grey = Image.open(path).convert("L")
    grey.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    print("greyscale", path)

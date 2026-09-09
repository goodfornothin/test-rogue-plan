#!/usr/bin/env python3
"""1200x630 Open Graph card: Change of venue / Coffee Origin tonight."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1200, 630
SRC = "images/coffee-origin-shopfront.jpg"
OUT = "images/coffee-origin-change-of-venue-og.jpg"

SERIF = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SANS = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
SANS_MED = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"

GOLD = (245, 201, 122)
WHITE = (255, 255, 255)
CREAM = (255, 248, 240)


def cover_crop(im, w, h):
    src_w, src_h = im.size
    scale = max(w / src_w, h / src_h)
    nw, nh = int(src_w * scale), int(src_h * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    # Bias toward the awning (upper third of the shopfront).
    left = (nw - w) // 2
    top = max(0, int((nh - h) * 0.18))
    return im.crop((left, top, left + w, top + h))


def main():
    photo = cover_crop(Image.open(SRC).convert("RGB"), W, H)
    photo = ImageEnhance.Contrast(photo).enhance(1.08)
    photo = ImageEnhance.Color(photo).enhance(1.05)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Darken the lower half so type stays readable on any crop.
    for y in range(H):
        t = (y - 210) / (H - 210)
        if t < 0:
            a = 28
        else:
            a = int(28 + min(1.0, t) * 200)
        d.line([(0, y), (W, y)], fill=(16, 42, 34, a))

    # Solid band behind the headline block
    d.rectangle([0, 300, W, H], fill=(16, 42, 34, 218))
    d.rectangle([0, 300, W, 308], fill=GOLD + (255,))

    card = photo.convert("RGBA")
    card = Image.alpha_composite(card, overlay)
    draw = ImageDraw.Draw(card)

    kicker = ImageFont.truetype(SANS, 36)
    headline = ImageFont.truetype(SERIF, 58)
    sub = ImageFont.truetype(SANS_MED, 30)
    brand = ImageFont.truetype(SANS, 22)

    pad = 52
    draw.text((pad, 22), "ROGUE BACHATA  ·  WEDNESDAY 9 SEPTEMBER", font=brand, fill=GOLD)

    y = 340
    draw.text((pad, y), "CHANGE OF VENUE", font=kicker, fill=GOLD)
    y += 48
    draw.text((pad, y), "Tonight: Coffee Origin,", font=headline, fill=WHITE)
    y += 68
    draw.text((pad, y), "Blackstock Road", font=headline, fill=WHITE)
    y += 70
    draw.text(
        (pad, y),
        "225 Blackstock Road, London N5 2LL  ·  7:30pm  ·  tonight only",
        font=sub,
        fill=CREAM,
    )

    out = card.convert("RGB")
    out.save(OUT, "JPEG", quality=90, optimize=True, progressive=True)
    print("wrote", OUT, out.size)


if __name__ == "__main__":
    main()

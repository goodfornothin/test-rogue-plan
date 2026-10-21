#!/usr/bin/env python3
"""
Café Sol yellow neon logo — a seamless 60s sparkling loop on pure black.

Drop it on top of a video with a Screen / Lighten / Add blend mode: the black disappears.
Everything moving is periodic with a period that divides 60s, so frame 1800 == frame 0.

  - the sun's line-art rendered as warm yellow neon tubes with white-hot cores
  - a bright wave chasing round the rays, a slow solar corona turning behind the sun
  - CAFÉ SOL letters light up in sequence every 15s, with the odd neon flicker
  - star sparkles popping on the tubes, glitter dust orbiting, a shine sweep every 12s

Usage:
  python3 render_cafe_sol_neon.py                     # render the 60s MP4
  python3 render_cafe_sol_neon.py --preview 0 7.5     # PNG stills at given seconds
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cv2
import numpy as np

W, H, FPS, DUR = 1080, 1920, 30, 60.0
N = int(FPS * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "images", "cafe-sol-logo.jpg")
OUT = os.path.join(HERE, "CafeSol_Logo_Neon_Loop_1080x1920_60s_black.mp4")

TAU = 2 * math.pi
YELLOW = np.array([1.0, 0.78, 0.05], np.float32)
WHITE = np.array([1.0, 1.0, 1.0], np.float32)
# one yellow throughout; highlights are the same yellow pushed hotter, not white or orange
HOT = YELLOW * 0.85 + WHITE * 0.15

cv2.setNumThreads(1)


def smoothstep(e0, e1, x):
    x = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def blur(img, sigma):
    return cv2.GaussianBlur(img, (0, 0), sigma)


def glow_q(img, layers):
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    acc = np.zeros_like(small)
    for sigma, weight in layers:
        acc += weight * blur(small, sigma / 4.0)
    return cv2.resize(acc, (W, H), interpolation=cv2.INTER_LINEAR)


def tonemap(x, exposure=1.0):
    return 1.0 - np.exp(-exposure * np.maximum(x, 0.0))


_DITHER = np.random.default_rng(7).random((H, W, 3), dtype=np.float32) - 0.5


def to_bytes(img, i):
    """Float RGB -> uint8, dithering lit pixels only so the background stays exactly 0,0,0."""
    v = img * 257.0 - 2.0  # drop the faint far tail of the wide glow to true black
    d = np.roll(_DITHER, (i * 37) % H, axis=0)
    v = v + d * np.clip(v * 0.5, 0.0, 1.0)
    v[v < 0.5] = 0.0
    return np.clip(v + 0.5, 0, 255).astype(np.uint8).tobytes()


# ----------------------------------------------------------------------------- logo
LOGO_W = 900
PAD = 60
# letters in the source image (214x235 px). Most are separate blobs; É and S touch rays,
# so they are cut out with boxes.  (x0, y0, x1, y1) in source pixels, in reading order.
LETTER_BOXES = [
    (8, 66, 36, 96),     # C
    (28, 46, 54, 74),    # A
    (50, 24, 73, 54),    # F
    (79, 7, 105, 40),    # É (with accent)
    (133, 19, 161, 49),  # S
    (158, 38, 186, 64),  # O
    (178, 58, 204, 90),  # L
]
SUN_C_SRC = (107.5, 117.8)  # centre of the face disc in source pixels


def load_logo():
    src = cv2.imread(LOGO).astype(np.float32)
    b, g, r = src[..., 0], src[..., 1], src[..., 2]
    yel = (np.minimum(r, g) - b) * smoothstep(110, 170, r)  # yellow ink only, no shadow
    ink = yel > 70
    ys, xs = np.nonzero(ink)
    x0, x1, y0, y1 = xs.min() - 3, xs.max() + 4, ys.min() - 3, ys.max() + 4
    scale = LOGO_W / (x1 - x0)
    tw, th = LOGO_W, int(round((y1 - y0) * scale))

    # source label map: 1..7 letters, 8 sun (rays + ring), 9 face features
    lab = np.zeros(ink.shape, np.int32)
    n, comp, stats, cent = cv2.connectedComponentsWithStats(ink.astype(np.uint8), connectivity=8)
    sun_comp = 1 + np.argmax(stats[1:, 4])
    cx, cy = SUN_C_SRC
    for k in range(1, n):
        d = math.hypot(cent[k][0] - cx, cent[k][1] - cy)
        if k == sun_comp:
            lab[comp == k] = 8
        elif d < 34:
            lab[comp == k] = 9
        else:
            lab[comp == k] = 8
    for li, (bx0, by0, bx1, by1) in enumerate(LETTER_BOXES, start=1):
        box = np.zeros_like(ink)
        box[by0:by1, bx0:bx1] = True
        lab[box & ink] = li
    # every non-ink source pixel takes the label of its nearest ink pixel
    _, nearest = cv2.distanceTransformWithLabels((~ink).astype(np.uint8), cv2.DIST_L2, 5,
                                                 labelType=cv2.DIST_LABEL_PIXEL)
    ink_labels = np.concatenate([[0], lab[ink]])  # pixel labels are in raster order of ink pixels
    lab_full = ink_labels[nearest]

    # supersampled smooth mask
    S = 2
    crop = yel[y0:y1, x0:x1]
    up = cv2.resize(crop, (tw * S, th * S), interpolation=cv2.INTER_CUBIC)
    up = smoothstep(66, 112, blur(up, 0.7 * scale * S))
    mask = cv2.resize(up, (tw, th), interpolation=cv2.INTER_AREA)
    binm = np.pad(up > 0.5, PAD * S)
    din = cv2.distanceTransform(binm.astype(np.uint8), cv2.DIST_L2, 5)
    dout = cv2.distanceTransform((~binm).astype(np.uint8), cv2.DIST_L2, 5)
    sd = cv2.resize((dout - din) / S, (tw + 2 * PAD, th + 2 * PAD), interpolation=cv2.INTER_AREA)
    labels = cv2.resize(lab_full[y0:y1, x0:x1].astype(np.float32), (tw, th),
                        interpolation=cv2.INTER_NEAREST).astype(np.int32)
    mask, labels = np.pad(mask, PAD), np.pad(labels, PAD)
    sun_c = ((cx - x0) * scale + PAD, (cy - y0) * scale + PAD)
    return mask.astype(np.float32), sd.astype(np.float32), labels, sun_c, scale


MASK, SD, LABELS, (SCX, SCY), SCALE = load_logo()
RH, RW = MASK.shape
RX0, RY0 = (W - RW) // 2, (H - RH) // 2
FCX, FCY = SCX + RX0, SCY + RY0  # sun centre in frame coords
RY, RX = np.mgrid[0:RH, 0:RW].astype(np.float32)
FX, FY = RX + RX0, RY + RY0
THETA = np.arctan2(RY - SCY, RX - SCX)
RAD = np.hypot(RX - SCX, RY - SCY)
# neon tube shading: slim the strokes a touch, then make each one hottest along its centre line
TUBE = smoothstep(0.7, -0.7, SD + 2.0)
_din = np.maximum(-SD - 2.0, 0).astype(np.float32)
_hw = np.maximum(cv2.dilate(_din, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))), 1.0)
_p = blur(np.clip(_din / _hw, 0, 1), 1.5)
BODY = TUBE * (0.5 + 0.5 * _p)
CORE = blur(TUBE * smoothstep(0.5, 0.95, _p), 1.0)
SUN = (LABELS == 8).astype(np.float32)
FACE = (LABELS == 9).astype(np.float32)
LETTERS = [(LABELS == k).astype(np.float32) for k in range(1, 8)]
TEXT = sum(LETTERS)
RAYS = SUN * smoothstep(34 * SCALE, 44 * SCALE, RAD)


def place(roi):
    full = np.zeros((H, W) + roi.shape[2:], np.float32)
    x0, y0 = max(RX0, 0), max(RY0, 0)
    x1, y1 = min(RX0 + RW, W), min(RY0 + RH, H)
    full[y0:y1, x0:x1] = roi[y0 - RY0:y1 - RY0, x0 - RX0:x1 - RX0]
    return full


# ----------------------------------------------------------------------------- sparkles
def star_sprite(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32)
    d = np.hypot(x, y)
    arm = lambda a, b, L, w: np.exp(-(b / w) ** 2) * np.clip(1 - np.abs(a) / L, 0, 1) ** 2.5
    u, v = (x + y) / math.sqrt(2), (x - y) / math.sqrt(2)
    s = arm(x, y, r, 1.3) + arm(y, x, r, 1.3)
    s += 0.45 * (arm(u, v, r * 0.45, 1.1) + arm(v, u, r * 0.45, 1.1))
    s += np.exp(-(d / (0.07 * r + 1.2)) ** 2) * 1.6 + np.exp(-(d / (0.22 * r)) ** 2) * 0.35
    return s.astype(np.float32)


SPRITES = {r: star_sprite(r) for r in (40, 58, 84, 110, 150)}
_rng = np.random.default_rng(21)
_tube_px = np.argwhere(CORE > 0.6)  # (y, x) on the neon lines
_on_rays = (CORE > 0.6) & (RAYS > 0.5) & (MASK > 0.5)
_tips = np.argwhere(_on_rays & (RAD > RAD[_on_rays].max() * 0.8))
SPARKS = []  # (start s, life s, sprite radius, y, x, brightness, spin)
for _ in range(250):
    y, x = _tube_px[_rng.integers(len(_tube_px))]
    r = int(_rng.choice([40, 40, 58, 58, 84, 110]))
    SPARKS.append((_rng.uniform(0, DUR), _rng.uniform(0.45, 0.95), r, int(y), int(x), _rng.uniform(0.6, 1.0),
                   _rng.uniform(-0.6, 0.6)))
for k in range(16):  # hero sparkles on ray tips, one every 3.75s
    y, x = _tips[_rng.integers(len(_tips))]
    SPARKS.append((k * 3.75 + 1.1, 1.1, 150, int(y), int(x), 1.0, _rng.uniform(-0.5, 0.5)))


def render_sparkles(t):
    canvas = np.zeros((RH, RW), np.float32)
    for s0, life, r, y, x, bri, spin in SPARKS:
        u = ((t - s0) % DUR) / life
        if u >= 1.0:
            continue
        env = math.sin(math.pi * u) ** 2
        spr = SPRITES[r]
        M = cv2.getRotationMatrix2D((r, r), math.degrees(spin * u), 0.45 + 0.55 * env)
        spr = cv2.warpAffine(spr, M, spr.shape[::-1])
        y0, x0 = y - r, x - r
        ys0, xs0 = max(y0, 0), max(x0, 0)
        ys1, xs1 = min(y0 + 2 * r + 1, RH), min(x0 + 2 * r + 1, RW)
        canvas[ys0:ys1, xs0:xs1] += spr[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0] * (env * bri)
    return canvas


# glitter dust orbiting the sun
NP = 140
P_R = _rng.uniform(260, 640, NP)
P_PH = _rng.uniform(0, 1, NP)
P_LAPS = _rng.choice([1, 1, 2, -1, -1], NP)
P_WOB = _rng.uniform(5, 30, NP)
P_WF = _rng.integers(3, 11, NP)
P_TW = _rng.integers(20, 75, NP)
P_BRI = _rng.uniform(0.3, 1.0, NP)
P_COL = _rng.choice([0, 1, 2], NP, p=[0.5, 0.3, 0.2])
P_COLORS = [YELLOW, HOT, YELLOW]


def render_dust(t):
    layers = [np.zeros((H, W), np.float32) for _ in range(3)]
    a = TAU * (P_PH + P_LAPS * t / DUR)
    rr = P_R + P_WOB * np.sin(TAU * (P_WF * t / DUR + P_PH))
    x = FCX + rr * np.cos(a)
    y = FCY + rr * np.sin(a) * 1.1
    tw = (0.5 + 0.5 * np.sin(TAU * (P_TW * t / DUR + P_PH))) ** 4
    for k in range(NP):
        b = P_BRI[k] * tw[k]
        xi, yi = int(round(x[k])), int(round(y[k]))
        if b < 0.02 or not (1 <= xi < W - 1 and 1 <= yi < H - 1):
            continue
        L = layers[P_COL[k]]
        L[yi, xi] += b * 2.5
        L[yi - 1:yi + 2, xi - 1:xi + 2] += b * 0.5
    out = np.zeros((H, W, 3), np.float32)
    for L, c in zip(layers, P_COLORS):
        out += blur(L, 0.9)[..., None] * c
    return out


# solar corona behind the sun (quarter res)
QW, QH = W // 4, H // 4
_qy, _qx = np.mgrid[0:QH, 0:QW].astype(np.float32)
Q_TH = np.arctan2(_qy - FCY / 4, _qx - FCX / 4)
Q_R = np.hypot(_qx - FCX / 4, _qy - FCY / 4) * 4
Q_RADIAL = smoothstep(150, 300, Q_R) * np.exp(-np.maximum(Q_R - 300, 0) / 200)
BEHIND = 1 - place(blur(cv2.dilate(MASK, np.ones((7, 7), np.uint8)), 3)) * 0.95

FLICKERS = [(9.5, 0.6, (6,)), (27.3, 0.5, (1,)), (44.6, 0.9, (4, 5, 6)), (52.1, 0.45, (0,))]


def letter_levels(t, i):
    lv = np.ones(7)
    for e, (s, d, letters) in enumerate(FLICKERS):
        if s <= t < s + d:
            r = np.random.default_rng(900 * e + i).random()
            v = 1.0 if (t - s) / d > 0.85 else (0.08 if r < 0.5 else (1.2 if r > 0.85 else 0.45))
            for k in letters:
                lv[k] = v
    return lv


def frame(i):
    t = i / FPS
    breathe = 0.93 + 0.07 * math.sin(TAU * t / 6.0)
    buzz = 1.0 + 0.015 * math.sin(TAU * t * 37.0) * math.sin(TAU * t * 5.0)

    # chase wave round the rays (one lap every 5s) + softer counter wave
    chase = (0.5 + 0.5 * np.cos(THETA - TAU * t / 5.0)) ** 4
    chase2 = (0.5 + 0.5 * np.cos(2 * THETA + TAU * t / 7.5)) ** 6
    sun_lv = SUN * (0.78 + 0.55 * chase * RAYS + 0.2 * chase2 * RAYS)

    # marquee: letters light up C -> L every 15s
    tm = t % 15.0
    lv = letter_levels(t, i)
    txt_lv = np.zeros_like(MASK)
    txt_flash = np.zeros_like(MASK)
    for k, L in enumerate(LETTERS):
        boost = math.exp(-((tm - 0.4 - 0.16 * k) / 0.13) ** 2)
        txt_lv += L * lv[k]
        txt_flash += L * (boost * lv[k])

    face_lv = FACE * (0.95 + 0.12 * math.sin(TAU * t / 4.0))
    level = (sun_lv + txt_lv + face_lv) * breathe * buzz
    E = YELLOW * (BODY * level * 1.15)[..., None]
    E += HOT * (CORE * level * 0.75)[..., None]
    E += HOT * ((txt_flash * (BODY * 0.6 + CORE * 0.6)) * breathe)[..., None]

    # shine sweep every 12s
    u = (t % 12.0) / 1.5
    if u < 1.0:
        pos = -700 + u * 2600
        band = np.exp(-(((FX * 0.8 + FY * 0.6) - (pos + FCY * 0.6)) / 40.0) ** 2)
        E += HOT * (band * (BODY * 0.7 + CORE * 0.5))[..., None]

    spark = render_sparkles(t)
    E += (HOT * 1.6 + WHITE * 0.25) * spark[..., None]

    full = place(E)
    full += blur(full, 3.0) * 0.45
    full += glow_q(full, [(14, 0.7), (42, 0.4)])
    warm = glow_q(full, [(120, 0.15)]).mean(axis=2, keepdims=True)
    full += warm * YELLOW

    # corona + dust behind / around
    spin = TAU * t / 30.0
    beams = (0.5 + 0.5 * np.cos(16 * Q_TH + spin)) ** 6 + 0.6 * (0.5 + 0.5 * np.cos(9 * Q_TH - spin * 2)) ** 8
    pulse = 0.85 + 0.15 * math.sin(TAU * t / 6.0)
    corona = cv2.resize((beams * Q_RADIAL * 0.09 * pulse).astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    full += (corona * BEHIND)[..., None] * YELLOW
    full += render_dust(t) * BEHIND[..., None]
    return tonemap(full, 1.25)


def _work(i):
    return to_bytes(frame(i), i)


def render():
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-level", "4.2",
        "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-color_range", "tv", "-movflags", "+faststart", "-tag:v", "avc1", OUT,
    ]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, buf in enumerate(pool.imap(_work, range(N), chunksize=6)):
            ff.stdin.write(buf)
            if k % 300 == 0:
                print(f"frame {k}/{N}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", OUT)


def preview(seconds):
    out_dir = os.environ.get("PREVIEW_DIR", os.path.join(HERE, "_preview"))
    os.makedirs(out_dir, exist_ok=True)
    for s in seconds:
        i = int(round(s * FPS)) % N
        img = np.frombuffer(to_bytes(frame(i), i), np.uint8).reshape(H, W, 3)
        p = os.path.join(out_dir, f"cafesol_{s:05.1f}s.png")
        cv2.imwrite(p, img[..., ::-1])
        print(p)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        preview([float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]])
    else:
        render()

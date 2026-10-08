#!/usr/bin/env python3
"""
Rogue Bachata logo loops — three seamless 60s overlay animations.

Each version is rendered on pure black (RGB 0,0,0) so it can be dropped on top of a
dark club video with a Screen / Add / Lighten blend mode: black disappears, light stays.
Every moving part is a periodic function of time whose period divides 60s, so the
last frame flows straight back into the first (frame 1800 == frame 0).

  v1  NEON      neon-tube RB, rolling pink/blue colour, current racing round the tubes,
                neon flicker, chrome shine sweeps
  v2  LIGHTSHOW liquid pink/blue fill, god-rays bursting from behind the logo,
                club lasers in four scenes, rising glitter
  v3  DUET      a pink partner and a blue partner orbiting each other like a bachata turn,
                snapping together into white-hot hits with shockwave rings + glitch

Usage:
  python3 render_logo_loops.py v1 [v2 v3]          # render full 60s MP4s
  python3 render_logo_loops.py v1 --preview 0 5.5  # write PNG stills at given seconds
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
LOGO_PNG = os.path.join(HERE, "..", "images", "Rogue Bachata Logo _transparent_.png")
OUT_DIR = HERE

TAU = 2 * math.pi
PINK = np.array([1.0, 0.07, 0.56], np.float32)
BLUE = np.array([0.06, 0.42, 1.0], np.float32)
CYAN = np.array([0.0, 0.72, 1.0], np.float32)
WHITE = np.array([1.0, 1.0, 1.0], np.float32)
BEAT = 60.0 / 128.0  # 128 BPM -> exactly 128 beats per loop

cv2.setNumThreads(1)


# ----------------------------------------------------------------------------- helpers
def smoothstep(e0, e1, x):
    x = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def sstep(e0, e1, x):  # scalar version
    x = min(max((x - e0) / (e1 - e0), 0.0), 1.0)
    return x * x * (3 - 2 * x)


def blur(img, sigma):
    return cv2.GaussianBlur(img, (0, 0), sigma)


def glow_q(img, layers):
    """Wide glows computed at quarter resolution over the whole frame."""
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    acc = np.zeros_like(small)
    for sigma, weight in layers:
        acc += weight * blur(small, sigma / 4.0)
    return cv2.resize(acc, (W, H), interpolation=cv2.INTER_LINEAR)


def tonemap(x, exposure=1.0):
    return 1.0 - np.exp(-exposure * np.maximum(x, 0.0))


_DITHER = np.random.default_rng(7).random((H, W, 3), dtype=np.float32) - 0.5


def to_bytes(img, i):
    """Float RGB -> uint8 with dither on lit pixels only, so true black stays 0,0,0."""
    v = img * 255.0
    d = np.roll(_DITHER, (i * 37) % H, axis=0)
    v = v + d * np.clip(v * 0.5, 0.0, 1.0)
    v[v < 0.5] = 0.0
    return np.clip(v + 0.5, 0, 255).astype(np.uint8).tobytes()


def shift_affine(dx, dy, scale, cx, cy):
    return np.float32([[scale, 0, cx - scale * cx + dx], [0, scale, cy - scale * cy + dy]])


# ----------------------------------------------------------------------------- logo
LOGO_W = 900
ROI_PAD = 70


def load_logo():
    rgba = cv2.imread(LOGO_PNG, cv2.IMREAD_UNCHANGED)
    a = rgba[..., 3].astype(np.float32) / 255.0
    ys, xs = np.nonzero(a > 0.05)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    a = a[y0:y1, x0:x1]
    scale = LOGO_W / a.shape[1]
    lw, lh = LOGO_W, int(round(a.shape[0] * scale))

    # supersample, soften the traced jaggies, re-threshold, then area-downsample
    S = 4
    up = cv2.resize(a, (lw * S, lh * S), interpolation=cv2.INTER_CUBIC)
    up = smoothstep(0.40, 0.60, blur(up, S * 0.9))
    mask = cv2.resize(up, (lw, lh), interpolation=cv2.INTER_AREA)

    # signed distance (px, positive outside) computed at 2x for accuracy
    up2 = cv2.resize(up, (lw * 2, lh * 2), interpolation=cv2.INTER_AREA) > 0.5
    pad = ROI_PAD * 2
    up2 = np.pad(up2, pad)
    din = cv2.distanceTransform(up2.astype(np.uint8), cv2.DIST_L2, 5)
    dout = cv2.distanceTransform((~up2).astype(np.uint8), cv2.DIST_L2, 5)
    sd = cv2.resize((dout - din) / 2.0, (lw + 2 * ROI_PAD, lh + 2 * ROI_PAD), interpolation=cv2.INTER_AREA)

    mask = np.pad(mask, ROI_PAD)
    # text band "ROGUE BACHATA" sits between the two halves of the monogram (source rows ~218-302)
    t0 = int((214 - y0) * scale) + ROI_PAD
    t1 = int((305 - y0) * scale) + ROI_PAD
    rows = np.arange(mask.shape[0])[:, None]
    text = ((rows >= t0) & (rows < t1)).astype(np.float32) * np.ones_like(mask)
    # split monogram into R (left) and B (right): source column ~474 is the gap between letters
    split = int((474 - x0) * scale) + ROI_PAD
    cols = np.arange(mask.shape[1])[None, :]
    left = (cols < split).astype(np.float32) * np.ones_like(mask)
    return mask.astype(np.float32), sd.astype(np.float32), text, left


MASK, SD, TEXTBAND, LEFT = load_logo()
RH, RW = MASK.shape
RX0, RY0 = (W - RW) // 2, (H - RH) // 2  # ROI top-left in frame
CX, CY = W / 2.0, H / 2.0
RCX, RCY = CX - RX0, CY - RY0  # logo centre in ROI coords
TEXT = MASK * TEXTBAND
MONO = MASK * (1 - TEXTBAND)
MONO_SD = np.where(TEXTBAND > 0, 50.0, SD).astype(np.float32)
RY, RX = np.mgrid[0:RH, 0:RW].astype(np.float32)
FX, FY = RX + RX0, RY + RY0  # frame coords of ROI pixels


def place(roi):
    full = np.zeros((H, W) + roi.shape[2:], np.float32)
    full[RY0:RY0 + RH, RX0:RX0 + RW] = roi
    return full


def col3(scalar_map, color):
    return scalar_map[..., None] * color


# ============================================================================ V1  NEON
TUBE_OFF = 5.0
TUBE_CORE = np.exp(-((MONO_SD + TUBE_OFF) / 1.25) ** 2) * (1 - TEXTBAND)
TUBE_BODY = np.exp(-((MONO_SD + TUBE_OFF) / 3.2) ** 2) * (1 - TEXTBAND)
TEXT_CORE = smoothstep(-1.0, -3.2, SD) * TEXTBAND


def _contours():
    inner = ((MONO_SD < -TUBE_OFF) & (TEXTBAND == 0)).astype(np.uint8)
    cs, _ = cv2.findContours(inner, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        p = c[:, 0, :].astype(np.float32)
        p = np.vstack([p, p[:1]])
        seg = np.sqrt((np.diff(p, axis=0) ** 2).sum(1))
        L = float(seg.sum())
        if L < 250:
            continue
        out.append((p, np.concatenate([[0], np.cumsum(seg)]), L))
    return out


CONTOURS = _contours()
COMETS = []  # (contour idx, laps per loop (signed), phase offset)
for ci, (_, _, L) in enumerate(CONTOURS):
    laps = max(1, round(320 * DUR / L))
    n_comets = 2 if L > 1400 else 1
    direction = 1 if ci % 2 == 0 else -1
    for k in range(n_comets):
        COMETS.append((ci, direction * laps, (k / n_comets + ci * 0.137) % 1.0))

FLICKERS = [  # (start s, duration s, target)
    (6.4, 0.85, "B"), (17.2, 0.55, "T"), (27.9, 1.10, "R"),
    (38.3, 0.45, "ALL"), (46.8, 0.70, "T"), (53.6, 0.60, "B"),
]


def flicker(t, i, target):
    v = 1.0
    for k, (s, d, tg) in enumerate(FLICKERS):
        if tg in (target, "ALL") and s <= t < s + d:
            r = np.random.default_rng(1000 * k + i).random()
            prog = (t - s) / d
            if prog > 0.8:
                v = 1.0 if r > 0.15 else 0.6
            else:
                v = 0.08 if r < 0.55 else (1.15 if r > 0.85 else 0.5)
            if tg == "ALL":
                v = 0.35 + 0.65 * v
    return v


def render_comets(t):
    """Bright 'current' racing round the tubes: bilinear-splatted tail + flared head."""
    canvas = np.zeros((RH, RW), np.float32)
    heads = np.zeros((RH, RW), np.float32)
    tail_len, step = 170.0, 0.5
    k = np.arange(0, tail_len, step, dtype=np.float32)
    fall = (1 - k / tail_len) ** 2.0 * (step / 1.0)
    for ci, laps, off in COMETS:
        p, cum, L = CONTOURS[ci]
        head = ((off + laps * t / DUR) % 1.0) * L
        s = (head - np.sign(laps) * k) % L
        x = np.interp(s, cum, p[:, 0])
        y = np.interp(s, cum, p[:, 1])
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        fx, fy = (x - x0).astype(np.float32), (y - y0).astype(np.float32)
        ok = (x0 >= 0) & (x0 < RW - 1) & (y0 >= 0) & (y0 < RH - 1)
        x0, y0, fx, fy, w = x0[ok], y0[ok], fx[ok], fy[ok], fall[ok]
        np.add.at(canvas, (y0, x0), w * (1 - fx) * (1 - fy))
        np.add.at(canvas, (y0, x0 + 1), w * fx * (1 - fy))
        np.add.at(canvas, (y0 + 1, x0), w * (1 - fx) * fy)
        np.add.at(canvas, (y0 + 1, x0 + 1), w * fx * fy)
        hx, hy = int(round(x[0])), int(round(y[0]))
        if 0 <= hx < RW and 0 <= hy < RH:
            heads[hy, hx] += 1.0
    return blur(canvas, 1.0) * 4.0 + blur(heads, 4.0) * 160.0


def frame_v1(i):
    t = i / FPS
    h = 0.5 + 0.5 * np.sin(TAU * ((FX - CX) / 1150.0 - (FY - CY) / 2600.0 - t / 6.0))
    col = PINK + (BLUE - PINK) * h[..., None]
    tcol = PINK + (BLUE - PINK) * (1 - h[..., None])

    breathe = 0.9 + 0.1 * math.sin(TAU * t / 5.0)
    buzz = 1.0 + 0.02 * math.sin(TAU * t * 41.0) * math.sin(TAU * t * 7.0)
    fR, fB, fT = flicker(t, i, "R"), flicker(t, i, "B"), flicker(t, i, "T")
    mono_int = (LEFT * fR + (1 - LEFT) * fB) * breathe * buzz
    txt_int = fT * breathe * buzz

    E = col * (TUBE_BODY * 1.3 + MONO * 0.07)[..., None] * mono_int[..., None]
    E += WHITE * (TUBE_CORE * 0.7 * mono_int)[..., None]
    E += tcol * (TEXT * 1.15 * txt_int)[..., None] + WHITE * (TEXT_CORE * 0.55 * txt_int)[..., None]

    comet = render_comets(t) * mono_int
    E += tcol * comet[..., None] * 0.9 + WHITE * (comet * 1.1)[..., None]

    # chrome shine sweep every 10s
    u = (t % 10.0) / 1.6
    if u < 1.0:
        pos = -500 + u * 2100
        band = np.exp(-(((FX * 0.82 + FY * 0.57) - (pos + CY * 0.57)) / 38.0) ** 2)
        E += WHITE * (band * (TUBE_BODY * 1.2 + TEXT * 0.9 + MONO * 0.25) * 0.9)[..., None]

    full = place(E)
    full += blur(full, 3.0) * 0.55
    full += glow_q(full, [(14, 0.75), (42, 0.5), (130, 0.22)])
    return tonemap(full, 1.35)


# ============================================================================ V2  LIGHTSHOW
def _noise_tile(n=512, seed=3):
    rng = np.random.default_rng(seed)
    acc = np.zeros((n, n), np.float32)
    for sigma, w in [(40, 1.0), (18, 0.5), (8, 0.22)]:
        r = rng.standard_normal((n, n)).astype(np.float32)
        p = int(sigma * 4)
        r = blur(np.pad(r, p, mode="wrap"), sigma)[p:p + n, p:p + n]  # seamless tile
        acc += w * r / r.std()
    return (acc / acc.std()).astype(np.float32)


NOISE = _noise_tile()
RIM = np.exp(-((SD + 1.6) / 1.6) ** 2) * MASK

QW, QH = W // 4, H // 4
qy, qx = np.mgrid[0:QH, 0:QW].astype(np.float32)
Q_THETA = np.arctan2(qy - CY / 4, qx - CX / 4)
Q_R = np.sqrt(((qx - CX / 4) / (QW * 0.5)) ** 2 + ((qy - CY / 4) / (QH * 0.5)) ** 2)
Q_VIGNETTE = np.clip(1.15 - 0.55 * Q_R ** 2, 0, 1)
LOGO_SHADOW = place(blur(cv2.dilate(MASK, np.ones((9, 9), np.uint8)), 4))
BACKLIGHT_Q = cv2.resize(place(blur((MASK > 0.5).astype(np.float32), 22)), (QW, QH), interpolation=cv2.INTER_AREA)

_prng = np.random.default_rng(11)
NP = 210
P_X = _prng.uniform(0, W, NP)
P_Y = _prng.uniform(0, H + 80, NP)
P_LAPS = _prng.choice([1, 1, 2, 2, 3], NP)
P_SWAY_A = _prng.uniform(8, 45, NP)
P_SWAY_F = _prng.integers(2, 9, NP)
P_PH = _prng.uniform(0, 1, NP)
P_TW = _prng.integers(18, 70, NP)
P_SIZE = _prng.choice([0, 0, 0, 1, 1, 2], NP)
P_COL = _prng.choice([0, 1, 2], NP, p=[0.42, 0.42, 0.16])
P_BRI = _prng.uniform(0.35, 1.0, NP)
P_COLORS = [PINK, CYAN, WHITE]


def render_particles(t):
    layers = [np.zeros((H, W), np.float32) for _ in range(3)]
    y = (P_Y - P_LAPS * (H + 80) * t / DUR) % (H + 80) - 40
    x = P_X + P_SWAY_A * np.sin(TAU * (P_SWAY_F * t / DUR + P_PH))
    tw = (0.5 + 0.5 * np.sin(TAU * (P_TW * t / DUR + P_PH))) ** 3
    # fade particles that would sit on top of the letters
    for k in range(NP):
        b = P_BRI[k] * tw[k]
        if b < 0.02:
            continue
        xi, yi = int(round(x[k])), int(round(y[k]))
        if not (2 <= xi < W - 2 and 2 <= yi < H - 2):
            continue
        L = layers[P_COL[k]]
        L[yi, xi] += b * 3.0
        if P_SIZE[k] >= 1:
            L[yi - 1:yi + 2, xi - 1:xi + 2] += b * 0.8
        if P_SIZE[k] == 2 and b > 0.35:
            arm = int(10 + 22 * b)
            cv2.line(L, (xi - arm, yi), (xi + arm, yi), b * 0.9, 1, cv2.LINE_AA)
            cv2.line(L, (xi, yi - arm), (xi, yi + arm), b * 0.9, 1, cv2.LINE_AA)
    out = np.zeros((H, W, 3), np.float32)
    for L, c in zip(layers, P_COLORS):
        out += blur(L, 0.9)[..., None] * c
    return out


def scene_weights(t, n=4, fade=1.2):
    seg = DUR / n
    w = []
    for s in range(n):
        start = s * seg
        d = (t - start) % DUR
        a = sstep(0, fade, d) * (1 - sstep(seg - fade * 0.2, seg + fade * 0.8, d))
        w.append(a)
    return w


def laser_beams(t):
    beams = []  # (ox, oy, angle_rad, color, intensity)
    w = scene_weights(t)
    pulse = 0.8 + 0.2 * math.cos(TAU * t / BEAT) ** 8
    if w[0] > 0:  # bottom-centre fan
        spread = math.radians(26 + 16 * math.sin(TAU * t / 7.5))
        sway = math.radians(14 * math.sin(TAU * t / 5.0))
        for k in range(9):
            a = -math.pi / 2 + sway + (k - 4) / 4 * spread
            beams.append((CX, H + 40, a, PINK if k % 2 == 0 else CYAN, w[0] * pulse))
    if w[1] > 0:  # top-corner scissors
        for side, ox in ((1, -40), (-1, W + 40)):
            base = math.pi / 2 - side * math.radians(38 + 20 * math.sin(TAU * t / 3.75))
            for k in range(5):
                a = base - side * math.radians(7 * (k - 2))
                beams.append((ox, -40, a, PINK if side > 0 else CYAN, w[1] * pulse))
    if w[2] > 0:  # bottom-corner beams converging & opening
        for side, ox in ((1, -30), (-1, W + 30)):
            open_ = math.radians(7 + 5 * math.sin(TAU * t / 2.5 + (0 if side > 0 else math.pi)))
            aim = math.atan2(CY - (H + 30), CX - ox) + side * math.radians(10 * math.sin(TAU * t / 7.5))
            for k in range(6):
                a = aim + side * (k - 2.5) * open_
                beams.append((ox, H + 30, a, CYAN if side > 0 else PINK, w[2] * pulse))
    if w[3] > 0:  # rotating sunburst from behind the logo
        rot = TAU * t / 12.0
        for k in range(16):
            a = rot + TAU * k / 16
            beams.append((CX, CY, a, PINK if k % 2 == 0 else CYAN, w[3] * pulse * 0.9))
    return beams


def render_lasers(t):
    """Beams drawn in segments so they fade into the haze away from the emitter."""
    sharp = np.zeros((H, W, 3), np.float32)
    seg = 160.0
    for ox, oy, a, c, inten in laser_beams(t):
        ca, sa = math.cos(a), math.sin(a)
        for k in range(16):
            d0, d1 = k * seg, (k + 1) * seg + 2
            fade = inten * 0.75 * (1 - 0.7 * (k + 0.5) / 16) ** 1.5
            p0 = (int((ox + d0 * ca) * 16), int((oy + d0 * sa) * 16))
            p1 = (int((ox + d1 * ca) * 16), int((oy + d1 * sa) * 16))
            cv2.line(sharp, p0, p1, tuple(float(v * fade) for v in c), 2, cv2.LINE_AA, shift=4)
    return sharp


def frame_v2(i):
    t = i / FPS
    # --- liquid fill: periodic noise sampled along a circle in noise space
    a1 = TAU * t / 30.0
    mx = ((RX * 0.55 + 180 * math.cos(a1)) % 512).astype(np.float32)
    my = ((RY * 0.55 + 180 * math.sin(a1)) % 512).astype(np.float32)
    n1 = cv2.remap(NOISE, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    a2 = -TAU * t / 20.0
    mx2 = ((RX * 1.2 + 120 * math.cos(a2) + 200) % 512).astype(np.float32)
    my2 = ((RY * 1.2 + 120 * math.sin(a2) + 77) % 512).astype(np.float32)
    n2 = cv2.remap(NOISE, mx2, my2, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    f = 0.32 * n1 + 0.12 * n2 + (FX - CX) / 900.0 + (FY - CY) / 2000.0 - t / 5.0
    c = 0.5 + 0.5 * np.cos(TAU * f)
    fill = PINK + (CYAN - PINK) * c[..., None]
    hl = np.clip(np.cos(TAU * (2 * f + 0.25)), 0, 1) ** 14

    hit_tau = (t - 0.5) % 7.5
    hit = math.exp(-hit_tau / 0.35)
    beat_tau = t % BEAT
    beat = math.exp(-beat_tau / 0.12)

    E = fill * (MONO * 1.25)[..., None]
    E += (WHITE * 0.85 + fill * 0.5) * TEXT[..., None]
    E += WHITE * ((hl * 0.4 + RIM * 0.6 + hit * 0.7) * MASK)[..., None]
    logo = place(E)

    # --- god rays: zoom blur of the logo + backlight at quarter res, spun by angular beams
    src = cv2.resize(logo, (QW, QH), interpolation=cv2.INTER_AREA)
    bl = 0.5 + 0.5 * math.sin(TAU * t / 15.0)
    src = src * (0.55 + 0.6 * hit) + BACKLIGHT_Q[..., None] * (PINK * bl + CYAN * (1 - bl)) * 0.7
    rays = np.zeros_like(src)
    K = 26
    for k in range(K):
        s = 1.0 + 0.9 * (k / K) ** 1.4
        M = shift_affine(0, 0, s, CX / 4, CY / 4)
        rays += cv2.warpAffine(src, M, (QW, QH), flags=cv2.INTER_LINEAR) * (1 - k / K) ** 1.5
    rays /= K * 0.28
    spin = TAU * t / 20.0
    beams = (0.5 + 0.5 * np.cos(10 * Q_THETA + spin)) ** 5 * 0.85 + 0.15
    beams2 = (0.5 + 0.5 * np.cos(7 * Q_THETA - TAU * t / 12.0 + 1.0)) ** 7 * 0.5
    sector = 0.5 + 0.5 * np.cos(4 * Q_THETA + spin * 2)
    tint = PINK + (CYAN - PINK) * sector[..., None]
    ray_lum = rays.mean(axis=2, keepdims=True)
    rays = (rays * 0.4 + tint * ray_lum * 1.2) * (beams + beams2)[..., None] * Q_VIGNETTE[..., None]
    rays *= 0.8 + 0.25 * beat
    rays = cv2.resize(blur(rays, 1.2), (W, H), interpolation=cv2.INTER_LINEAR)

    # --- lasers (behind the logo)
    lasers = render_lasers(t)
    laser_glow = glow_q(lasers, [(6, 1.6), (22, 0.9)])
    behind = (1 - LOGO_SHADOW * 0.97)[..., None]
    full = (rays + lasers * 1.6 + laser_glow) * behind

    full += render_particles(t) * behind
    full += logo
    full += blur(logo, 3.0) * 0.5
    full += glow_q(logo, [(16, 0.6), (50, 0.35)])
    return tonemap(full, 1.3)


# ============================================================================ V3  DUET
DUET_P = 7.5  # one partner turn per 16 beats @128 BPM -> 8 per loop
DUET_OFF = 1.2
RMAX = 30.0
DUET_PAD = 60
DMASK = np.pad(MASK, DUET_PAD)
DTEXT = np.pad(TEXT, DUET_PAD)
DSD = np.pad(SD, DUET_PAD, constant_values=60.0)
DCORE = smoothstep(-1.5, -5.0, DSD)
DH, DW = DMASK.shape
DX0, DY0 = RX0 - DUET_PAD, RY0 - DUET_PAD
DCX, DCY = CX - DX0, CY - DY0
DYY = np.mgrid[0:DH, 0:DW][0].astype(np.float32)


def duet_state(t):
    k = math.floor((t - DUET_OFF) / DUET_P)
    u = ((t - DUET_OFF) % DUET_P) / DUET_P
    direction = 1 if k % 2 == 0 else -1
    ease = u * u * (3 - 2 * u)
    r = RMAX * math.sin(math.pi * u) ** 0.75
    phi = direction * TAU * ease + (k % 8) * 1.3
    breath = 1.0 + 0.015 * math.sin(math.pi * u) ** 2
    return r * math.cos(phi), r * math.sin(phi) * 0.6, breath


def place_duet(roi):
    full = np.zeros((H, W, 3), np.float32)
    x0, y0 = max(DX0, 0), max(DY0, 0)
    x1, y1 = min(DX0 + DW, W), min(DY0 + DH, H)
    full[y0:y1, x0:x1] = roi[y0 - DY0:y1 - DY0, x0 - DX0:x1 - DX0]
    return full


def frame_v3(i):
    t = i / FPS
    tau = (t - DUET_OFF) % DUET_P
    k_hit = math.floor((t - DUET_OFF) / DUET_P)
    flash = math.exp(-tau / 0.22) + 0.4 * math.exp(-(DUET_P - tau) / 0.06)
    punch = 1.0 + 0.045 * math.exp(-tau / 0.18)
    beat = math.exp(-(t % BEAT) / 0.1)

    acc = np.zeros((DH, DW, 3), np.float32)
    trail_dt = 1.6 / FPS
    for j in range(5):
        tj = t - j * trail_dt
        dx, dy, br = duet_state(tj)
        wj = 0.42 ** j if j else 1.0
        s = br * (punch if j == 0 else 1.0)
        Mp = shift_affine(dx, dy, s * 1.006, DCX, DCY)
        Mb = shift_affine(-dx, -dy, s * 0.994, DCX, DCY)
        mp = cv2.warpAffine(DMASK, Mp, (DW, DH), flags=cv2.INTER_LINEAR)
        mb = cv2.warpAffine(DMASK, Mb, (DW, DH), flags=cv2.INTER_LINEAR)
        acc += (PINK * mp[..., None] + BLUE * mb[..., None]) * (1.25 * wj)
        if j == 0:
            overlap = mp * mb
            acc += WHITE * (overlap * 0.35)[..., None]

    # white-hot core that blooms when the partners meet
    dx, dy, _ = duet_state(t)
    togetherness = math.exp(-math.hypot(dx, dy) / 6.0)
    core_amt = 0.25 * togetherness + 0.55 * flash
    M0 = shift_affine(0, 0, punch, DCX, DCY)
    core = cv2.warpAffine(DCORE, M0, (DW, DH), flags=cv2.INTER_LINEAR)
    acc += WHITE * (core * core_amt)[..., None]
    # text always keeps a bright readable centre
    text = cv2.warpAffine(DTEXT * DCORE, M0, (DW, DH), flags=cv2.INTER_LINEAR)
    acc += WHITE * (text * (0.45 + 0.25 * beat))[..., None]

    # hologram shimmer band sweeping down every 3.75s
    sweep_u = (t % 3.75) / 3.75
    band_y = -80 + sweep_u * (DH + 160)
    band = np.exp(-((DYY - band_y) / 14.0) ** 2)
    acc += (WHITE * 0.6 + CYAN * 0.4) * (band * np.clip(acc.mean(axis=2), 0, 1) * 0.7)[..., None]

    full = place_duet(acc)

    # shockwave rings on each hit (pink then blue)
    rings = np.zeros((H, W, 3), np.float32)
    for delay, c in ((0.0, PINK), (0.14, CYAN)):
        rt = tau - delay
        if 0 <= rt < 1.6:
            grow = rt ** 0.55
            ax = int((LOGO_W * 0.52 + 520 * grow) * 16)
            ay = int((MASK.shape[0] * 0.5 + 300 * grow) * 16)
            inten = math.exp(-rt / 0.45) * 1.4
            cv2.ellipse(rings, (int(CX * 16), int(CY * 16)), (ax, ay), 0, 0, 360,
                        tuple(float(v * inten) for v in c), 3, cv2.LINE_AA, shift=4)
    full += rings

    full += blur(full, 3.0) * 0.5
    full += glow_q(full, [(14, 0.7), (44, 0.45 + 0.15 * flash), (140, 0.12 + 0.1 * flash)])

    # glitch: slices + chromatic split right on the hit, and a few micro-glitches between
    rng = np.random.default_rng(5000 + k_hit % 8)
    micro = [(2.1 + rng.random() * 1.5), (4.6 + rng.random() * 1.8)]
    gl = 1.0 if tau < 0.14 else 0.0
    for m in micro:
        if m <= tau < m + 0.1:
            gl = 0.45
    if gl > 0:
        frng = np.random.default_rng(i)
        y = int(CY - 300)
        while y < CY + 300:
            hgt = int(frng.integers(6, 46))
            if frng.random() < 0.4:
                sh = int(frng.integers(-36, 36) * gl)
                full[y:y + hgt] = np.roll(full[y:y + hgt], sh, axis=1)
                if frng.random() < 0.5:
                    full[y:y + hgt, :, 0] = np.roll(full[y:y + hgt, :, 0], int(14 * gl), axis=1)
                    full[y:y + hgt, :, 2] = np.roll(full[y:y + hgt, :, 2], -int(14 * gl), axis=1)
            y += hgt
    return tonemap(full, 1.3)


# ============================================================================ driver
VERSIONS = {
    "v1": (frame_v1, "RogueBachata_Logo_Loop_v1_Neon"),
    "v2": (frame_v2, "RogueBachata_Logo_Loop_v2_Lightshow"),
    "v3": (frame_v3, "RogueBachata_Logo_Loop_v3_Duet"),
}
_FN = None


def _work(i):
    return to_bytes(_FN(i), i)


def _init(name):
    global _FN
    _FN = VERSIONS[name][0]


def render(name):
    fn, base = VERSIONS[name]
    out = os.path.join(OUT_DIR, base + "_1080x1920_60s_black.mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.2",
        "-g", "60", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-color_range", "tv", "-movflags", "+faststart", "-tag:v", "avc1", out,
    ]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count(), initializer=_init, initargs=(name,)) as pool:
        for k, buf in enumerate(pool.imap(_work, range(N), chunksize=6)):
            ff.stdin.write(buf)
            if k % 150 == 0:
                print(f"{name}: frame {k}/{N}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


def preview(name, seconds):
    fn = VERSIONS[name][0]
    for s in seconds:
        i = int(round(s * FPS)) % N
        img = np.frombuffer(to_bytes(fn(i), i), np.uint8).reshape(H, W, 3)
        p = os.path.join(os.environ.get("PREVIEW_DIR", os.path.join(OUT_DIR, "_preview")), f"{name}_{s:05.1f}s.png")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        cv2.imwrite(p, img[..., ::-1])
        print(p)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--preview" in args:
        k = args.index("--preview")
        names, secs = args[:k], [float(x) for x in args[k + 1:]]
        for n in names:
            preview(n, secs)
    else:
        for n in args or list(VERSIONS):
            render(n)

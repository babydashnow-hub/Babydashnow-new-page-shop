#!/usr/bin/env python3
"""
Full Circle - OPENING TEST v4 "Living Emblem" (3.5 s, silent). Opening only (4.0 s); not the advertisement.

The ORIGINAL squirrel is completely stationary (one uniform downscale, nothing else).
All motion belongs to the official BabyDashNow green dot, which orbits the squirrel
continuously and draws the circle around it. "Give $5. Get $5." is legible from frame 0;
the first verified condition arrives as the circle completes.
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle as b

W, H, FPS = b.W, b.H, b.FPS
NF = 120
OUTDIR = os.path.join(b.OUT, "opening_test_v4")

CX, CY, R = 540, 1000, 300           # the emblem: circle centred on the squirrel
TH0 = 20.0                           # dot already travelling at frame 0
V_END = 2.2                          # deg/frame once the circle is complete (continuous, calm)
V_START = 6.52                       # chosen so the first lap closes the circle at frame 78
LAP_F = 78
COND_TOP = 1338                      # first condition, under the emblem
COND_IN = (88, 102)


def theta(f):
    """Integrated angular position: decelerating first lap, then steady orbit (no stop-start)."""
    th, step = TH0, 0.25
    t = 0.0
    while t < f:
        u = min(t / LAP_F, 1.0)
        s = u * u * (3 - 2 * u)
        v = V_END + (V_START - V_END) * (1 - s) if t < LAP_F else V_END
        th += v * step
        t += step
    return th


def pos(th):
    a = math.radians(th)              # 0 = 6 o'clock, increasing counter-clockwise on screen
    return CX + R * math.sin(a), CY + R * math.cos(a)


def ring(th_end, ss=3):
    pad = 40
    box = (CX - R - pad, CY - R - pad)
    size = (2 * (R + pad), 2 * (R + pad))
    m = Image.new("L", (size[0] * ss, size[1] * ss), 0)
    end = min(th_end, TH0 + 360.0)
    start = TH0 - 0.001 if th_end - TH0 < 360 else 0.0
    n = max(2, int((end - TH0) / 0.4))
    pts = []
    for k in range(n + 1):
        a = math.radians(TH0 + (end - TH0) * k / n)
        pts.append(((CX + R * math.sin(a) - box[0]) * ss, (CY + R * math.cos(a) - box[1]) * ss))
    ImageDraw.Draw(m).line(pts, fill=255, width=int(round(b.LINE_W * ss)), joint="curve")
    return box, m.resize(size, Image.LANCZOS)


def dot(fr, x, y, r):
    ss, pad = 4, int(r + 4)
    m = Image.new("L", (pad * 2 * ss, pad * 2 * ss), 0)
    ImageDraw.Draw(m).ellipse(((pad - r) * ss, (pad - r) * ss, (pad + r) * ss, (pad + r) * ss), fill=255)
    m = m.resize((pad * 2, pad * 2), Image.LANCZOS)
    fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x)) - pad, int(round(y)) - pad))


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    R_ = b.build_resources(False)
    sq = R_["sq"]
    a = np.array(sq.getchannel("A")) > 30
    ys, xs = np.where(a)
    fx, fy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    sq_pos = (int(round(CX - fx)), int(round(CY - fy + 6)))          # optically centred in the emblem
    out = os.path.join(OUTDIR, "PassTheCare_OpeningTest_v4_LivingEmblem_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(NF):
        fr = Image.new("RGBA", (W, H), b.IVORY + (255,))
        th = theta(f)
        box, m = ring(th)
        fr.alpha_composite(b.solid(b.GREEN, m), box)
        fr.alpha_composite(sq, sq_pos)                                   # unaltered, stationary
        x, y = pos(th)
        dot(fr, x, y, b.DOT_R)
        # offer hierarchy: legible from frame 0
        b.paste(fr, R_["label"], b.CX + 14, b.LABEL_Y)
        lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
        ImageDraw.Draw(fr).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=b.TEXT_GREEN)
        b.paste(fr, R_["head"], b.CX, b.HEAD_Y)
        b.paste(fr, R_["tag"], b.CX, b.TAG_Y)
        if f >= COND_IN[0]:
            p = b.ease(b.prog(f, COND_IN))
            b.paste(fr, R_["c1"], b.CX, COND_TOP, p, 12 * (1 - p))
        im = fr.convert("RGB")
        if f in (0, 15, 30, 50, 87, 119):
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    print("wrote", out, "| lap closes near frame", next(f for f in range(NF) if theta(f) >= TH0 + 360))


if __name__ == "__main__":
    main()

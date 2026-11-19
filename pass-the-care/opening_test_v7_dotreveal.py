#!/usr/bin/env python3
"""
OPENING TEST v7 - "Green Dot Reveal" (4.2 s, with sound). Opening only; not a master.

One continuous gesture built on Organic v6:
  f0      the official green dot is already on screen (ivory), with a soft tick
  f0-26   it travels right, drawing a fine horizontal line at the emblem's 6 o'clock height
  f0-29   that line is the reveal edge, driven by the dot: Organic v6 is lifted into view above it
          (squirrel first, then "Give $5. Get $5.", label last) and completes as the dot meets the circle
  f26-36  the dot meets the circle's lowest point, where a circle's tangent is horizontal,
          and curves straight into the v6 orbit; the line retracts into the circle's start
  f36+    Organic v6 continues unchanged (its own frame 0 onwards)

The squirrel, wording, colours and type are v6's own; nothing is redrawn.
"""
import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle_v6 as v

b = v.b
OPEN = 36                       # 1.20 s opening
V6_FRAMES = 90                  # show 3.0 s of v6 afterwards
NF = OPEN + V6_FRAMES
OUTDIR = os.path.join(b.OUT, "opening_test_v7")
SR = b.SR

LINE_Y = b.CY + b.R             # 1255: the circle's 6 o'clock height
X_START = 150
X_JOIN = b.CX                   # the circle's lowest point
H_LEN = X_JOIN - X_START        # 390 px
ARC_AT_OPEN = math.radians(v.TH_START) * b.R      # where v6's dot is at its frame 0 (18 deg)
V6_SPEED = (v.theta(1) - v.theta(0)) * math.pi / 180 * b.R   # px/frame at v6 frame 0
REVEAL = (8, 34)
FEATHER = 46


def s_of(f):
    """Arc length travelled: cubic Hermite from rest to v6's own speed, landing exactly on v6's start."""
    u = min(max(f / OPEN, 0.0), 1.0)
    p1, m1 = H_LEN + ARC_AT_OPEN, V6_SPEED * OPEN
    return (-2 * u ** 3 + 3 * u ** 2) * p1 + (u ** 3 - u ** 2) * m1


def dot_xy(f):
    s = s_of(f)
    if s <= H_LEN:
        return X_START + s, LINE_Y, 0.0
    th = math.degrees((s - H_LEN) / b.R)
    x, y = b.ring_xy(th)
    return x, y, th


def static_layer(R_):
    """v6's composition at rest (label, headline, tagline, squirrel) on transparent ground."""
    v.retype(R_)
    if v.HEAD is None:
        v.HEAD = v.headline_parts(R_)
    lay = Image.new("RGBA", (b.W, b.H), (0, 0, 0, 0))
    sx, sy = v.sq_pos(R_)
    lay.alpha_composite(R_["sq"], (sx, sy))
    b.paste(lay, R_["label"], b.CX + 14, b.LABEL_Y)
    lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
    ImageDraw.Draw(lay).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=b.TEXT_GREEN + (255,))
    give, get, gx, tx = v.HEAD
    b.paste(lay, give, gx, b.HEAD_Y)
    b.paste(lay, get, tx, b.HEAD_Y)
    b.paste(lay, R_["tag"], b.CX, b.TAG_Y)
    return lay


def reveal_p(f):
    """Reveal progress is driven by the dot: it completes as the dot meets the circle."""
    return min(1.0, max(0.0, s_of(f) / H_LEN)) ** 0.8


def reveal_mask(f):
    p = reveal_p(f)
    edge = LINE_Y + 10 - (LINE_Y + 10 - 230) * p          # moves up from the line to above the label
    y = np.arange(b.H, dtype=np.float32)
    a = np.clip((y - edge) / FEATHER, 0, 1)
    a[int(LINE_Y + 12):] = 0 if p < 1 else a[int(LINE_Y + 12):]   # nothing below the line
    return Image.fromarray((np.repeat(a[:, None], b.W, axis=1) * 255).astype(np.uint8))


def hline(fr, x0, x1, alpha=1.0):
    if x1 - x0 < 1:
        return
    SS = 4
    w = int(x1 - x0) + 8
    m = Image.new("L", (w * SS, 8 * SS), 0)
    ImageDraw.Draw(m).line((4 * SS, 4 * SS, (x1 - x0 + 4) * SS, 4 * SS), fill=255, width=int(round(b.LINE_W * SS)))
    m = m.resize((w, 8), Image.LANCZOS).point(lambda q: int(q * alpha))
    fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x0 - 4)), int(round(LINE_Y - 4))))


def dot(fr, x, y, r):
    SS, pad = 4, int(r + 4)
    m = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
    ImageDraw.Draw(m).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
    m = m.resize((pad * 2, pad * 2), Image.LANCZOS)
    fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x)) - pad, int(round(y)) - pad))


def line_left(f):
    """Left end of the horizontal line: holds at X_START, then retracts into the circle's start."""
    return X_START + (X_JOIN - X_START) * b.ease(b.prog(f, (28, 50))) if f >= 28 else X_START


def frame(f, R_, STATIC):
    if f < OPEN:
        fr = Image.new("RGBA", (b.W, b.H), b.IVORY + (255,))
        lay = STATIC.copy()
        lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel("A")), np.array(reveal_mask(f)))))
        rise = int(round(28 * (1 - b.ease(reveal_p(f)))))          # content is lifted by the line
        fr.alpha_composite(lay, (0, rise))
        x, y, th = dot_xy(f)
        if th > 0:
            box, m = v.ring_mask(th, 1.0)
            fr.alpha_composite(b.solid(b.GREEN, m), box)
        hline(fr, line_left(f), min(x, X_JOIN))
        r = b.DOT_R * (0.72 + 0.28 * b.ease(min(1.0, f / 5.0)))   # appears already present, settles in 5 frames
        dot(fr, x, y, r)
        return fr
    fr = v.story_frame(f - OPEN, R_)
    if line_left(f) < X_JOIN - 1:                       # the line's last stretch retracts into the circle
        tmp = Image.new("RGBA", (b.W, b.H), (0, 0, 0, 0))
        hline(tmp, line_left(f), X_JOIN)
        fr.alpha_composite(tmp)
    return fr


# ------------------------------------------------------------------ sound
def tick(amp=0.065):
    t = np.arange(int(0.09 * SR)) / SR
    body = np.sin(2 * np.pi * 1320 * t) * np.exp(-t / 0.012) + 0.45 * np.sin(2 * np.pi * 660 * t) * np.exp(-t / 0.03)
    return amp * body * (1 - np.exp(-t / 0.0006))


def line_sound(dur_f, amp=0.05):
    n = int(dur_f / b.FPS * SR)
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(n)
    # gentle band-pass (two one-pole filters) -> soft "drawn" texture, no whoosh
    lp = np.zeros(n); hp = np.zeros(n); a1, a2 = 0.12, 0.985
    for i in range(1, n):
        lp[i] = lp[i - 1] + a1 * (noise[i] - lp[i - 1])
        hp[i] = a2 * (hp[i - 1] + lp[i] - lp[i - 1])
    t = np.arange(n) / SR
    speed = np.array([abs(s_of(k / SR * b.FPS + 0.5) - s_of(k / SR * b.FPS - 0.5)) for k in range(0, n)])
    env = speed / max(speed.max(), 1e-6)
    glide = 0.35 * np.sin(2 * np.pi * (587.33 * t + 40 * t ** 2)) * np.exp(-t / 0.5)   # faint pitched trace
    return amp * env * (hp / (np.abs(hp).max() + 1e-9) + glide)


def mix_audio():
    n = int(NF / b.FPS * SR)
    y = np.zeros(n)

    def add(sig, frame_i):
        s = int(frame_i / b.FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    add(tick(), 0)
    add(line_sound(OPEN - 6), 1)
    add(b.note(392.0, dur=2.2, amp=0.115) + b.note(587.33, dur=2.2, amp=0.055), 30)   # warm G/D dyad: offer revealed
    add(b.note(493.88, amp=0.11), OPEN + 40)                                          # v6's outward phrase continues
    add(b.note(587.33, amp=0.11), OPEN + 82)
    t = np.arange(n) / SR
    bed = 0.010 * (np.sin(2 * np.pi * 98 * t) + 0.5 * np.sin(2 * np.pi * 147 * t)) * np.clip((t - 0.9) / 0.6, 0, 1)
    return y + bed


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    R_ = b.build_resources(False)
    STATIC = static_layer(R_)
    silent = os.path.join(OUTDIR, "silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{b.W}x{b.H}",
                            "-r", str(b.FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    keep = {0, 6, 14, 22, 30, 36, 48, 125}
    for f in range(NF):
        im = frame(f, R_, STATIC).convert("RGB")
        if f in keep:
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    mix = mix_audio()
    raw = os.path.join(OUTDIR, "mix_raw.wav"); b.write_wav(raw, mix)
    I, TP = b.loudness(raw)
    g = min(-19.0 - I, -1.0 - TP)                       # match the v6 master's level (~-19 LUFS), linear gain
    wav = os.path.join(OUTDIR, "mix.wav"); b.write_wav(wav, mix * 10 ** (g / 20))
    out = os.path.join(OUTDIR, "PassTheCare_OpeningTest_v7_DotReveal.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"| v6 start speed {V6_SPEED:.1f} px/f | dot meets circle at frame",
          next(k for k in range(OPEN) if s_of(k) >= H_LEN), "| gain", round(g, 2))


if __name__ == "__main__":
    main()

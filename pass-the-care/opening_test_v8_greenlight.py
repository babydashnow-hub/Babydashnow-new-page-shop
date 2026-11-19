#!/usr/bin/env python3
"""
OPENING PROTOTYPE v8 - "The Green Light Reveal" (3.0 s, with sound). Prototype only; not a master.

Narrative causality, one event chain:
  f0-20   uniform ivory; the official green dot enters from the left (the only moving element)
          and decelerates to a deliberate stop at the emblem's centre
  f20-24  anticipation (still)
  f24-26  PRESS: the dot compresses to 82 %          (soft pre-click)
  f26     CLICK: release, back to 100 %               (crisp click)
  f27-47  the click OPENS the composition: a circular aperture grows from the dot itself.
          The aperture has no drawn edge (ivory on ivory); content simply exists inside it.
          The squirrel opens from its centre outward (never feet-first); the offer follows.
          The dot rides the aperture's lowest edge down to the circle's 6 o'clock point,
          so it never crosses visible artwork.
  f47+    the dot, now at 6 o'clock, eases into the Full Circle orbit; Organic v6 continues.
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle_v6 as v
import opening_test_v7_dotreveal as v7

b = v.b
OUTDIR = os.path.join(b.OUT, "opening_test_v8")
SR, FPS = b.SR, b.FPS

ENTER = (0, 20)
PRESS = (24, 26)
CLICK = 26
OPEN = (27, 47)
OPEN_END = OPEN[1]
V6_SHOW = 46
NF = OPEN_END + V6_SHOW                    # 93 frames = 3.1 s
X0 = 40
CENTRE = (b.CX, b.CY)                      # (540, 940)
R_MAX = 800                                # just beyond the label/headline corners (~720 px)
FEATHER = 34


def ease_out3(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def aperture_r(f):
    if f < OPEN[0]:
        return 0.0
    return R_MAX * b.ease((f - OPEN[0]) / (OPEN[1] - OPEN[0]))      # deliberate: opens, then settles


def dot_state(f):
    """(x, y, radius) during the opening."""
    if f < ENTER[1]:
        p = ease_out3(f / ENTER[1])
        return X0 + (CENTRE[0] - X0) * p, CENTRE[1], b.DOT_R
    r = b.DOT_R
    if PRESS[0] <= f < CLICK:
        r = b.DOT_R * (1 - 0.18 * b.ease((f - PRESS[0]) / (PRESS[1] - PRESS[0])))
    elif CLICK <= f < CLICK + 3:
        r = b.DOT_R * (0.82 + 0.18 * b.ease((f - CLICK + 1) / 3))
    y = CENTRE[1] + min(aperture_r(f), b.R)            # rides the aperture's lowest edge to 6 o'clock
    return CENTRE[0], y, r


# v6's orbit, eased in from rest at 6 o'clock (theta 0) instead of v6's moving start (18 deg)
_v6_theta = v.theta
BLEND = 14


def theta_from_rest(f):
    if f >= BLEND:
        return _v6_theta(f)
    target = _v6_theta(BLEND)
    u = f / BLEND
    return target * (u * u * (3 - 2 * u)) * 0.6 + target * 0.4 * u ** 3


def frame(f, R_, STATIC):
    if f < OPEN_END:
        fr = Image.new("RGBA", (b.W, b.H), b.IVORY + (255,))
        r_ap = aperture_r(f)
        if r_ap > 0:
            yy, xx = np.mgrid[:b.H, :b.W].astype(np.float32)
            d = np.sqrt((xx - CENTRE[0]) ** 2 + (yy - CENTRE[1]) ** 2)
            m = np.clip((r_ap - d) / FEATHER, 0, 1)
            lay = STATIC.copy()
            lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel("A")), (m * 255).astype(np.uint8))))
            fr.alpha_composite(lay)
        x, y, r = dot_state(f)
        v7.dot(fr, x, y, r)
        return fr
    return v.story_frame(f - OPEN_END, R_)


# ------------------------------------------------------------------ sound
def click_sound():
    """Press (soft) + release (crisp): band-limited transients with a small low body. No whoosh."""
    rng = np.random.default_rng(5)

    def transient(dur, f_lo, f_hi, decay, amp):
        n = int(dur * SR); t = np.arange(n) / SR
        noise = rng.standard_normal(n)
        spec = np.fft.rfft(noise); freqs = np.fft.rfftfreq(n, 1 / SR)
        spec[(freqs < f_lo) | (freqs > f_hi)] = 0
        burst = np.fft.irfft(spec, n)
        burst /= np.abs(burst).max() + 1e-9
        return amp * burst * np.exp(-t / decay)

    press = transient(0.03, 1800, 4500, 0.004, 0.10)
    t = np.arange(int(0.12 * SR)) / SR
    body = 0.16 * np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.018)
    release = transient(0.04, 2500, 7000, 0.003, 0.26)
    rel = np.zeros(len(t)); rel[:len(release)] += release; rel += body
    return press, rel


def bloom(dur):
    """The opening: a soft low swell (G2/G3 + filtered air) that rises and settles with the aperture."""
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    tone = 0.5 * np.sin(2 * np.pi * 98 * t) + 0.35 * np.sin(2 * np.pi * 196 * t)
    rng = np.random.default_rng(9)
    air = np.convolve(rng.standard_normal(n), np.ones(300) / 300, mode="same") * 4
    return 0.06 * env * (tone + air)


def entry_glide(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(13)
    air = np.convolve(rng.standard_normal(n), np.ones(120) / 120, mode="same")
    env = (1 - np.clip(t / dur, 0, 1)) ** 2 * np.clip(t / 0.05, 0, 1)        # follows the decelerating dot
    return 0.02 * env * air / (np.abs(air).max() + 1e-9) * 8


def mix():
    n = int(NF / FPS * SR); y = np.zeros(n)

    def add(sig, fr_):
        s = int(fr_ / FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    press, release = click_sound()
    add(entry_glide(ENTER[1] / FPS), 0)
    add(press, PRESS[0])
    add(release, CLICK)
    add(bloom((OPEN[1] - OPEN[0] + 10) / FPS), OPEN[0])
    add(b.note(392.0, dur=2.2, amp=0.11) + b.note(587.33, dur=2.2, amp=0.05), 41)   # offer revealed
    add(b.note(493.88, amp=0.10), OPEN_END + 40)                                      # v6 outward phrase
    return y


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v.theta = theta_from_rest
    R_ = b.build_resources(False)
    STATIC = v7.static_layer(R_)
    silent = os.path.join(OUTDIR, "silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{b.W}x{b.H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    keep = {0, 10, 20, 25, 27, 31, 35, 39, 44, 47, 92}
    for f in range(NF):
        im = frame(f, R_, STATIC).convert("RGB")
        if f in keep:
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    y = mix()
    raw = os.path.join(OUTDIR, "mix_raw.wav"); b.write_wav(raw, y)
    I, TP = b.loudness(raw)
    g = min(-19.0 - I, -1.0 - TP)
    wav = os.path.join(OUTDIR, "mix.wav"); b.write_wav(wav, y * 10 ** (g / 20))
    out = os.path.join(OUTDIR, "PassTheCare_OpeningPrototype_v8_GreenLight.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    hd = next(f for f in range(OPEN[0], OPEN_END) if aperture_r(f) >= math.hypot(540 - 136, 940 - 346))
    print("wrote", out, "| headline fully inside aperture at frame", hd, f"({hd / FPS:.2f}s)", "| gain", round(g, 2))


if __name__ == "__main__":
    main()

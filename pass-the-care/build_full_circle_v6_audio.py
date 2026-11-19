#!/usr/bin/env python3
"""
Full Circle - Organic v6, AUDIO REVIEW version. Picture is Organic v6 unchanged; only the
story soundtrack (0.00-10.67 s) is redesigned as a sonic narrative of the dot's journey.
The official outro's own audio, including the approved chime, is used as is.

Cues (frames at 30 fps; v6 picture timing):
  f0        opening accent: a soft, precise tick + a low, quiet G (the dot is already moving)
  f0-120    outward journey: a very low, airy texture that follows the dot's speed, and three
            felt-piano notes rising G4 -> B4 -> D5 at 1/3, 2/3 and 90 % of the outward travel
  f114-150  deliberate quiet: everything thins out for the qualifying-order pause (f120-150);
            the dot's pulse and the underline glide are left silent
  f150      warm answer as the dot turns back: a soft B4/G4 dyad, then A4 at mid-return
  f270      the circle closes: a low, soft G3, resolving the phrase
  f292-320  hand-off to the outro is left quiet
  f377      the official BabyDashNow chime (outro audio, untouched)
"""
import math

import numpy as np

import build_full_circle_v6 as v

b = v.b
b.TAG_PREFIX = "PassTheCare_FullCircle_CANDIDATE_v6_AUDIO"
SR, FPS = b.SR, b.FPS


def felt(freq, amp, dur=2.4, decay=0.7):
    """Softer felt-piano voice than v6: slower attack, fewer upper partials."""
    t = np.arange(int(dur * SR)) / SR
    env = (1 - np.exp(-t / 0.014)) * np.exp(-t / decay)
    y = (np.sin(2 * np.pi * freq * t)
         + 0.28 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 1.6)
         + 0.07 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t * 3.0))
    return amp * env * y


def tick(amp):
    t = np.arange(int(0.08 * SR)) / SR
    y = np.sin(2 * np.pi * 1760 * t) * np.exp(-t / 0.006) + 0.5 * np.sin(2 * np.pi * 880 * t) * np.exp(-t / 0.02)
    return amp * y * (1 - np.exp(-t / 0.0008))


def dot_speed(fr):
    """Angular speed of the v6 dot (deg/frame) at a fractional frame."""
    return abs(v.theta(min(fr + 0.5, 319)) - v.theta(max(fr - 0.5, 0)))


def air_trace(n):
    """Very low band-limited air whose level follows the dot's speed (outward and return legs)."""
    rng = np.random.default_rng(21)
    noise = rng.standard_normal(n)
    spec = np.fft.rfft(noise); fq = np.fft.rfftfreq(n, 1 / SR)
    spec *= np.exp(-((fq - 1400) / 900) ** 2)              # soft band around 1.4 kHz, no hiss, no whoosh
    air = np.fft.irfft(spec, n); air /= np.abs(air).max() + 1e-9
    frames = np.arange(n) / SR * FPS
    sp = np.array([dot_speed(f) for f in np.arange(0, b.STORY + 1)])
    env = np.interp(frames, np.arange(len(sp)), sp / sp.max())
    env = np.convolve(env, np.ones(2400) / 2400, mode="same")   # 50 ms smoothing
    return 0.035 * air * env


def story_audio():
    n = int(b.STORY / FPS * SR)
    y = np.zeros(n)

    def add(sig, fr):
        s = int(fr / FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]

    G3, G4, A4, B4, D5 = 196.0, 392.0, 440.0, 493.88, 587.33
    # 1. opening accent
    add(tick(0.05), 0)
    add(felt(G3, 0.05, dur=1.6, decay=0.5), 0)
    # 2. outward journey: notes at the dot's 1/3, 2/3 and arrival points
    marks = [next(f for f in range(0, 121) if v.theta(f) >= v.TH_START + (180 - v.TH_START) * k) for k in (1 / 3, 2 / 3, 0.9)]
    for f, note_hz, amp in zip(marks, (G4, B4, D5), (0.10, 0.095, 0.10)):
        add(felt(note_hz, amp, decay=0.6 if note_hz != D5 else 0.45), f)
    # 4. warm answer on the turn back, a quieter echo at mid-return
    add(felt(B4, 0.085, dur=3.0, decay=0.9) + felt(G4, 0.06, dur=3.0, decay=0.9), 150)
    mid = next(f for f in range(150, 271) if v.theta(f) >= 270)
    add(felt(A4, 0.065, decay=0.6), mid)
    # 5. closure resolves low and soft
    add(felt(G3, 0.08, dur=2.4, decay=0.8), 270)
    y += air_trace(n)

    # 3. deliberate quiet around the qualifying-order pause (f114-152), then hand-off quiet
    t = np.arange(n) / SR
    gate = np.ones(n)
    q0, q1, q2, q3 = 114 / FPS, 122 / FPS, 146 / FPS, 150 / FPS
    gate[(t >= q0) & (t < q1)] = np.linspace(1, 0.12, ((t >= q0) & (t < q1)).sum())
    gate[(t >= q1) & (t < q2)] = 0.12
    gate[(t >= q2) & (t < q3)] = np.linspace(0.12, 1, ((t >= q2) & (t < q3)).sum())
    y_tail = y.copy()
    y *= gate
    y[t >= q3] = y_tail[t >= q3]                            # the answer at f150 starts clean, ungated
    tail = np.clip((b.STORY / FPS - t) / 0.9, 0, 1)         # let it all settle before the outro
    return y * tail


b.story_audio = story_audio

if __name__ == "__main__":
    b.main()
    R_ = b.build_resources(False)
    v.story_frame(0, R_, cover=True).convert("RGB").save(f"{b.OUT}/{b.TAG_PREFIX}_VariantB_cover.png")
    print("cover written")

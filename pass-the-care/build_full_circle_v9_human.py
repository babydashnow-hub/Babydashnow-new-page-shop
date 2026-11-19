#!/usr/bin/env python3
"""
PASS THE CARE(TM) - REVIEW CANDIDATE v9 "Human-first" (Organic v6 system + real-parent opening).

Progression: real parent -> understanding -> useful local service -> PASS THE CARE -> action.

  0.00-3.00  Pexels video 7279098 (source 0.5-3.5 s, supplied 1080x1920/30 fps edit), unaltered
             "Your hands are / already full."
  2.80-3.40  the footage dissolves into BabyDashNow ivory
  3.27-6.33  "Let us take one thing / off your list."  + the official BabyDashNow logo,
             "Baby essentials, delivered locally." and the four towns
  ~6.0       the logo's green dot detaches (drawn over the official dot, same colour) and glides
             to the emblem's 6 o'clock point while the rest of the card leaves
  6.53-16.4  Organic v6 PASS THE CARE system (squirrel, Give $5. Get $5., moving rule, out-and-back
             orbit with both verified statements), retimed: 9.87 s instead of 10.67 s
  16.4-22.4  official 6 s outro (unaltered picture) + Discover PASS THE CARE(TM)
Sound: restrained felt-piano narrative; v6 AUDIO cues retimed; bridge under the outro's silent
lead-in; official chime -3 dB (the approved B2 correction), otherwise untouched.

The footage is stock: no customer, purchase or endorsement is stated or implied.
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle_v6 as v
import build_full_circle_v6_audio as va
import audio_ab_v6_bridge as ab

b = v.b
FOOTAGE = os.path.join(b.A, "footage_pexels_7279098_0p5-3p5.mp4")   # supplied edit of Pexels video 7279098, source 0.5-3.5 s
LOGO = os.path.join(b.A, "logo", "babydashnow-logo.png")
FPS, SR = b.FPS, b.SR

# ------------------------------------------------------------------ global timeline (frames)
S0 = 196                                   # Organic v6 story starts here (6.53 s)
V6_LEN = 296                               # retimed v6 story length (9.87 s)
b.STORY = S0 + V6_LEN                      # 492 -> outro 492-671, total 672 frames = 22.4 s
b.N = b.STORY + 180
b.CTA_IN = b.STORY + 90
b.TAG_PREFIX = "PassTheCare_HumanFirst_REVIEW_v9"

T1 = (6, 90)                               # "Your hands are already full."
DISSOLVE = (84, 102)
T2 = (98, 190)                             # "Let us take one thing off your list."
LOGO_IN = (116, 190)
LINE_IN = (124, 190)
DOT_ON = 170                               # drawn dot replaces the logo's dot (identical position/size)
GLIDE = (180, 196)
V6_IN = 14                                 # v6 composition fades in over its first 14 frames

# retime the v6 story (reading times kept: statement 1 = 4.3 s, statement 2 = 4.8 s)
v.OUT, v.HOLD, v.RET = (0, 110), (110, 134), (134, 244)
b.TXT = {"c1": (6, 136), "c2": (138, 282)}
v.FADE, v.BG, v.LAND, v.SHRINK = (270, 284), (272, 295), (266, 286), (278, 295)
CHIME_DB = -3.0

# v6's orbit starts from rest at 6 o'clock (the dot arrives there from the logo)
_v6_theta = v.theta
BLEND = 14


def theta_from_rest(f):
    if f >= BLEND:
        return _v6_theta(f)
    tgt = _v6_theta(BLEND); u = max(f, 0) / BLEND
    return tgt * (0.6 * u * u * (3 - 2 * u) + 0.4 * u ** 3)


v.theta = theta_from_rest

# ------------------------------------------------------------------ assets
FOOT = []
LOGO_IM = None


def load_assets():
    global LOGO_IM
    if not FOOT:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", FOOTAGE, "-vf", "scale=in_color_matrix=bt709:in_range=tv",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        n = len(raw) // (b.W * b.H * 3)
        for i in range(n):
            FOOT.append(Image.frombuffer("RGB", (b.W, b.H), raw[i * b.W * b.H * 3:(i + 1) * b.W * b.H * 3]).convert("RGBA"))
    if LOGO_IM is None:
        LOGO_IM = Image.open(LOGO).convert("RGBA")


LOGO_W = 620
LOGO_TOP = 1010


def logo_geom():
    s = LOGO_W / LOGO_IM.width
    im = LOGO_IM.resize((LOGO_W, round(LOGO_IM.height * s)), Image.LANCZOS)
    x = (b.W - LOGO_W) // 2
    dot_c = (x + 195.5 * s, LOGO_TOP + 195.5 * s)       # centre of the logo's dot in the 2000 px master
    dot_r = 69 * s
    return im, (x, LOGO_TOP), dot_c, dot_r


def two_tone(line_a, line_b, size, top_color=b.INK):
    """Fraunces 700 line + Fraunces 400 italic green line, centred."""
    fa, fb = b.font(v.FR700, size), b.font(v.FR400I, size)
    ia = b.text_img([line_a], fa, top_color + (255,))
    ib = b.text_img([line_b], fb, b.TEXT_GREEN + (255,))
    w = max(ia.width, ib.width); h = ia.height + ib.height - 18
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(ia, ((w - ia.width) // 2, 0)); im.alpha_composite(ib, ((w - ib.width) // 2, ia.height - 18))
    return im


TXT_IMG = {}


def texts():
    if not TXT_IMG:
        TXT_IMG["t1"] = two_tone("Your hands are", "already full.", 74)
        TXT_IMG["t2"] = two_tone("Let us take one thing", "off your list.", 70)
        TXT_IMG["svc"] = b.text_img(["Baby essentials, delivered locally."], b.font(v.INTER_REG, 38), b.SOFT_INK + (255,))
        TXT_IMG["towns"] = b.text_img(["Stamford · Darien · Norwalk · Greenwich"], b.font(b.INTER_MED, 30), b.INK + (255,))
    return TXT_IMG


def fade(f, span, fin=12, fout=12):
    return b.appear(f, span, fin=fin, fout=fout, rise=10)


def solid_dot(fr, x, y, r):
    SS, pad = 4, int(r + 4)
    m = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
    ImageDraw.Draw(m).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
    m = m.resize((pad * 2, pad * 2), Image.LANCZOS)
    fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x)) - pad, int(round(y)) - pad))


def glide_xy(f, dot_c, dot_r):
    p = b.ease(b.prog(f, GLIDE)) if f >= GLIDE[0] else 0.0
    tx, ty = b.ring_xy(0.0)
    return dot_c[0] + (tx - dot_c[0]) * p, dot_c[1] + (ty - dot_c[1]) * p, dot_r + (b.DOT_R - dot_r) * p


def global_frame(f, R_):
    load_assets(); T = texts()
    if f >= S0:
        local = f - S0
        fr6 = v.story_frame(local, R_)
        if local >= V6_IN:
            return fr6
        base = Image.new("RGBA", (b.W, b.H), b.IVORY + (255,))
        x, y, r, _ = v.dot_state(local)
        solid_dot(base, x, y, r)
        a = b.ease(local / V6_IN)
        fr6.putalpha(int(255 * a)); base.alpha_composite(fr6)
        return base

    # opening: footage -> ivory card
    fr = Image.new("RGBA", (b.W, b.H), b.IVORY + (255,))
    if f < DISSOLVE[1]:
        foot = FOOT[min(f, len(FOOT) - 1)].copy()
        a = 1 - b.ease(b.prog(f, DISSOLVE)) if f >= DISSOLVE[0] else 1.0
        foot.putalpha(int(255 * a)); fr.alpha_composite(foot)
    a1, dy1 = fade(f, T1, fin=12, fout=10)
    b.paste(fr, T["t1"], b.CX, 236, a1, dy1)
    a2, dy2 = fade(f, T2)
    b.paste(fr, T["t2"], b.CX, 640, a2, dy2)
    im, (lx, ly), dot_c, dot_r = logo_geom()
    al, _ = fade(f, LOGO_IN)
    if al > 0:
        lim = im.copy(); lim.putalpha(lim.getchannel("A").point(lambda q, k=al: int(q * k)))
        fr.alpha_composite(lim, (lx, ly))
    asv, dsv = fade(f, LINE_IN)
    b.paste(fr, T["svc"], b.CX, ly + im.height + 46, asv, dsv)
    b.paste(fr, T["towns"], b.CX, ly + im.height + 108, asv, dsv)
    if f >= DOT_ON:
        x, y, r = glide_xy(f, dot_c, dot_r)
        solid_dot(fr, x, y, r)
    return fr


b.story_frame = global_frame


def dot_state_global(f):
    return v.dot_state(f - S0) if f >= S0 else (0, 0, 0, 0)


b.dot_state = dot_state_global
b.qa_sq_pos = v.sq_pos
b.QA_DOT_FRAME = S0 + 200
b.QA_SQ_FRAME = S0 + 100
b.QA_BOX_FRAMES = (S0 + 30, S0 + 120, S0 + 200, S0 + 250)


def qa_squirrel_frame(f, R_):
    return v.story_frame(f - S0, R_)


# ------------------------------------------------------------------ sound
def story_audio():
    n = int(b.STORY / FPS * SR); y = np.zeros(n)

    def add(sig, fr_):
        s = int(fr_ / FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    felt, tick = va.felt, va.tick
    G3, D4, E4, G4, A4, B4, D5 = 196.0, 293.66, 329.63, 392.0, 440.0, 493.88, 587.33
    # real parent: quiet, open, unresolved
    add(felt(G3, 0.050, dur=3.0, decay=1.2) + felt(D4, 0.032, dur=3.0, decay=1.2), 0)
    add(felt(B4 / 2, 0.030, dur=2.4, decay=0.9), 48)
    # understanding: a gentle lift as the card appears
    add(felt(E4, 0.045, dur=2.6, decay=1.0) + felt(G4, 0.030, dur=2.6, decay=1.0), 98)
    # useful local service: warm, settled chord with the logo
    add(felt(G4, 0.050, dur=2.6, decay=1.0) + felt(B4, 0.036, dur=2.6, decay=1.0) + felt(D5, 0.026, dur=2.6, decay=1.0), 118)
    # the dot detaches: the soft accent
    add(tick(0.035), GLIDE[0])
    # PASS THE CARE: v6 AUDIO cues, retimed to the new orbit
    marks = [next(f for f in range(0, v.OUT[1] + 1) if v.theta(f) >= 180 * k) for k in (1 / 3, 2 / 3, 0.9)]
    for f_, hz, amp in zip(marks, (G4, B4, D5), (0.10, 0.095, 0.10)):
        add(felt(hz, amp, decay=0.6 if hz != D5 else 0.45), S0 + f_)
    add(felt(B4, 0.085, dur=3.0, decay=0.9) + felt(G4, 0.06, dur=3.0, decay=0.9), S0 + v.RET[0])
    mid = next(f for f in range(v.RET[0], v.RET[1] + 1) if v.theta(f) >= 270)
    add(felt(A4, 0.065, decay=0.6), S0 + mid)
    add(felt(G3, 0.08, dur=2.4, decay=0.8), S0 + v.RET[1])
    y += 0.6 * va.air_trace(n) * (np.arange(n) / SR >= S0 / FPS)
    # deliberate quiet at the qualifying-order pause
    t = np.arange(n) / SR
    q0, q1, q2, q3 = (S0 + v.HOLD[0] - 6) / FPS, (S0 + v.HOLD[0] + 2) / FPS, (S0 + v.HOLD[1] - 4) / FPS, (S0 + v.HOLD[1]) / FPS
    gate = np.ones(n)
    m0 = (t >= q0) & (t < q1); gate[m0] = np.linspace(1, 0.12, m0.sum())
    gate[(t >= q1) & (t < q2)] = 0.12
    m2 = (t >= q2) & (t < q3); gate[m2] = np.linspace(0.12, 1, m2.sum())
    keep = y.copy(); y *= gate; y[t >= q3] = keep[t >= q3]
    return y * 10 ** (ab.STORY_LIFT_DB / 20)


b.story_audio = story_audio
_outro_audio = b.outro_audio


def outro_with_bridge():
    """Official outro track at -3 dB (approved B2 correction) + the B bridge under its silent lead-in."""
    ab.T_OUTRO = b.STORY / FPS                       # bridge timing follows this edit's outro start
    ab.T_CHIME = ab.T_OUTRO + 57 / FPS
    o = _outro_audio() * 10 ** (CHIME_DB / 20)
    total = int(b.N / FPS * SR)
    br = ab.bridge(total) * 10 ** (ab.STORY_LIFT_DB / 20)
    s0 = int(b.STORY / FPS * SR)
    seg = br[s0:s0 + len(o)]
    o[:len(seg)] += seg
    return o


if __name__ == "__main__":
    b.outro_audio = outro_with_bridge
    b.main()
    b.outro_audio = _outro_audio
    R_ = b.build_resources(False)
    global_frame(45, R_).convert("RGB").save(f"{b.OUT}/{b.TAG_PREFIX}_VariantB_cover_parent.png")
    v.story_frame(0, R_, cover=True).convert("RGB").save(f"{b.OUT}/{b.TAG_PREFIX}_VariantB_cover_offer.png")
    print("covers written")

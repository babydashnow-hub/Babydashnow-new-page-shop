#!/usr/bin/env python3
"""
Full Circle - REVIEW v5: the approved "Living Emblem" system with a storytelling orbit.

* The ORIGINAL squirrel is stationary at the centre of the emblem (one uniform downscale,
  7% larger than in the v4 test).
* The official green dot leaves from beneath the squirrel and travels OUT along the right
  half (the referred parent's $5), holds at the top (their qualifying order), and RETURNS
  along the left half (the referrer's $5 reward), closing the circle where it began.
* "Give $5. Get $5." is fully visible at frame 0. While the dot travels out, "Give $5." leads;
  on the way back, "Get $5." leads (the other half stays readable, never hidden).
* The two verified statements appear in sync with the two halves, in full, under the emblem.
* The emblem then hands its dot to the official 6 s outro (unaltered); Variant B CTA.

16.67 s: 320 story frames + 180 outro frames.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle as b

# ------------------------------------------------------------------ format
b.STORY = 320
b.N = b.STORY + 180
b.TAG_PREFIX = "PassTheCare_FullCircle_REVIEW_v5"
b.CTA_IN = b.STORY + 90

# ------------------------------------------------------------------ emblem geometry
b.CX, b.CY, b.R = 540, 940, 315
b.SQ_HEIGHT = 470                 # v4 test used 440
COND_TOP = 1288                   # statements sit under the emblem, never inside it

# ------------------------------------------------------------------ timing (frames)
OUT = (0, 120)                    # 6 -> 3 -> 12 o'clock: the referred parent's $5
HOLD = (120, 150)                 # their qualifying order
RET = (150, 270)                  # 12 -> 9 -> 6 o'clock: the referrer's $5 reward
TH_START = 18.0                   # already travelling at frame 0
b.TXT = {"c1": (6, 148), "c2": (150, 294)}
EMPH = 0.66                       # opacity of the half of the headline that is not leading
FADE = (292, 304)                 # emblem and text leave
BG = (298, 319)                   # ivory lifts to the outro's white
LAND = (294, 316)                 # dot glides to the outro dot's centre
SHRINK = (306, 317)

b.QA_DOT_FRAME = 200
b.QA_BOX_FRAMES = (0, 60, 130, 200, 280)
b.QA_SQ_FRAME = 100


def theta(f):
    if f < OUT[1]:
        return TH_START + (180 - TH_START) * b.ease_from(b.prog(f, OUT), 0.3)
    if f < HOLD[1]:
        return 180.0
    if f < RET[1]:
        return 180 + 180 * b.ease(b.prog(f, RET))
    return 360.0


def dot_state(f):
    th = theta(f)
    x, y = b.ring_xy(th)
    r = b.DOT_R
    if HOLD[0] <= f < HOLD[1]:
        r *= 1 + 0.10 * math.sin(math.pi * b.prog(f, HOLD))
    if f >= LAND[0]:
        p = b.ease(b.prog(f, LAND))
        x, y = x + (b.LAND[0] - x) * p, y + (b.LAND[1] - y) * p
        r = b.DOT_R * (1 - b.ease(b.prog(f, SHRINK))) if f >= SHRINK[0] else r
    return x, y, r, th


b.dot_state = dot_state


def ring_mask(th_end, alpha):
    pad = 40
    box = (b.CX - b.R - pad, b.CY - b.R - pad)
    size = (2 * (b.R + pad), 2 * (b.R + pad))
    SS = 3
    m = Image.new("L", (size[0] * SS, size[1] * SS), 0)
    if th_end > 0.5:
        n = max(2, int(th_end / 0.4))
        pts = []
        for k in range(n + 1):
            a = math.radians(th_end * k / n)
            pts.append(((b.CX + b.R * math.sin(a) - box[0]) * SS, (b.CY + b.R * math.cos(a) - box[1]) * SS))
        ImageDraw.Draw(m).line(pts, fill=255, width=int(round(b.LINE_W * SS)), joint="curve")
    m = m.resize(size, Image.LANCZOS)
    if alpha < 1:
        m = m.point(lambda v: int(v * alpha))
    return box, m


def headline_parts(R_):
    f = b.font(b.LORA, 112, b"Bold")
    give = b.text_img(["Give $5."], f, b.TEXT_GREEN + (255,))
    get = b.text_img(["Get $5."], f, b.TEXT_GREEN + (255,))
    space = f.getlength(" ")
    total = give.width + get.width - 16 + space
    x0 = b.CX - total / 2
    return give, get, x0 + give.width / 2, x0 + give.width - 8 + space + get.width / 2 - 8


def emphasis(f):
    """(give_alpha, get_alpha): both full at frame 0 and at the close; the leading half follows the dot."""
    def blend(f0, f1, a0, a1):
        p = b.ease(b.prog(f, (f0, f1)))
        return a0 + (a1 - a0) * p
    if f < 10:
        return 1.0, 1.0
    if f < 22:
        return 1.0, blend(10, 22, 1.0, EMPH)
    if f < HOLD[1]:
        return 1.0, EMPH
    if f < HOLD[1] + 14:
        return blend(HOLD[1], HOLD[1] + 14, 1.0, EMPH), blend(HOLD[1], HOLD[1] + 14, EMPH, 1.0)
    if f < RET[1]:
        return EMPH, 1.0
    if f < RET[1] + 12:
        return blend(RET[1], RET[1] + 12, EMPH, 1.0), 1.0
    return 1.0, 1.0


SQ_POS = None


def sq_pos(R_):
    global SQ_POS
    if SQ_POS is None:
        a = np.array(R_["sq"].getchannel("A")) > 30
        ys, xs = np.where(a)
        fx, fy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        SQ_POS = (int(round(b.CX - fx)), int(round(b.CY - fy + 6)))
    return SQ_POS


b.qa_sq_pos = sq_pos
HEAD = None


def story_frame(f, R_, cover=False):
    global HEAD
    if HEAD is None:
        HEAD = headline_parts(R_)
    ui = 1 - b.ease(b.prog(f, FADE)) if f >= FADE[0] else 1.0
    bgp = b.ease(b.prog(f, BG)) if f >= BG[0] else 0.0
    bg = tuple(int(round(b.IVORY[i] + (b.WHITE[i] - b.IVORY[i]) * bgp)) for i in range(3))
    fr = Image.new("RGBA", (b.W, b.H), bg + (255,))

    x, y, r, th = dot_state(f)
    box, m = ring_mask(360.0 if cover else th, ui)
    fr.alpha_composite(b.solid(b.GREEN, m), box)
    sx, sy = sq_pos(R_)
    if ui >= 1:
        fr.alpha_composite(R_["sq"], (sx, sy))                       # unaltered, stationary
    else:
        b.paste(fr, R_["sq"], sx + R_["sq"].width / 2, sy, ui)
    if cover:
        x, y = b.ring_xy(0.0); r = b.DOT_R
    if r > 0.3:
        SS, pad = 4, int(r + 4)
        dm = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
        ImageDraw.Draw(dm).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
        dm = dm.resize((pad * 2, pad * 2), Image.LANCZOS)
        fr.alpha_composite(b.solid(b.GREEN, dm), (int(round(x)) - pad, int(round(y)) - pad))

    # label, headline (with leading half), tagline
    b.paste(fr, R_["label"], b.CX + 14, b.LABEL_Y, ui)
    if ui > 0:
        c = tuple(int(bg[i] + (b.TEXT_GREEN[i] - bg[i]) * ui) for i in range(3))
        lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
        ImageDraw.Draw(fr).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=c)
    give, get, gx, tx = HEAD
    ga, ta = (1.0, 1.0) if cover else emphasis(f)
    b.paste(fr, give, gx, b.HEAD_Y, ga * ui)
    b.paste(fr, get, tx, b.HEAD_Y, ta * ui)
    b.paste(fr, R_["tag"], b.CX, b.TAG_Y, ui)
    if not cover:
        for key in ("c1", "c2"):
            a, dy = b.appear(f, b.TXT[key], fin=12, fout=10, rise=10)
            b.paste(fr, R_[key], b.CX, COND_TOP, a * ui, dy)
    return fr


b.story_frame = story_frame


def story_audio():
    SR, n = b.SR, int(b.STORY / b.FPS * b.SR)
    y = np.zeros(n)
    G3, G4, A4, B4, D5 = 196.0, 392.0, 440.0, 493.88, 587.33
    events = [(0, G4, 0.15), (40, B4, 0.12), (82, D5, 0.12),          # out: rising
              (152, D5, 0.10), (196, B4, 0.10), (240, A4, 0.09),      # back: answering; hold 120-150 quiet
              (270, G3, 0.08)]                                        # the circle closes, softly (chime reserved for the outro)
    for fr_, fq, amp in events:
        s = int(fr_ / b.FPS * SR); seg = b.note(fq, amp=amp); e = min(n, s + len(seg))
        y[s:e] += seg[: e - s]
    t = np.arange(n) / SR
    bed = 0.012 * (np.sin(2 * np.pi * 98 * t) + 0.5 * np.sin(2 * np.pi * 147 * t))
    env = np.clip(t / 0.6, 0, 1) * np.clip((b.STORY / b.FPS - 0.4 - t) / 0.8, 0, 1)
    env[int(4.0 * SR):int(5.0 * SR)] *= np.linspace(1, 0.4, int(5.0 * SR) - int(4.0 * SR))
    return y + bed * env


b.story_audio = story_audio

if __name__ == "__main__":
    b.main()
    R_ = b.build_resources(False)
    story_frame(0, R_, cover=True).convert("RGB").save(f"{b.OUT}/{b.TAG_PREFIX}_VariantB_cover.png")
    print("cover written")

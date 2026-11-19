#!/usr/bin/env python3
"""
Full Circle - FINAL REVIEW CANDIDATE v6 (from approved v5 "Living Emblem").

Refinements only:
* Typography matched to the live PASS THE CARE page: headline in Fraunces 700, "passed forward."
  in Fraunces 400 italic (as on the page), statements in Inter (the page's body sans).
* "Give $5. Get $5." stays at full contrast throughout. Emphasis is carried by motion: a fine
  rule in the official green travels under "Give $5." while the dot goes out, glides to
  "Get $5." as the dot turns back, and spans both when the circle closes.
* Hand-off to the outro tightened: the dot arrives at the outro dot's centre and settles to the
  outro's own first-frame size and strength, so only the outro's single blank frame remains.
* Squirrel, dot colour, verified wording, official outro (unaltered) and chime unchanged.

16.67 s: 320 story frames + 180 outro frames.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle as b

# ------------------------------------------------------------------ format
b.STORY = 320
b.N = b.STORY + 180
b.TAG_PREFIX = "PassTheCare_FullCircle_CANDIDATE_v6"
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
FADE = (294, 308)                 # emblem and text leave
BG = (296, 319)                   # ivory lifts to the outro's white
LAND = (292, 312)                 # dot glides to the outro dot's centre
SHRINK = (304, 319)               # ...and settles to the outro's first-frame size/strength
END_R, END_A = 12.5, 0.25         # outro frame 1: ~25 px dot at ~25% strength (measured)
FR700 = b.os.path.join(b.A, "fonts", "fraunces-latin-700-normal.woff2")
FR400I = b.os.path.join(b.A, "fonts", "fraunces-latin-400-italic.woff2")
INTER_REG = b.os.path.join(b.A, "fonts", "Inter-Regular.otf")
b.TAG_Y = 520
b.CTA_Y = 1158                    # clear of the outro (ends y 1099) and above paid-ad bottom bands (Meta 35% = y 1248, TikTok 660 px = y 1260)
b.HEAD_Y = 346

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
        if f >= SHRINK[0]:
            r = b.DOT_R + (END_R - b.DOT_R) * b.ease(b.prog(f, SHRINK))
    return x, y, r, th


def dot_alpha(f):
    return 1.0 + (END_A - 1.0) * b.ease(b.prog(f, SHRINK)) if f >= SHRINK[0] else 1.0


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
    f = b.font(FR700, 108)
    give = b.text_img(["Give $5."], f, b.TEXT_GREEN + (255,))
    get = b.text_img(["Get $5."], f, b.TEXT_GREEN + (255,))
    space = f.getlength(" ")
    total = give.width + get.width - 16 + space
    x0 = b.CX - total / 2
    gx, tx = x0 + give.width / 2, x0 + give.width - 8 + space + get.width / 2 - 8

    def ink(im, cx):
        xs = np.where(np.array(im.getchannel("A")).max(axis=0) > 60)[0]
        return cx - im.width / 2 + xs.min(), cx - im.width / 2 + xs.max()
    asc, _ = f.getmetrics()
    global RULE_Y, SPAN_GIVE, SPAN_GET
    RULE_Y = b.HEAD_Y + 4 + asc + 30
    SPAN_GIVE, SPAN_GET = ink(give, gx), ink(get, tx)
    return give, get, gx, tx


RULE_Y = SPAN_GIVE = SPAN_GET = None


def rule_span(f):
    """Motion-based emphasis: (x0, x1, drawn fraction). Under 'Give $5.' going out,
    glides to 'Get $5.' as the dot turns back, spans both as the circle closes."""
    g0, g1 = SPAN_GIVE
    t0, t1 = SPAN_GET
    if f < HOLD[0] + 4:
        return g0, g1, b.ease(min(1.0, f / 16.0))
    if f < RET[0] + 2:
        p = b.ease(b.prog(f, (HOLD[0] + 4, RET[0] + 2)))
        return g0 + (t0 - g0) * p, g1 + (t1 - g1) * p, 1.0
    if f < RET[1]:
        return t0, t1, 1.0
    p = b.ease(b.prog(f, (RET[1], RET[1] + 16)))
    return t0 + (g0 - t0) * p, t1, 1.0


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


def retype(R_):
    """Replace the v5 type with the live page's families (once)."""
    if R_.get("_v6"):
        return
    tf_b, tf_i = b.font(FR700, 50), b.font(FR400I, 50)
    ta = b.text_img(["A little help, "], tf_b, b.INK + (255,))
    tb = b.text_img(["passed forward."], tf_i, b.TEXT_GREEN + (255,))
    tag = Image.new("RGBA", (ta.width + tb.width - 8, max(ta.height, tb.height)), (0, 0, 0, 0))
    tag.alpha_composite(ta, (0, 0)); tag.alpha_composite(tb, (ta.width - 8, 0))
    R_["tag"] = tag
    cf = b.font(INTER_REG, 40)
    R_["c1"] = b.text_img(b.COND_1, cf, b.SOFT_INK + (255,), leading=1.42)
    R_["c2"] = b.text_img(b.COND_2, cf, b.SOFT_INK + (255,), leading=1.42)
    R_["_v6"] = True


def story_frame(f, R_, cover=False):
    global HEAD
    retype(R_)
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
        if not cover and dot_alpha(f) < 1:
            dm = dm.point(lambda v, k=dot_alpha(f): int(v * k))
        fr.alpha_composite(b.solid(b.GREEN, dm), (int(round(x)) - pad, int(round(y)) - pad))

    # label, headline (with leading half), tagline
    b.paste(fr, R_["label"], b.CX + 14, b.LABEL_Y, ui)
    if ui > 0:
        c = tuple(int(bg[i] + (b.TEXT_GREEN[i] - bg[i]) * ui) for i in range(3))
        lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
        ImageDraw.Draw(fr).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=c)
    give, get, gx, tx = HEAD
    b.paste(fr, give, gx, b.HEAD_Y, ui)                                # full contrast, always
    b.paste(fr, get, tx, b.HEAD_Y, ui)
    if not cover and ui > 0:
        x0, x1, frac = rule_span(f)
        x1 = x0 + (x1 - x0) * frac
        if x1 - x0 > 1:
            SS = 4
            w = int(x1 - x0 + 8)
            mm = Image.new("L", (w * SS, 6 * SS), 0)
            ImageDraw.Draw(mm).rounded_rectangle((4 * SS, 1.5 * SS, (x1 - x0 + 4) * SS, 4.5 * SS), 1.5 * SS, fill=255)
            mm = mm.resize((w, 6), Image.LANCZOS).point(lambda v, k=ui: int(v * k))
            fr.alpha_composite(b.solid(b.GREEN, mm), (int(round(x0 - 4)), int(RULE_Y)))
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

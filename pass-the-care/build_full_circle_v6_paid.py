#!/usr/bin/env python3
"""
Full Circle - PAID-SAFE Variant B (Meta Reels ads + TikTok In-Feed ads), derived from organic v6.

Same story, same assets, same wording; recomposed for the strictest published ad overlays
(intersection of Meta 14% top / 35% bottom / 6% sides and TikTok 240 top / 660 bottom /
120 sides + right icon column x 780-960 for y >= 840):

  essential area: x 120-960, y 270-1248, and x <= 780 below y 840.

* Left-aligned editorial grid at x = 128, like the PASS THE CARE page hero.
* One statement slot directly under the headline: the tagline opens it at frame 0, then the
  two verified statements take it in turn (2 lines each, wider measure, same 40 px Inter).
* The emblem sits on the left of the lower field (centre x 450), clear of TikTok's icon
  column; the squirrel stays large (440 px, the approved v4 size), optically offset (-16, -12 px)
  inside the ring so the travelling dot keeps ~26 px clearance.
* Orbit, rule emphasis, colours, outro (unaltered), CTA position and chime as organic v6.

17.00 s: 330 story frames + 180 outro frames.
"""
import numpy as np
from PIL import Image, ImageDraw

import build_full_circle_v6 as v

b = v.b

b.TAG_PREFIX = "PassTheCare_FullCircle_CANDIDATE_v6_PAIDSAFE"
b.STORY = 330
b.N = b.STORY + 180
b.CTA_IN = b.STORY + 90

LEFT = 128
b.CX, b.CY, b.R = 450, 938, 285
b.SQ_HEIGHT = 440
LABEL_Y, HEAD_Y, SLOT_Y = 286, 326, 488
HEAD_PX = 100

v.FADE = (304, 318)
v.BG = (306, 329)
v.LAND = (302, 322)
v.SHRINK = (314, 329)
SLOT = {"tag": (-20, 28), "c1": (30, 160), "c2": (162, 312)}

C1_LINES = ["They save $5 on their first order", "of $40+ in merchandise."]
C2_LINES = ["You earn a $5 BabyDashNow reward", "when their qualifying order is completed."]
assert " ".join(C1_LINES) == " ".join(b.COND_1) and " ".join(C2_LINES) == " ".join(b.COND_2)

SQ_OFFSET = (-16, -12)            # optical placement inside the ring (measured for dot clearance)


def sq_pos(R_):
    al = np.array(R_["sq"].getchannel("A")) > 30
    ys, xs = np.where(al)
    fx, fy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    return int(round(b.CX - fx + SQ_OFFSET[0])), int(round(b.CY - fy + SQ_OFFSET[1]))


v.sq_pos = sq_pos
b.qa_sq_pos = sq_pos

b.QA_DOT_FRAME = 200
b.QA_BOX_FRAMES = (0, 60, 130, 200, 280)
b.QA_SQ_FRAME = 100


def ltext(lines, fnt, color, leading=1.4):
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * leading)
    w = int(max(fnt.getlength(ln) for ln in lines)) + 8
    h = lh * (len(lines) - 1) + asc + desc + 8
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text((4, 4 + i * lh), ln, font=fnt, fill=color)
    return im


def prepare(R_):
    if R_.get("_paid"):
        return
    fb, fi = b.font(v.FR700, 46), b.font(v.FR400I, 46)
    ta = ltext(["A little help, "], fb, b.INK + (255,))
    tb = ltext(["passed forward."], fi, b.TEXT_GREEN + (255,))
    tag = Image.new("RGBA", (ta.width + tb.width - 8, max(ta.height, tb.height)), (0, 0, 0, 0))
    tag.alpha_composite(ta, (0, 0)); tag.alpha_composite(tb, (ta.width - 8, 0))
    cf = b.font(v.INTER_REG, 40)
    R_["tag"], R_["c1"], R_["c2"] = tag, ltext(C1_LINES, cf, b.SOFT_INK + (255,)), ltext(C2_LINES, cf, b.SOFT_INK + (255,))
    hf = b.font(v.FR700, HEAD_PX)
    give = ltext(["Give $5."], hf, b.TEXT_GREEN + (255,))
    get = ltext(["Get $5."], hf, b.TEXT_GREEN + (255,))
    gx = LEFT - 4
    tx = gx + give.width - 8 + hf.getlength(" ")

    def ink(im, x):
        xs = np.where(np.array(im.getchannel("A")).max(axis=0) > 60)[0]
        return x + xs.min(), x + xs.max()
    asc, _ = hf.getmetrics()
    v.RULE_Y = HEAD_Y + 4 + asc + 26
    v.SPAN_GIVE, v.SPAN_GET = ink(give, gx), ink(get, tx)
    R_["head_parts"] = (give, get, gx, tx)
    R_["_paid"] = True


def put(fr, im, x, y, a=1.0, dy=0.0):
    if a <= 0:
        return
    if a < 1:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda q: int(q * a)))
    fr.alpha_composite(im, (int(round(x)), int(round(y + dy))))


def slot_alpha(f, span, fin=12, fout=10):
    a0, a1 = span
    if f < a0 or f >= a1:
        return 0.0, 0.0
    i = 1.0 if a0 < 0 else b.ease((f - a0) / fin)
    o = 1 - b.ease((f - (a1 - fout)) / fout) if f >= a1 - fout else 1.0
    return min(i, o), 10 * (1 - i)


def story_frame(f, R_, cover=False):
    prepare(R_)
    ui = 1 - b.ease(b.prog(f, v.FADE)) if f >= v.FADE[0] else 1.0
    bgp = b.ease(b.prog(f, v.BG)) if f >= v.BG[0] else 0.0
    bg = tuple(int(round(b.IVORY[i] + (b.WHITE[i] - b.IVORY[i]) * bgp)) for i in range(3))
    fr = Image.new("RGBA", (b.W, b.H), bg + (255,))

    x, y, r, th = v.dot_state(f)
    box, m = v.ring_mask(360.0 if cover else th, ui)
    fr.alpha_composite(b.solid(b.GREEN, m), box)
    sx, sy = v.sq_pos(R_)
    if ui >= 1:
        fr.alpha_composite(R_["sq"], (sx, sy))                           # unaltered, stationary
    else:
        b.paste(fr, R_["sq"], sx + R_["sq"].width / 2, sy, ui)
    if cover:
        x, y = b.ring_xy(0.0); r = b.DOT_R
    if r > 0.3:
        SS, pad = 4, int(r + 4)
        dm = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
        ImageDraw.Draw(dm).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
        dm = dm.resize((pad * 2, pad * 2), Image.LANCZOS)
        if not cover and v.dot_alpha(f) < 1:
            dm = dm.point(lambda q, k=v.dot_alpha(f): int(q * k))
        fr.alpha_composite(b.solid(b.GREEN, dm), (int(round(x)) - pad, int(round(y)) - pad))

    # label (dot + tracked caps), left-aligned
    lab = R_["label"]
    put(fr, lab, LEFT + 30, LABEL_Y, ui)
    if ui > 0:
        c = tuple(int(bg[i] + (b.TEXT_GREEN[i] - bg[i]) * ui) for i in range(3))
        ly = LABEL_Y + lab.height / 2
        ImageDraw.Draw(fr).ellipse((LEFT + 1, ly - 7, LEFT + 15, ly + 7), fill=c)
    give, get, gx, tx = R_["head_parts"]
    put(fr, give, gx, HEAD_Y, ui)                                         # full contrast, always
    put(fr, get, tx, HEAD_Y, ui)
    if not cover and ui > 0:
        x0, x1, frac = v.rule_span(f)
        x1 = x0 + (x1 - x0) * frac
        if x1 - x0 > 1:
            SS = 4
            w = int(x1 - x0 + 8)
            mm = Image.new("L", (w * SS, 6 * SS), 0)
            ImageDraw.Draw(mm).rounded_rectangle((4 * SS, 1.5 * SS, (x1 - x0 + 4) * SS, 4.5 * SS), 1.5 * SS, fill=255)
            mm = mm.resize((w, 6), Image.LANCZOS).point(lambda q, k=ui: int(q * k))
            fr.alpha_composite(b.solid(b.GREEN, mm), (int(round(x0 - 4)), int(v.RULE_Y)))
    if cover:
        put(fr, R_["tag"], LEFT - 4, SLOT_Y)
    else:
        for key in ("tag", "c1", "c2"):
            a, dy = slot_alpha(f, SLOT[key])
            put(fr, R_[key], LEFT - 4, SLOT_Y, a * ui, dy)
    return fr


v.story_frame = story_frame
b.story_frame = story_frame


def story_audio():
    SR, n = b.SR, int(b.STORY / b.FPS * b.SR)
    y = np.zeros(n)
    G3, G4, A4, B4, D5 = 196.0, 392.0, 440.0, 493.88, 587.33
    events = [(0, G4, 0.15), (40, B4, 0.12), (82, D5, 0.12),
              (152, D5, 0.10), (196, B4, 0.10), (240, A4, 0.09), (270, G3, 0.08)]
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

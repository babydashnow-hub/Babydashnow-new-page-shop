#!/usr/bin/env python3
"""
PASS THE CARE(TM) - FINAL FOCUSED REVIEW CANDIDATE v10 (Organic Full Circle v6 baseline).

Hierarchy (one column, centred):
  PASS THE CARE(TM)              small campaign identifier
  Give $5. Get $5.               dominant headline (Fraunces 700, travelling green rule)
  with BabyDashNow(TM)           supporting line
  [original squirrel inside the Full Circle orbit]
  verified statement (1, then 2) synchronized with the dot's outward / return movement
  A little help, passed forward. closing line, low but inside every platform's safe area

Safe area used (conservative organic envelope across Instagram/Facebook Reels and TikTok):
  essential content within y 260-1440 and x 90-930.
Sound: the approved v6 AUDIO cues, the outro-lead-in bridge, the official chime at -3 dB
relative to the story (same waveform and timing).
"""
import numpy as np
from PIL import Image

import build_full_circle_v6 as v
import build_full_circle_v6_audio as va
import audio_ab_v6_bridge as ab

b = v.b
b.TAG_PREFIX = "PassTheCare_FINAL_REVIEW_v10"
b.STORY = 320
b.N = b.STORY + 180
b.CTA_IN = b.STORY + 90

# layout
b.LABEL_Y, b.HEAD_Y = 286, 330
HEAD_PX = 104
WITH_Y = 486
b.CX, b.CY, b.R = 540, 896, 300
b.SQ_HEIGHT = 448
v.COND_TOP = 1230
TAG_LOW_Y = 1374
COND_PX, TAG_PX, WITH_PX = 38, 44, 44
C1_LINES = ["They save $5 on their first order", "of $40+ in merchandise."]
C2_LINES = ["You earn a $5 BabyDashNow reward", "when their qualifying order is completed."]
assert " ".join(C1_LINES) == " ".join(b.COND_1) and " ".join(C2_LINES) == " ".join(b.COND_2)
CHIME_DB = -3.0

b.QA_DOT_FRAME = 200
b.QA_BOX_FRAMES = (0, 60, 130, 200, 280)
b.QA_SQ_FRAME = 100
SQ_OFFSET = (-16, -10)            # optical placement inside the ring (keeps the dot clear of the art)


def sq_pos(R_):
    al = np.array(R_["sq"].getchannel("A")) > 30
    ys, xs = np.where(al)
    fx, fy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    return int(round(b.CX - fx + SQ_OFFSET[0])), int(round(b.CY - fy + SQ_OFFSET[1]))


v.sq_pos = sq_pos
b.qa_sq_pos = sq_pos

_retype_v6 = v.retype
_headline_v6 = v.headline_parts


def headline_parts(R_):
    f = b.font(v.FR700, HEAD_PX)
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
    v.RULE_Y = b.HEAD_Y + 4 + asc + 26
    v.SPAN_GIVE, v.SPAN_GET = ink(give, gx), ink(get, tx)
    return give, get, gx, tx


v.headline_parts = headline_parts


def joined(parts):
    ims = [b.text_img([t], fnt, col + (255,)) for t, fnt, col in parts]
    w = sum(im.width for im in ims) - 8 * (len(ims) - 1)
    im = Image.new("RGBA", (w, max(i.height for i in ims)), (0, 0, 0, 0))
    x = 0
    for i in ims:
        im.alpha_composite(i, (x, 0)); x += i.width - 8
    return im


def retype(R_):
    _retype_v6(R_)
    if R_.get("_v10"):
        return
    # "with BabyDashNow(TM)" takes the slot under the headline (v6 draws R_["tag"] at b.TAG_Y)
    base = joined([("with ", b.font(v.FR400I, WITH_PX), b.SOFT_INK), ("BabyDashNow", b.font(v.FR700, WITH_PX), b.INK)])
    tm = b.text_img(["™"], b.font(b.INTER_MED, 20), b.INK + (255,))        # small superscript TM
    tag = Image.new("RGBA", (base.width + tm.width - 6, base.height), (0, 0, 0, 0))
    tag.alpha_composite(base, (0, 0)); tag.alpha_composite(tm, (base.width - 6, 8))
    R_["tag"] = tag
    b.TAG_Y = WITH_Y
    R_["closing"] = joined([("A little help, ", b.font(v.FR700, TAG_PX), b.INK), ("passed forward.", b.font(v.FR400I, TAG_PX), b.TEXT_GREEN)])
    cf = b.font(v.INTER_REG, COND_PX)
    R_["c1"] = b.text_img(C1_LINES, cf, b.SOFT_INK + (255,), leading=1.32)
    R_["c2"] = b.text_img(C2_LINES, cf, b.SOFT_INK + (255,), leading=1.32)
    R_["_v10"] = True


v.retype = retype
_story_v6 = v.story_frame


def story_frame(f, R_, cover=False):
    fr = _story_v6(f, R_, cover=cover)
    ui = 1 - b.ease(b.prog(f, v.FADE)) if (f >= v.FADE[0] and not cover) else 1.0
    b.paste(fr, R_["closing"], b.CX, TAG_LOW_Y, ui)
    return fr


v.story_frame = story_frame
b.story_frame = story_frame

# sound: approved v6 AUDIO story cues (+2 dB, as in B), bridge, chime -3 dB relative
b.story_audio = lambda: va.story_audio() * 10 ** (ab.STORY_LIFT_DB / 20)
_outro_audio = b.outro_audio


def outro_with_bridge():
    ab.T_OUTRO = b.STORY / b.FPS
    ab.T_CHIME = ab.T_OUTRO + 57 / b.FPS
    o = _outro_audio() * 10 ** (CHIME_DB / 20)
    total = int(b.N / b.FPS * b.SR)
    br = ab.bridge(total) * 10 ** (ab.STORY_LIFT_DB / 20)
    s0 = int(b.STORY / b.FPS * b.SR)
    seg = br[s0:s0 + len(o)]
    o[:len(seg)] += seg
    return o


def cover(R_):
    """Cover: complete composition with statement 1 visible, so the $5 is never shown without its condition."""
    fr = story_frame(0, R_, cover=True)
    b.paste(fr, R_["c1"], b.CX, v.COND_TOP)
    return fr


if __name__ == "__main__":
    b.outro_audio = outro_with_bridge
    b.main()
    b.outro_audio = _outro_audio
    R_ = b.build_resources(False)
    cover(R_).convert("RGB").save(f"{b.OUT}/{b.TAG_PREFIX}_VariantB_cover.png")
    print("cover written")

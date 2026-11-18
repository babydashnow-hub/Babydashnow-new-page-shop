#!/usr/bin/env python3
"""
Full Circle - REVIEW v2: stronger opening, same approved structure.

Opening (0.0-3.0 s): the ORIGINAL static squirrel, framed close on a warm winter
evening - the acorn as the scene's light source (warm falloff to soft evening shadow).
Snow and town-light bokeh were tested and removed: on ivory they read as specks. Implied motion only: the camera drifts and pulls
back; the artwork itself is never redrawn, deformed or animated. The glow then
condenses into the official BabyDashNow green dot and Full Circle continues.

Reuses everything else from build_full_circle.py (text, outro, audio, safeguards).
17.50 s: 345 story frames + the official 180-frame outro.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import build_full_circle as b

# ------------------------------------------------------------------ format / timing
b.STORY = 345
b.N = b.STORY + 180
b.TAG_PREFIX = "PassTheCare_FullCircle_REVIEW_v2"
b.CTA_IN = b.STORY + 90

OPEN_DRIFT = (0, 66)       # close hero framing, gentle forward drift
PULL = (40, 96)            # camera pulls back to the Full Circle layout
SCENE_OUT = (66, 120)      # evening light resolves into the ivory field
SNOW_OUT = (84, 132)
CONDENSE = (72, 96)        # warm glow condenses into the green dot

b.T_FWD = (96, 170)
b.T_PAUSE = (170, 192)
b.T_RET = (192, 324)
b.T_FADE = (326, 338)
b.T_BG = (330, 344)
b.T_LAND = (326, 342)
LAND_SHRINK = (334, 343)
b.TXT = {"c1": (84, 210), "c2": (212, 340)}
b.THETA0 = 0.0

b.QA_DOT_FRAME = 200
b.QA_BOX_FRAMES = (0, 40, 100, 150, 260, 300)
b.QA_SQ_FRAME = 140

# ------------------------------------------------------------------ evening scene (built once)
EDGE = (210, 200, 184)      # warm evening shadow at the frame edges
LIGHT = (250, 242, 226)     # the acorn is the light source
WARM = (246, 206, 146)
HERO_SCALE = 2.0           # close framing = 2x the final squirrel size (still a downscale of the source)
HERO_ACORN = (700, 1150)   # where the acorn sits in the hero frame
random.seed(7)

W, H = b.W, b.H


def lerp(a, c, t):
    return a + (c - a) * t


def gradient():
    """Evening light falling off from the acorn: light at the centre, warm shadow at the edges."""
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    d = np.sqrt((xx - HERO_ACORN[0]) ** 2 + ((yy - HERO_ACORN[1]) * 0.8) ** 2) / 1150
    t = np.clip(d, 0, 1)
    t = t * t * (3 - 2 * t)
    g = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        g[:, :, i] = LIGHT[i] + (EDGE[i] - LIGHT[i]) * t
    return Image.fromarray(g.astype(np.uint8)).convert("RGBA")


def bokeh_layer():
    """Distant town lights far below the vantage point: soft, out of focus, low and sparse."""
    lay = Image.new("RGBA", (W + 200, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(16):
        x = random.uniform(0, W + 200)
        y = random.gauss(1380, 45)
        r = random.uniform(26, 58)
        a = int(random.uniform(60, 120))
        col = random.choice([WARM, (250, 222, 170), (238, 196, 140)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (a,))
    return lay.filter(ImageFilter.GaussianBlur(16))


FLAKES = [dict(x=random.uniform(0, W), y=random.uniform(-200, H), r=random.uniform(1.6, 4.2),
               v=random.uniform(1.2, 2.6), drift=random.uniform(0.4, 1.0), a=random.uniform(0.55, 0.9))
          for _ in range(70)]


def snow_layer(f, alpha):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if alpha <= 0:
        return lay
    d = ImageDraw.Draw(lay)
    for fl in FLAKES:
        y = (fl["y"] + fl["v"] * f) % (H + 200) - 100
        x = (fl["x"] + fl["drift"] * f + 6 * math.sin(f / 30 + fl["x"])) % W
        if y < 600:          # keep the headline zone clear
            continue
        r = fl["r"]
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(255 * fl["a"] * alpha)))
    return lay.filter(ImageFilter.GaussianBlur(0.8))


def glow(radius, strength):
    size = int(radius * 2)
    yy, xx = np.mgrid[:size, :size]
    d = np.sqrt((xx - radius) ** 2 + (yy - radius) ** 2) / radius
    a = np.clip(1 - d, 0, 1) ** 2.2 * 255 * strength
    im = Image.new("RGBA", (size, size), WARM + (0,))
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im


GRAD = BOKEH = None
SRC = None


def setup():
    global GRAD, BOKEH, SRC
    GRAD, BOKEH = gradient(), bokeh_layer()
    SRC = Image.open(b.SQUIRREL)
    SRC.load()


# ------------------------------------------------------------------ squirrel placement (scale + position only)
def squirrel_at(scale_rel, R_):
    """Return the original artwork at scale_rel x the final size, plus its acorn anchor."""
    base = R_["sq"].info["scale"]
    s = base * scale_rel
    if s > 1:
        raise SystemExit("would upscale the squirrel")
    if abs(scale_rel - 1) < 1e-6:
        im = R_["sq"]
    else:
        im = SRC.resize((round(SRC.width * s), round(SRC.height * s)), Image.LANCZOS)
    return im, (b.SQ_ANCHOR_SRC[0] * s, b.SQ_ANCHOR_SRC[1] * s)


def camera(f):
    """Scale of the squirrel relative to final, and where its acorn sits."""
    final = (b.CX, b.CY + b.R)
    p = b.ease(b.prog(f, PULL)) if f >= PULL[0] else 0.0
    drift = b.ease(min(1.0, f / OPEN_DRIFT[1])) if f < PULL[1] else 1.0
    hero = (HERO_ACORN[0] - 56 + 56 * drift, HERO_ACORN[1])      # gentle forward glide (to the right, where it faces)
    push = HERO_SCALE + 0.06 * b.ease(min(1.0, f / PULL[0]))      # a slow breath in before the pull-back
    sc = lerp(push, 1.0, p)
    return sc, (lerp(hero[0], final[0], p), lerp(hero[1], final[1], p))


# ------------------------------------------------------------------ dot (starts at the acorn after the glow condenses)
def dot_state(f):
    if f < b.T_FWD[0]:
        _, (ax, ay) = camera(f)
        r = b.DOT_R * b.ease(b.prog(f, CONDENSE)) if f >= CONDENSE[0] else 0.0
        return ax, ay, r, 0.0
    if f < b.T_FWD[1]:
        th = b.THETA_PAUSE * b.ease(b.prog(f, b.T_FWD))
        x, y = b.ring_xy(th)
        return x, y, b.DOT_R, th
    if f < b.T_PAUSE[1]:
        p = b.prog(f, b.T_PAUSE)
        x, y = b.ring_xy(b.THETA_PAUSE)
        return x, y, b.DOT_R * (1 + 0.10 * math.sin(math.pi * p)), b.THETA_PAUSE
    th = b.THETA_PAUSE + (b.THETA_END - b.THETA_PAUSE) * b.ease(b.prog(f, b.T_RET))
    x, y = b.ring_xy(th)
    r = b.DOT_R
    if f >= b.T_LAND[0]:
        p = b.ease(b.prog(f, b.T_LAND))
        x, y = lerp(x, b.LAND[0], p), lerp(y, b.LAND[1], p)
        r = b.DOT_R * (1 - b.ease(b.prog(f, LAND_SHRINK)))
    return x, y, r, th


b.dot_state = dot_state


def story_frame(f, R_):
    if GRAD is None:
        setup()
    ui = 1 - b.ease(b.prog(f, b.T_FADE)) if f >= b.T_FADE[0] else 1.0
    scene = 1 - b.ease(b.prog(f, SCENE_OUT)) if f >= SCENE_OUT[0] else 1.0
    bgp = b.ease(b.prog(f, b.T_BG)) if f >= b.T_BG[0] else 0.0
    base = tuple(int(round(lerp(b.IVORY[i], b.WHITE[i], bgp))) for i in range(3))

    fr = Image.new("RGBA", (W, H), base + (255,))
    if scene > 0:
        g = GRAD.copy(); g.putalpha(int(255 * scene)); fr.alpha_composite(g)

    sc, (ax, ay) = camera(f)
    sq, (qx, qy) = squirrel_at(sc, R_)
    sx, sy = int(round(ax - qx)), int(round(ay - qy))

    if scene > 0:                                                   # soft contact shadow grounds the figure
        sw = int(260 * sc); sh = int(34 * sc)
        sh_im = Image.new("RGBA", (sw * 2, sh * 4), (0, 0, 0, 0))
        ImageDraw.Draw(sh_im).ellipse((sw / 2, sh * 1.5, sw * 1.5, sh * 2.5), fill=(60, 45, 30, int(70 * scene)))
        sh_im = sh_im.filter(ImageFilter.GaussianBlur(10 * sc))
        feet_y = sy + (1243 * sq.height / SRC.height)
        fr.alpha_composite(sh_im, (int(sx + sq.width * 0.47 - sw), int(feet_y - sh * 2)))
        gl = glow(230 * sc, 0.75 * scene * (0.92 + 0.08 * math.sin(f / 9)))       # warm light behind the acorn
        fr.alpha_composite(gl, (int(ax - gl.width / 2), int(ay - gl.height / 2)))

    # Full Circle trail (behind the squirrel), only once the dot travels
    if f >= b.T_FWD[0]:
        (bx, by), line, _ = b.vector_layer(f, ui)
        fr.alpha_composite(b.solid(b.GREEN, line), (bx, by))

    if ui >= 1:
        fr.alpha_composite(sq, (sx, sy))                            # unaltered pixels
    else:
        b.paste(fr, sq, sx + sq.width / 2, sy, ui)

    if scene > 0:                                                   # glow in front of the acorn, condensing
        c = 1 - b.ease(b.prog(f, CONDENSE)) if f >= CONDENSE[0] else 1.0
        if c > 0:
            gl = glow(70 * sc * (0.4 + 0.6 * c), 0.5 * c * scene)
            fr.alpha_composite(gl, (int(ax - gl.width / 2), int(ay - gl.height / 2)))

    x, y, r, _ = dot_state(f)
    if r > 0.3:
        SS = 4
        pad = int(r + 4)
        m = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
        ImageDraw.Draw(m).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
        m = m.resize((pad * 2, pad * 2), Image.LANCZOS)
        fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x)) - pad, int(round(y)) - pad))


    # text: label + headline + tagline from frame 0 (approved rule), conditions as before
    bgc = fr.getpixel((b.CX, b.LABEL_Y + 14))[:3]
    b.paste(fr, R_["label"], b.CX + 14, b.LABEL_Y, ui)
    if ui > 0:
        col = tuple(int(bgc[i] + (b.TEXT_GREEN[i] - bgc[i]) * ui) for i in range(3))
        lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
        ImageDraw.Draw(fr).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=col)
    b.paste(fr, R_["head"], b.CX, b.HEAD_Y, ui)
    b.paste(fr, R_["tag"], b.CX, b.TAG_Y, ui)
    for key in ("c1", "c2"):
        a, dy = b.appear(f, b.TXT[key])
        b.paste(fr, R_[key], b.CX, b.TEXT_CY - R_[key].height / 2, a * ui, dy)
    return fr


b.story_frame = story_frame


# ------------------------------------------------------------------ audio: same palette, retimed
def story_audio():
    SR, n = b.SR, int(b.STORY / b.FPS * b.SR)
    y = np.zeros(n)
    G3, G4, A4, B4, D5 = 196.0, 392.0, 440.0, 493.88, 587.33
    events = [(0, G3, 0.10), (0, D5 / 2, 0.06),                       # low, open fifth: evening, anticipation
              (84, G4, 0.15),                                        # glow becomes the dot
              (104, B4, 0.12), (128, D5, 0.12),                      # forward
              (200, D5, 0.10), (240, B4, 0.10), (286, A4, 0.09)]     # return; pause 170-192 is quiet
    for fr_, fq, amp in events:
        s = int(fr_ / b.FPS * SR); seg = b.note(fq, dur=2.2 if fr_ == 0 else 1.6, amp=amp); e = min(n, s + len(seg))
        y[s:e] += seg[: e - s]
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)                                  # faint winter air: filtered noise, very low
    air = np.convolve(rng.standard_normal(n), np.ones(400) / 400, mode="same") * 0.05
    airenv = np.clip(t / 0.3, 0, 1) * np.clip((4.0 - t) / 1.5, 0, 1)
    bed = 0.012 * (np.sin(2 * np.pi * 98 * t) + 0.5 * np.sin(2 * np.pi * 147 * t))
    bedenv = np.clip(t / 0.6, 0, 1) * np.clip((b.STORY / b.FPS - 0.4 - t) / 0.8, 0, 1)
    return y + air * airenv + bed * bedenv


b.story_audio = story_audio

if __name__ == "__main__":
    b.main()

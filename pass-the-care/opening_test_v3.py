#!/usr/bin/env python3
"""
Full Circle - OPENING TEST v3 (5.0 s, silent). Review of the opening only; not the advertisement.

Choreography taken from the founder's reference clip (IMG_7219): enter, move,
brief pause, move, stop, attention toward what lies ahead. The ORIGINAL static
squirrel is moved only by rigid transforms (translation, uniform downscale,
rotation <= 1.6 deg) plus true motion blur from sub-frame sampling. The rail
surface is real wood photographed in the same clip (frame at 2.35 s).
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import build_full_circle as b

REF = "/root/.claude/uploads/533057bf-068f-5dc4-985d-7dcc3d40595d/8a5888aa-IMG_7219.mov"
OUTDIR = os.path.join(b.OUT, "opening_test_v3")
W, H, FPS = b.W, b.H, b.FPS
NF = 150

EDGE = (206, 196, 180)
LIGHT_C = (252, 244, 228)
WARM = (246, 206, 146)
LIGHT_POS = (905, 1020)          # the warm light the squirrel travels toward
RAIL_TOP = 1320                  # far edge of the rail top; feet rest 32 px in
HERO = 1.55                      # squirrel size vs. its final Full Circle size
FEET_SRC_Y = 1243                # lowest opaque row of the artwork (feet)

# path of the acorn x-position (screen) during the walk: enter, move, pause, move, stop
KEYS = [(0, 40), (24, 380), (34, 380), (56, 560), (150, 560)]
ease = b.ease


def walk_x(t):
    for (f0, x0), (f1, x1) in zip(KEYS, KEYS[1:]):
        if t <= f1:
            p = (t - f0) / (f1 - f0)
            if f0 == 0:                                   # already moving at frame 0: ease-out only
                p = 1 - (1 - p) ** 2
            else:
                p = ease(p)
            return x0 + (x1 - x0) * p
    return KEYS[-1][1]


def speed(t):
    return abs(walk_x(t + 0.5) - walk_x(t - 0.5))


# ------------------------------------------------------------------ assets
def rail_texture():
    path = os.path.join(OUTDIR, "rail_src.png")
    if not os.path.exists(path):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.35", "-i", REF, "-frames:v", "1", path], check=True)
    im = Image.open(path).convert("RGB")
    im = im.rotate(-1.05, resample=Image.BICUBIC, center=(1080, 2660))       # level the rail
    src = im.crop((0, 2652, 2160, 2990))                                     # rail face only
    a = np.array(src).astype(np.float32)
    low = np.array(src.filter(ImageFilter.GaussianBlur(70))).astype(np.float32)
    a = a / np.maximum(low, 1) * low.mean(axis=(0, 1))                       # flatten cast shadows, keep the grain
    a = (a - a.mean()) * 0.7 + a.mean()
    a = a * np.array([1.06, 0.98, 0.86]) + np.array([8, 2, -6])               # warm, honey-toned pine
    tex = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    face = tex.resize((1620, 190), Image.LANCZOS)
    top = tex.resize((1620, 58), Image.LANCZOS)
    top = Image.fromarray(np.clip(np.array(top).astype(np.float32) * 1.07 + 6, 0, 255).astype(np.uint8))
    rail = Image.new("RGBA", (1620, 58 + 190), (0, 0, 0, 0))
    rail.paste(top, (0, 0)); rail.paste(face, (0, 58))
    # soft top highlight + falloff toward the bottom, so it reads as a crafted beam
    yy = np.linspace(0, 1, rail.height)[:, None]
    shade = (np.clip(1 - yy * 0.55, 0, 1) * 255).astype(np.uint8)
    dark = Image.new("RGBA", rail.size, (60, 45, 30, 0))
    dark.putalpha(Image.fromarray(np.repeat(255 - shade, rail.width, axis=1)).point(lambda v: int(v * 0.35)))
    rail.alpha_composite(dark)
    d = ImageDraw.Draw(rail)
    d.line((0, 58, rail.width, 58), fill=(255, 238, 205, 170), width=3)     # lit front edge
    d.line((0, 0, rail.width, 0), fill=(120, 95, 70, 90), width=2)           # far edge
    return rail


def background():
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    d = np.sqrt((xx - LIGHT_POS[0]) ** 2 + ((yy - LIGHT_POS[1]) * 0.85) ** 2) / 1250
    t = np.clip(d, 0, 1); t = t * t * (3 - 2 * t)
    g = np.zeros((H, W, 3), np.float32)
    for i in range(3):
        g[:, :, i] = LIGHT_C[i] + (EDGE[i] - LIGHT_C[i]) * t
    return Image.fromarray(g.astype(np.uint8)).convert("RGBA")


def glow(radius, strength, col=WARM):
    size = max(2, int(radius * 2))
    yy, xx = np.mgrid[:size, :size]
    d = np.sqrt((xx - radius) ** 2 + (yy - radius) ** 2) / radius
    a = np.clip(1 - d, 0, 1) ** 2.0 * 255 * strength
    im = Image.new("RGBA", (size, size), col + (0,))
    im.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    return im


# ------------------------------------------------------------------ squirrel (rigid transforms only)
SRC = None
CACHE = {}


def squirrel(scale_abs):
    key = round(scale_abs, 4)
    if key not in CACHE:
        CACHE.clear() if len(CACHE) > 40 else None
        CACHE[key] = SRC.resize((round(SRC.width * scale_abs), round(SRC.height * scale_abs)), Image.LANCZOS)
    return CACHE[key]


def place_squirrel(fr, acorn_xy, scale_abs, tilt_deg, alpha=1.0):
    sq = squirrel(scale_abs)
    ax, ay = b.SQ_ANCHOR_SRC[0] * scale_abs, b.SQ_ANCHOR_SRC[1] * scale_abs
    if abs(tilt_deg) > 0.01:                                    # rotate about the feet (weight shift)
        fx, fy = ax, FEET_SRC_Y * scale_abs
        sq = sq.rotate(tilt_deg, resample=Image.BICUBIC, center=(fx, fy))
    x, y = acorn_xy[0] - ax, acorn_xy[1] - ay
    if alpha >= 1:
        fr.alpha_composite(sq, (int(round(x)), int(round(y))))
    else:
        b.paste(fr, sq, x + sq.width / 2, y, alpha)


# ------------------------------------------------------------------ frame
BG = RAIL = R_ = None
FINAL_SCALE = None


def walk_state(t):
    """Acorn position, scale and lean during the walk (t may be fractional for motion blur)."""
    s_abs = FINAL_SCALE * HERO
    x = walk_x(t)
    v = speed(t)
    lean = -min(1.6, v * 0.12)                                  # lean into travel, upright when still
    settle = 0.0
    for stop in (24, 56):                                       # weight settles after each stop
        if stop <= t < stop + 10:
            settle = 3.0 * math.sin(math.pi * (t - stop) / 10)
    feet_to_acorn = (FEET_SRC_Y - b.SQ_ANCHOR_SRC[1]) * s_abs
    return (x, RAIL_TOP + 32 - feet_to_acorn + settle), s_abs, lean


PULL = (104, 136)
SCENE_OUT = (100, 134)
TEXT_IN = (112, 128)


def frame(f):
    final_acorn = (b.CX, b.CY + b.R)
    p = ease(b.prog(f, PULL)) if f >= PULL[0] else 0.0
    scene = 1 - ease(b.prog(f, SCENE_OUT)) if f >= SCENE_OUT[0] else 1.0

    fr = Image.new("RGBA", (W, H), b.IVORY + (255,))
    if scene > 0:
        bg = BG.copy(); bg.putalpha(int(255 * scene)); fr.alpha_composite(bg)
        light = ease(b.prog(f, (44, 84))) if f >= 44 else 0.0          # the light ahead blooms as it stops
        gl = glow(420, (0.40 + 0.50 * light) * scene)
        fr.alpha_composite(gl, (LIGHT_POS[0] - gl.width // 2, LIGHT_POS[1] - gl.height // 2))
        cam = -0.25 * (walk_x(f) - KEYS[0][1])                           # camera follows a little: rail drifts
        rail = RAIL.copy(); rail.putalpha(rail.getchannel("A").point(lambda v: int(v * scene)))
        sh = Image.new("RGBA", (W, 60), (70, 50, 30, 0))                 # soft shadow under the rail
        ImageDraw.Draw(sh).rectangle((0, 18, W, 40), fill=(70, 50, 30, int(55 * scene)))
        fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (0, RAIL_TOP + RAIL.height - 26))
        fr.alpha_composite(rail, (int(-200 + cam), RAIL_TOP))

    # squirrel: walk, then the camera pulls back to the Full Circle position
    if f < PULL[0]:
        subs = [f - 0.33, f, f + 0.33] if speed(f) > 1.0 else [f]          # true motion blur while moving
        if len(subs) == 1:
            (ax, ay), s_abs, lean = walk_state(f)
            # contact shadow
            if scene > 0:
                cs = Image.new("RGBA", (420, 80), (0, 0, 0, 0))
                ImageDraw.Draw(cs).ellipse((40, 30, 380, 52), fill=(60, 40, 25, int(60 * scene)))
                fr.alpha_composite(cs.filter(ImageFilter.GaussianBlur(9)), (int(ax - 330), RAIL_TOP - 8))
            place_squirrel(fr, (ax, ay), s_abs, lean)
        else:
            acc = None
            for t in subs:
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                (ax, ay), s_abs, lean = walk_state(t)
                place_squirrel(layer, (ax, ay), s_abs, lean)
                arr = np.array(layer).astype(np.float32)
                arr[:, :, :3] *= arr[:, :, 3:4] / 255.0                    # premultiply
                acc = arr if acc is None else acc + arr
            acc /= len(subs)
            alpha = acc[:, :, 3:4]
            rgb = np.where(alpha > 0, acc[:, :, :3] * 255.0 / np.maximum(alpha, 1e-3), 0)
            blur = Image.fromarray(np.dstack([rgb, alpha]).clip(0, 255).astype(np.uint8), "RGBA")
            (ax, ay), _, _ = walk_state(f)
            if scene > 0:
                cs = Image.new("RGBA", (420, 80), (0, 0, 0, 0))
                ImageDraw.Draw(cs).ellipse((40, 30, 380, 52), fill=(60, 40, 25, int(60 * scene)))
                fr.alpha_composite(cs.filter(ImageFilter.GaussianBlur(9)), (int(ax - 330), RAIL_TOP - 8))
            fr.alpha_composite(blur)
        acorn = (ax, ay)
    else:
        (wx, wy), s_abs, _ = walk_state(PULL[0])
        s = s_abs + (FINAL_SCALE - s_abs) * p
        acorn = (wx + (final_acorn[0] - wx) * p, wy + (final_acorn[1] - wy) * p)
        place_squirrel(fr, acorn, s, 0.0)

    # the acorn warms, and the warmth becomes the BabyDashNow dot
    warm = ease(b.prog(f, (70, 92))) if f >= 70 else 0.0
    cond = ease(b.prog(f, (92, 106))) if f >= 92 else 0.0
    if warm > 0 and cond < 1:
        g2 = glow(90, 0.55 * warm * (1 - cond))
        fr.alpha_composite(g2, (int(acorn[0] - 90), int(acorn[1] - 90)))
    if f >= 92:
        if f < PULL[1]:
            x, y, r = acorn[0], acorn[1], b.DOT_R * cond
        else:
            th = 40 * ease((f - PULL[1]) / 14)                             # begins its forward arc
            x, y = b.ring_xy(th); r = b.DOT_R
        SS = 4; pad = int(r + 4)
        m = Image.new("L", (pad * 2 * SS, pad * 2 * SS), 0)
        ImageDraw.Draw(m).ellipse(((pad - r) * SS, (pad - r) * SS, (pad + r) * SS, (pad + r) * SS), fill=255)
        m = m.resize((pad * 2, pad * 2), Image.LANCZOS)
        if f >= 120:                                                       # trail behind the squirrel
            pass
        fr.alpha_composite(b.solid(b.GREEN, m), (int(round(x)) - pad, int(round(y)) - pad))

    # reveal: label, Give $5. Get $5., tagline - only after the opening
    a = ease(b.prog(f, TEXT_IN)) if f >= TEXT_IN[0] else 0.0
    if a > 0:
        b.paste(fr, R_["label"], b.CX + 14, b.LABEL_Y, a, 10 * (1 - a))
        lx, ly = b.CX + 14 - R_["label"].width / 2 - 22, b.LABEL_Y + R_["label"].height / 2
        c = tuple(int(b.IVORY[i] + (b.TEXT_GREEN[i] - b.IVORY[i]) * a) for i in range(3))
        ImageDraw.Draw(fr).ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=c)
        b.paste(fr, R_["head"], b.CX, b.HEAD_Y, a, 12 * (1 - a))
        b.paste(fr, R_["tag"], b.CX, b.TAG_Y, a, 12 * (1 - a))
    return fr


def main():
    global BG, RAIL, R_, SRC, FINAL_SCALE
    os.makedirs(OUTDIR, exist_ok=True)
    R_ = b.build_resources(False)
    FINAL_SCALE = R_["sq"].info["scale"]
    if FINAL_SCALE * HERO > 1:
        raise SystemExit("would upscale the squirrel")
    SRC = Image.open(b.SQUIRREL); SRC.load()
    BG, RAIL = background(), rail_texture()
    out = os.path.join(OUTDIR, "PassTheCare_OpeningTest_v3_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(NF):
        im = frame(f).convert("RGB")
        if f in (0, 20, 30, 56, 84, 100, 120, 149):
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
BabyDashNow(TM) animated brand outro - v1 preview renderer.

Geometry and colours are measured from the reference logo (1200x1200 JPEG,
white background). Reference pixels map 1:1 onto the 1080x1920 master, so the
wordmark and tagline are cut straight from the reference and not resampled.
Everything is laid out in reference coordinates, then offset by (OX, OY) into
the final centred lockup.

Outputs (written to ./out):
  *_with_sound.mp4   H.264 1080x1920 30fps + AAC chime       (master)
  *_silent.mp4       H.264 1080x1920 30fps, no audio
  *_alpha.mov        ProRes 4444 with alpha (transparent background)
  *_alpha.webm       VP9 with alpha (transparent background)
  *_final_still.png  final composition
  *_chime.wav        original notification chime (48 kHz mono, 16-bit)

Requires: numpy, Pillow, ffmpeg on PATH.  Run:  python3 build_outro.py
"""
import math
import os
import shutil
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------- paths
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "out")
REF_SRC = "/root/.claude/uploads/eb91e799-d27d-5abd-98d5-847c2b27b4ce/a2ae5bf7-image.jpg"
REF_COPY = os.path.join(ASSETS, "reference_logo.jpg")
VERSION = "v1_PREVIEW"

# ----------------------------------------------------------------- format
W, H, FPS = 1080, 1920, 30
DURATION = 6.00
NFRAMES = int(round(DURATION * FPS))  # 180
SR = 48000

# ----------------------------------------------------------------- brand geometry (reference px)
GREEN = (59, 110, 17)            # sampled from the reference dot centre
WORD_COLOR = (14, 14, 10)        # sampled from wordmark ink
TAG_COLOR = (0, 0, 0)            # sampled from tagline ink
CITY_COLOR = WORD_COLOR
RING_C_REF = (175.75, 602.1)     # symbol centre in reference
RING_R = 60.3                    # ring centre-line radius
RING_W = 1.7                     # ring stroke width
DOT_R = 20.0                     # dot radius (40 px diameter)
WM_BOX = (240, 550, 952, 646)    # wordmark crop (ref px), x0,y0,x1,y1
TAG_BOX = (240, 646, 952, 700)   # tagline crop (ref px)

# Reference lockup spans x 114..948 (width 835). OX centres it on the 1080 canvas;
# OY centres the whole block (lockup + cities line) vertically.
OX, OY = 9, 279
CITIES_Y = 1068                  # centre line of the cities row (master px)
CITIES = "Stamford · Darien · Norwalk · Greenwich"
CITY_SIZE = 28
CITY_TRACK = 1.2

# ----------------------------------------------------------------- timeline (seconds)
T_DOT_IN = (0.00, 0.70)          # scene 01: dot scale-in
T_ORBIT = (0.70, 2.00)           # scene 02: clockwise orbit, ring revealed behind dot
T_CHIME = 2.00                   # scene 03: chime at circle closure
T_SETTLE = (2.00, 2.30)          #           dot settles to centre
T_SLIDE = (2.30, 3.00)           # scene 04: lockup glides into final position
T_WORD = (2.90, 3.50)            #           wordmark reveal (opacity + 14px drift)
T_TAG = (3.50, 4.40)             # scene 05: tagline fade
T_CITY = (4.40, 5.20)            # scene 06: cities fade
#                                  scene 07: hold to 6.00

# Screen-space ring centre during scenes 01-03. The dot appears at the screen
# centre (540, 960), which is the 3 o'clock point of this ring.
START_C = (W / 2 - RING_R, H / 2)
FINAL_C = (RING_C_REF[0] + OX, RING_C_REF[1] + OY)

WM_DRIFT = 14.0


# ----------------------------------------------------------------- easing
def clamp01(p):
    return min(max(p, 0.0), 1.0)


def win(t, a, b):
    return clamp01((t - a) / (b - a))


def ease_io(p):
    p = clamp01(p)
    return 4 * p * p * p if p < 0.5 else 1 - ((-2 * p + 2) ** 3) / 2


def ease_out(p):
    p = clamp01(p)
    return 1 - (1 - p) ** 3


def ease_sine_io(p):
    p = clamp01(p)
    return -(math.cos(math.pi * p) - 1) / 2


# ----------------------------------------------------------------- assets
def build_assets():
    """Cut wordmark and tagline from the reference as alpha-correct RGBA PNGs."""
    os.makedirs(ASSETS, exist_ok=True)
    if not os.path.exists(REF_COPY):
        shutil.copy(REF_SRC, REF_COPY)
    lum = np.asarray(Image.open(REF_COPY).convert("L")).astype(np.float32)

    def cut(box, color, name):
        x0, y0, x1, y1 = box
        L = lum[y0:y1, x0:x1]
        Lc = float(np.mean(color))
        a = np.clip((255.0 - L) / (255.0 - Lc), 0.0, 1.0)
        rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        rgba[..., 0], rgba[..., 1], rgba[..., 2] = color
        rgba[..., 3] = np.round(a * 255).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(os.path.join(ASSETS, name))
        return name

    cut(WM_BOX, WORD_COLOR, "wordmark_BabyDashNow_tm.png")
    cut(TAG_BOX, TAG_COLOR, "tagline_We_show_up_when_it_matters.png")


def load_rgba(name):
    arr = np.asarray(Image.open(os.path.join(ASSETS, name)).convert("RGBA")).astype(np.float32)
    return arr


def font_path():
    for p in ("/usr/share/fonts/opentype/inter/Inter-Regular.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return p
    raise FileNotFoundError("no fallback font found")


def build_cities():
    """Render the cities line once, with manual letter-spacing."""
    font = ImageFont.truetype(font_path(), CITY_SIZE)
    adv = [font.getlength(c) for c in CITIES]
    width = int(sum(adv) + CITY_TRACK * (len(CITIES) - 1)) + 8
    height = CITY_SIZE * 2
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 4.0
    for c, a in zip(CITIES, adv):
        d.text((x, height / 2), c, font=font, fill=CITY_COLOR + (255,), anchor="lm")
        x += a + CITY_TRACK
    return np.asarray(img).astype(np.float32)


# ----------------------------------------------------------------- timeline state
def state(t):
    g = ease_io(win(t, *T_SLIDE))
    gx = START_C[0] + (FINAL_C[0] - START_C[0]) * g
    gy = START_C[1] + (FINAL_C[1] - START_C[1]) * g

    # ring sweep (radians, clockwise from 3 o'clock)
    if t < T_ORBIT[0]:
        sweep = 0.0
    elif t < T_ORBIT[1]:
        sweep = 2 * math.pi * ease_sine_io(win(t, *T_ORBIT))
    else:
        sweep = 2 * math.pi

    # dot angle and radius from ring centre
    theta = sweep
    if t < T_SETTLE[0]:
        rad = RING_R
    elif t < T_SETTLE[1]:
        rad = RING_R * (1 - ease_io(win(t, *T_SETTLE)))
    else:
        rad = 0.0

    # dot size and opacity (scale-in in scene 01)
    dp = ease_out(win(t, *T_DOT_IN))
    dot_scale = 0.5 + 0.5 * dp
    dot_alpha = dp

    dot_x = gx + rad * math.cos(theta)
    dot_y = gy + rad * math.sin(theta)

    return dict(gx=gx, gy=gy, sweep=sweep, dot_x=dot_x, dot_y=dot_y,
                dot_r=DOT_R * dot_scale, dot_alpha=dot_alpha)


# ----------------------------------------------------------------- compositing
def over(canvas, rgb, a, x, y):
    """Composite straight-alpha colour rgb (h,w,3) with coverage a (h,w), 0..1, at (x,y)."""
    h, w = a.shape
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    sx0, sy0 = x0 - x, y0 - y
    sx1, sy1 = sx0 + (x1 - x0), sy0 + (y1 - y0)
    s = a[sy0:sy1, sx0:sx1, None]
    src = rgb[sy0:sy1, sx0:sx1]
    d = canvas[y0:y1, x0:x1]
    da = d[..., 3:4] / 255.0
    oa = s + da * (1 - s)
    col = (src * s + d[..., :3] * da * (1 - s)) / np.maximum(oa, 1e-6)
    d[..., :3] = col
    d[..., 3:4] = oa * 255.0


def draw_symbol(canvas, st):
    """Anti-aliased ring (progressive sweep) and dot, drawn analytically."""
    gx, gy = st["gx"], st["gy"]
    pad = RING_R + DOT_R + 4
    x0, y0 = int(math.floor(gx - pad)), int(math.floor(gy - pad))
    x1, y1 = int(math.ceil(gx + pad)), int(math.ceil(gy + pad))
    xs = np.arange(x0, x1) + 0.5
    ys = np.arange(y0, y1) + 0.5
    X, Y = np.meshgrid(xs, ys)
    alpha = np.zeros(X.shape, np.float32)

    if st["sweep"] > 0:
        dx, dy = X - gx, Y - gy
        r = np.hypot(dx, dy)
        cov_r = np.clip(RING_W / 2 - np.abs(r - RING_R) + 0.5, 0, 1)
        if st["sweep"] >= 2 * math.pi - 1e-9:
            cov_a = 1.0
        else:
            ang = np.mod(np.arctan2(dy, dx), 2 * math.pi)
            cov_a = np.clip((st["sweep"] - ang) * RING_R + 0.5, 0, 1)
        alpha = (cov_r * cov_a).astype(np.float32)

    if st["dot_alpha"] > 0:
        dd = np.hypot(X - st["dot_x"], Y - st["dot_y"])
        a_dot = np.clip(st["dot_r"] - dd + 0.5, 0, 1) * st["dot_alpha"]
        alpha = 1 - (1 - alpha) * (1 - a_dot)

    rgb = np.broadcast_to(np.array(GREEN, np.float32), (y1 - y0, x1 - x0, 3))
    over(canvas, rgb, alpha, x0, y0)


def overlay_asset(canvas, arr, opacity, x, y):
    a = arr[..., 3] / 255.0 * opacity
    over(canvas, arr[..., :3], a.astype(np.float32), x, y)


def render(t, A):
    canvas = np.zeros((H, W, 4), np.float32)
    st = state(t)
    draw_symbol(canvas, st)
    gx, gy = st["gx"], st["gy"]

    # wordmark: opacity reveal with a short horizontal drift
    wp = win(t, *T_WORD)
    w_op = ease_io(wp)
    drift = WM_DRIFT * (1 - ease_out(wp))
    wx = round(gx + (WM_BOX[0] - RING_C_REF[0]) + drift)
    wy = round(gy + (WM_BOX[1] - RING_C_REF[1]))
    if w_op > 0:
        overlay_asset(canvas, A["wordmark"], w_op, wx, wy)

    # tagline: understated fade
    t_op = ease_io(win(t, *T_TAG))
    if t_op > 0:
        tx = round(gx + (TAG_BOX[0] - RING_C_REF[0]))
        ty = round(gy + (TAG_BOX[1] - RING_C_REF[1]))
        overlay_asset(canvas, A["tagline"], t_op, tx, ty)

    # cities: fade, centred under the lockup
    c_op = ease_io(win(t, *T_CITY))
    if c_op > 0:
        cw, ch = A["cities"].shape[1], A["cities"].shape[0]
        overlay_asset(canvas, A["cities"], c_op,
                      round(W / 2 - cw / 2), round(CITIES_Y - ch / 2))
    return canvas


def to_white(canvas):
    a = canvas[..., 3:4] / 255.0
    rgb = canvas[..., :3] * a + 255.0 * (1 - a)
    return np.clip(np.round(rgb), 0, 255).astype(np.uint8)


def to_rgba(canvas):
    return np.clip(np.round(canvas), 0, 255).astype(np.uint8)


# ----------------------------------------------------------------- chime
def make_chime(path):
    """Original, synthesised chime. Starts exactly at T_CHIME (circle closure)."""
    n = int(round(DURATION * SR))
    start = int(round(T_CHIME * SR))
    tt = np.arange(n - start) / SR
    attack = np.minimum(tt / 0.006, 1.0)  # 6 ms onset, no click
    partials = [  # (freq Hz, amplitude, decay time constant s)
        (880.0, 1.00, 0.60),    # A5, body
        (1318.5, 0.42, 0.45),   # E6, perfect fifth above
        (1760.0, 0.16, 0.28),   # A6, soft sparkle
    ]
    y = sum(a * np.sin(2 * math.pi * f * tt) * np.exp(-tt / tau)
            for f, a, tau in partials) * attack
    y = y / np.max(np.abs(y)) * 0.30  # about -10 dBFS peak, subtle
    sig = np.zeros(n)
    sig[start:] = y
    pcm = (sig * 32767).astype("<i2")
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


# ----------------------------------------------------------------- main
def ff(args, stdin=True):
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-s", f"{W}x{H}", "-r", str(FPS)] + args
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def main():
    build_assets()
    os.makedirs(OUT, exist_ok=True)
    A = {
        "wordmark": load_rgba("wordmark_BabyDashNow_tm.png"),
        "tagline": load_rgba("tagline_We_show_up_when_it_matters.png"),
        "cities": build_cities(),
    }
    base = f"BabyDashNow_Outro_{VERSION}"
    p_silent = os.path.join(OUT, f"{base}_silent.mp4")
    p_sound = os.path.join(OUT, f"{base}_with_sound.mp4")
    p_mov = os.path.join(OUT, f"{base}_alpha.mov")
    p_webm = os.path.join(OUT, f"{base}_alpha.webm")
    p_still = os.path.join(OUT, f"{base}_final_still.png")
    p_wav = os.path.join(OUT, f"BabyDashNow_Chime_{VERSION}.wav")

    make_chime(p_wav)

    proc_silent = ff(["-pix_fmt", "rgb24", "-i", "-",
                      "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                      "-c:v", "libx264", "-preset", "slow", "-crf", "14",
                      "-colorspace", "bt709", "-color_primaries", "bt709",
                      "-color_trc", "bt709", "-movflags", "+faststart", p_silent])
    proc_mov = ff(["-pix_fmt", "rgba", "-i", "-",
                   "-c:v", "prores_ks", "-profile:v", "4444",
                   "-pix_fmt", "yuva444p10le", "-vendor", "apl0", p_mov])
    proc_webm = ff(["-pix_fmt", "rgba", "-i", "-",
                    "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0",
                    "-crf", "18", "-auto-alt-ref", "0", "-row-mt", "1", p_webm])

    last = None
    for i in range(NFRAMES):
        c = render(i / FPS, A)
        proc_silent.stdin.write(to_white(c).tobytes())
        proc_mov.stdin.write(to_rgba(c).tobytes())
        proc_webm.stdin.write(to_rgba(c).tobytes())
        last = c
        if i % 30 == 0:
            print(f"frame {i}/{NFRAMES}", flush=True)
    for p in (proc_silent, proc_mov, proc_webm):
        p.stdin.close()
        if p.wait() != 0:
            raise SystemExit("ffmpeg failed")

    Image.fromarray(to_white(last)).save(p_still)

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-i", p_silent, "-i", p_wav,
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-ac", "2", "-t", str(DURATION), "-movflags", "+faststart",
                    p_sound], check=True)
    print("done:", p_sound)


if __name__ == "__main__":
    main()

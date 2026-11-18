#!/usr/bin/env python3
"""
BabyDashNow(TM) PASS THE CARE(TM) - "Full Circle" review renderer.

16.00 s, 1080x1920, 30 fps (480 frames):
  frames   0-299  story (ivory): original static squirrel + official green dot
  frames 300-479  official 6 s BabyDashNow outro, decoded unmodified
                  (Variant B adds "Discover PASS THE CARE(TM)" below it)

The renderer refuses to build a review export unless the ORIGINAL squirrel
artwork is present at assets/squirrel/squirrel_original.png (transparent PNG).
`--layout-test` draws a labelled placeholder instead and stamps every frame
"LAYOUT TEST - NOT FOR REVIEW"; it only writes stills.

Requires numpy, Pillow, ffmpeg/ffprobe.   python3 build_full_circle.py [--variant A|B]
"""
import argparse
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "out")
OUTRO = os.path.join(A, "outro", "BabyDashNow_Official_Outro_Final.mp4")
SQUIRREL = os.path.join(A, "squirrel", "squirrel_original.webp")
LORA = os.path.join(A, "fonts", "Lora-Variable-latin.woff2")
INTER_MED = os.path.join(A, "fonts", "Inter-Medium.otf")
INTER_SEMI = os.path.join(A, "fonts", "Inter-SemiBold.otf")

W, H, FPS = 1080, 1920, 30
N, STORY = 480, 300
SR = 48000

# ------------------------------------------------------------------ colour
GREEN = (59, 110, 17)        # the official outro's own dot/ring value (#3B6E11)
TEXT_GREEN = (45, 97, 17)    # live PASS THE CARE page text green, sampled from the screen recording (#2D6111)
INK = (14, 14, 10)           # the official outro's wordmark ink
SOFT_INK = (74, 74, 66)
IVORY = (245, 243, 237)      # live PASS THE CARE hero panel, sampled from the screen recording (#F5F3ED)
WHITE = (255, 255, 255)      # official outro background

# ------------------------------------------------------------------ copy (live page wording, pending screenshot check)
LABEL = "PASS THE CARE™"
HEADLINE = "Give $5. Get $5."
COND_1 = ["They save $5 on their", "first order of $40+", "in merchandise."]
COND_2 = ["You earn a $5 BabyDashNow", "reward when their qualifying", "order is completed."]
TAG_A, TAG_B = "A little help, ", "passed forward."
CTA_B = "Discover PASS THE CARE™"

# ------------------------------------------------------------------ layout
CX, CY, R = 540, 980, 345
LAND = (540, 960)              # the outro dot's centre
DOT_R = 22.0                   # outro dot radius
LINE_W = 2.2
SQ_HEIGHT = 440                # displayed height of the squirrel figure (px)
SQ_ANCHOR_SRC = (914, 770)     # acorn centre in the source artwork; sits on the 6 o'clock point
LABEL_Y, HEAD_Y, TAG_Y = 296, 352, 500
TEXT_CY = 915                  # centre of the text block inside the circle
CTA_Y = 1236                   # Variant B, under the outro (outro content ends y~1096)

# ------------------------------------------------------------------ timing (frames)
T_FWD = (0, 96)        # dot travels 6 -> 3 -> 12 o'clock, already moving at frame 0
T_PAUSE = (96, 124)     # one slow pulse at 12 o'clock
T_RET = (124, 276)     # 12 -> 9 -> ~7 o'clock, the circle stays open
T_FADE = (276, 290)    # story elements leave
T_BG = (280, 299)      # ivory lifts to the outro's white
T_LAND = (278, 297)    # dot glides to (540, 960) and settles to nothing
TXT = {"c1": (6, 140), "c2": (142, 284)}
CTA_IN = 390
THETA0, THETA_PAUSE, THETA_END = 14.0, 180.0, 328.0


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * t)


def ease_from(t, start=0.3):
    """Ease-in-out entered part-way, so motion is already under way at t=0."""
    e0 = ease(start)
    return (ease(start + (1 - start) * min(max(t, 0), 1)) - e0) / (1 - e0)


def prog(f, span):
    return (f - span[0]) / float(span[1] - span[0])


def ring_xy(theta_deg):
    th = math.radians(theta_deg)  # 0 = 6 o'clock, increasing counter-clockwise on screen (rightwards first)
    return CX + R * math.sin(th), CY + R * math.cos(th)


def dot_state(f):
    """Return (x, y, radius) of the green dot for story frame f."""
    if f < T_FWD[1]:
        th = THETA0 + (THETA_PAUSE - THETA0) * ease_from(prog(f, T_FWD))
        x, y = ring_xy(th); return x, y, DOT_R, th
    if f < T_PAUSE[1]:
        p = prog(f, T_PAUSE)
        x, y = ring_xy(THETA_PAUSE)
        return x, y, DOT_R * (1 + 0.10 * math.sin(math.pi * p)), THETA_PAUSE
    th = THETA_PAUSE + (THETA_END - THETA_PAUSE) * ease(prog(f, T_RET))
    x, y = ring_xy(th)
    if f >= T_LAND[0]:
        p = ease(prog(f, T_LAND))
        x, y = x + (LAND[0] - x) * p, y + (LAND[1] - y) * p
        r = DOT_R * (1 - ease(prog(f, (288, 298))))
        return x, y, r, th
    return x, y, DOT_R, th


# ------------------------------------------------------------------ text
def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_name(weight)
    return f


def text_img(lines, fnt, color, tracking=0.0, leading=1.25):
    """Render centred lines to a tight RGBA image."""
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * leading)
    widths = []
    for ln in lines:
        if tracking:
            widths.append(sum(fnt.getlength(c) for c in ln) + tracking * (len(ln) - 1))
        else:
            widths.append(fnt.getlength(ln))
    w = int(max(widths)) + 8
    h = lh * (len(lines) - 1) + asc + desc + 8
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (w - widths[i]) / 2
        y = 4 + i * lh
        if tracking:
            for c in ln:
                d.text((x, y), c, font=fnt, fill=color)
                x += fnt.getlength(c) + tracking
        else:
            d.text((x, y), ln, font=fnt, fill=color)
    return im


def paste(base, im, cx, top, alpha=1.0, dy=0.0):
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(top + dy))))


def appear(f, span, fin=12, fout=10, rise=12):
    a, b = span
    if f < a or f >= b:
        return 0.0, 0.0
    i = ease((f - a) / fin)
    o = 1 - ease((f - (b - fout)) / fout) if f >= b - fout else 1.0
    return min(i, o), rise * (1 - i)


# ------------------------------------------------------------------ squirrel
def load_squirrel(layout_test):
    if os.path.exists(SQUIRREL):
        im = Image.open(SQUIRREL)
        im.load()
        if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] == 255:
            sys.exit("Squirrel source has no transparency; supply the original transparent artwork.")
        # measure the figure (ignoring faint alpha noise) but never crop or alter the artwork itself
        a = np.array(im.getchannel("A"))
        ys = np.where((a > 30).any(axis=1))[0]
        fig_top, fig_h = int(ys.min()), int(ys.max() - ys.min() + 1)
        s = SQ_HEIGHT / fig_h
        if s > 1:
            sys.exit(f"Squirrel figure is {fig_h}px tall; upscaling refused.")
        size = (round(im.width * s), round(im.height * s))           # one uniform scale factor
        out = im.resize(size, Image.LANCZOS)
        out.info.update(scale=s, anchor=(SQ_ANCHOR_SRC[0] * s, SQ_ANCHOR_SRC[1] * s))
        return out, False
    if not layout_test:
        sys.exit("Missing original squirrel artwork at assets/squirrel/squirrel_original.png - "
                 "review render refused. Use --layout-test for a labelled placeholder.")
    ph = Image.new("RGBA", (360, SQ_HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, 359, SQ_HEIGHT - 1), 40, fill=(200, 196, 186, 255))
    d.text((180, SQ_HEIGHT / 2), "SQUIRREL\nSOURCE\nPENDING", font=font(INTER_SEMI, 34),
           fill=(90, 90, 84, 255), anchor="mm", align="center")
    ph.info.update(scale=1.0, anchor=(180, 0))
    return ph, True


# ------------------------------------------------------------------ story frame
SS = 3  # supersampling for the ring and dot


def vector_layer(f, alpha):
    x, y, r, th = dot_state(f)
    pad = 40
    box = (CX - R - pad, CY - R - pad, CX + R + pad, CY + R + pad)
    bw, bh = box[2] - box[0], box[3] - box[1]
    line = Image.new("L", (bw * SS, bh * SS), 0)
    dot = Image.new("L", (bw * SS, bh * SS), 0)
    dl, dd = ImageDraw.Draw(line), ImageDraw.Draw(dot)
    # trail from 6 o'clock to the dot's angle; drawn in short chords for an even stroke
    end = th
    steps = max(2, int(end / 0.5))
    pts = []
    for k in range(steps + 1):
        t = math.radians(end * k / steps)
        px = (CX + R * math.sin(t) - box[0]) * SS
        py = (CY + R * math.cos(t) - box[1]) * SS
        pts.append((px, py))
    dl.line(pts, fill=255, width=int(round(LINE_W * SS)), joint="curve")
    if r > 0.3:
        cx, cy = (x - box[0]) * SS, (y - box[1]) * SS
        dd.ellipse((cx - r * SS, cy - r * SS, cx + r * SS, cy + r * SS), fill=255)
    line = line.resize((bw, bh), Image.LANCZOS).point(lambda v: int(v * alpha))
    dot = dot.resize((bw, bh), Image.LANCZOS)
    return box[:2], line, dot


def solid(color, mask):
    im = Image.new("RGBA", mask.size, color + (0,))
    im.putalpha(mask)
    return im


def story_frame(f, R_):
    bgp = ease(prog(f, T_BG)) if f >= T_BG[0] else 0.0
    bg = tuple(int(round(IVORY[i] + (WHITE[i] - IVORY[i]) * bgp)) for i in range(3))
    fr = Image.new("RGBA", (W, H), bg + (255,))
    ui = 1 - ease(prog(f, T_FADE)) if f >= T_FADE[0] else 1.0

    (bx, by), line, dot = vector_layer(f, ui)
    fr.alpha_composite(solid(GREEN, line), (bx, by))                      # trail behind the squirrel
    sq = R_["sq"]
    ax, ay = R_["sq_anchor"]
    sx, sy = int(round(CX - ax)), int(round(CY + R - ay))                 # acorn on the 6 o'clock point
    if ui >= 1:
        fr.alpha_composite(sq, (sx, sy))                                  # unaltered pixels
    else:
        paste(fr, sq, sx + sq.width / 2, sy, ui)
    fr.alpha_composite(solid(GREEN, dot), (bx, by))                       # dot in front

    # label + headline: visible at frame 0
    paste(fr, R_["label"], CX + 14, LABEL_Y, ui)
    lw = R_["label"].width
    d = ImageDraw.Draw(fr)
    if ui > 0:
        c = tuple(int(bg[i] + (GREEN[i] - bg[i]) * ui) for i in range(3))
        lx, ly = CX + 14 - lw / 2 - 22, LABEL_Y + R_["label"].height / 2
        d.ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=c)
    paste(fr, R_["head"], CX, HEAD_Y, ui)
    paste(fr, R_["tag"], CX, TAG_Y, ui)
    for key, img in (("c1", R_["c1"]), ("c2", R_["c2"])):
        a, dy = appear(f, TXT[key])
        paste(fr, img, CX, TEXT_CY - img.height / 2, a * ui, dy)
    return fr


def build_resources(layout_test):
    sq, placeholder = load_squirrel(layout_test)
    tf = font(LORA, 48, b"Medium")
    ta = text_img([TAG_A], tf, INK + (255,)); tb = text_img([TAG_B], tf, TEXT_GREEN + (255,))
    tag = Image.new("RGBA", (ta.width + tb.width - 8, max(ta.height, tb.height)), (0, 0, 0, 0))
    tag.alpha_composite(ta, (0, 0)); tag.alpha_composite(tb, (ta.width - 8, 0))
    return {
        "sq": sq, "placeholder": placeholder, "sq_anchor": sq.info["anchor"],
        "label": text_img([LABEL], font(INTER_SEMI, 28), TEXT_GREEN + (255,), tracking=4.5),
        "head": text_img([HEADLINE], font(LORA, 112, b"Bold"), TEXT_GREEN + (255,)),
        "tag": tag,
        "c1": text_img(COND_1, font(LORA, 44, b"Regular"), SOFT_INK + (255,), leading=1.3),
        "c2": text_img(COND_2, font(LORA, 44, b"Regular"), SOFT_INK + (255,), leading=1.3),
        "cta": text_img([CTA_B], font(INTER_MED, 36), TEXT_GREEN + (255,)),
    }


def stamp(fr):
    d = ImageDraw.Draw(fr)
    d.text((W / 2, 60), "LAYOUT TEST - NOT FOR REVIEW", font=font(INTER_SEMI, 30), fill=(200, 40, 40, 255), anchor="mm")


# ------------------------------------------------------------------ audio
def note(freq, dur=1.6, amp=0.18):
    t = np.arange(int(dur * SR)) / SR
    env = (1 - np.exp(-t / 0.008)) * np.exp(-t / 0.55)
    harm = [(1, 1.0), (2, 0.35), (3, 0.12), (4, 0.05)]                 # soft, felt-like
    y = sum(a * np.sin(2 * np.pi * freq * h * t) * np.exp(-t * h * 0.9) for h, a in harm)
    return amp * env * y


def story_audio():
    n = int(STORY / FPS * SR)
    y = np.zeros(n)
    # G major, voiced below the official chime (G5/D6) so the chime resolves the phrase
    G4, A4, B4, D5 = 392.0, 440.0, 493.88, 587.33
    events = [(0, G4, 0.16), (22, B4, 0.13), (44, D5, 0.13),            # forward
              (112, D5, 0.11), (152, B4, 0.11), (198, A4, 0.10)]        # return; pause 75-96 is silent
    for fr, fq, amp in events:
        s = int(fr / FPS * SR); seg = note(fq, amp=amp); e = min(n, s + len(seg))
        y[s:e] += seg[: e - s]
    t = np.arange(n) / SR                                               # very quiet warm bed
    bed = 0.012 * (np.sin(2 * np.pi * 98 * t) + 0.5 * np.sin(2 * np.pi * 147 * t))
    bedenv = np.clip(t / 0.6, 0, 1) * np.clip((STORY / FPS - 0.4 - t) / 0.8, 0, 1)
    bedenv[int(2.5 * SR):int(3.2 * SR)] *= np.linspace(1, 0.35, int(3.2 * SR) - int(2.5 * SR))
    return y + bed * bedenv


def outro_audio():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OUTRO, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def write_wav(path, y):
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):]
    I = float(tail.split("I:")[1].split("LUFS")[0]); TP = float(tail.split("Peak:")[1].split("dBFS")[0])
    return I, TP


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="B", choices=["A", "B"])
    ap.add_argument("--layout-test", action="store_true")
    ap.add_argument("--stills", default="0,40,85,150,240,285,299,357,479")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    R_ = build_resources(args.layout_test)
    test = R_["placeholder"]

    def outro_frames():
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", OUTRO, "-vf", "scale=in_color_matrix=bt709:in_range=tv",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             stdout=subprocess.PIPE)
        while True:
            b = p.stdout.read(W * H * 3)
            if len(b) < W * H * 3:
                break
            yield Image.frombuffer("RGB", (W, H), b).convert("RGBA")

    def frames():
        for f in range(STORY):
            yield story_frame(f, R_)
        for k, fr in enumerate(outro_frames()):
            g = STORY + k
            if args.variant == "B" and g >= CTA_IN:
                a = ease((g - CTA_IN) / 15)
                paste(fr, R_["cta"], CX, CTA_Y, a)
            yield fr

    if test:
        d = os.path.join(OUT, "layout_test"); os.makedirs(d, exist_ok=True)
        want = {int(s) for s in args.stills.split(",")}
        for i, fr in enumerate(frames()):
            if i in want:
                stamp(fr); fr.convert("RGB").save(os.path.join(d, f"layout_test_f{i:03d}.png"))
            if i >= max(want):
                break
        print("Layout-test stills written to", d)
        return

    tag = f"PassTheCare_FullCircle_REVIEW_v1_Variant{args.variant}"
    silent = os.path.join(OUT, tag + "_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-c:v", "libx264", "-profile:v", "high", "-crf", "14",
                            "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries",
                            "bt709", "-color_trc", "bt709", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    count = 0
    for i, fr in enumerate(frames()):
        rgb = fr.convert("RGB")
        if i == 0:
            rgb.save(os.path.join(OUT, tag + "_cover.png"))
        enc.stdin.write(rgb.tobytes()); count += 1
    enc.stdin.close(); enc.wait()
    assert count == N, f"expected {N} frames, wrote {count}"

    mix = np.concatenate([story_audio(), outro_audio()])[: int(N / FPS * SR)]
    raw = os.path.join(OUT, tag + "_mix_raw.wav"); write_wav(raw, mix)
    I, TP = loudness(raw)
    gain_db = min(-14.0 - I, -1.0 - TP)                                   # linear gain only; chime untouched
    final_wav = os.path.join(OUT, tag + "_mix.wav"); write_wav(final_wav, mix * 10 ** (gain_db / 20))
    master = os.path.join(OUT, tag + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", final_wav, "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", master], check=True)
    print(f"Wrote {master}  (pre-gain {I:.1f} LUFS / {TP:.1f} dBTP, gain {gain_db:+.2f} dB)")


if __name__ == "__main__":
    main()

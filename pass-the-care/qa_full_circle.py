#!/usr/bin/env python3
"""Automated checks for the Full Circle review export. Prints JSON-ish lines; used to write QA_REPORT.md."""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

import os
import importlib
b = importlib.import_module(os.environ.get("FC_BUILD", "build_full_circle"))
b = getattr(b, "b", b)  # v2 patches the base module in place

TAG = b.TAG_PREFIX + "_VariantB"
ST = b.STORY
MP4 = f"{b.OUT}/{TAG}.mp4"
W, H = b.W, b.H


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def frames(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", "scale=in_color_matrix=bt709:in_range=tv",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            return
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)


def psnr(a, b_):
    mse = np.mean((a.astype(float) - b_.astype(float)) ** 2)
    return 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def rel_lum(c):
    c = np.array(c) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, c):
    la, lc = sorted([rel_lum(a), rel_lum(c)], reverse=True)
    return (la + 0.05) / (lc + 0.05)


res = {}
probe = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", MP4]).stdout)
v = [s for s in probe["streams"] if s["codec_type"] == "video"][0]
a = [s for s in probe["streams"] if s["codec_type"] == "audio"][0]
res["specs"] = dict(size=f'{v["width"]}x{v["height"]}', fps=v["r_frame_rate"], frames=v.get("nb_frames"),
                    duration=probe["format"]["duration"], vcodec=f'{v["codec_name"]} {v.get("profile")}',
                    pix=v["pix_fmt"], color=v.get("color_space"), acodec=a["codec_name"], ar=a["sample_rate"])

# ---- video: outro fidelity, blank frames, dot colour, CTA clearance
outro = list(frames(b.OUTRO))
out = list(frames(MP4))
res["frame_count"] = len(out)
cta_top, cta_bot = b.CTA_Y - 10, b.CTA_Y + 70
mask = np.ones((H, W), bool); mask[cta_top:cta_bot, :] = False
ps = [psnr(out[ST + k][mask], outro[k][mask]) for k in range(180)]
res["outro_psnr_outside_cta_min_mean"] = (round(min(ps), 2), round(float(np.mean(ps)), 2))
ps_pre = [psnr(out[ST + k], outro[k]) for k in range(90)]
res["outro_psnr_full_frame_before_cta_min"] = round(min(ps_pre), 2)
rows = [np.where((255 - fr.min(axis=2)) > 12)[0] for fr in outro]
lowest = max(r.max() for r in rows if len(r))
res["outro_lowest_content_row"] = int(lowest)
cta_rows = np.where((np.abs(out[-1].astype(int) - outro[179].astype(int)).sum(2) > 120).any(axis=1))[0]
res["cta_rows"] = (int(cta_rows.min()), int(cta_rows.max())) if len(cta_rows) else None
res["cta_clearance_px"] = int(cta_rows.min() - lowest) if len(cta_rows) else None
blank = [i for i, fr in enumerate(out) if fr.std() < 0.5 and fr.mean() < 20]
res["black_frames"] = blank
uniform = [i for i, fr in enumerate(out) if fr.std() < 0.5]
res["uniform_frames"] = uniform


def dot_colour(fr, x, y):
    return tuple(int(c) for c in np.median(fr[y - 6:y + 7, x - 6:x + 7].reshape(-1, 3), axis=0))


QD = getattr(b, "QA_DOT_FRAME", 150)
x, y, r, _ = b.dot_state(QD)
res[f"story_dot_rgb_f{QD}"] = dot_colour(out[QD], int(round(x)), int(round(y)))
res["outro_dot_rgb_outro_f19_in_export"] = dot_colour(out[ST + 19], 540, 960)
res["outro_dot_rgb_f19_in_original"] = dot_colour(outro[19], 540, 960)
lx, ly, lr, _ = b.dot_state(ST - 3)
res["landing_point_f297"] = (round(lx, 1), round(ly, 1), round(lr, 2))

# ---- safe zones (story frames): rows/cols that differ from background
def content_box(fr, bg):
    d = np.abs(fr.astype(int) - np.array(bg)).sum(2) > 24
    ys, xs = np.where(d)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())

boxes = [content_box(out[f], b.IVORY) for f in getattr(b, "QA_BOX_FRAMES", (0, 60, 110, 200, 260))]
res["story_content_bbox_union"] = (min(bx[0] for bx in boxes), min(bx[1] for bx in boxes),
                                   max(bx[2] for bx in boxes), max(bx[3] for bx in boxes))

# ---- squirrel integrity: rendered frame 0 (pre-encode) vs. the source resized on ivory
R_ = b.build_resources(False)
sq = R_["sq"]
src = Image.open(b.SQUIRREL)
res["squirrel_source"] = dict(file=b.SQUIRREL.split("/")[-1], size=src.size, mode=src.mode)
res["squirrel_scale_xy"] = (round(sq.width / src.width, 5), round(sq.height / src.height, 5))
QS = getattr(b, "QA_SQ_FRAME", 0)
f0 = b.story_frame(QS, R_).convert("RGB")
ax, ay = R_["sq_anchor"]; sx, sy = int(round(b.CX - ax)), int(round(b.CY + b.R - ay))
ref = Image.new("RGBA", sq.size, b.IVORY + (255,)); ref.alpha_composite(sq)
crop = np.array(f0.crop((sx, sy, sx + sq.width, sy + sq.height))).astype(int)
refa = np.array(ref.convert("RGB")).astype(int)
dot_free = np.ones(crop.shape[:2], bool)
dx, dy = b.dot_state(QS)[0] - sx, b.dot_state(QS)[1] - sy
yy, xx = np.mgrid[:crop.shape[0], :crop.shape[1]]
dot_free &= (xx - dx) ** 2 + (yy - dy) ** 2 > (b.DOT_R + 4) ** 2
opaque = np.array(sq.getchannel("A")) >= 250
res["squirrel_opaque_px_maxdiff_vs_source"] = int(np.abs(crop - refa)[dot_free & opaque].max())
res["squirrel_opaque_px_checked"] = int((dot_free & opaque).sum())
alpha = np.array(sq.getchannel("A")).astype(int)
fig = alpha > 30
from PIL import ImageFilter
near = np.array(Image.fromarray((fig * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
stray = (~near) & (alpha > 0)
res["squirrel_stray_alpha_px_after_scaling"] = int(stray.sum())
res["squirrel_stray_max_visible_delta"] = int(np.abs(refa - np.array(b.IVORY))[stray].max()) if stray.any() else 0

# ---- text legibility
res["contrast"] = {
    "headline TEXT_GREEN on ivory": round(contrast(b.TEXT_GREEN, b.IVORY), 2),
    "conditions SOFT_INK on ivory": round(contrast(b.SOFT_INK, b.IVORY), 2),
    "tagline INK on ivory": round(contrast(b.INK, b.IVORY), 2),
    "CTA TEXT_GREEN on white": round(contrast(b.TEXT_GREEN, (255, 255, 255)), 2),
}

# ---- audio: loudness, chime intact
r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", MP4, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
tail = r[r.rfind("Summary:"):]
res["loudness_LUFS"] = float(tail.split("I:")[1].split("LUFS")[0])
res["true_peak_dBFS"] = float(tail.split("Peak:")[1].split("dBFS")[0])
mix = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{b.OUT}/{TAG}_mix.wav", "-f", "f32le", "-ac", "1", "-"],
                                   capture_output=True).stdout, np.float32).astype(float)
orig_full = b.outro_audio()
res["outro_audio_tail_trimmed_samples_peak"] = (len(orig_full) - 6 * b.SR, round(float(np.abs(orig_full[6 * b.SR:]).max()), 6))
orig = orig_full[:6 * b.SR]
o0 = int(ST / 30 * b.SR)
seg = mix[o0:o0 + len(orig)]
g = np.dot(seg, orig) / np.dot(orig, orig)
resid = seg - g * orig
res["outro_audio_gain_x"] = round(float(g), 4)
res["outro_audio_residual_dB_rel"] = round(float(20 * np.log10(np.sqrt(np.mean(resid ** 2)) / np.sqrt(np.mean((g * orig) ** 2)))), 1)
dec = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", MP4, "-f", "f32le", "-ac", "1", "-ar", "48000", "-"],
                                   capture_output=True).stdout, np.float32).astype(float)
w0 = ST / 30 + 1.5
win = dec[int(w0 * b.SR):int((w0 + 0.8) * b.SR)]
env = np.abs(win)
on = np.argmax(env > 0.2 * env.max())
res["chime_onset_s_in_export"] = round(w0 + on / b.SR, 4)
res["chime_expected_s"] = round(ST / 30 + 57 / 30, 4)

for k, val in res.items():
    print(f"{k}: {val}")

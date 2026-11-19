#!/usr/bin/env python3
"""
BabyDashNow(TM) brand + conversion Reel - REVIEW CANDIDATE v2 (image-fidelity refinement of v1).

Same storyline, text, logo and direction as v1. Changes:
  * Mother: decoded from the ORIGINAL Pexels 7279098 UHD file (2160x3840, 23.976 fps, 15 Mbps),
    downscaled once with Lanczos to 1080x1920; 23.976 -> 30 fps by frame repetition (no interpolation).
    No grade. (v1 used a 3.1 Mbps 1080p edit, which had lost ~20 % fine detail.)
  * Shopping: original IMG_7019 HLG/BT.2020 4K, HLG -> SDR BT.709 with a neutral tone curve only
    (npl 203, Mobius shoulder). The v1 creative grade (gamma 1.04, contrast 0.96, saturation 0.86,
    warm balance) is REMOVED - it was the cause of the lifted blacks and muted packaging colour.
  * Tighter pacing (10.4 s); longer cart shot with Pampers and wipes together; larger CTA.
  * Brand graphics are never graded: official outro picture untouched, text/CTA in brand colours.
  * Export: x264 High, CRF 12, preset slow, tune film, BT.709 tagged, 4:2:0.
"""
import os
import subprocess

import numpy as np
from PIL import Image

import build_full_circle as b
import build_full_circle_v6 as v6
import build_full_circle_v6_audio as va
import build_brand_ad_v1 as v1

W, H, FPS, SR = b.W, b.H, b.FPS, b.SR
MOM_ORIG = os.path.join(b.A, "originals", "pexels_7279098_uhd_2160x3840.mp4")
SHOP = v1.SHOP
TAG = "BabyDashNow_BrandReel_REVIEW_v2"
OUTDIR = os.path.join(b.OUT, "brand_reel_v2")

MOM_T0 = 0.5                       # same moment as v1
S1 = (0, 69)                       # 2.30 s mother
S2A = (69, 99)                     # 1.00 s shelf  (source 1.15-2.15 s)
S2B = (99, 144)                    # 1.50 s cart, Pampers + wipes together (source 6.78-8.28 s)
SHOP_A, SHOP_B = (1.15, 34), (6.78, 45)
S3 = 132                           # official outro starts; cart dissolves into its white opening (12 frames)
N = S3 + 180                       # 312 frames = 10.40 s
XF = 4
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
CHIME_DB, MUSIC_LIFT_DB = -3.0, 3.3
WHITE = (255, 255, 255)


def decode(path, start, n, pre=None, fps=None):
    chain = ",".join([c for c in (pre, f"fps={fps}" if fps else None,
                                  f"scale={W}:{H}:flags=lanczos+accurate_rnd+full_chroma_int",
                                  "scale=in_color_matrix=bt709:in_range=tv") if c])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start}", "-i", path, "-frames:v", str(n), "-vf", chain,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    k = len(raw) // (W * H * 3)
    return [Image.frombuffer("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]).convert("RGBA") for i in range(k)]


def build_frames():
    mom = decode(MOM_ORIG, MOM_T0, S1[1] + XF, fps=30)
    shop_a = decode(SHOP, SHOP_A[0], SHOP_A[1], TONEMAP)
    shop_b = decode(SHOP, SHOP_B[0], SHOP_B[1], TONEMAP)
    outro = v1.decode(v1.OUTRO, 0.0, 180)
    fa, fi = b.font(v6.FR700, 56), b.font(v6.FR400I, 56)
    ia = b.text_img(["Your hands are "], fa, b.INK + (255,)); ib = b.text_img(["already full."], fi, b.TEXT_GREEN + (255,))
    t1 = Image.new("RGBA", (ia.width + ib.width - 8, max(ia.height, ib.height)), (0, 0, 0, 0))
    t1.alpha_composite(ia, (0, 0)); t1.alpha_composite(ib, (ia.width - 8, 0))
    t2 = v1.shadowed(v1.two_line("We’ll handle", "the essentials.", 72, WHITE, (236, 232, 220)))
    t3 = v1.two_line("Baby essentials,", "delivered locally.", 66, b.INK, b.TEXT_GREEN)
    cta = v1.pill("Order at BabyDashNow.com", size=46)
    scrim = v1.top_scrim(alpha_max=0.5)

    def frame(f):
        if f < S2A[0]:
            fr = mom[f].copy()
        elif f < S2B[0]:
            k = f - S2A[0]; fr = shop_a[min(k, len(shop_a) - 1)].copy()
            if k < XF:
                fr = Image.blend(mom[min(S1[1] + k, len(mom) - 1)].convert("RGB"), fr.convert("RGB"), (k + 1) / (XF + 1)).convert("RGBA")
        elif f < S3:
            k = f - S2B[0]; fr = shop_b[min(k, len(shop_b) - 1)].copy()
            if k < XF:
                fr = Image.blend(shop_a[-1].convert("RGB"), fr.convert("RGB"), (k + 1) / (XF + 1)).convert("RGBA")
        else:
            fr = outro[f - S3].copy()
            k = f - S2B[0]
            if f < S2B[1]:                                            # cart dissolves into the outro's white opening
                p = (f - S3 + 1) / (S2B[1] - S3 + 1)
                fr = Image.blend(shop_b[min(k, len(shop_b) - 1)].convert("RGB"), fr.convert("RGB"), b.ease(p)).convert("RGBA")
        a, dy = v1.appear(f, (4, S1[1]))
        b.paste(fr, t1, W / 2, 292, a, dy)
        if S2A[0] <= f < S2B[1]:
            sa = min(1.0, (f - S2A[0] + 1) / 6) * (1 - b.ease(max(0, f - S3) / (S2B[1] - S3)))
            sc = scrim.copy(); sc.putalpha(sc.getchannel("A").point(lambda q, kk=sa: int(q * kk)))
            fr.alpha_composite(sc, (0, 0))
        a, dy = v1.appear(f, (S2A[0] + 4, S3 + 4))
        b.paste(fr, t2, W / 2, 262, a, dy)
        a, dy = v1.appear(f, (S3 + 6, N + 20), fin=12)
        b.paste(fr, t3, W / 2, 560, a, dy)
        a, dy = v1.appear(f, (S3 + 66, N + 20), fin=12)
        b.paste(fr, cta, W / 2, 1176, a, dy)
        return fr
    return frame


def music():
    n = int(N / FPS * SR); y = np.zeros(n)

    def add(sig, fr_):
        s = int(fr_ / FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    felt = va.felt
    G2, D3, E3, G3, A3, B3, C4, D4, E4, Fs4, G4 = 98.0, 146.83, 164.81, 196.0, 220.0, 246.94, 261.63, 293.66, 329.63, 369.99, 392.0
    chord = lambda notes, amp, d=3.2, dec=1.3: sum(felt(fq, amp * (0.85 if i else 1.0), dur=d, decay=dec) for i, fq in enumerate(notes))
    add(chord([G3, D4, B3], 0.045), 0)
    add(felt(G4, 0.030, decay=0.9), 38)
    add(chord([E3, B3, E4], 0.045), S2A[0])
    add(chord([C4, E4, G3], 0.045), S2B[0])
    add(chord([D3, A3, Fs4], 0.042, d=3.6, dec=1.6), S3)
    t = np.arange(n) / SR
    t_chime = (S3 + 57) / FPS
    bed = 0.010 * (np.sin(2 * np.pi * G2 * t) + 0.5 * np.sin(2 * np.pi * D3 * t))
    y += bed * np.clip(t / 0.5, 0, 1) * np.clip((t_chime - 0.12 - t) / 1.0, 0, 1)
    y *= np.clip((t_chime - 0.12 - t) / 0.35, 0, 1) * (t < t_chime)
    return y


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    frame = build_frames()
    silent = os.path.join(OUTDIR, TAG + "_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "12", "-preset", "slow", "-tune", "film",
                            "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-color_range", "tv", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    for f in range(N):
        im = frame(f).convert("RGB")
        if f in (34, 84, 124, 150, 250, 311):
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        if f == 34:
            im.save(os.path.join(OUTDIR, TAG + "_cover.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    bed = music() * 10 ** (MUSIC_LIFT_DB / 20)
    o = b.outro_audio()[: int(6 * SR)] * 10 ** (CHIME_DB / 20)
    mix = bed.copy(); s0 = int(S3 / FPS * SR); mix[s0:s0 + len(o)] += o[: len(mix) - s0]
    raw = os.path.join(OUTDIR, "mix_raw.wav"); b.write_wav(raw, mix)
    I, TP = b.loudness(raw)
    g = min(-16.0 - I, -1.0 - TP)
    wav = os.path.join(OUTDIR, TAG + "_mix.wav"); b.write_wav(wav, mix * 10 ** (g / 20))
    out = os.path.join(OUTDIR, TAG + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"| pre-gain {I:.1f} LUFS / {TP:.1f} dBTP, gain {g:+.2f} dB")


if __name__ == "__main__":
    main()

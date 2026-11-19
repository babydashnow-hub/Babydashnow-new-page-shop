#!/usr/bin/env python3
"""
BabyDashNow(TM) brand + conversion Reel - REVIEW CANDIDATE v1 (not PASS THE CARE).

Structure (30 fps, 1080x1920):
  0.00-2.67  Scene 1  Pexels 7279098 (clean supplied edit, source 0.5-3.17 s), unaltered
             "Your hands are already full."
  2.67-5.80  Scene 2  BabyDashNow's own shopping footage (IMG_7019, HDR -> SDR, light grade)
             2.67-4.27 hand selects Pampers Swaddlers on the shelf (source 1.00-2.60 s)
             4.27-5.80 the box in the cart beside baby wipes  (source 6.75-8.28 s)
             "We'll handle the essentials."
  5.80-11.80 Scene 3  official 6 s BabyDashNow outro (unaltered picture) with
             "Baby essentials, delivered locally." and the CTA "Order at BabyDashNow.com"
Sound: an original felt-piano bed (synthesised here, no third-party music), bridged under the
outro's silent lead-in; the official chime at -3 dB relative to the bed (same waveform/timing).
Footage audio is not used.
"""
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import build_full_circle as b
import build_full_circle_v6 as v6          # fonts (Fraunces, Inter) and colours as approved
import build_full_circle_v6_audio as va    # felt-piano voice

W, H, FPS, SR = b.W, b.H, b.FPS, b.SR
MOM = os.path.join(b.A, "footage_pexels_7279098_0p5-3p5.mp4")
SHOP = "/root/.claude/uploads/533057bf-068f-5dc4-985d-7dcc3d40595d/06099622-IMG_7019.mov"
OUTRO = b.OUTRO
TAG = "BabyDashNow_BrandReel_REVIEW_v1"
OUTDIR = os.path.join(b.OUT, "brand_reel_v1")

S1 = (0, 80)                       # frames
S2A = (80, 128)                    # shelf
S2B = (128, 174)                   # cart
S3 = 174                           # outro starts (5.80 s)
N = S3 + 180                       # 354 frames = 11.80 s
SHOP_A = (1.00, 48)                # source start (s), frames
SHOP_B = (6.75, 46)
XFADE = 4                          # short, quiet dissolves between shots
GRADE = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
         "tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,"
         "eq=saturation=0.86:contrast=0.96:gamma=1.04,colorbalance=rm=0.03:bm=-0.04:rh=0.02:bh=-0.03")
CHIME_DB = -3.0
MUSIC_LIFT_DB = 3.3
WHITE = (255, 255, 255)


def decode(path, start, n, vf=None):
    chain = (vf + "," if vf else "") + f"scale={W}:{H}:flags=lanczos,scale=in_color_matrix=bt709:in_range=tv"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start}", "-i", path, "-frames:v", str(n), "-vf", chain,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    k = len(raw) // (W * H * 3)
    return [Image.frombuffer("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]).convert("RGBA") for i in range(k)]


def two_line(a, b_, size, col_a, col_b):
    fa, fb = b.font(v6.FR700, size), b.font(v6.FR400I, size)
    ia, ib = b.text_img([a], fa, col_a + (255,)), b.text_img([b_], fb, col_b + (255,))
    w = max(ia.width, ib.width); h = ia.height + ib.height - 16
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.alpha_composite(ia, ((w - ia.width) // 2, 0)); im.alpha_composite(ib, ((w - ib.width) // 2, ia.height - 16))
    return im


def shadowed(im, strength=110, blur=10):
    """Soft, low shadow for white type on footage (no outline, no box)."""
    from PIL import ImageFilter
    a = im.getchannel("A").point(lambda q: int(q * strength / 255))
    sh = Image.new("RGBA", (im.width + 40, im.height + 40), (20, 14, 8, 0))
    m = Image.new("L", sh.size, 0); m.paste(a, (20, 22))
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(blur)))
    sh.alpha_composite(im, (20, 20))
    return sh


def top_scrim(alpha_max=0.58, h=660):
    y = np.linspace(0, 1, h)
    a = alpha_max * np.clip(1 - (np.clip(y - 0.45, 0, 1) / 0.55), 0, 1) ** 1.4
    m = (np.repeat(a[:, None], W, axis=1) * 255).astype(np.uint8)
    im = Image.new("RGBA", (W, h), (24, 18, 10, 0)); im.putalpha(Image.fromarray(m))
    return im


def pill(text, size=40):
    f = b.font(b.INTER_SEMI, size)
    tw = f.getlength(text); asc, desc = f.getmetrics()
    pw, ph = int(tw + 2 * 46), int(asc + desc + 2 * 26)
    SS = 4
    m = Image.new("L", (pw * SS, ph * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pw * SS - 1, ph * SS - 1), radius=ph * SS // 2, fill=255)
    m = m.resize((pw, ph), Image.LANCZOS)
    im = Image.new("RGBA", (pw, ph), b.TEXT_GREEN + (0,)); im.putalpha(m)
    ImageDraw.Draw(im).text((pw / 2, ph / 2 + 1), text, font=f, fill=WHITE + (255,), anchor="mm")
    return im


def appear(f, span, fin=10, fout=8):
    return b.appear(f, span, fin=fin, fout=fout, rise=8)


def build_frames():
    mom = decode(MOM, 0.0, S1[1] + XFADE)
    shop_a = decode(SHOP, SHOP_A[0], SHOP_A[1] + XFADE, GRADE)
    shop_b = decode(SHOP, SHOP_B[0], SHOP_B[1], GRADE)
    outro = decode(OUTRO, 0.0, 180)
    fa, fi = b.font(v6.FR700, 56), b.font(v6.FR400I, 56)
    ia = b.text_img(["Your hands are "], fa, b.INK + (255,)); ib = b.text_img(["already full."], fi, b.TEXT_GREEN + (255,))
    t1 = Image.new("RGBA", (ia.width + ib.width - 8, max(ia.height, ib.height)), (0, 0, 0, 0))
    t1.alpha_composite(ia, (0, 0)); t1.alpha_composite(ib, (ia.width - 8, 0))       # one line, on the clear wall
    t2 = shadowed(two_line("We’ll handle", "the essentials.", 72, WHITE, (236, 232, 220)))
    t3 = two_line("Baby essentials,", "delivered locally.", 66, b.INK, b.TEXT_GREEN)
    cta = pill("Order at BabyDashNow.com")
    scrim = top_scrim()

    def frame(f):
        if f < S2A[0]:
            fr = mom[f].copy()
        elif f < S2B[0]:
            k = f - S2A[0]
            fr = shop_a[k].copy()
            if k < XFADE:                                             # mom -> shelf
                fr = Image.blend(mom[S1[1] + k - XFADE if S1[1] + k - XFADE < len(mom) else -1].convert("RGB"),
                                 fr.convert("RGB"), (k + 1) / (XFADE + 1)).convert("RGBA")
        elif f < S3:
            k = f - S2B[0]
            fr = shop_b[min(k, len(shop_b) - 1)].copy()
            if k < XFADE:                                             # shelf -> cart
                fr = Image.blend(shop_a[min(S2A[1] + k, len(shop_a) - 1)].convert("RGB"), fr.convert("RGB"),
                                 (k + 1) / (XFADE + 1)).convert("RGBA")
            if f >= S3 - 6:                                           # cart -> outro white
                fr = Image.blend(fr.convert("RGB"), Image.new("RGB", (W, H), WHITE), (f - (S3 - 6) + 1) / 7).convert("RGBA")
        else:
            fr = outro[f - S3].copy()
        # on-screen type
        a, dy = appear(f, (4, S1[1]))
        b.paste(fr, t1, W / 2, 292, a, dy)
        if S2A[0] <= f < S3:
            sa = min(1.0, (f - S2A[0] + 1) / 6) * (1 - max(0, f - (S3 - 6)) / 6)
            sc = scrim.copy(); sc.putalpha(sc.getchannel("A").point(lambda q, k=sa: int(q * k)))
            fr.alpha_composite(sc, (0, 0))
        a, dy = appear(f, (S2A[0] + 4, S3 - 2))
        b.paste(fr, t2, W / 2, 262, a, dy)
        a, dy = appear(f, (S3 + 4, N + 20), fin=12)
        b.paste(fr, t3, W / 2, 560, a, dy)
        a, dy = appear(f, (S3 + 78, N + 20), fin=12)
        b.paste(fr, cta, W / 2, 1186, a, dy)
        return fr
    return frame


def music():
    """Original bed: G - Em - C - D, resolving to the official chime's G. Felt-piano voice synthesised here."""
    n = int(N / FPS * SR); y = np.zeros(n)

    def add(sig, fr_):
        s = int(fr_ / FPS * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    felt = va.felt
    G2, D3, E3, G3, A3, B3, C4, D4, E4, Fs4, G4, A4 = 98.0, 146.83, 164.81, 196.0, 220.0, 246.94, 261.63, 293.66, 329.63, 369.99, 392.0, 440.0
    chord = lambda notes, amp, d=3.2, dec=1.3: sum(felt(fq, amp * (0.85 if i else 1.0), dur=d, decay=dec) for i, fq in enumerate(notes))
    add(chord([G3, D4, B3], 0.045), 0)                 # parent: open, quiet
    add(felt(G4, 0.030, decay=0.9), 42)
    add(chord([E3, B3, E4], 0.045), S2A[0])             # shopping: warmth
    add(felt(G4, 0.030, decay=0.9), S2A[0] + 26)
    add(chord([C4, E4, G3], 0.045), S2B[0])             # into the cart
    add(chord([D3, A3, Fs4], 0.042, d=3.6, dec=1.6), S3) # brand: suspended, waiting for the chime's G
    t = np.arange(n) / SR
    bed = 0.010 * (np.sin(2 * np.pi * G2 * t) + 0.5 * np.sin(2 * np.pi * D3 * t))
    t_chime = (S3 + 57) / FPS
    env = np.clip(t / 0.5, 0, 1) * np.clip((t_chime - 0.12 - t) / 1.0, 0, 1)
    y += bed * env
    y *= np.clip((t_chime - 0.12 - t) / 0.35, 0, 1) * (t < t_chime) + (t >= t_chime) * 0.0
    return y


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    frame = build_frames()
    silent = os.path.join(OUTDIR, TAG + "_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                            "-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    for f in range(N):
        im = frame(f).convert("RGB")
        if f in (40, 100, 150, 200, 300, 353):
            im.save(os.path.join(OUTDIR, f"f{f:03d}.png"))
        if f == 40:
            im.save(os.path.join(OUTDIR, TAG + "_cover.png"))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait()
    bed = music() * 10 ** (MUSIC_LIFT_DB / 20)      # bed lifted so the chime is a gentle accent, not a jump
    o = b.outro_audio()[: int(6 * SR)] * 10 ** (CHIME_DB / 20)
    mix = bed.copy(); s0 = int(S3 / FPS * SR); mix[s0:s0 + len(o)] += o[: len(mix) - s0]
    raw = os.path.join(OUTDIR, "mix_raw.wav"); b.write_wav(raw, mix)
    I, TP = b.loudness(raw)
    g = min(-16.0 - I, -1.0 - TP)                     # one linear gain, peak-safe; no compression/limiting
    wav = os.path.join(OUTDIR, TAG + "_mix.wav"); b.write_wav(wav, mix * 10 ** (g / 20))
    out = os.path.join(OUTDIR, TAG + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"| pre-gain {I:.1f} LUFS / {TP:.1f} dBTP, gain {g:+.2f} dB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
BabyDashNow(TM) "For a Special New Mom" - V2 HDR master + review copy.

Picture: original iPhone HLG/BT.2020 10-bit sources, cut frame-exactly, kept in 10-bit YUV throughout
(no RGB round trip, no grading). Only clip A (1440x2560 export) is scaled to 2160x3840. Text is drawn as
HLG graphics (BT.2408: graphics white = 75 % HLG) and composited in the same 10-bit YUV domain.
Dolby Vision: each output frame receives the ORIGINAL camera RPU of the exact source frame it shows, and
the file gets a Dolby Vision 8.4 configuration (profile 8, BL compatibility 4).
Sources are opened read-only.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "pass-the-care"))
import mp4dv                                    # noqa: E402
import build_full_circle_v6_audio as va         # felt-piano voice (original synthesis)  # noqa: E402
import build_full_circle as bfc                 # loudness helper, wav writer  # noqa: E402

U = "/root/.claude/uploads/533057bf-068f-5dc4-985d-7dcc3d40595d/"
FONTS = os.path.join(HERE, "..", "..", "pass-the-care", "assets", "fonts")
LOGO = os.path.join(HERE, "..", "..", "pass-the-care", "assets", "logo", "babydashnow-logo.png")
OUT = os.path.join(HERE, "out")
W, H, FPS, SR = 2160, 3840, 30, 48000

# (shot, id, file, first_frame, frame_count, source_fps, purpose)
EDL = [
    (1, "A", "6a2af4f0-E6A28B63-3737-4971-8332-26A1812ABEFC.mp4", 252, 60, 30, "A hand writes to someone"),
    (2, "A", "6a2af4f0-E6A28B63-3737-4971-8332-26A1812ABEFC.mp4", 314, 55, 30, "Heading completed and revealed"),
    (3, "D", "d3ff4db1-IMG_7306.mov", 102, 30, 30, "An empty box, waiting"),
    (4, "C", "76696015-IMG_7306.mov", 0, 54, 30, "Hands shape a soft bed of paper"),
    (5, "E", "569b4059-IMG_7308.mov", 90, 60, 30, "The swaddle pressed gently in"),
    (6, "G", "4a5690ce-IMG_7315.mov", 84, 48, 30, "Lotion laid in"),
    (7, "H", "d696e046-IMG_7319.mov", 54, 54, 30, "Tissue folded over"),
    (8, "I", "83b39bbf-IMG_7321.mov", 21, 51, 30, "The BabyDashNow card"),
    (9, "J", "ecacd315-IMG_7325.mov", 54, 51, 30000 / 1001, "Sealed: We show up when it matters"),
    (10, "K", "26d3beb0-IMG_7326.mov", 141, 30, 30, "On its way"),
    (11, "P", "66ad8ba5-IMG_7356.mov", 0, 150, 30, "Waiting at her door"),
]
TOTAL = sum(e[4] for e in EDL)                                       # 643 frames = 21.43 s
STARTS = np.cumsum([0] + [e[4] for e in EDL])

TEXT = {
    "open": (6, 108),                                                 # 0.20-3.60 s
    "close": (int(STARTS[10]) + 14, int(STARTS[10]) + 86),            # on the doorstep
    "sign": (int(STARTS[10]) + 92, TOTAL),
}


# ---------------------------------------------------------------- HLG graphics colour (BT.2408-style)
def srgb_to_hlg(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]])
    lin2020 = np.clip(lin @ m.T, 0, 1)
    e = 0.2647 * lin2020                                               # graphics white -> HLG 0.75
    a, b, cc = 0.17883277, 0.28466892, 0.55991073
    return np.where(e <= 1 / 12, np.sqrt(3 * np.maximum(e, 0)), a * np.log(np.maximum(12 * e - b, 1e-9)) + cc)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def layer_from(img_rgba):
    """8-bit sRGB RGBA layer -> rgba64le bytes with HLG-encoded colour (alpha kept)."""
    a = np.asarray(img_rgba).astype(np.float64)
    hlg = srgb_to_hlg(a[..., :3])
    out = np.zeros((H, W, 4), dtype=np.uint16)
    out[..., :3] = np.round(np.clip(hlg, 0, 1) * 65535)
    out[..., 3] = np.round(a[..., 3] / 255 * 65535)
    return out.tobytes()


def text_layer(lines, top, color, shadow=False):
    """lines: [(text, font, color or None)] stacked & centred. Returns RGBA 8-bit full-frame image."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = top
    boxes = []
    for txt, f, col in lines:
        w = d.textlength(txt, font=f)
        boxes.append(((W - w) / 2, y, txt, f, col or color))
        asc, desc = f.getmetrics(); y += asc + desc + int(0.12 * (asc + desc))
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        for x, yy, txt, f, _ in boxes:
            sd.text((x, yy + 6), txt, font=f, fill=(10, 8, 4, 150))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(img)
    for x, yy, txt, f, col in boxes:
        d.text((x, yy), txt, font=f, fill=col + (255,))
    return img


def build_layers():
    os.makedirs(OUT, exist_ok=True)
    ivory = (245, 243, 237); ink = (14, 14, 10); soft = (40, 38, 34)
    L = {}
    L["open"] = text_layer([("For a special new mom.", font("fraunces-latin-400-italic.woff2", 128), None)],
                           top=520, color=ivory, shadow=True)
    L["close"] = text_layer([("Someone thought of you today.", font("fraunces-latin-700-normal.woff2", 100), None)],
                            top=2500, color=ink)
    sign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    logo = Image.open(LOGO).convert("RGBA")
    lw = 1040; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    sign.alpha_composite(logo, ((W - lw) // 2, 2440))
    tag = text_layer([("We show up when it matters.", font("Inter-Medium.otf", 72), None)],
                     top=2440 + logo.height + 40, color=soft)
    L["sign"] = Image.alpha_composite(sign, tag)
    for k, img in L.items():
        open(os.path.join(OUT, f"layer_{k}.rgba64"), "wb").write(layer_from(img))
        img.save(os.path.join(OUT, f"layer_{k}_preview.png"))
    return L


# ---------------------------------------------------------------- picture
def filter_graph():
    parts = []
    for i, (_, sid, f, k0, n, sfps, _) in enumerate(EDL):
        t0 = (k0 - 0.5) / sfps
        if sfps == 30:
            t1 = (k0 + n - 0.5) / sfps
            chain = [f"[{i}:v]trim=start={t0:.6f}:end={t1:.6f}", "setpts=PTS-STARTPTS"]
        else:                                                         # 29.97 -> 30 conform, frame-count exact
            chain = [f"[{i}:v]trim=start={t0:.6f}", "setpts=PTS-STARTPTS", "fps=30", f"trim=end_frame={n}"]
        if sid == "A":
            chain.append("scale=2160:3840:flags=lanczos+accurate_rnd+full_chroma_int:in_range=tv:out_range=tv")
        chain += ["format=yuv420p10le", "setsar=1"]
        parts.append(",".join(chain) + f"[v{i}]")
    parts.append("".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[base]")
    prev = "base"
    for j, key in enumerate(("open", "close", "sign")):
        a, b = TEXT[key]
        idx = len(EDL) + j
        fi, fo = a / FPS, b / FPS
        fade_out = "" if key == "sign" else f",fade=t=out:st={fo - 0.35:.3f}:d=0.35:alpha=1"
        parts.append(f"[{idx}:v]loop=loop=-1:size=1:start=0,setpts=N/{FPS}/TB,trim=end_frame={TOTAL},"
                     f"scale=in_range=pc:out_range=tv:out_color_matrix=bt2020nc,format=yuva420p10le,"
                     f"fade=t=in:st={fi:.3f}:d=0.4:alpha=1{fade_out}[o{j}]")
        parts.append(f"[{prev}][o{j}]overlay=format=yuv420p10:enable='between(t,{fi - 0.01:.3f},{fo:.3f})'[c{j}]")
        prev = f"c{j}"
    return ";".join(parts), prev


def music():
    dur = TOTAL / FPS; n = int(dur * SR); y = np.zeros(n)

    def add(sig, t):
        s = int(t * SR); e = min(n, s + len(sig)); y[s:e] += sig[: e - s]
    felt = va.felt
    G2, D3, G3, A3, B3, C4, D4, E4, Fs4, G4, A4, B4, D5 = 98.0, 146.83, 196.0, 220.0, 246.94, 261.63, 293.66, 329.63, 369.99, 392.0, 440.0, 493.88, 587.33
    s3 = STARTS[2] / FPS; s8 = STARTS[7] / FPS; s9 = STARTS[8] / FPS; s10 = STARTS[9] / FPS; s11 = STARTS[10] / FPS
    add(felt(B3, 0.040, dur=3.0, decay=1.4), 0.25)                     # a single, quiet thought
    add(felt(D4, 0.032, dur=3.0, decay=1.4), 2.2)
    for k, (t, f, a) in enumerate([(s3, G3, .05), (s3 + .9, D4, .045), (s3 + 1.8, G4, .05), (s3 + 3.4, B3, .045),
                                    (s3 + 4.3, D4, .045), (s3 + 5.6, A3, .045), (s3 + 6.6, C4, .045), (s3 + 7.6, E4, .045)]):
        add(felt(f, a, dur=2.6, decay=1.1), t)
    add(felt(G3, .045, dur=3, decay=1.3) + felt(D4, .04, dur=3, decay=1.3), s8)        # the card
    add(felt(B4, .05, dur=3, decay=1.2), s9 + 0.15)                                      # the seal
    add(felt(A4, .04, dur=2.4, decay=1.0), s10)                                          # on its way
    add(felt(G3, .05, dur=5, decay=2.2) + felt(D4, .04, dur=5, decay=2.2) + felt(G4, .045, dur=5, decay=2.2), s11 + 0.2)
    add(felt(D5, .03, dur=4, decay=2.0), s11 + 2.0)
    add(felt(G2, .035, dur=4, decay=2.4) + felt(B3, .03, dur=4, decay=2.4), s11 + 3.4)  # quiet resolution
    t = np.arange(n) / SR
    bed = 0.006 * (np.sin(2 * np.pi * G2 * t) + 0.5 * np.sin(2 * np.pi * D3 * t)) * np.clip((t - s3) / 1.2, 0, 1)
    y += bed * np.clip((dur - 0.6 - t) / 1.5, 0, 1)
    y *= np.clip((dur - t) / 0.4, 0, 1)
    return y


def render_master():
    graph, last = filter_graph()
    wav = os.path.join(OUT, "music_raw.wav"); bfc.write_wav(wav, music())
    I, TP = bfc.loudness(wav)
    g = min(-16.0 - I, -1.0 - TP)
    wavg = os.path.join(OUT, "music.wav"); bfc.write_wav(wavg, music() * 10 ** (g / 20))
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for _, _, f, *_ in EDL:
        cmd += ["-i", U + f]
    for key in ("open", "close", "sign"):
        cmd += ["-f", "rawvideo", "-pix_fmt", "rgba64le", "-s", f"{W}x{H}", "-i", os.path.join(OUT, f"layer_{key}.rgba64")]
    cmd += ["-i", wavg, "-filter_complex", graph, "-map", f"[{last}]", "-map", f"{len(EDL) + 3}:a",
            "-c:v", "libx265", "-preset", "slow", "-pix_fmt", "yuv420p10le", "-profile:v", "main10", "-tag:v", "hvc1",
            "-x265-params", "crf=12:keyint=30:min-keyint=30:bframes=3:colorprim=bt2020:transfer=arib-std-b67:"
                            "colormatrix=bt2020nc:range=limited:chromaloc=0:repeat-headers=1",
            "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            os.path.join(OUT, "master_noDV.mov")]
    subprocess.run(cmd, check=True)
    print(f"music loudness pre-gain {I:.1f} LUFS / {TP:.1f} dBTP, gain {g:+.2f} dB")


def rpu_table():
    """RPU for every output frame = the camera RPU of the exact source frame shown."""
    cache, table = {}, []
    for _, sid, f, k0, n, sfps, _ in EDL:
        if f not in cache:
            cache[f] = mp4dv.source_rpus_ff(U + f)
        r = cache[f]
        keys = sorted(r)
        for j in range(n):
            if sfps == 30:
                target = (k0 + j) / 30
            else:                                                       # fps filter picks nearest source frame
                target = (k0 + j * sfps / 30) / sfps
            pts = min(keys, key=lambda p: abs(p - target))
            table.append((sid, pts, r[pts]))
    return table


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("layers", "all"):
        build_layers()
    if step in ("master", "all"):
        render_master()
    if step in ("inject", "all"):
        tab = rpu_table()
        assert len(tab) == TOTAL
        mp4dv.inject(os.path.join(OUT, "master_noDV.mov"),
                     os.path.join(OUT, "BabyDashNow_ForASpecialNewMom_V2_MASTER_2160x3840_HLG_DV84.mov"),
                     lambda i: tab[i][2],
                     extra_boxes=[mp4dv.sample_entry_box(U + EDL[2][2], b"amve")])
        print("injected", len(tab), "RPUs")

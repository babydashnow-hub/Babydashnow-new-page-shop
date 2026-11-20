#!/usr/bin/env python3
"""
BabyDashNow(TM) New Mom Surprise - Phase 2A Assembly Cut V1 (creative review only).

Straight cuts from the original HLG sources (read-only), per the edit decision list below.
No grading, no effects, no reframing, no text, no music. Audio muted (see report).

Outputs (new-mom-surprise/v1/):
  NewMomSurprise_AssemblyV1_HDR_HLG_1080x1920.mp4  HEVC Main10, BT.2020/HLG - archival HDR master
  NewMomSurprise_AssemblyV1_SDR_REVIEW_1080x1920.mp4  H.264, BT.709 - technical HLG->SDR conversion
"""
import os
import subprocess

SRC = "/root/.claude/uploads/533057bf-068f-5dc4-985d-7dcc3d40595d"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "v1")

# (shot, source file, in, out, purpose) - source seconds; 30 fps sources except J (29.97)
EDL = [
    (1, "D", "d3ff4db1-IMG_7306.mov", 3.40, 4.60, "Curiosity: an empty box"),
    (2, "C", "76696015-IMG_7306.mov", 0.00, 2.40, "Hands begin preparing it (paper fill)"),
    (3, "E", "569b4059-IMG_7308.mov", 2.60, 5.20, "Swaddle placed and pressed in"),
    (4, "F", "0f6549da-IMG_7314.mov", 1.50, 3.40, "Pacifiers placed"),
    (5, "G", "4a5690ce-IMG_7315.mov", 2.60, 4.70, "Lotion laid in"),
    (6, "H", "d696e046-IMG_7319.mov", 1.80, 3.80, "Tissue folded over the gifts"),
    (7, "I", "83b39bbf-IMG_7321.mov", 0.70, 2.60, "BabyDashNow card placed"),
    (8, "J", "ecacd315-IMG_7325.mov", 1.40, 3.50, "Sealed: 'We show up when it matters'"),
    (9, "K", "26d3beb0-IMG_7326.mov", 4.60, 5.80, "Departure: the gift in the car"),
    (10, "P", "66ad8ba5-IMG_7356.mov", 0.00, 4.20, "Delivered: waiting at her door"),
]

HLG_TAGS = ["-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc", "-color_range", "tv"]
SDR_TAGS = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
# Technical HLG -> SDR conversion (identical for every shot; no creative adjustment):
# BT.2100 HLG decoded to linear light with nominal peak 203 cd/m2 (HLG reference white, ITU-R BT.2408),
# BT.2020 -> BT.709 primaries, Mobius shoulder for highlights above reference white, BT.709 OETF.
HLG_TO_SDR = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,"
              "zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv")


def graph(sdr):
    parts = []
    for i, (_, _, _, tin, tout, _) in enumerate(EDL):
        chain = [f"[{i}:v]trim=start={tin}:end={tout}", "setpts=PTS-STARTPTS", "fps=30"]
        # identical downscale for both versions (HLG signal domain), then SDR only: technical conversion
        chain += ["scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int:in_range=tv:out_range=tv",
                  "format=yuv420p10le"]
        if sdr:
            chain += [HLG_TO_SDR, "format=yuv420p"]
        parts.append(",".join(chain) + f"[v{i}]")
    parts.append("".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[vout]")
    return ";".join(parts)


def render(sdr):
    dur = sum(t1 - t0 for *_, t0, t1, _ in [(e[0], e[1], e[2], e[3], e[4], e[5]) for e in EDL])
    name = "NewMomSurprise_AssemblyV1_SDR_REVIEW_1080x1920.mp4" if sdr else "NewMomSurprise_AssemblyV1_HDR_HLG_1080x1920.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for _, _, f, *_ in EDL:
        cmd += ["-i", os.path.join(SRC, f)]
    cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd += ["-filter_complex", graph(sdr), "-map", "[vout]", "-map", f"{len(EDL)}:a"]
    if sdr:
        cmd += ["-c:v", "libx264", "-profile:v", "high", "-crf", "14", "-preset", "slow", "-tune", "film",
                "-pix_fmt", "yuv420p"] + SDR_TAGS
    else:
        cmd += ["-c:v", "libx265", "-pix_fmt", "yuv420p10le", "-tag:v", "hvc1",
                "-x265-params", "crf=14:preset=slow:colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:hdr10=0"] + HLG_TAGS
    cmd += ["-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", os.path.join(OUT, name)]
    subprocess.run(cmd, check=True)
    return name


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    import sys
    for sdr in ((True,) if "--sdr-only" in sys.argv else (False, True)):
        print("wrote", render(sdr))

#!/usr/bin/env python3
"""Technical QA for the V2 master / review copy. Read-only; prints a report (JSON + text)."""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v2 as b   # noqa: E402
import mp4dv           # noqa: E402

U = b.U


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                                     capture_output=True, text=True).stdout)


def frame_side(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries",
                                   "frame=pts_time:frame_side_data=side_data_type", "-of", "json", p],
                                  capture_output=True, text=True).stdout)["frames"]
    rpu = sum(any(sd.get("side_data_type") == "Dolby Vision RPU Data" for sd in f.get("side_data_list", [])) for f in j)
    amb = sum(any(sd.get("side_data_type") == "Ambient viewing environment" for sd in f.get("side_data_list", [])) for f in j)
    return len(j), rpu, amb


def output_rpus(p):
    r = mp4dv.source_rpus_ff(p)
    return [r[k] for k in sorted(r)]


def luma(path, w, h, sel=None, ss=None, vf_extra=""):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.4f}"] if ss is not None else []) + ["-i", path]
    vf = (vf_extra + "," if vf_extra else "") + "format=gray16le"
    if sel is not None:
        vf = f"select=eq(n\\,{sel})," + vf
    cmd += ["-frames:v", "1", "-vf", vf, "-vsync", "0", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint16).reshape(h, w).astype(np.float64) / 64


def ssim(x, y, k=8):
    C1 = (0.01 * 1023) ** 2; C2 = (0.03 * 1023) ** 2
    def blk(a):
        hh, ww = a.shape; a = a[:hh // k * k, :ww // k * k]
        return a.reshape(hh // k, k, ww // k, k).transpose(0, 2, 1, 3).reshape(-1, k * k)
    bx, by = blk(x), blk(y); mx, my = bx.mean(1), by.mean(1); vx, vy = bx.var(1), by.var(1)
    cxy = ((bx - mx[:, None]) * (by - my[:, None])).mean(1)
    return float((((2 * mx * my + C1) * (2 * cxy + C2)) / ((mx ** 2 + my ** 2 + C1) * (vx + vy + C2))).mean())


def run(master, size=(2160, 3840)):
    W, H = size
    rep = {"file": os.path.basename(master), "bytes": os.path.getsize(master), "sha256": sha(master)}
    pr = probe(master)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    rep["video"] = {k: v.get(k) for k in ("codec_name", "profile", "codec_tag_string", "width", "height", "pix_fmt", "r_frame_rate",
                                          "nb_frames", "color_range", "color_space", "color_transfer", "color_primaries", "bit_rate")}
    rep["dovi_config"] = [{k: sd.get(k) for k in ("dv_profile", "dv_level", "rpu_present_flag", "el_present_flag", "bl_present_flag",
                                                  "dv_bl_signal_compatibility_id")}
                          for sd in v.get("side_data_list", []) if sd.get("side_data_type") == "DOVI configuration record"]
    rep["audio"] = [{k: s.get(k) for k in ("codec_name", "channels", "sample_rate", "bit_rate")} for s in a]
    rep["duration"] = pr["format"]["duration"]
    n, rpu, amb = frame_side(master)
    rep["frames_decoded"], rep["frames_with_rpu"], rep["frames_with_ambient"] = n, rpu, amb
    tab = b.rpu_table()
    out = output_rpus(master)
    rep["rpu_identical_to_source_frame"] = sum(1 for i in range(min(len(out), len(tab))) if out[i] == tab[i][2])
    # picture fidelity: per shot, middle frame vs its exact source frame (outside text layers)
    shots = []
    for i, (shot, sid, f, k0, cnt, sfps, _) in enumerate(b.EDL):
        j = cnt // 2; tl = int(b.STARTS[i]) + j
        src_t = (k0 + (j if sfps == 30 else j * sfps / 30)) / sfps
        o = luma(master, W, H, sel=tl)
        if sid == "A":
            s = luma(U + f, 1440, 2560, ss=src_t)
            o = luma(master, 1440, 2560, sel=tl, vf_extra="scale=1440:2560:flags=lanczos")
        else:
            s = luma(U + f, 2160, 3840, ss=src_t)
            if (W, H) != (2160, 3840):
                s = luma(U + f, W, H, ss=src_t, vf_extra=f"scale={W}:{H}:flags=lanczos")
        mask = np.ones_like(o, dtype=bool)
        for key, (fa, fb) in b.TEXT.items():
            if fa <= tl < fb:
                hh = o.shape[0]
                band = {"open": (0.10, 0.22), "close": (0.62, 0.72), "sign": (0.60, 0.78)}[key]
                mask[int(band[0] * hh):int(band[1] * hh), :] = False
        shots.append(dict(shot=shot, src=sid, timeline_frame=tl,
                          mean_diff=round(float(o[mask].mean() - s[mask].mean()), 2),
                          p99_diff=round(float(np.percentile(o[mask], 99) - np.percentile(s[mask], 99)), 2),
                          ssim=round(ssim(np.where(mask, o, 0), np.where(mask, s, 0)), 4)))
    rep["shots"] = shots
    return rep


if __name__ == "__main__":
    master = sys.argv[1]
    size = tuple(int(x) for x in sys.argv[2].split("x")) if len(sys.argv) > 2 else (2160, 3840)
    rep = run(master, size)
    print(json.dumps(rep, indent=1))

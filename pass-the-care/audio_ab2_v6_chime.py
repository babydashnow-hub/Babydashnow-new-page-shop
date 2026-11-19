#!/usr/bin/env python3
"""
Loudness-balance study for the v6 outro chime (picture untouched; excerpts only).

B  = the approved-direction bridge mix (audio_ab_v6_bridge.py), chime at its current level.
B2 = B with ONE controlled change: a static linear gain on the official outro track
     (the chime is the only sound in it). No compression, limiting, EQ or normalisation;
     the chime's waveform shape, tonal character and timing are untouched - it is the
     same samples, scaled.

Measures perceived loudness with EBU R128 momentary loudness (400 ms, K-weighted,
the weighting that tracks how bright sounds like this chime are heard) and reports how
far the chime jumps above (a) the loudest story cue and (b) the 2 s just before it.
"""
import os
import re
import subprocess

import numpy as np

import audio_ab_v6_bridge as ab

b = ab.b
SR = b.SR
OUT = ab.OUT
CANDIDATES_DB = (0.0, -2.0, -3.0, -4.0, -5.0, -6.0)


def momentary(path):
    r = subprocess.run(["ffmpeg", "-v", "verbose", "-hide_banner", "-nostats", "-i", path,
                        "-af", "ebur128=framelog=verbose", "-f", "null", "-"], capture_output=True, text=True).stderr
    rows = [(float(m.group(1)), float(m.group(2)))
            for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(-?[\d.]+)", r)]
    return np.array(rows)


def build(chime_db):
    outro = b.outro_audio()
    total = int(b.N / b.FPS * SR)
    story_b, t = ab.story_untailed()
    fade = np.clip((b.STORY / b.FPS - t) / 0.9, 0, 1)
    sb = story_b * fade * 10 ** (ab.STORY_LIFT_DB / 20)
    x = np.zeros(total); x[:len(sb)] += sb
    x += ab.bridge(total) * 10 ** (ab.STORY_LIFT_DB / 20)
    x *= ab.GAIN_A
    o0 = len(sb)
    x[o0:o0 + len(outro)] += outro[: total - o0] * ab.GAIN_A * 10 ** (chime_db / 20)
    return x


def analyse(x, tag):
    wav = os.path.join(OUT, f"{tag}_full.wav"); b.write_wav(wav, x)
    I, TP = b.loudness(wav)
    m = momentary(wav)

    def mx(t0, t1):
        s = m[(m[:, 0] >= t0) & (m[:, 0] < t1)]
        return s[:, 1].max()
    story = mx(0.5, 10.7)
    pre = mx(10.6, 12.55)
    chime = mx(12.6, 14.2)
    return dict(wav=wav, I=I, TP=TP, story=story, pre=pre, chime=chime,
                jump_story=chime - story, jump_pre=chime - pre,
                cues={k: mx(*w) for k, w in {"outward": (0.5, 4.0), "answer": (5.0, 6.6), "closure": (9.0, 10.4)}.items()})


def main():
    res = {}
    for g in CANDIDATES_DB:
        res[g] = analyse(build(g), f"B2_chime{g:+.0f}dB" if g else "B_bridge_check")
        r = res[g]
        print(f"chime {g:+.0f} dB | {r['I']:.1f} LUFS, {r['TP']:.1f} dBTP | max momentary: story {r['story']:.1f} "
              f"(outward {r['cues']['outward']:.1f}, answer {r['cues']['answer']:.1f}, closure {r['cues']['closure']:.1f}), "
              f"lead-in {r['pre']:.1f}, chime {r['chime']:.1f} | chime above loudest cue {r['jump_story']:+.1f} LU, "
              f"above preceding 2 s {r['jump_pre']:+.1f} LU")
    return res


if __name__ == "__main__":
    main()

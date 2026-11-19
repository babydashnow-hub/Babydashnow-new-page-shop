#!/usr/bin/env python3
"""
A/B audio comparison for Organic v6 AUDIO (picture untouched): the outro lead-in.

A = current approved-concept mix (v6 AUDIO): story cues, then 1.9 s of digital silence
    while the outro dot orbits, then the official chime.
B = proposal:
    1. Bridge: the closing G-major material of the story continues UNDER the outro's
       silent lead-in - the same felt-piano voice and the same low bed, nothing new:
         - the story's low bed (G2/D3 sines, as used throughout) is no longer cut at 10.67 s;
           it carries on at -40 dBFS and fades out completely before the chime;
         - one soft re-voicing of the story's own closing interval (G3 + D4) as the outro dot
           appears, decaying into the ring's closure.
       The bridge stops 120 ms before the chime, so the chime enters on clean air.
    2. Balance: the story cues are lifted +2.0 dB relative to the outro, narrowing the gap to
       the chime without touching it (linear gain, no compression, no limiting).
    The official outro track is mixed sample-for-sample unchanged (one linear gain, identical
    to A's), so the chime's waveform, level and timing are identical in A and B.

Outputs short excerpts (8.5-14.5 s, v6 picture) and full-length WAVs for measurement only.
No new master is rendered.
"""
import os
import subprocess

import numpy as np

import build_full_circle_v6_audio as a

b = a.b
SR, FPS = b.SR, b.FPS
OUT = os.path.join(b.OUT, "audio_ab_v6")
SILENT = os.path.join(b.OUT, "PassTheCare_FullCircle_CANDIDATE_v6_AUDIO_VariantB_silent.mp4")
T_OUTRO = b.STORY / FPS                         # 10.667 s
T_CHIME = T_OUTRO + 57 / FPS                    # 12.567 s (outro ring closure)
GAIN_A = 10 ** (10.10 / 20)                     # the global linear gain the A master used
STORY_LIFT_DB = 2.0


def story_untailed():
    """The v6 AUDIO story layer without its final fade (the fade is re-applied by the bridge)."""
    n = int(b.STORY / FPS * SR)
    t = np.arange(n) / SR
    y = a.story_audio()
    tail = np.clip((b.STORY / FPS - t) / 0.9, 0, 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        y = np.where(tail > 1e-3, y / np.maximum(tail, 1e-3), 0.0)
    return y, t


def bridge(total_n):
    t = np.arange(total_n) / SR
    y = np.zeros(total_n)
    # same bed as the story (98/147 Hz), continued at a low level and gone before the chime
    bed = 0.006 * (np.sin(2 * np.pi * 98 * t) + 0.5 * np.sin(2 * np.pi * 147 * t))
    env = np.clip((t - (T_OUTRO - 1.2)) / 0.8, 0, 1) * np.clip((T_CHIME - 0.12 - t) / 1.1, 0, 1)
    y += bed * env
    # one soft re-voicing of the closing interval (G3 + D4) as the outro dot appears
    s = int((T_OUTRO + 2 / FPS) * SR)
    note = a.felt(196.0, 0.035, dur=2.2, decay=0.7) + a.felt(293.66, 0.022, dur=2.2, decay=0.7)
    e = min(total_n, s + len(note)); y[s:e] += note[: e - s]
    y *= np.clip((T_CHIME - 0.12 - t) / 0.35, 0, 1)        # clean air for the chime
    return y


def mixes():
    outro = b.outro_audio()
    total = int(b.N / FPS * SR)
    story_a = a.story_audio()
    A = np.zeros(total); A[:len(story_a)] += story_a
    o0 = len(story_a); A[o0:o0 + len(outro)] += outro[: total - o0]
    A *= GAIN_A

    story_b, t = story_untailed()
    fade = np.clip((b.STORY / FPS - t) / 0.9, 0, 1)
    sb = story_b * fade * 10 ** (STORY_LIFT_DB / 20)
    B = np.zeros(total); B[:len(sb)] += sb
    B += bridge(total) * 10 ** (STORY_LIFT_DB / 20)
    B *= GAIN_A
    B[o0:o0 + len(outro)] += outro[: total - o0] * GAIN_A      # official outro track, unchanged
    return A, B, outro


def seg_db(x, t0, t1):
    s = x[int(t0 * SR):int(t1 * SR)]
    return round(20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-12), 1), round(20 * np.log10(np.abs(s).max() + 1e-12), 1)


def main():
    os.makedirs(OUT, exist_ok=True)
    A, B, outro = mixes()
    for name, x in (("A_current", A), ("B_bridge", B)):
        wav = os.path.join(OUT, f"{name}_full.wav"); b.write_wav(wav, x)
        I, TP = b.loudness(wav)
        sil = x[int(10.0 * SR):int(T_CHIME * SR)]
        zero_run = 0; best = 0
        for v_ in np.abs(sil) < 10 ** (-90 / 20):
            zero_run = zero_run + 1 if v_ else 0; best = max(best, zero_run)
        print(f"{name}: {I:.1f} LUFS, {TP:.1f} dBTP | longest digital silence before chime {best / SR:.2f} s")
        for lab, (t0, t1) in {"outward cues 0.3-3.7": (0.3, 3.7), "answer 5.0-6.0": (5.0, 6.0),
                              "closure 9.0-9.8": (9.0, 9.8), "outro lead-in 10.7-12.4": (10.7, 12.4),
                              "chime 12.57-13.5": (12.57, 13.5)}.items():
            print(f"    {lab:24s} RMS/peak dBFS {seg_db(x, t0, t1)}")
        exc = os.path.join(OUT, f"{name}_excerpt_8.5-14.5s.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "8.5", "-t", "6.0", "-i", SILENT,
                        "-ss", "8.5", "-t", "6.0", "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", exc], check=True)
    # chime identity: B minus the bridge/story layers in the chime window equals A there
    w = slice(int((T_CHIME - 0.05) * SR), int((T_CHIME + 2.0) * SR))
    diff = np.abs(A[w] - B[w]).max()
    print("max |A-B| from 50 ms before the chime through +2 s:", f"{20 * np.log10(diff + 1e-12):.1f} dBFS")


if __name__ == "__main__":
    main()

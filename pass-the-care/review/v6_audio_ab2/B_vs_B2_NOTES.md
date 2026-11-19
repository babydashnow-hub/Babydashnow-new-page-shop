# Organic v6 audio: B vs B2 (chime level)

**Status: comparison only. No master rendered and nothing published.** The picture is identical in both excerpts (Organic v6, 8.5–14.5 s).

## Measured with EBU R128 momentary loudness

EBU R128 momentary loudness uses 400 ms windows and K-weighting, which tracks how a bright sound like the chime is perceived better than plain RMS does.

| | B (bridge) | B2 (bridge + chime −3 dB) |
|---|---|---|
| Loudest story cue (the answer dyad) | −13.1 LUFS | −13.1 LUFS |
| Outro lead-in (max) | −21.9 LUFS | −21.9 LUFS |
| **Chime (max)** | **−10.6 LUFS** | **−13.6 LUFS** |
| Chime vs loudest story cue | +2.5 LU | −0.5 LU (level with the loudest cue) |
| **Chime vs the 2 s just before it** | **+11.3 LU** | **+8.3 LU** |
| Integrated loudness / true peak | −18.2 LUFS / −1.0 dBTP | −18.8 LUFS / −4.0 dBTP |

Other gains tested: −2 dB (+0.5 / +9.3 LU), −4 dB (−1.5 / +7.3 LU), −5 dB, −6 dB.

## 1. Continuity

**B removes the dropout.**
- Pure digital silence before the chime falls from 1.90 s to **0.12 s**, a deliberate clean entry.
- **One observation:** B's bridge fades out over the last ~1 s before the chime, so the level dips to around −35 LUFS just before it enters (visible on the loudness plot). That dip is not a dropout, but it makes the chime's entry feel bigger. It could be addressed separately by a shorter bridge fade. I haven't changed it, so that this comparison tests only one variable.

## 2. Loudness balance

**Yes, the chime still feels disproportionate in B.**
- Its absolute level is only +2.5 LU above the story's loudest cue.
- The issue is **contrast**: it arrives +11.3 LU above the quiet passage right before it. As a bright, fast transient (G5, D6, G6), it reads louder than its momentary level suggests, especially on small phone speakers, which emphasise that range.

## Recommendation: B2, with the chime 3 dB lower

- **What changes:** the chime sits level with the warmest moment of the story instead of above it, and the jump out of the lead-in drops by 3 dB.
- **What stays:** the chime remains the clearest attack in the film, by its shape and brightness rather than its volume.
- **Method:** one static linear gain on the official outro track, which contains only the chime. Same samples, same timing (it still lands at the ring closure), same tonal character. No compression, limiting, EQ or loudness normalisation. The integrated loudness was **not** re-normalised afterwards, because that would push the chime back up.
- **−2 dB** keeps the chime slightly above the story, if you prefer more prominence. **−4 dB or lower** starts to make the sign-off feel tentative.

## Files

- `B_bridge_excerpt_8.5-14.5s.mp4` and `B2_chime-3dB_excerpt_8.5-14.5s.mp4`: compare on a phone speaker first, then on headphones.
- `B_vs_B2_momentary_loudness.png`: the loudness traces for both.

**Note:** this is a change of level only, not of the chime's sound. Because it changes the official outro's output level, it needs your explicit approval before it goes into a master.

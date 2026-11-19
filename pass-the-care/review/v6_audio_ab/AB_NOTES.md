# Organic v6 audio: A/B of the outro lead-in

**Status: comparison only. No new master has been rendered.** The picture in both excerpts is the Organic v6 AUDIO picture (8.5–14.5 s), unchanged.

## 1. Is the silence intentional or an interruption?

- The official outro's own track is effectively silent for its first **1.90 s**. It holds about −76 dBFS of encoder noise until the chime, which is synced to the ring closing.
- On its own, as a standalone end card, that silence works as anticipation.
- After 10.7 s of continuous music, it becomes **1.90 s of pure digital silence while the picture is still active**: the outro dot fades in and orbits for the whole gap.
- On a phone this tends to read as an audio dropout rather than a designed rest. The intentional pause at the qualifying order (3.8–5.0 s) is quiet, but not digitally silent, and it's tied to a still dot.
- **Assessment:** an unintended interruption, so an adjustment is justified.

## 2. Proposal B (vs current A)

| | A (current) | B (proposal) |
|---|---|---|
| Outro lead-in 10.7–12.4 s | Digital silence (1.90 s) | The story's own low bed carries on underneath at about −40 dBFS, plus **one soft re-voicing of the story's closing interval (G3 + D4)** as the outro dot appears, decaying into the ring closure. Average −25 dBFS, peak −12 dBFS. |
| Clean air before the chime | n/a | The bridge is fully gone **120 ms before the chime**, so the chime enters on clean air (only intentional silence) |
| Story cues | As approved | **+2.0 dB**, linear gain on the story layer only. The gap to the chime narrows (answer −14.6 vs chime −13.3 dBFS average); the chime is still the loudest moment. |
| Official chime | Unchanged | **Identical to A**, sample for sample: max \|A−B\| across the chime window is −240 dBFS, i.e. no difference |
| Loudness | −19.2 LUFS, −1.0 dBTP | −18.2 LUFS, −1.0 dBTP |

- **No compression, no limiting, no normalisation.** Only linear gains, and the outro's audio track is mixed in unchanged.
- **No new sound material:** same instrument, same key, same bed.

## 3. Files

- `A_current_excerpt_8.5-14.5s.mp4` and `B_bridge_excerpt_8.5-14.5s.mp4`: listen back to back on a phone speaker and on headphones.
- `AB_levels_8.5-14.5s.png`: the level traces for both.

**If B is approved,** the full master is re-mixed with exactly this audio. The picture stays identical to Organic v6, checked by frame checksums. Final approval still requires listening on a physical smartphone.

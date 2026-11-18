# PASS THE CARE™ "Full Circle": QA report, review version 2 (Variant B)

**Status: REVIEW VERSION. Not a publication master.** v2 changes only the opening. Everything after 3.2 s follows the approved v1 structure.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FullCircle_REVIEW_v2_VariantB.mp4` | 1080×1920, 30 fps, **525 frames, 17.50 s** (345 story frames plus the 180-frame official outro). H.264 High, BT.709, AAC 48 kHz. |
| `PassTheCare_FullCircle_REVIEW_v2_VariantB_cover.png` | Frame 0: the hero squirrel in warm evening light, with PASS THE CARE™, "Give $5. Get $5." and "A little help, passed forward." |
| `../build_full_circle_v2.py` | The v2 opening. It reuses the v1 renderer, text, outro handling and safeguards. |

## What changed (opening, 0.0–3.2 s)

| Time | What you see |
|---|---|
| 0.0–1.3 s | Close hero framing of the **original, still squirrel**, about 2× its later size. The scene is lit as if the acorn were the light source: warm light at the acorn falling off to soft evening shadow at the edges. A soft contact shadow grounds the figure. The camera drifts slowly to the right, the direction the squirrel faces, and breathes in slightly (+3%). |
| 1.3–3.2 s | The camera pulls back to the Full Circle layout while the evening light resolves into the brand ivory. |
| 2.4–3.2 s | The warm glow at the acorn **condenses into the official green dot**. A soft G4 note marks the moment, and the dot then begins its circle. |
| 2.8 s onward | Condition 1 appears. The rest of the timing follows v1. |

- "PASS THE CARE™ / Give $5. Get $5. / A little help, passed forward." stays visible from frame 0, as approved.
- **Tested and removed:**
  - **Falling snow:** on ivory it read as dust specks.
  - **Distant town-light bokeh:** it read as smudges.
  - Neither looked premium, so the setting is carried by light alone.

## Checks

| Check | Result |
|---|---|
| Squirrel unaltered | **PASS.** It only changes scale (uniform on both axes) and position. The largest scale used is 0.738× the source, so it is always a downscale, never an enlargement. Opaque pixels match the scaled source within 4/255 across 109,973 pixels. No warp, mirror, recolour or animation. |
| Wording | **PASS.** Identical to v1 and word for word from the live page. Nothing about reward type, expiry, how the $40 is calculated or what "completed" means. |
| Readability | **PASS.** Headline on the darkest evening background: 4.8:1 contrast (large text needs 3:1). Tagline: 12.4:1. Conditions: 7.6–8.1:1. Condition 1 is on screen 4.2 s and condition 2 is 4.3 s, both slightly shorter than in v1. |
| Safe zones | **PASS.** Opening squirrel stays within x 57–817 and y 593–1499. All text stays inside y 296–1494 and keeps at least 120 px clear of the right edge. |
| Official outro | **PASS.** Agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical): at least 57.2 dB on whole frames before the CTA appears, and at least 56.0 dB outside the CTA band. Outro audio is the original track with one gain (×3.20); anything left over is −77.3 dB below the signal. The chime starts at 13.402 s against 13.400 s expected. |
| Green dot | **PASS.** Story dot (56,108,14) is identical to the original outro dot. It lands at (540, 960). |
| CTA clearance | **PASS.** 148 px below the outro's town line. |
| Loudness | −18.4 LUFS, −1.0 dBTP. Limited by true peak; no limiter was applied to the chime. |

## Trade-offs to review

1. **Length is 17.5 s, not 16 s.** The new opening adds 2.6 s. Keeping 16 s would cut the condition lines to under 3.5 s each, which is too short to read 12-word legal-style lines. If 16 s is firm, the cleanest cut is a shorter hero shot (about 0.8 s instead of 1.3 s).
2. **There is no literal rooftop.** A convincing rooftop needs a real environment asset. Drawing or AI-generating one beside a photoreal squirrel would look composited and could cost trust. "Elevated winter evening" is suggested through light and camera movement only.
3. **The opening relies on scale and light, not action, for stop-scroll.** It is calmer than a typical social hook, by design.

## Not yet verified (required before a publication master)

Viewing on a phone under the real Instagram, TikTok and Facebook interface overlays; listening on a phone speaker; confirming the site typeface; Variant A export.

# PASS THE CARE™ "Full Circle": QA report, review version 5 (Variant B)

**Status: REVIEW VERSION. Not final and not for publication.** This version uses the approved Living Emblem system, with the storytelling and composition refinements you asked for.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FullCircle_REVIEW_v5_VariantB.mp4` | 1080×1920, 30 fps, 500 frames, **16.67 s** (320 story frames plus the 180-frame official outro). H.264 High, BT.709, AAC 48 kHz. |
| `PassTheCare_FullCircle_REVIEW_v5_VariantB_cover.png` | A still composed from the same elements: the closed emblem, the full "Give $5. Get $5." and the tagline. It is not frame 0. Everything sits inside the safe zones, and the headline is 112 px. |
| `../build_full_circle_v5.py` | The renderer. It reuses the approved base renderer and its safeguards. |

## Storytelling (what changed from the v4 test)

| Time | Dot | Headline | Statement under the emblem |
|---|---|---|---|
| 0.0 s | Already moving away from just beneath the squirrel | Both halves at full strength (frame 0 rule) | none |
| 0.2–4.0 s | **Out** along the right half to the top: the referred parent's $5 | "Give $5." leads | "They save $5 on their first order of $40+ in merchandise." (on screen 0.2–4.9 s, **4.7 s**) |
| 4.0–5.0 s | Holds at the top with one slow pulse: their qualifying order | | |
| 5.0–9.0 s | **Returns** along the left half to where it started: the referrer's $5 reward | "Get $5." leads | "You earn a $5 BabyDashNow reward when their qualifying order is completed." (on screen 5.0–9.8 s, **4.8 s**) |
| 9.0 s | The circle closes beneath the squirrel | Both halves at full strength | |
| 9.7–10.6 s | The emblem fades and the dot glides to (540, 960), the outro dot's centre | | |
| 10.67 s | Official outro, unaltered | | "Discover PASS THE CARE™" from 13.67 s |

- **Headline emphasis:** the half that isn't leading drops only to 66% opacity, which still gives 3.1:1 contrast. That passes WCAG's 3:1 minimum for large text, so "Give $5. Get $5." stays fully readable throughout.
- **Sound:** a rising phrase on the way out, quiet during the hold, an answering phrase on the way back, and a soft low G as the circle closes. The official chime is reserved for the outro.

## Checks

| Check | Result |
|---|---|
| Squirrel unaltered and stationary | **PASS.** One uniform scale (0.38278 on both axes, a downscale) and no movement at all. Opaque pixels match the scaled source exactly (maximum difference 0 across 131,048 pixels). |
| Squirrel size | **+7%** versus the v4 test (470 px figure height). The nearest point of the squirrel is 36 px from the circle line and **14 px from the dot's edge**, so it is not crowded. |
| Wording | **PASS.** Both statements are verbatim from the live PASS THE CARE™ page, in full; only the line breaks differ. Nothing about reward type, expiry, how the $40 is calculated or what "completed" means. |
| Readability | **PASS.** Headline 6.7:1 (3.1:1 when not leading). Statements 8.1:1 at 44 px, each on screen at least 4.7 s. Tagline 17.4:1. CTA 7.4:1. |
| Safe zones | **PASS.** All story content sits within x 136–943 and y 306–1497. |
| Official outro | **PASS.** Agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical): at least 57.2 dB on whole frames before the CTA appears, and at least 56.0 dB outside the CTA band. Audio is the original track with one gain change; anything left over is −77.3 dB below the signal. The chime starts at 12.569 s against 12.567 s expected. |
| Green dot | **PASS.** Story dot (56,108,14) is identical to the original outro dot, and it lands exactly at (540, 960). |
| CTA clearance | **PASS.** 148 px below the outro's town line, and it doesn't overlap any official element. |
| Frames and specs | No black frames. 500 frames. Frames 316–321 (0.2 s) are near-white while the dot settles into the outro, as in earlier versions. |
| Loudness | −19.2 LUFS, −1.0 dBTP. Capped by true peak; no limiter was applied to the chime. |

## Not yet verified (required before a publication master)

Viewing on a physical phone under the real Instagram, TikTok and Facebook interface overlays; listening on a phone speaker; confirming the site typeface (this build uses Lora and Inter); Variant A export.

# BabyDashNow™ New Mom Surprise: Phase 2A Assembly Cut V1

**Status: assembly for creative review. Not a publication master.** Straight cuts only. No text, music, sound effects, transitions or end card.

## 1. Deliverables

| File | What it is |
|---|---|
| `NewMomSurprise_AssemblyV1_SDR_REVIEW_1080x1920.mp4` | **Review version.** H.264 High, 1080×1920, 30 fps, 648 frames, **21.60 s**, BT.709 SDR, 24.4 Mbps. Silent AAC stereo track. |
| `NewMomSurprise_AssemblyV1_HDR_HLG_1080x1920.mp4` | **HDR master.** HEVC Main 10, 1080×1920, 30 fps, 648 frames, 21.60 s, BT.2020 / HLG (ARIB STD-B67), limited range, 16.5 Mbps. Silent AAC stereo track. |
| `AssemblyV1_EDL.csv` | The source-to-timeline edit decision list |
| `AssemblyV1_cut_points_SDR.png` | The first and last frame of every shot |
| `../build_assembly_v1.py` | Reproducible build from the EDL |

## 2. Edit decision list

| # | Source | In → out (source s) | Dur | Timeline | Purpose |
|---|---|---|---|---|---|
| 1 | D IMG_7306 (d3ff4db1) | 3.40 → 4.60 | 1.20 | 00:00 – 01:06 | **Curiosity:** an empty box |
| 2 | C IMG_7306 (76696015) | 0.00 → 2.40 | 2.40 | 01:06 – 03:18 | Hands begin preparing it (paper fill) |
| 3 | E IMG_7308 | 2.60 → 5.20 | 2.60 | 03:18 – 06:06 | Swaddle placed and pressed in |
| 4 | F IMG_7314 | 1.50 → 3.40 | 1.90 | 06:06 – 08:03 | Pacifiers |
| 5 | G IMG_7315 | 2.60 → 4.70 | 2.10 | 08:03 – 10:06 | Lotion |
| 6 | H IMG_7319 | 1.80 → 3.80 | 2.00 | 10:06 – 12:06 | **Care:** tissue folded over |
| 7 | I IMG_7321 | 0.70 → 2.60 | 1.90 | 12:06 – 14:03 | BabyDashNow card |
| 8 | J IMG_7325 | 1.40 → 3.50 | 2.10 | 14:03 – 16:06 | Sealed: the BabyDashNow seal |
| 9 | K IMG_7326 | 4.60 → 5.80 | 1.20 | 16:06 – 17:12 | **Departure:** the gift in the car |
| 10 | P IMG_7356 | 0.00 → 4.20 | 4.20 | 17:12 – 21:18 | **Fulfilment:** delivered, waiting at her door |

Timecodes are seconds:frames at 30 fps. Total: **21.60 s (648 frames)**.

**Differences from the approved structure:**
- **The building-entry beat is missing.** No privacy-safe segment exists (see §4).
- **The letter is omitted.** See §4.
- **Ranges were extended** within the verified audit ranges to reach 21–23 s, cutting on settled frames.
- **D starts at 3.40 s,** not the audited 2.3 s, because a hand edge enters the frame at about 2.9 s.

## 3. Technical export report

**Sources:**
- All 10 used sources are iPhone 16 Pro HEVC 10-bit HLG / BT.2020, 2160×3840 (displayed after the camera's rotation flag), 30 fps. J is 29.97 fps.
- **The source files were opened read-only and verified unchanged** by MD5 checksums before and after the build (10/10 match).

**Common to both versions:**
- Trimmed to exact frames, with no interpolation. J is conformed 29.97 → 30 by retiming (no frame was duplicated within its 2.1 s).
- **One Lanczos downscale** 2160×3840 → 1080×1920 in the HLG signal domain, with high-precision rounding.
- **No crop, reframe, zoom, stabilisation, sharpening, denoise, grade, LUT or retouch.**

**HDR master:**
- Encoded directly in HLG (HEVC Main 10, CRF 14) with correct HLG / BT.2020 tags.
- **Check:** luma of the master against the source (scaled only) gives **47.5–48.8 dB PSNR**. Average signal is identical (37592 vs 37593, and 42003 vs 42002 on a 16-bit scale). The image is the camera's, with no change in level.

**SDR review version (technical conversion only):**
1. HLG (BT.2100) decoded to linear light with the HLG reference white at **203 cd/m²**, following ITU-R BT.2408.
2. Primaries converted **BT.2020 → BT.709**.
3. A **Mobius tone curve**, with saturation preservation (`desat=0`), compresses only highlights above reference white.
4. BT.709 transfer applied; limited range.

- The identical, fixed parameters are applied to every shot.
- **Check:** export frames against an independent single-frame conversion of the source give 41.7–45.1 dB PSNR, with identical average RGB. The pipeline adds nothing beyond the conversion.

**Limitations (disclosed):**
- HDR highlights above SDR white (window light, glossy packaging) are compressed and can't be shown at their HDR brightness in SDR.
- Very saturated BT.2020 colours outside BT.709 are clipped to the nearest BT.709 colour.
- **The SDR file will not exactly match the iPhone Photos app**, which shows HLG with Apple's own adaptive display mapping. Compare against the HDR master on an HDR-capable phone.
- The HDR master is the faithful reference. Platform HDR playback varies by device (see Phase 1B §G).

**Audio:**
- **Muted in both versions** (silent stereo track, verified peak 0.0).
- The source audio could not be reliably reviewed for intelligible speech, radio or music in this environment, so **no source audio is included.** This is a disclosed limitation, not a creative decision.

## 4. Privacy and continuity QA

**Privacy:**

| Item | Finding | Action in V1 |
|---|---|---|
| Building entry (IMG_7337, both trims) | **The doormat reads "Residences at Bedford … Luxury Apartments"** (legible from about 5.0 s at 1080p). Earlier frames show the recognisable entrance and canopy; the 3.9 s trim shows the residential façade and balconies. No segment avoids these without masking or cropping, which is not allowed. | **Excluded** |
| Handwritten letter (A, B) | B: the full text is legible. A: the text isn't legible, but with no attribution, a writing hand in a gift story reads as the sender's note, and the note is never seen going into the box. | **Omitted** |
| Licence plates (N, O, M) | Legible or present | **Excluded** (no driving shots used) |
| Doorstep (P 0–4.2 s) | Plain grey door, **no unit number, no address, no people**; hallway floor | Included (low risk) |
| Car (K 4.6–5.8 s) | Interior only; no plate | Included |
| BabyDashNow card (I) | Card copy is partly legible at 1080p (BabyDashNow's own text) | Included; **please confirm the card copy may be shown** |
| Third-party marks | SwaddleMe, MAM, Aquaphor, Aveeno, Huggies, Pampers, Johnson's | Visible; business decision |
| Reaction or hand-off | None shown or implied; the film ends on the gift at the door | ✓ |

**Continuity:**
- **The setting changes at shot 8 (J):** the box is sealed on a different table, side-on against a plain wall, while shots 1–7 are overhead. It reads as a new moment, which works, but it's a visible change in angle.
- **Shot 9 (K) in-frame has motion blur** from the blue envelope for about 3 frames. The car shot also introduces items not seen being packed (Huggies, plush, Johnson's).
- **Shot 10 (P) at 4.0–4.2 s:** the camera starts to drift backwards before the out-point. Option: end at 3.8 s (21.2 s total).
- **No beat between the car and the door.** Without the building entry, the film cuts from the car straight to the door; the delivery reads clearly, the journey only briefly.
- Gift order is consistent: fill → swaddle → pacifiers → lotion → tissue → card → sealed.

## 5. Recommendations (not implemented)

**Text (proposed, for approval):**
- 0.3–2.5 s: "Someone thought of you today." Small, Fraunces, over the empty box; it answers the curiosity without explaining it.
- About 14–16 s (seal): no text needed. The seal already reads "We show up when it matters".
- End: "Delivered on their behalf by BabyDashNow™". This accurately describes delivering for the sender without implying who wrote anything.

**Music:**
- Soft solo piano or felt-piano bed, original or properly licensed, about 70 bpm, with no vocals.
- Keep it under quiet room ambience **only after** the source audio has been reviewed for privacy.
- Target −14 to −16 LUFS, −1 dBTP; no compression on the brand chime.

**Outro:**
- Append the **official 6 s BabyDashNow outro** (approved master, unaltered) after P.
- That brings the film to about 27.6 s. To stay near 23 s total, trim P to about 2.5 s and K to 1.0 s.
- The outro is SDR and white; transition with a straight cut from P.

**Optional pickups to fill the journey gap (no consent needed):**
- A closed-box hero on a neutral surface.
- The letter folded and placed into the box, if the letter is to stay.
- The gift being set down at the door, filmed from a neutral angle with no signage.

## 6. Decisions requested

1. Is ending without the building entry acceptable, or will you pick up a neutral-angle replacement?
2. Should the letter stay out, or will you film the letter going into the box?
3. May the BabyDashNow card copy be shown? And the third-party brands?
4. Should P end at 3.8 s (the camera drift)?
5. Do you approve the text, music and outro proposals above for Phase 2B?

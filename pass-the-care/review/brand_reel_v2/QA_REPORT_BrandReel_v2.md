# BabyDashNow™ Brand Reel: QA report, review candidate v2 (image fidelity)

**Status: REVIEW CANDIDATE. Not published.** The storyline, text, official logo and creative direction are unchanged from v1.

## 1. Audit: what caused v1's quality loss

Measured at matching source timestamps, excluding the text band (`Compare_Source_v1_v2.png`).

| Shot | Cause in v1 | Evidence (original → v1) |
|---|---|---|
| **Mother** | **The source, not the grade.** v1 used a supplied **1080p edit at 3.1 Mbps** instead of the original. Exposure and colour were already correct. | Detail **7.19 → 5.82 (−19%)**. Black p1 11.6 → 11.0, white p99 237.9 → 236.6, saturation 0.274 → 0.276 (tone essentially unchanged) |
| **Shopping** | **The v1 creative grade** applied after the HLG tone map: gamma 1.04, contrast 0.96, saturation 0.86, warm balance | Shelf: **black p1 9.2 → 14.7 (lifted)**, contrast sd 57.0 → 54.2, saturation 0.495 → 0.476. Cart: p1 39.0 → 42.8, midtone 178.7 → 167.3. Blacks lifted and contrast flattened: the washed-out look. |
| Scaling | Not a cause: the 4K shopping footage was already downscaled once with Lanczos. | — |
| Compression | A minor factor (CRF 14). v2 uses CRF 12 + tune film. | — |
| Colour conversion | Not a cause: correct BT.709 limited-range handling throughout. | — |

## 2. v2 pipeline

| Item | v2 |
|---|---|
| Mother | **Original Pexels 7279098 UHD** (2160×3840, 23.976 fps, 15 Mbps, SDR BT.709), downloaded from Pexels. Downscaled once (Lanczos, accurate rounding) to 1080×1920. Converted from 23.976 to 30 fps by **frame repetition, no interpolation**. **No grade, no sharpening.** |
| Shopping | Original IMG_7019 (4K HEVC, HLG/BT.2020). **HLG → SDR BT.709 with a neutral tone curve only** (reference white 203 nits, Mobius shoulder). **No creative grade, no saturation change, no sharpening.** Downscaled once with Lanczos. The two shots are matched perceptually only by being converted correctly; each keeps its own light (soft daylight vs. warm store lighting). |
| Brand graphics | **Never graded.** Official outro picture unaltered (white background as in the approved master). Text in brand ink and green. CTA pill measured at (44, 96, 16) against spec #2D6111 (45, 97, 17): a difference of one level from encoding. |
| Export | **1080×1920, 30 fps, 312 frames, 10.40 s.** H.264 High, level 5.0, CRF 12, preset slow, tune film. yuv420p, BT.709, limited range. **12.4 Mbps** video; AAC 48 kHz (~143 kbps). |

## 3. Objective results (original → v1 → v2)

| Shot | Detail | Black p1 | Contrast sd | Saturation | Clipped highlights (luma ≥252) | Crushed blacks (luma ≤4) |
|---|---|---|---|---|---|---|
| Mother | 7.19 → 5.82 → **7.05 (98% of original)** | 11.6 → 11.0 → 10.3 | 70.8 → 70.7 → 70.9 | 0.274 → 0.276 → 0.277 | 0 / 0 / **0%** | 0 / 0.01 / 0.01% |
| Shelf | 3.22 → 3.09 → **3.39** | 9.2 → 14.7 → **8.9** | 57.0 → 54.2 → **56.8** | 0.495 → 0.476 → **0.500** | 0 / 0 / **0%** | 0.40 / 0.00 / 0.56% |
| Cart | 1.96 → 2.05 → **2.30** | 39.0 → 42.8 → **35.6** | 63.2 → 61.8 → **65.3** | 0.293 → 0.324 → **0.305** | 0 / 0 / **0%** | 0 / 0 / 0% |

**Honest notes:**
- The mother's detail is **restored because it exists in the 4K original**; v2 reaches 98% of it.
- The shopping footage's detail is limited by the source itself: **the hand in the cart shot is motion-blurred in the original**, and that can't be recovered. v2 slightly exceeds the reference on the detail metric only because of a one-frame timing difference and encoding noise. It's not sharpening.
- **No highlights are clipped** in any v2 shot.
- The small dark areas in the shelf shot (0.56% near black) are the deep gaps between shelves, as in the source (0.40%).
- **The visible change in the shopping shots is subtle:** deeper blacks, firmer midtones and truer packaging cyan and yellow. It isn't a dramatic "before/after", and I haven't presented it as one.

## 4. Edit (v2 timeline)

| Time | Shot | Text |
|---|---|---|
| 0.00–2.30 | Mother and baby (source 0.50–2.80 s) | **Your hands are** *already full.* (0.13–2.30 s) |
| 2.30–3.30 | Hand selects Pampers Swaddlers (source 1.15–2.15 s) | **We'll handle** / *the essentials.* (2.43–4.53 s) |
| 3.30–4.80 | **Pampers box and baby wipes together in the cart** (source 6.78–8.28 s; 1.5 s, longer than v1's 1.3 s) | (continues) |
| 4.40–4.80 | The cart shot dissolves into the official outro's white opening (0.4 s overlap; the outro picture itself is untouched) | |
| 4.40–10.40 | **Official BabyDashNow outro** | **Baby essentials,** / *delivered locally.* (from 4.60 s). **CTA "Order at BabyDashNow.com"** (from 6.60 s, 3.8 s on screen; larger, 46 px Inter SemiBold, white on deep green) |

- **Total 10.40 s** (v1 was 11.80 s).
- The challenge, the service and "Baby essentials, delivered locally." are all on screen by **4.6 s**.

## 5. Typography and safe zones

All within the conservative organic envelope (y 260–1440, x 90–930):

| Element | Position (x, y) |
|---|---|
| Scene 1 line | x 170–910, y 292–356 |
| Scene 2 lines | x 320–758, y 302–439 |
| Brand line | x 279–799, y 579–719 |
| **CTA pill** | x 182–898, y 1176–1284 |

- **Contrast:** text 5.8–19:1; CTA 7.4:1.
- **Documented exception:** the official outro wordmark's right edge passes x 930 (approved master, untouched).
- **Paid placements** (not the target): the lower part of the CTA would sit inside Meta's ad bottom band (y ≥1248).

## 6. Audio

- **Music:** original felt-piano bed (no third-party music); footage audio not used.
- **Chime:** the official BabyDashNow chime, same waveform (residual −75 dB), **starting at 6.302 s** (offset 0.0 ms from the outro's own timing). −3 dB relative, with the bed +3.3 dB.
- **Balance (EBU R128 momentary max):** scene 1 −14.2 · scene 2 −12.7 · brand lead-in −13.0 · **chime −12.4 LUFS**. That's **+0.3 LU** above the loudest music: no jump.
- **Continuity:** longest digital silence before the chime is 0.11 s, the deliberate clean entry.
- **Loudness:** **−16.0 LUFS integrated, −2.0 dBTP.** Linear gains only; no compression or limiting.

## 7. Before publication

1. Watch on physical iOS and Android phones in Instagram, Facebook and TikTok (picture and sound).
2. Confirm the ordering flow at BabyDashNow.com on a phone.
3. **Third-party marks:** Pampers and Kirkland Signature (Costco) wipes remain visible, and the cart shot is now longer. Please confirm you're comfortable showing them.
4. **Pexels licence:** the original was downloaded from pexels.com. Keep the licence record for video 7279098.

# BabyDashNow™ brand and conversion Reel: QA report, review candidate v1

**Status: REVIEW CANDIDATE. Not published.** This is not a PASS THE CARE™ asset: no referral messaging, no squirrel, no "Give $5. Get $5.".

## Deliverables

| File | Description |
|---|---|
| `BabyDashNow_BrandReel_REVIEW_v1.mp4` | The review candidate |
| `BabyDashNow_BrandReel_REVIEW_v1_cover.png` | Cover: the mother and baby with "Your hands are already full." (frame at 1.33 s) |
| `BrandReel_v1_keyframes.png` | Six key moments |
| `../../build_brand_ad_v1.py` | The renderer |

## Export specifications

1080×1920, 9:16, 30 fps, **354 frames = 11.80 s**. H.264 High, yuv420p, BT.709 (SDR). AAC 48 kHz. Integrated **−16.0 LUFS**, true peak **−1.6 dBFS**.

## Source selection

| Source | Used | Why |
|---|---|---|
| Mother and baby (Pexels video 7279098) | Clean supplied edit, frames 0.00–2.67 s (source 0.5–3.17 s) | **The newly uploaded 6 s file already has an earlier edit's text and brand card burned in**, so it can't be used as clean footage. The same clip's clean edit (no text) was already stored in the project and is used unaltered. Agreement with the source outside the text band, measured as PSNR (higher means closer; above about 40 dB is visually identical): ≥43.1 dB. |
| BabyDashNow shopping footage (IMG_7019, 4K HDR HLG, portrait) | **1.00–2.60 s**: hand selects the Pampers Swaddlers on the shelf. **6.75–8.28 s**: the box in the cart beside the baby wipes. | 3.4–6.0 s is mostly motion blur while the box is lifted, so it's skipped with a short dissolve. That's an edit between two real moments, not a fabricated action. |

**Colour:** the HLG footage is converted to SDR BT.709 with a gentle tone curve. A light grade (saturation −14%, slightly warmer, contrast −4%) keeps it closer to the warm, soft mother footage. The mother footage itself is not graded.

## Timeline (actual)

| Time | Picture | On screen | Sound |
|---|---|---|---|
| 0.00–2.67 | Mother with baby at her laptop | **Your hands are** *already full.* (0.13–2.67 s; Fraunces 56 px, ink plus green italic, one line on the clear wall) | Open, quiet felt-piano G chord |
| 2.67–2.80 | Short dissolve | | |
| 2.80–4.27 | Hand selects Pampers Swaddlers | **We'll handle** / *the essentials.* (2.80–5.73 s; Fraunces 72 px, white with a soft shadow and a soft top shading) | Warm E-minor chord |
| 4.27–5.60 | Box in the cart beside the wipes | (continues) | C-major chord |
| 5.60–5.80 | Fade to white | | |
| 5.80–11.80 | **Official BabyDashNow outro** (unaltered picture: dot, ring, logo, "We show up when it matters", Stamford · Darien · Norwalk · Greenwich) | **Baby essentials,** / *delivered locally.* (5.93–11.80 s; Fraunces 66 px). **CTA pill: "Order at BabyDashNow.com"** (8.40–11.80 s, 3.4 s; Inter SemiBold 40 px, white on deep green) | A suspended D chord carries under the outro's silent lead-in and clears 0.12 s before the **official chime at 7.70 s** |

**Within the first 7 seconds:**
- The parenting challenge lands by **0.1 s**.
- "We'll handle the essentials." lands by **2.8 s**.
- "Baby essentials, delivered locally." lands by **5.9 s**.

The four towns appear in the official outro's own lockup line from about 10 s.

## Typography and readability

| Text | Contrast (median against its background) |
|---|---|
| "Your hands are already full." on the wall | 16.1:1 |
| "We'll handle the essentials." over the shelf | 14.2:1 |
| "We'll handle the essentials." over the cart (brightest shot) | 5.8:1 |
| "Baby essentials, delivered locally." on white | 19.3:1 |
| CTA (white on #2D6111) | 7.4:1 |

- **Fonts:** Fraunces and Inter (the site's typefaces as previously confirmed). Brand ivory and green, plus the official logo through the approved outro.

## Safe zones (organic Reels / Facebook / TikTok)

The conservative envelope is y 260–1440 and x 90–930 (third-party consensus, not official specs).

| Element | Position (x, y) | Result |
|---|---|---|
| Scene 1 line | x 170–910, y 292–356 | ✅ |
| Scene 2 lines | x 320–758, y 302–439 | ✅ |
| Brand line | x 279–799, y 579–719 | ✅ |
| CTA pill | x 222–857, y 1186–1286 | ✅ |

- **Official outro:** the wordmark's right edge ("…Now™") extends past x 930 into the right-hand icon area. It's part of the approved master and is left untouched.
- **Paid placements** (not the target here): the lower part of the CTA pill (below y 1248) would sit inside Meta's paid-ad bottom band.

## Audio

- **Music:** original felt-piano bed (G – Em – C – D), synthesised for this edit. No third-party music, no licensing dependency. Footage audio is not used.
- **Chime:** the official BabyDashNow chime, same waveform (residual −76 dB against the official track), **starting at 7.702 s** (cross-correlation; offset 0.0 ms). Level: −3 dB relative, plus the music bed lifted +3.3 dB, so the chime is a gentle accent.
- **Balance (EBU R128 momentary max):** scene 1 −13.3 · scene 2 −12.5 · brand lead-in −13.1 · **chime −11.5 LUFS**. That's **+1.0 LU** above the loudest music and **+1.6 LU** above the lead-in: no sudden jump.
- **Continuity:** the longest digital silence before the chime is 0.12 s, the deliberate clean entry.
- **Processing:** linear gains only. No compression, limiting or EQ.

## Accuracy and trust notes

- **The mother is stock footage** (Pexels 7279098). She is not presented as a customer: no name, quote, purchase or endorsement. The lines address the viewer.
- **The shopping footage is real** but **does not show a delivery**. The copy ("We'll handle the essentials.") describes the service; it doesn't claim this order was delivered.
- **Third-party brands visible:** Pampers packaging, and **Kirkland Signature (Costco) baby wipes**, whose name is readable on the box in the cart, in a recognisable warehouse store. This shows where products were bought, which you may or may not want to communicate. **Please confirm you're comfortable showing these marks.** It's a business and legal judgement rather than a technical issue.
- No delivery times, prices or guarantees are stated.

## Required before publication

1. Watch and listen on physical iOS and Android phones in Instagram, Facebook and TikTok (speaker and headphones).
2. Confirm BabyDashNow.com and the ordering flow work from a phone.
3. Decide on the visible third-party marks (Pampers / Kirkland).

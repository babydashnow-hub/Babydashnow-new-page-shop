# PASS THE CARE™: final focused review candidate v10 (Variant B)

**Status: REVIEW CANDIDATE. Not published, not final.** It still requires physical-phone review (picture and sound) and a check of the referral landing page.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FINAL_REVIEW_v10_VariantB.mp4` | 1080×1920, 30 fps, 500 frames, **16.67 s**. H.264 High, BT.709, AAC 48 kHz. Organic Full Circle v6 baseline; no human footage. |
| `PassTheCare_FINAL_REVIEW_v10_VariantB_cover.png` | The complete composition with **statement 1 visible**, so the cover never shows "$5" without its condition. |
| `../../build_full_circle_v10_final.py` | The renderer: v6 plus the layout changes and the approved audio. |

## Hierarchy (one centred column)

| y (px) | Element | Type |
|---|---|---|
| 296–322 | PASS THE CARE™, the campaign identifier | Inter SemiBold 28, tracked, green |
| 346–460 | **Give $5. Get $5.**, the dominant headline, with the travelling green underline | Fraunces 700, 104 px, green, 6.7:1 contrast |
| 492–540 | *with* **BabyDashNow**™, the supporting line | Fraunces 400 italic + 700, 44 px |
| 574–1218 | The original squirrel (stationary) inside the Full Circle orbit | Official green dot and ring |
| 1238–1340 | Statement 1 (outward), then statement 2 (return) | Inter 38 px, 8.1:1 contrast |
| 1382–1432 | **A little help,** *passed forward.*, the closing line | Fraunces 700 + 400 italic, 44 px |

## Offer accuracy

- **Statement 1** ("They save $5 on their first order of $40+ in merchandise.") is on screen 0.2–4.9 s while the dot travels out.
- **Statement 2** ("You earn a $5 BabyDashNow reward when their qualifying order is completed.") is on screen 5.0–9.8 s while the dot returns.
- Both are verbatim from the live page; only the line breaks differ (checked in code).
- On screen times: **4.7 s and 4.8 s**.
- Between 0.2 s and 9.8 s, "Give $5. Get $5." never appears without one of the conditions.
- The cover carries statement 1.
- Nothing about reward type, expiry, how the $40 is calculated or what "completed" means.

## Safe zones (every frame scanned)

Published figures vary and none is official, so I used the **conservative organic envelope**: content within y 260–1440 and x 90–930. That combines a 260 px top margin (brand guideline), TikTok's 480 px caption band and a 150 px right-hand icon column.

Sources: [Canadian Tire brand motion guide](https://brand-qa2.canadiantire.ca/en/ctr/design-system/omni-channel/motion/margins-and-safe-space.html), [Reap safe-zone guide](https://reap.video/blog/short-form-video-safe-zones), [Postiz](https://postiz.com/blog/vertical-video-dimensions), [socialync](https://www.socialync.io/tools/safe-zones/instagram-reels). These are third-party estimates.

| Zone | Story (0–10.67 s) | Official outro + CTA |
|---|---|---|
| Organic envelope (Instagram/Facebook Reels, TikTok) | **0 px**: all content within x 152–927, y 296–1433 | Up to 1,903 px: the **official outro wordmark's right edge ("…Now™")** passes x 930. This is part of the approved master and is left untouched. The CTA itself is clear. |
| Meta Reels **ads** (14/35/6%) | The statements and closing line sit below y 1248 | 109 px (the outro's "™" for 2 frames during its own slide-in) |
| TikTok In-Feed **ads** (240/660/120 + icons) | The statements and closing line sit below y 1260, and the right edge of the orbit passes the icon column | Wordmark under the icon column (outro master) |

**Paid ads:** this candidate is built for organic posts. Paid placements would need the separate paid-safe layout.

## Checks

| Check | Result |
|---|---|
| Squirrel | Exact original artwork, one uniform scale (0.36443), stationary. Opaque pixels match the source (max difference 0 across 113,951 pixels). Optical offset (−16, −10 px) inside the ring keeps the dot **34 px** clear of it. |
| Green dot / colours / type | Dot (56,108,14) identical to the official outro dot. Ivory #F5F3ED; text green #2D6111; Fraunces and Inter as on the live page. |
| Official outro picture | Agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical): at least 57.2 dB on whole frames before the CTA, and at least 56.05 dB outside the CTA band. "Discover PASS THE CARE™" at y 1169–1197, 70 px clear of the town line. |
| Official chime | Same waveform, scaled only (residual −77.3 dB). Starts at **12.569 s** against 12.567 s expected. |
| Sound narrative | The approved v6 AUDIO cues: opening accent, rising outward notes, **deliberate quiet at the qualifying-order pause** (−53 dBFS), warm answer on the return, soft close. |
| Outro continuity | Longest digital silence before the chime is **0.12 s**, a deliberate clean entry. The bridge uses the story's own bed and closing interval. |
| Chime balance (EBU R128 momentary max) | Outward −11.4 · answer −10.1 · close −12.9 · lead-in −18.9 · **chime −10.6 LUFS**. The chime sits **level with the loudest cue (−0.5 LU)** and 8.3 LU above the lead-in, using the B2 −3 dB relative correction. |
| Loudness | −15.8 LUFS integrated, −1.0 dBTP. One linear gain, set so the true peak is −1 dBTP; no compression, limiting or EQ. |
| Specs | 500 frames, no black frames. The near-uniform frames 320–321 are the outro's own first frames. |

## Required before publication

1. Watch and listen on physical iOS and Android phones in Instagram Reels, Facebook Reels and TikTok (speaker and headphones).
2. Check the referral landing page from "Discover PASS THE CARE™".
3. Decide whether the official outro wordmark reaching under the right-hand icons is acceptable, or whether the outro master should be revised separately.

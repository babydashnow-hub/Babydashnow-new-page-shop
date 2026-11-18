# PASS THE CARE™ "Full Circle": QA report, review version 1 (Variant B)

**Status: REVIEW VERSION. Not a publication master.** This is for your approval before any final export.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FullCircle_REVIEW_v1_VariantB.mp4` | 1080×1920, 30 fps, 480 frames, 16.00 s. H.264 High, yuv420p, BT.709. AAC 48 kHz. |
| `PassTheCare_FullCircle_REVIEW_v1_VariantB_cover.png` | Frame 0 at 1080×1920. Shows the squirrel, PASS THE CARE™, "Give $5. Get $5." and "A little help, passed forward." |
| `../build_full_circle.py`, `../qa_full_circle.py` | The renderer and the automated checks behind this report. |

## Source assets used

| Asset | Source | Verification |
|---|---|---|
| Squirrel | Original artwork you supplied in chat: 1254×1254 WebP with transparency. SHA-256 `7db9696d…df0b`. | See check 1. |
| Offer wording | Your screen recording of babydashnow.com/pass-the-care/, recorded 18 Nov 2026. Reference crops are in `assets/reference/`. | See check 2. |
| Official outro | `BabyDashNow_Official_Outro_Final.mp4`, byte-identical to the approved master (SHA-256 `97e56caf…f1a6`). | See check 4. |
| Colours | Dot and line: #3B6E11, the outro's own dot value. Text green: #2D6111, sampled from the live page. Ivory: #F5F3ED, the page's PASS THE CARE™ panel. | See check 5. |

## The seven requested checks

**1. Squirrel integrated without redesign or distortion: PASS**
- One uniform scale factor of 0.35805 on both axes (Lanczos, downscale only). No crop, mirror, recolour, warp, retouch or animation.
- The squirrel's opaque pixels were compared against the scaled source over 109,973 pixels. The largest difference was 4/255, which is rounding. A small area around the dot was excluded from the comparison.
- The squirrel is completely still for the whole story section, and the acorn is untouched.
- The source contains faint stray alpha specks in its background. They were left in place, not edited. After scaling, 119 such pixels remain, each at most 1/255 visible against the ivory, which is invisible.

**2. Referral wording matches the page: PASS (please confirm)**

| On screen | Live page |
|---|---|
| PASS THE CARE™ | Label: "PASS THE CARE™" |
| Give $5. Get $5. | "Give $5. Get $5." |
| A little help, passed forward. | Headline: "A little help, passed forward." |
| They save $5 on their / first order of $40+ / in merchandise. | "They save $5 on their first order of $40+ in merchandise." |
| You earn a $5 BabyDashNow / reward when their qualifying / order is completed. | "You earn a $5 BabyDashNow reward when their qualifying order is completed." |
| Discover PASS THE CARE™ | The CTA you approved |

- Words are verbatim; only the line breaks differ.
- Nothing appears about reward type beyond the page wording, expiry, how the $40 is calculated, or what "completed" means.
- **No caption has been written.** Any caption should reuse the sentences above.

**3. Readable on a mobile device: PASS, with two notes**

| Element | Size | Contrast | Time on screen |
|---|---|---|---|
| Headline "Give $5. Get $5." | Lora Bold 112 px | 6.7:1 | 9.6 s, from frame 0 |
| Tagline | Lora Medium 48 px | ink 17.4:1, green 6.7:1 | 9.6 s |
| Condition 1 (8 words) | Lora 44 px | 8.1:1 | about 4.5 s |
| Condition 2 (12 words) | Lora 44 px | 8.1:1 | about 4.7 s |
| CTA | Inter Medium 36 px | 7.4:1 on white | 3.0 s |

- 44 px on a 1080 px-wide frame is about 16 pt on a typical phone.
- **Note 1:** I'd like your review on whether condition 2 reads comfortably at normal speed, since it is the longest line.
- **Note 2:** all story content stays within x 132–946 and y 306–1494, so it sits inside the Reels and TikTok safe zone, clear of the interface at the top, bottom and right. I haven't yet viewed it under real app overlays on a phone, which still needs doing (see "Not yet verified").

**4. Official outro preserved visually and audibly: PASS**
- **Visual:**
  - Frames 300–479 are the decoded official outro, re-encoded once with no edits.
  - Agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical): at least 57.2 dB on whole frames before the CTA appears, and at least 56.0 dB (mean 60.4 dB) across all frames outside the CTA band.
- **Audio:**
  - The outro's sound is the original track with one uniform gain of ×3.20 (+10.1 dB). Anything left over after removing that gain is −77.3 dB below the signal, meaning the waveform is otherwise unchanged.
  - The chime starts at 11.902 s in the export, against 11.900 s expected. That is the outro's 1.90 s plus 10.00 s of story, so it is inside one frame.
  - The outro track's last 768 samples (16 ms) fall past 16.00 s and were trimmed. They were completely silent.
- **Loudness:** −17.9 LUFS integrated, −1.0 dBTP true peak.
  - The gain was capped by the −1 dBTP peak limit before reaching −14 LUFS.
  - Getting louder would need a limiter, which would change the chime, so I didn't use one.
  - Reels and TikTok normalise playback anyway, so this is safe, but it will sound slightly quieter than heavily limited ads.

**5. Green-dot transition and colour consistency: PASS**
- The story dot's colour in the export is (56,108,14), which exactly matches the original outro's dot as decoded.
- The outro's dot in the export is (54,106,12), a difference of 2 from video encoding.
- At frame 297 the story dot lands at exactly (540, 960), the outro dot's centre, and shrinks to nothing. The outro's own dot then appears from the same point.
- A colour-conversion error in my first render made the greens drift by up to 12 levels. I fixed it before this export by using BT.709 conversion consistently.
- **Note:** frames 296–301 (0.2 s) are near-plain white while the dot settles and the outro's opening frames run. This is intentional, but tell me if you'd like it shorter.

**6. CTA does not overlap any official outro elements: PASS**
- The lowest row of outro content (the town line) is y 1099.
- The CTA occupies y 1247–1275, leaving **148 px** of clear space below the town line.
- The CTA fades in from frame 390 (13.0 s), after the outro's lockup has settled.

**7. QA report and cover frame included: PASS** (this file and the cover PNG).

## Other checks

- No black frames.
- Frame count is 480.
- The dot is already moving at frame 0, as approved.
- The fine line is drawn behind the squirrel and the dot in front. The circle stays open until the official outro closes it.

## Not yet verified (required before a publication master)

1. Viewing on a physical phone under the real Instagram, TikTok and Facebook interface overlays. I've only checked numerically and on frame extracts.
2. Listening on a phone speaker and headphones. Audio was checked by measurement only.
3. **Typeface:** this build uses Lora and Inter, as in BabyDashNow's earlier production files. The live page's headline serif looks heavier than Lora. Please confirm the site's font name, and I'll swap it in if it differs.
4. **Squirrel file:** the artwork arrived as a 1254 px WebP through chat. If a larger original PNG exists, I can swap it in with no other changes.
5. **Variant A** (no CTA) has not been exported. It needs only `--variant A`.
6. The **Santa hat** reads as Christmas more than Thanksgiving. That's a choice about the copy and posting timing, not something to change in the artwork.

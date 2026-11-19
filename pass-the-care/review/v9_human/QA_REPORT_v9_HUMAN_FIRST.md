# PASS THE CARE™: human-first review candidate v9 (Variant B)

**Status: REVIEW CANDIDATE. Not final and not for publication.** It still requires review on a physical phone (picture and sound) and a check of the referral landing page.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_HumanFirst_REVIEW_v9_VariantB.mp4` | 1080×1920, 30 fps, 672 frames, **22.4 s**. H.264 High, BT.709, AAC 48 kHz. |
| `..._cover_parent.png` | Cover option 1: the mother and baby with "Your hands are already full." (frame at 1.5 s) |
| `..._cover_offer.png` | Cover option 2: the Organic v6 offer cover |
| `../../build_full_circle_v9_human.py` | The renderer. It reuses Organic v6 and the approved audio work. |

## Structure: real parent → understanding → local service → PASS THE CARE™ → action

| Time | Picture | On screen | Sound |
|---|---|---|---|
| 0.00–3.00 | **Pexels video 7279098** (supplied edit, source 0.5–3.5 s), unaltered | *Your hands are* / *already full.* (Fraunces 700 ink plus Fraunces italic green, 74 px, on the clear wall above the mother) | A quiet, open felt-piano interval (G3/D4), a soft B3 at 1.6 s |
| 2.80–3.40 | The footage dissolves into BabyDashNow ivory | | |
| 3.27–6.33 | Ivory brand card | *Let us take one thing* / *off your list.* · official BabyDashNow logo · "Baby essentials, delivered locally." · Stamford · Darien · Norwalk · Greenwich | A gentle lift (E4/G4) as the card appears; a warm G-major chord with the logo |
| 5.67–6.53 | **The logo's green dot detaches** (a drawn dot of the same colour and size placed exactly over it) and glides to the emblem's 6 o'clock while the card leaves | | A soft accent tick as it detaches |
| 6.53–16.40 | **Organic v6 system**, fading in around the arriving dot: squirrel, PASS THE CARE™, Give $5. Get $5., the moving underline, the out-and-back orbit | Statement 1 on the outward leg; statement 2 on the return | The v6 AUDIO cues retimed: rising notes outward, **quiet at the qualifying-order pause**, warm answer on the return, soft close |
| 16.40–22.40 | **Official outro**, unaltered picture, plus "Discover PASS THE CARE™" | | Bridge under the outro's silent lead-in; **official chime 3 dB lower relative to the story** (the B2 correction) |

**Retiming of Organic v6 (not a straight attachment):**
- The v6 story now runs **9.87 s instead of 10.67 s**: a shorter outward and return leg, a 0.8 s order pause and a tighter hand-off.
- It starts from rest at the dot delivered by the logo, so the brand card and the offer read as one continuous movement.

## Reading times

| Text | On screen |
|---|---|
| "Your hands are already full." | 2.8 s |
| "Let us take one thing off your list." | 3.1 s |
| "Baby essentials, delivered locally." plus the towns | 2.2 s |
| PASS THE CARE™ / Give $5. Get $5. / tagline | 9.9 s |
| Statement 1: "They save $5 on their first order of $40+ in merchandise." | **4.3 s** |
| Statement 2: "You earn a $5 BabyDashNow reward when their qualifying order is completed." | **4.8 s** |

- Both statements are verbatim from the live page.
- Nothing about reward type, expiry, how the $40 is calculated or what "completed" means.

## Trust and accuracy

- **The footage is stock and is presented as a moment, not a testimonial.** No name, quote, purchase, delivery or endorsement is stated or implied. The lines are addressed to the viewer ("Your hands…", "Let us…"), not spoken by the mother.
- **Footage untouched:** no generated people and no alteration of the mother or baby. Frames before the dissolve match the supplied clip at ≥42.7 dB PSNR (higher means closer; above about 40 dB is visually identical) outside the text band; the only difference is one re-encode.
- **Licence note:** the Pexels licence permits commercial use without attribution, but **does not allow implying that identifiable people endorse a product**. This edit is consistent with that. Please keep the clip ID and licence on file.
- **Service line:** "Baby essentials, delivered locally." and the four towns come from your brief and the official outro. No delivery times, prices or other claims are made.

## Checks

| Check | Result |
|---|---|
| Squirrel | Unchanged: opaque pixels match the source exactly (max difference 0 across 125,732 pixels); one uniform scale; stationary. |
| Green dot | Story dot (56,108,14) is identical to the official outro dot. It settles into the outro's own first frame. |
| Official outro (picture) | Agreement with the original, measured as PSNR: at least 57.2 dB on whole frames before the CTA, and at least 56.05 dB outside the CTA band. CTA at y 1169–1197, 70 px clear of the town line. |
| Official chime | Same waveform, scaled only (residual −77.3 dB against the official track). Starts at **18.302 s** against 18.300 s expected. |
| Continuity | The longest digital silence before the chime is **0.12 s** (the deliberate clean entry). |
| Loudness balance (EBU R128 momentary max) | Parent −15.3 · card −13.9 · story −10.1 · outro lead-in −18.8 · **chime −10.4 LUFS**. The chime sits **level with the loudest story cue (−0.3 LU)** and 8.4 LU above the lead-in. |
| Integrated loudness | −16.5 LUFS, −1.0 dBTP. One linear gain, set so the true peak is −1 dBTP; no compression or limiting. |
| Frames and specs | 672 frames, no black frames. One near-uniform frame (the outro's own frame 0). |
| Safe zones | Story content stays within x 136–941 and y 306–1476. The opening line sits at y 236–395. **These are organic placements.** The opening line's top edge sits inside Meta's paid-ad top band (y < 269). |

## Required before publication

1. Watch and listen on physical iOS and Android phones (speaker and headphones) in the actual apps.
2. **Choose a cover:** the parent moment (more human) or the offer (clearer).
3. Check the referral landing page from "Discover PASS THE CARE™".
4. Keep the Pexels licence record for video 7279098.

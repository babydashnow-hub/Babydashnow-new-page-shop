# PASS THE CARE™ "Full Circle": QA report, final review candidate v6 (Variant B)

**Status: FINAL REVIEW CANDIDATE. Not approved for publication.** Publication still needs your visual, audio and on-phone checks (see the end of this report).

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FullCircle_CANDIDATE_v6_VariantB.mp4` | 1080×1920, 30 fps, 500 frames, 16.67 s. H.264 High, BT.709, AAC 48 kHz. |
| `PassTheCare_FullCircle_CANDIDATE_v6_VariantB_cover.png` | Composed cover: the closed emblem, the full headline and the tagline. |
| `v6_safezones/*.png` | Story frame and final frame with the Meta Reels ads and TikTok In-Feed ads safe zones overlaid. |
| `v6_safezones/Typeface_check_page_vs_Fraunces_vs_Lora.png` | Typeface check against the live page. |
| `../build_full_circle_v6.py` | The renderer: the v5 renderer with only these refinements. |

## The six requested refinements

**1. "Give $5. Get $5." readable throughout: DONE**
- Both halves now stay at **full contrast (6.7:1) in every frame**; the dimming is removed.
- Emphasis is shown by motion instead. A fine 3 px rule in the official green draws in under "Give $5." while the dot goes out. It glides to "Get $5." during the hold, as the dot turns back, and extends under both phrases when the circle closes.

**2. Near-white transition at about 10 s: IMPROVED, outro untouched**
- **Measured cause:** the official outro starts with one blank white frame, then its dot fades in from about 25% strength. In v5, the story dot shrank to nothing before the cut, so frames 316–321 (**6 frames, 0.20 s**) had nothing darker than 60 levels below white.
- **Fix:** the story dot now settles to the outro's own first-frame size (about 25 px) and strength (about 25%) at the outro dot's exact centre. Only the outro's own frames 0–1 remain near-white (**2 frames, 0.07 s**).
- Outro fidelity is unchanged (see check 6).

**3. CTA visibility against platform overlays: CTA FIXED; one finding for you to decide**
- **Reference:** I used the **published paid-placement safe zones**, which are the strictest:
  - Meta Reels ads: 14% top, 35% bottom, 6% sides. The bottom band starts at y 1248.
  - TikTok In-Feed ads: 240 px top, 660 px bottom (starts at y 1260), 120 px sides, plus the right-hand icon column (x 780–960, y ≥ 840).
  - Sources: [admanage.ai Reels checker](https://admanage.ai/instagram-reels-safe-zone), [adnova Meta safe-zones guide](https://adnova.ai/blogs/meta-ad-safe-zones-guide), [socialync TikTok](https://www.socialync.io/tools/safe-zones/tiktok), [merginit TikTok checker](https://merginit.com/tools/safe-zone-checker/tiktok).
  - These are third-party summaries of Meta's and TikTok's own guidance. **They are not screenshots of the real apps.**
- **CTA:** in v5 the CTA sat at y 1247–1275, right on Meta's line. It has moved up to **y 1169–1197**. That is 70 px clear of the outro's lowest element (the town line at y 1099) and **inside both platforms' paid safe areas**. It is composited into empty outro space only; no official element is covered.
- **Finding:** the two **offer statements (y 1288–1476) fall inside the paid-ad bottom bands** on both platforms. The emblem's right edge also passes under TikTok's icon column. For **organic** posts the bottom interface is smaller, and the statements sit above most of it, but that's borderline.
  - **If this video will run as a paid ad**, I recommend a paid-safe layout: statements raised above y 1248. That requires a smaller emblem and squirrel, so it's a creative decision for you, not something I changed silently.
- **Also noted:** the **official outro's** wordmark and tagline extend under TikTok's right icon column at their right edge. That is part of the approved master and is left untouched.

**4. Typeface: CONFIRMED and changed with a visual check**
- I took the families from the CSS you quoted (Fraunces, then Source Serif 4, then Georgia).
- I rendered Fraunces 700 and Lora Bold next to the live page's "Give $5. Get $5." from your screen recording (see the comparison image). **Fraunces 700 matches** the page's letterforms: "G", "$", ball terminals and weight. **Lora does not.**
- **Now used:**
  - Headline: Fraunces 700, 108 px.
  - Tagline: "A little help," in Fraunces 700 ink and *"passed forward."* in Fraunces 400 italic green, exactly as on the page.
  - Statements: **Inter** Regular 40 px, to match the page's sans-serif body text. Inter is also what the label already used. *Please confirm Inter is the site's body font.*
- Fraunces is SIL Open Font License 1.1, from the fontsource package. It uses static instances at their default optical size.

**5. Offer conditions in full, with reading time: PASS**
- Both statements are verbatim from the live page; only the line breaks differ.
- Condition 1 is on screen **4.7 s**; condition 2 is on screen **4.8 s**.
- Nothing about reward type, expiry, how the $40 is calculated or what "completed" means.

**6. Squirrel, dot, outro and chime preserved: PASS**
- **Squirrel:** stationary, one uniform scale (0.38278). Opaque pixels match the source exactly (maximum difference 0 across 125,732 pixels).
- **Dot:** (56,108,14), identical to the outro's dot.
- **Outro:** agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical), is at least 57.2 dB on whole frames before the CTA appears and at least 56.0 dB outside the CTA band. Audio is the original track with one gain change; anything left over is −77.3 dB below the signal.
- **Chime:** starts at 12.569 s, against 12.567 s expected.

## Other checks

| Check | Result |
|---|---|
| Frames and specs | 500 frames. No black frames. Only one near-uniform frame (the outro's own frame 0). |
| Story content | Stays within x 136–942 and y 306–1476. |
| Contrast | Headline 6.7:1, tagline 17.4:1, statements 8.1:1, CTA 7.4:1. |
| Loudness | −19.2 LUFS, −1.0 dBTP. Limited by true peak; the chime is not limited. |

## Required before publication (not done here)

1. Play it on physical iOS and Android phones in Instagram Reels, TikTok and Facebook Reels, both as an organic post and, if relevant, as an ad preview in Ads Manager or TikTok Ads Manager.
2. Listen on a phone speaker and on headphones.
3. **Decide on paid placement:** if it will run as a paid ad, approve a paid-safe layout variant first.
4. Confirm Inter as the site's body font.
5. Export Variant A (no CTA) if needed.

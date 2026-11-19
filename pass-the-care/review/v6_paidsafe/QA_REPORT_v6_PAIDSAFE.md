# PASS THE CARE™ "Full Circle": QA report, paid-safe Variant B (v6)

**Status: REVIEW CANDIDATE. Not approved for publication.** Nothing has been published and the website has not been changed.

## Deliverables

| File | Description |
|---|---|
| `PassTheCare_FullCircle_CANDIDATE_v6_PAIDSAFE_VariantB.mp4` | Paid-safe master for Meta Reels ads and TikTok In-Feed ads. 1080×1920, 30 fps, 510 frames, **17.00 s**. H.264 High, BT.709, AAC 48 kHz. |
| `PassTheCare_FullCircle_CANDIDATE_v6_PAIDSAFE_VariantB_cover.png` | Cover: label, full headline, tagline, closed emblem. Every element sits inside both platforms' safe areas. |
| `Compare_Organic_vs_PaidSafe_v6.mp4` | The two versions playing side by side (paid-safe audio). |
| `Compare_Organic_vs_PaidSafe_v6.png` | Four matched moments with the overlay zones tinted. |
| `BodyFont_check_*.png` | Live page body text against DM Sans and Inter. |
| `../../build_full_circle_v6_paid.py` | The renderer. It reuses organic v6 entirely and changes only the layout. |
| Organic candidate | `../PassTheCare_FullCircle_CANDIDATE_v6_VariantB.mp4`, preserved unchanged. |

## Overlay standard used

The **intersection** of the strictest published paid-placement zones:
- **Meta Reels ads:** 14% top, 35% bottom, 6% sides.
- **TikTok In-Feed ads:** 240 px top, 660 px bottom, 120 px sides, plus the right icon column (x 780–960, y ≥ 840).

**Essential area:** x 120–960, y 270–1248, and x ≤ 780 below y 840.

Sources (third-party summaries of the platforms' own guidance, **not app screenshots**): [admanage.ai](https://admanage.ai/instagram-reels-safe-zone), [adnova](https://adnova.ai/blogs/meta-ad-safe-zones-guide), [socialync TikTok](https://www.socialync.io/tools/safe-zones/tiktok), [merginit](https://merginit.com/tools/safe-zone-checker/tiktok).

## How it was recomposed (not shrunk)

- **Grid:** left-aligned editorial layout at x = 128, mirroring the left-aligned hero of the PASS THE CARE™ page. The right-hand strip under TikTok's icons is left as deliberate empty space.
- **Statement slot:** one slot sits directly under the headline. The tagline opens it at frame 0, then the two verified statements take turns in it. Each is set as **2 lines on a wider measure** at the same 40 px Inter, instead of 3 narrow lines below the emblem.
- **Emblem:** moved into the lower-left field (centre x 450, y 938, radius 285), fully clear of TikTok's icon column.
- **Squirrel:** stays at **440 px, the approved v4 size**, only 6% smaller than organic v6. It is placed with a small optical offset (−16, −12 px) so the travelling dot keeps **26 px** clearance from it.
- **Headline:** Fraunces 700 at 100 px (organic uses 108 px), at full contrast with the same travelling green rule.

## Checks

| Check | Result |
|---|---|
| **Overlay compliance (every frame scanned)** | **Story: 0 content pixels** inside any Meta or TikTok ad zone, across all 330 story frames. **CTA: 0.** Organic v6, for comparison: about 16,000 pixels per frame at worst. |
| Official outro under overlays (documented, not modified) | **TikTok:** the outro's wordmark ("…Now™"), "We show up when it matters" and the town line extend into TikTok's right margin and icon column (up to 9,950 px per frame). **Meta:** the "™" briefly crosses the 6% side margin for 2 frames during the outro's own lockup slide (outro frames 79–80). Both are properties of the approved master and are left untouched pending your decision. |
| Offer terms | Verbatim from the live page; only the line breaks differ (checked in code). Statement 1: 30–160 (**4.3 s**). Statement 2: 162–312 (**5.0 s**). Tagline: 0–28. Nothing about reward type, expiry, how the $40 is calculated or what "completed" means. |
| Readability | Headline 6.7:1 contrast, statements 8.1:1 at 40 px, tagline 17.4:1, CTA 7.4:1. All are full contrast at all times. |
| Squirrel | One uniform scale (0.35805). Opaque pixels match the source exactly (maximum difference 0 across 109,973 pixels). Stationary. |
| Green dot and hand-off | Story dot (56,108,14) is identical to the outro dot. It settles to the outro's first-frame state. Only the outro's own frames 0–1 are near-white. |
| Official outro | Agreement with the original, measured as PSNR (higher means closer; above about 50 dB is visually identical): at least 57.2 dB on whole frames before the CTA appears, and at least 56.06 dB outside the CTA band. Audio is the original track with one gain change; anything left over is −77.3 dB below the signal. **Chime** starts at 12.902 s against 12.900 s expected. |
| CTA | "Discover PASS THE CARE™" at y 1169–1197, 70 px below the outro's town line, inside both platforms' paid safe areas. |
| Specs | 510 frames, no black frames. Loudness −19.2 LUFS, −1.0 dBTP, capped by true peak; the chime is not limited. |

## Body typeface (DM Sans vs. Inter)

- **What I compared:** the page's rendered body text from your screen recording against DM Sans and Inter (see the `BodyFont_check` images).
- **Result:** the rendered page is **not DM Sans**. DM Sans's "0" is nearly circular, while the page shows a narrow oval "0" in "$40+". The page's letter widths and the shapes of "t", "r" and "a" also match **Inter**, or the macOS system font (SF Pro), which is almost identical at this size.
- **Likely cause:** the CSS names DM Sans, but the browser that made the recording fell back to another font. DM Sans may not be loading on the live site. **I have not changed the website.** The web team can confirm in the browser's developer tools (Computed, then Rendered Fonts).
- **Decision for the video:** **keep Inter**, because it matches what visitors actually see in your recording. If the site is fixed to load DM Sans, a one-line change switches the statements to DM Sans in both versions.

## Remaining gate (not done here)

1. Watch it on physical iOS and Android devices, including the Ads Manager and TikTok Ads Manager previews for the paid-safe version and the organic placements for v6.
2. Listen on a phone speaker and on headphones.
3. Check the referral landing-page experience end to end.
4. Decide whether the official outro's TikTok overlap is acceptable as is.
5. Confirm the body font with the web team.

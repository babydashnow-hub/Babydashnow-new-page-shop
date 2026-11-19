# BabyDashNow™ Brand Reel: publication candidate, QA report

**Status: PUBLICATION CANDIDATE, pending your physical-phone review. Not published.**

## 1. The "512 × 910" finding

- **The exported MP4 is 1080 × 1920.**
- The render pipeline has no 512 × 910 step anywhere:
  - footage is decoded and scaled once to 1080×1920 (Lanczos);
  - frames are encoded at `-s 1080x1920`.
- **Likely cause:** the inline video preview in the chat app, which re-encodes video for playback. The previous file was sent with an inline preview.
- **This time the MP4 is delivered as a download-only attachment**, so you receive the original bytes. You can verify the checksum below.
- **Proof the pixels are native, not upscaled:** fine detail above 512-px resolution (luma RMS after a 512 px round trip):

| Frame | Score |
|---|---|
| Mother frame, this file | **4.01** |
| Same frame sent through 512 px and back (control) | **0.90** |
| Shelf frame | 2.14 |
| CTA frame | 12.21 |

  A 512 × 910 file upscaled to 1080 would score close to the control.
- **Full-resolution still from the file:** `Verify_native_frame_1080x1920_f040.png` (1080×1920).

## 2. File metadata (ffprobe, actual export)

| Field | Value |
|---|---|
| File | `BabyDashNow_BrandReel_PUBLICATION_CANDIDATE_1080x1920.mp4` |
| SHA-256 | `a637dbc27c151d1f4276e4da96f4ff3177e7cee994e52a9ea601b7f11d29f539` |
| Size | 16,297,070 bytes |
| Video | H.264 High, level 5.0, **1080×1920** (coded 1080×1920), square pixels, **30 fps** (r = avg = 30/1), **312 frames**, yuv420p, BT.709 primaries/transfer/matrix, limited range, 12.38 Mbps |
| Audio | AAC-LC, 48 kHz, mono, ~144 kbps |
| Duration | 10.40 s |

**This is the same render as the approved v2** (byte-identical; same checksum), now named as the publication candidate. It was rendered directly from the originals:
- **Mother:** Pexels 7279098, UHD 2160×3840, 23.976 fps. One Lanczos downscale; 30 fps by frame repetition. No grade, no sharpening.
- **Shopping:** IMG_7019, 4K HLG/BT.2020. Neutral HLG → SDR BT.709 tone map only. No grade, no saturation change, no sharpening.
- **Export:** CRF 12, preset slow, tune film.

## 3. Image quality (from the v2 audit, unchanged)

| Shot | Detail vs original | Clipped highlights | Crushed blacks |
|---|---|---|---|
| Mother | 98% of the 4K original | 0% | 0.01% |
| Shelf | Matches the source tone map | 0% | 0.56% (dark shelf gaps, as in the source) |
| Cart | Matches the source tone map | 0% | 0% |

- No brightness lift, saturation boost or sharpening.
- The hand in the cart shot is motion-blurred in the original footage; that detail does not exist in the source and is not claimed.

## 4. Storyline and pacing (unchanged from v2)

| Time | Content |
|---|---|
| 0.00–2.30 | Mother and baby: "Your hands are *already full.*" |
| 2.30–4.80 | Pampers selected, then Pampers and wipes in the cart: "We'll handle *the essentials.*" |
| 4.40–10.40 | Official BabyDashNow outro, with "Baby essentials, *delivered locally.*" and the CTA "Order at BabyDashNow.com" (6.60–10.40 s) |

## 5. CTA against organic overlays (`CTA_vs_organic_overlays.png`)

**CTA pill:** x 182–898, y 1176–1284; Inter SemiBold 46 px, white on brand green; 7.4:1 contrast.

| Platform (organic) | UI zones used (third-party estimates) | CTA |
|---|---|---|
| Instagram Reels | Top 210 px, bottom 310 px (from y 1610), right 120 px | ✅ clear: 326 px above the caption band, 62 px from the icon column |
| TikTok | Top 130 px, bottom 480 px (from y 1440), right 150 px | ✅ clear: 156 px above the caption band, 32 px from the icon column |

- **Documented, not modified:** the official outro's wordmark ("…Now™") and the end of "We show up when it matters" reach under TikTok's right-hand icon column, and the "™" reaches under Instagram's. They're part of the approved master.
- Platform interfaces vary by device and caption length, so check on a real phone.

## 6. Brand and audio (unchanged from v2)

- **Brand:** official outro picture unaltered. CTA green measured at (44, 96, 16) against spec (45, 97, 17), a one-level encoding difference. No grading on any brand graphic.
- **Audio:**
  - −16.0 LUFS integrated, −2.0 dBTP; linear gains only.
  - The official chime is the same waveform, starting at 6.302 s.
  - The chime sits **+0.3 LU** above the loudest music: no jump.
  - Longest digital silence before the chime: 0.11 s (deliberate).

## 7. Before publishing

1. Watch on physical iOS and Android phones in Instagram Reels and TikTok, at full screen with sound.
2. Confirm the ordering flow at BabyDashNow.com on a phone.
3. Confirm the visible third-party marks (Pampers; Kirkland Signature / Costco).
4. Keep the Pexels licence record for video 7279098.

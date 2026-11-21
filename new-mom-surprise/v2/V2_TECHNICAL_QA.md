# V2 technical QA: "For a Special New Mom"

**Status: candidate for founder review. Not published.**

## Deliverables

| File | Size | SHA-256 |
|---|---|---|
| `BabyDashNow_ForASpecialNewMom_V2_MASTER_2160x3840_HLG_DV84.mov` | 164,133,549 B | `52eb9866ddfdc9b69a39bb18dcd4aa8e42090f82dccf8d23703c56c2d81deb8e` |
| `BabyDashNow_ForASpecialNewMom_V2_REVIEW_1080x1920_HLG_DV84.mov` | 36,506,074 B | `76a80eae1e6c6163b84e663536864e0d7a261d54b2bfe82b55d0f87cdb31a902` |

## Video specifications (measured with ffprobe on the delivered files)

| Property | Master | Review copy | iPhone sources (reference) |
|---|---|---|---|
| Codec / profile / tag | HEVC Main 10, `hvc1` | HEVC Main 10, `hvc1` | HEVC Main 10, `hvc1` |
| Bit depth / chroma | 10-bit 4:2:0 | 10-bit 4:2:0 | 10-bit 4:2:0 |
| Resolution | **2160×3840 portrait** | 1080×1920 portrait | 2160×3840 (A: 1440×2560) |
| Frame rate / frames / duration | 30/1, **644**, 21.467 s | 30/1, 644, 21.467 s | 30/1 (J: 29.97) |
| Colour | BT.2020 / **HLG** / BT.2020nc, limited | Same | Same |
| **Dolby Vision** | **Profile 8, level 7, BL compatibility 4**, RPU on **644/644** frames | Profile 8, level 4, compatibility 4, RPU on 644/644 | Profile 8.4 |
| Dolby Vision metadata values | **644/644 RPUs byte-identical to the exact source frame shown** | 644/644 | — |
| Ambient Viewing Environment | `amve` box + hvcC SEI, **644/644 frames** (copied unchanged from source) | 644/644 | Present |
| Video bitrate | 60.9 Mbps (x265 CRF 12, slow) | 13.4 Mbps (CRF 16) | about 25–29 Mbps |
| Decode | Clean, no errors | Clean | — |

## How fidelity was preserved

- **Sources:** opened read-only. **SHA-256 of all 10 sources is identical before and after** (10/10 OK).
- **Pixel path:**
  - Decoded 10-bit YUV → frame-exact trims → concatenation → 10-bit HEVC.
  - **No RGB conversion, grading, LUT, sharpening, denoise, stabilisation, crop or reframe.**
  - Only clip A (a 1440×2560 export) is scaled to 2160×3840 (Lanczos). That's unavoidable for a 4K timeline; the camera original of A was not available.
  - Clip J is conformed 29.97 → 30 fps by frame selection; no interpolation.
- **Text:** drawn as HLG graphics at reference white (75% HLG, the ITU-R BT.2408 graphics level) and composited in the same 10-bit YUV domain. Footage outside the text is untouched.
- **Dolby Vision:**
  - The camera's own per-frame RPUs were extracted from each source and appended, unchanged, as the last NAL unit of each output frame, matched by presentation timestamp (within 2 ms).
  - A Dolby Vision configuration box identical in form to the iPhone's (`dvvC`, profile 8, BL compatibility 4) and the source's `amve` / ambient SEI were added.
  - Done with a purpose-built script (`mp4dv.py`). The standard tools (`dovi_tool`, MP4Box) could not be installed in this environment.
- **Frame-exact edit:** the EDL (`V2_EDL.csv`) records the source timestamp of every first and last frame.
  - Note: shot 4 (clip C) contains 55 frames. That clip's first frames sit off the 1/30 s grid in the camera file, so the same 1.8 s window holds one extra real frame. It's documented, not a defect.

## Image fidelity against the exact source frame (middle frame of every shot, text areas excluded, 10-bit)

| Shot | Source | Mean luma difference (codes of 1023) | 99th percentile difference | SSIM |
|---|---|---|---|---|
| 1 | A (handwriting) | −0.02 | −0.38 | 0.9991 |
| 2 | A (heading) | −0.01 | 0.00 | 0.9987 |
| 3 | D (empty box) | +0.01 | 0.00 | 0.9979 |
| 4 | C (paper fill) | +0.01 | 0.00 | 0.9977 |
| 5 | E (swaddle) | 0.00 | 0.00 | 0.9968 |
| 6 | G (lotion) | 0.00 | 0.00 | 0.9962 |
| 7 | H (tissue) | −0.01 | 0.00 | 0.9975 |
| 8 | I (card) | +0.01 | 0.00 | 0.9962 |
| 9 | J (seal) | −0.05 | 0.00 | 0.9969 |
| 10 | K (car) | 0.00 | 0.00 | 0.9967 |
| 11 | P (doorstep) | −0.01 | 0.00 | 0.9963 |

- No measurable change in brightness or highlights; structural similarity 0.996–0.999.
- The review copy (1080p, compared against sources scaled to 1080p) gives SSIM 0.988–0.996.
- *These measurements support, but do not replace, the founder's visual review on the iPhone.*

## Audio

- **Original music only:** solo felt-piano composition synthesised for this film (no third-party music, no licence dependency). G major, sparse, resolving on the doorstep.
- **Loudness:** −17.2 LUFS integrated, −4.0 dB peak. AAC-LC stereo 48 kHz, about 237 kbps.
- **No source audio used.** Pen, paper and room sound were not included because the camera audio could not be reliably reviewed for private speech or radio in this environment. It can be added after the founder listens to the selected ranges.

## Not yet verified (needs the founder's devices)

1. **Apple playback of the injected Dolby Vision:** confirm in the iPhone Photos app (and QuickTime on the Mac) that the master plays as HDR and looks like the originals. The metadata is structurally identical to the iPhone's, but Apple-device behaviour can only be confirmed on the device.
2. Social upload behaviour: Instagram (iOS) Dolby Vision, YouTube HLG, and TikTok/Facebook via private test uploads.

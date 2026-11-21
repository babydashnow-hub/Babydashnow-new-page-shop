# T1 technical inspection: Apple-native HEVC export (`avconvert`, PresetHEVCHighestQuality)

**Scope:** read-only inspection of the uploaded T1 against the original IMG_7321.mov (SHA-256 `32a2cb38…98ac45`, which the founder confirmed is identical to the Mac copy). No files were modified. T2 and V2 have not been run.

## Files

| File | Size | SHA-256 |
|---|---|---|
| Upload `T1_IMG_7321_HEVC_full.mov.zip` | 21,420,904 B | `236afe58b82120b9b3f06aa6a547f2ebe077183a0c1ae50bb8f152db0d09f8d6` |
| `T1_IMG_7321_HEVC_full.mov` (inside, stored as a single entry) | 21,426,425 B | `7cd5d50a0482597df73c558b0893e4f8692f7ef1a5975ba721f27687200dd006` |

**→ Please compare this MOV checksum with the one your Terminal printed in step 5.** If they match, the file was not altered in transfer.

## Results (source vs T1)

| # | Check | Source | T1 | Result |
|---|---|---|---|---|
| 1 | Codec / profile / depth | HEVC Main 10, `hvc1`, 10-bit 4:2:0 | HEVC Main 10, `hvc1`, 10-bit 4:2:0 | **PASS** |
| 2 | Picture / orientation | 3840×2160 with rotation −90 (displays 2160×3840) | **2160×3840 stored upright** (rotation baked in, no matrix) | **PASS** (an equivalent display) |
| 3 | Colour signalling | BT.2020 / HLG (arib-std-b67) / BT.2020nc / limited | Identical | **PASS** |
| 4 | Dolby Vision configuration | Profile 8, level 7, RPU present, BL compatibility ID 4 | **Identical** | **PASS** |
| 5 | Dolby Vision RPU per frame | 203/203 frames | **204/204 frames** | **PASS** |
| 6 | Dolby Vision metadata values | — | **Identical to the source, frame for frame** (203/203 aligned frames) | **PASS** (note: the values are essentially constant across this clip, so this confirms the same mapping, not frame-level variation) |
| 7 | Ambient Viewing Environment | 203/203 frames | **204/204 frames** | **PASS** |
| 8 | Frame rate / timing | 30/1, 203 frames, 6.765 s, all intervals 33.33 ms | 30/1, **204 frames**, 6.795 s. One interval of 28.33 ms at the start. | **CAVEAT** (see A) |
| 9 | Luma signal vs source (aligned, 14 frames, native 4K) | — | Mean difference −0.16 to +0.32 codes (of 1023); 99th percentile ±0.0 | **PASS** (target ±2 / ±4) |
| 10 | Chroma vs source | — | Mean Cb/Cr difference ≤ +0.16 / +0.09 codes | **PASS** (target ±2) |
| 11 | Structural similarity (8×8 SSIM, native 4K, 10-bit) | — | Min 0.9811, mean 0.9881 | **PASS** (≥ 0.98; supporting evidence only) |
| 12 | Video bitrate / GOP | 25.1 Mbps; keyframe about every 1.07 s | 25.0 Mbps; keyframe about every 0.93 s | Comparable |
| 13 | Audio | AAC stereo + Apple spatial (APAC, 4 ch) | **Single AAC 4-channel (quad) track**; the stereo AAC track is not carried | **CAVEAT** (see B) |
| 14 | Apple metadata tracks (`mebx`) | Present | Not carried | Informational (not required for HDR playback) |

## Caveats

**A. One extra frame at the start (28 ms).**
- The source is a trimmed re-save whose edit list starts mid-GOP: 232 coded frames, 203 displayed.
- T1's first frame is the source's pre-roll frame just *before* the displayed start, shown for 28 ms. From T1 frame 1 onward, T1 matches the source frame for frame.
- Invisible in normal viewing, but it shows that **`avconvert` trims are not guaranteed frame-exact at edit-list boundaries.** This matters for T2 and V2 cut points; the in/out points will need verifying.

**B. Audio track changed.** The export keeps one 4-channel AAC track (converted from Apple's spatial audio) and drops the stereo AAC track. This is irrelevant to the picture test, but for V2 the audio route must be chosen deliberately (stereo mix, ambient sound only after the privacy review).

## Verdict

**The technical criteria for HDR and Dolby Vision preservation pass.** Apple's native HEVC export kept:
- 10-bit HEVC Main 10 at full 4K portrait resolution;
- BT.2020 / HLG signalling;
- the Dolby Vision 8.4 configuration and RPU on every frame;
- the Ambient Viewing Environment metadata;
- a picture signal statistically indistinguishable from the source.

That's the opposite of V1, which lost Dolby Vision, the ambient metadata and resolution.

**Not yet established:** the *visual* match as perceived by the founder. The measurements support it but don't replace it.

## Next step (requires approval)

The **visual A/B** from the approved procedure:

- **Mac:** QuickTime Player, `~/Downloads/IMG_7321.mov` vs `T1_IMG_7321_HEVC_full.mov`, both full screen, on mains power, with auto-brightness, True Tone and Night Shift off. Pause at 1.00 s, 2.40 s and 5.90 s and toggle (Cmd-`).
- **iPhone 16 Pro (primary HDR judge):** AirDrop T1 (Options → All Photos Data) and compare in Photos against the original at the same moments and brightness.
- **Judge:** white tissue and cream card, the dark green card, skin tone, print sharpness, highlight detail, banding, and any flicker in the first frames.

**T2, V2, SDR conversion and any effects remain unauthorized.**

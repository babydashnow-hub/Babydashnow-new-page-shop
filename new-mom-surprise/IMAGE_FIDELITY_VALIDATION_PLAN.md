# B. Image fidelity validation plan (to run **before** any V2 edit)

**Status:** plan only. No test files exist yet. Running it requires explicit authorization.

## 1. Test material: six representative moments

| # | Subject | Source | Test segment (source s) | Why |
|---|---|---|---|---|
| T1 | Handwriting | A (E6A28B63.mp4) | 10.47 → 12.30 | Skin tone, warm wood, white paper; resolution (1440p source) |
| T2 | White gift box interior | D IMG_7306 (d3ff4db1) | 3.40 → 4.60 | Large near-white area: **54% above reference white** |
| T3 | Paper filling | C IMG_7306 (76696015) | 0.00 → 1.80 | Fine texture; mid-tones; motion |
| T4 | Product packaging | E IMG_7308 | 3.00 → 5.00 | Saturated cyan/yellow; small printed text |
| T5 | BabyDashNow seal | J IMG_7325 | 1.80 → 3.50 | Brand detail; 29.97 fps conform |
| T6 | Final delivery scene | P IMG_7356 | 0.00 → 4.00 | Cool grey door; bright floor; skin-free colour reference |

## 2. Outputs to test (per approved workflow)

| ID | Output |
|---|---|
| **O-HDR** | Final Cut Pro export: HEVC 10-bit, HLG, Dolby Vision 8.4, 2160×3840, 30p. The six segments as one straight-cut file. |
| **O-SDR** | Final Cut Pro SDR export (Rec. 709) of the same segments |
| *(optional)* **O-B** | Workflow B file (camera RPU reinjected), only if A fails |

## 3. Required file metadata (pass/fail)

| Field | O-HDR | O-SDR |
|---|---|---|
| Codec / profile | HEVC Main 10, 4:2:0 10-bit | H.264 High or HEVC Main, 8-bit acceptable |
| Resolution / fps | **2160×3840**, 30/1, square pixels | 2160×3840 or 1080×1920, 30/1 |
| Colour signalling | BT.2020 primaries, **HLG (arib-std-b67)**, BT.2020nc, limited range | BT.709 / BT.709 / BT.709 |
| Dolby Vision | DOVI configuration record **profile 8, bl_compat_id 4**, plus a **RPU on every frame** (RPU count = frame count) | none |
| Duration | Equal to the sum of the segments, frame-exact | same |

Checked with `ffprobe` (stream side data plus per-frame side data count) and, on the Mac, MediaInfo if available.

## 4. Playback and display conditions (same Mac, same display)

- **Display:**
  - HDR-capable display with **High Dynamic Range on**.
  - **Fixed brightness:** auto-brightness off, True Tone off, Night Shift off.
  - On XDR displays, preset "Apple XDR Display (P3-1600 nits)" for HDR and "HDTV Video (BT.1886)" for the SDR test.
  - Battery "Optimize video streaming" off; on mains power.
  - Dim, constant room light; no window glare.
- **Player:** **QuickTime Player** for both the original and the test file. Optionally repeat in Photos. **No browser, Quick Look or chat preview.**
- **Files** must be opened from local disk. Never use transcoded previews.

## 5. Comparison method

1. **A/B toggle (primary):**
   - Open the original clip and the test output in two QuickTime windows, identical size, full-screen on the same display.
   - Pause on the **same frame**: use the frame numbers provided, with the timecode overlay off.
   - Toggle between windows (Cmd-`). Judge differences as flicker; this is more sensitive than side by side.
2. **Side by side (secondary):** both windows at "Actual Size" next to each other, same vertical position. Only for detail and resolution (T1, T3, T4).
3. **Moving playback:** watch each segment once in each version, to check for flicker, metadata glitches and frame-rate stutter (T5).
4. **iPhone cross-check:** AirDrop O-HDR to the iPhone and compare in Photos with the original clip at the same brightness.
5. **SDR test:** compare O-SDR against the **original with the Mac's HDR switched off**. Never compare SDR against HDR playback.

## 6. Visual acceptance criteria (founder decides)

A segment passes only if, in the A/B toggle:

1. **White paper, tissue and box interior** keep the same brightness and tint. No greying, no added whiteness.
2. **Skin tones** (T1) keep the same hue and warmth.
3. **Packaging colours** (T4: cyan, yellow, green) are unchanged in hue and saturation.
4. **Highlight detail** on paper and box edges is not clipped or flattened.
5. **Fine detail** (paper fibres, print, handwriting strokes) is equal at Actual Size. For T1, judge relative to its 1440p source.
6. **No banding** in smooth gradients (box interior, wall, floor).
7. **No new artefacts:** flicker, brightness pumping between shots, colour shifts at cuts, stutter.

**Any visible difference the founder flags = fail, regardless of the numbers below.**

## 7. Supporting measurements (inform, never replace, the visual judgement)

| Measurement | Tool | Indicative target |
|---|---|---|
| Dolby Vision RPU present on every frame | ffprobe per-frame side data | 100% |
| Signal-level equality (HDR): mean and 99th-percentile HLG luma, mean Cb/Cr per segment | ffmpeg / numpy on 10-bit planes | Mean code difference ≤ 2 (of 1023); p99 within 4 |
| Colour difference (HDR): median ΔE2000 after decoding both through the same BT.2100 display model | colour-science script, read-only | Median ≤ 1.0, 95th percentile ≤ 2.5 |
| Detail retention: SSIM and VMAF of export vs source at 2160×3840 | ffmpeg `libvmaf` (if available) / SSIM | SSIM ≥ 0.98; VMAF ≥ 95 |
| Highlight compression (SDR only): share of pixels clipped or compressed vs the original's share above reference white | numpy | Reported, not pass/fail |
| Banding: gradient step analysis on T2/T6 flat areas | numpy | No new visible steps |

**Measurement caveat:** the earlier V1 report showed that high PSNR can coexist with perceived loss. The numbers support the visual decision only.

## 8. Decision rule

- **All six segments pass visually** → authorize the V2 edit with the validated workflow and settings, frozen.
- **Any fail** → diagnose that segment (metadata, scaling, export setting). Re-test only that variable. Escalate to Workflow B only with authorization.
- **Record:** file names, checksums, ffprobe output, display settings, founder's verdict per segment.

# A. Technical workflow recommendation: "For a Special New Mom"

**Phase:** read-only investigation. Nothing was installed, converted, exported or modified.

## 1. Mac environment: limitation

**I don't have access to the founder's Mac.** This session runs in a cloud container. No computer is connected through Remote Control (the session's computer list is empty), so the macOS version, chip, display, HDR setting and installed editors **could not be inspected**. The findings below are therefore requirements and a verification procedure, not observations of the Mac.

**Shortest verification procedure (about 2 minutes, read-only).** In Terminal on the Mac, run these and send the output:

```
sw_vers
system_profiler SPHardwareDataType SPDisplaysDataType | grep -iE "Chip|Model Name|Memory|Display Type|Resolution|Main Display|Connection|XDR|HDR"
ls /Applications | grep -iE "Final Cut|iMovie|Compressor|DaVinci|Premiere"
mdls -name kMDItemVersion "/Applications/Final Cut Pro.app" "/Applications/iMovie.app" 2>/dev/null
```

Then also report:
- **System Settings → Displays:** is there a "High Dynamic Range" toggle, and is it on? Which preset is selected (for example "Apple XDR Display (P3-1600 nits)")? Are True Tone and automatic brightness on or off?
- **System Settings → Battery** (laptops): is "Optimize video streaming while on battery" on? It can limit HDR playback.
- Which app was used to watch V1 (QuickTime Player, Photos, Finder Quick Look or a browser)?

**Why it matters:**
- Only Macs with an HDR-capable (EDR) display, such as MacBook Pro Liquid Retina XDR, Pro Display XDR or certain external HDR monitors, show HLG/Dolby Vision highlights brighter than SDR white.
- On a non-HDR display, macOS tone-maps HDR to SDR, so the originals and any HDR master will look different than on the iPhone.
- **V1's SDR file was viewed on the Mac against originals that macOS rendered from Dolby Vision/HLG.** That alone can make V1 look flatter even before V1's own conversion losses (Report A of the reset).

## 2. Source facts that drive the workflow (verified)

| Item | Finding |
|---|---|
| iPhone clips (C–P, Q/R) | HEVC Main 10, 10-bit 4:2:0, 2160×3840 (rotation flag), 30 fps (J and L: 29.97), BT.2020 / HLG, **Dolby Vision Profile 8.4** (bl_compat_id 4) with **per-frame RPU** (60/60 frames checked), Ambient Viewing Environment SEI, 6 Apple metadata tracks |
| **Clip A (handwriting)** | HEVC 10-bit HLG with a Dolby Vision configuration record, but **1440×2560** with no camera metadata. **It contains an internal cut at 10.467 s (frame 314).** It's an **edited export, not a camera original.** |
| Keyframes | One keyframe per clip. **Frame-accurate lossless cutting is impossible**, so any edit re-encodes. |
| V1 | Dolby Vision, ambient environment and Apple metadata **dropped**; 1080p; generic SDR conversion (whites peaked at 227–238 / 255) |

## 3. Workflow comparison

### Workflow A: Apple-native HDR editing in **Final Cut Pro** (Mac)

- **Setup:** a Wide Gamut HDR library, and a project at Rec. 2020 HLG, 2160×3840 (custom vertical), 30p.
- **HLG and 10-bit:** preserved through editing (10-bit-or-higher pipeline) and on export with HEVC 10-bit or ProRes ([Apple: Edit HDR video recorded on iPhone](https://support.apple.com/HT211950), [Apple HDR/Wide Color paper](https://www.apple.com/final-cut-pro/docs/HDR_WideColor.pdf)).
- **Dolby Vision:** Final Cut Pro **does not pass through** the iPhone's per-frame Dolby Vision metadata. It ignores it while editing and **regenerates Dolby Vision 8.4 metadata on export** ("HEVC 10-bit, HLG, Dolby Vision 8.4") ([Final Cut Pro user guide](https://support.apple.com/guide/final-cut-pro/ver504d31dd2/mac); [Apple developer: HDR video with Dolby Vision](https://developer.Apple.com/av-foundation/Incorporating-HDR-video-with-Dolby-Vision-into-your-apps.pdf)).
  - **Preserving HLG does not mean preserving the camera's own Dolby Vision analysis.** The exported metadata is Apple-generated: same format and same intended Apple playback path, but not byte-identical.
- **iMovie on Mac is not suitable:** it imports HDR but **shares only SDR**. HDR from a Mac iMovie project requires sending it to Final Cut Pro (same Apple article). iMovie on iPhone/iPad can export HDR (Options → HDR), but with fewer controls for a vertical 4K master.
- **Aspect ratio and frame rate:** native 9:16 at 2160×3840, 30 fps. J and L (29.97) conform to 30 within the 30p project.
- **Clip A** (1440×2560) would be **scaled up 1.5×** in a 4K timeline, unless the camera original is supplied (recommended).

### Workflow B: High-fidelity HDR assembly with original metadata (scripted, outside Apple apps)

- **Method:** extract each clip's original Dolby Vision RPU (`dovi_tool`), cut it to the EDL, re-encode the HLG base layer at 2160×3840 with x265 in Dolby Vision 8.4 mode, and inject the **camera's own** RPU frame-for-frame.
- **Pros:**
  - Keeps the camera's per-frame metadata rather than regenerating it.
  - No SDR conversion.
  - Fully scriptable and repeatable.
- **Dependencies:** `dovi_tool`, a standalone x265 with Dolby Vision support, and an MP4 muxer that writes the `dvvC` box (for example MP4Box). **None is installed here; installation was not authorized.** The ffmpeg 6.1 here cannot write Dolby Vision.
- **Risks:**
  - RPU editing errors (frame misalignment shows as flicker or brightness shifts).
  - Clip A's internal cut and different resolution.
  - Platforms may re-process the metadata anyway.
  - Less proven than Apple's path for Apple-device playback.

### Workflow C: Apple-managed SDR delivery

- **Options:**
  - Export SDR from Final Cut Pro (Rec. 709 project or export with Apple's HDR→SDR tone mapping).
  - Export each clip from the iPhone as SDR (Photos share with HDR off / "Most Compatible") and cut those with straight cuts.
- **Expected appearance:** **SDR cannot look identical to the HDR original.** Highlights above SDR white (paper, tissue, box interior, window light; 25–54% of these frames) are compressed. Apple's mapping is tuned to Apple's look, so it should resemble "the iPhone in SDR mode" far more than V1's generic conversion did.
- **Evaluation:** compare against the original **with HDR turned off on the same display**: it's the fair SDR reference. Never compare SDR against HDR playback.

## 4. Platform compatibility (sources)

| Platform | HDR / Dolby Vision status |
|---|---|
| **Instagram** | **iOS app supports Dolby Vision and ambient viewing environment metadata** since Nov 2025. HLG uploads from iPhone play in HDR. Android and Facebook support was announced as coming later ([Meta Engineering, Nov 2025](https://engineering.fb.com/2025/11/17/ios/enhancing-hdr-on-instagram-for-ios-with-dolby-vision/)). |
| **YouTube / Shorts** | Accepts HLG (Rec. 2100) or PQ with a Rec. 2020 matrix and auto-generates SDR ([YouTube Help](https://support.google.com/youtube/answer/7126552)). Shorts-specific behaviour is not documented in what I found. |
| **Facebook** | Dolby Vision support "coming" per Meta. Expect HDR to be converted or SDR playback on many devices. |
| **TikTok** | **No authoritative source found** on HDR or Dolby Vision support. Treat as unknown and test with a private upload. |

## 5. Scoring (1 = poor, 5 = best)

| Criterion | A: Final Cut Pro HDR | B: Scripted Dolby Vision | C: Apple SDR |
|---|---|---|---|
| Visual fidelity (Apple devices) | **5** | 4–5 (untested) | 3 (SDR limits) |
| Social compatibility | 4 | 4 | **5** |
| Original resolution | **5** (except A unless original supplied) | **5** | 4–5 |
| Metadata integrity | 4 (Dolby Vision regenerated) | **5** (camera RPU kept) | n/a |
| Repeatability | 4 | **5** | 4 |
| Technical complexity (5 = simplest) | **4** | 2 | **5** |
| Risk of unexpected colour change (5 = lowest) | **4** | 3 | 3 |

## 6. Recommended pipeline

**Workflow A (Final Cut Pro on the founder's Mac), plus Workflow C exports made by Final Cut Pro, both gated by the validation test.**

1. **Master:** a Final Cut Pro project at Rec. 2020 HLG, 2160×3840, 30p. Straight cuts per the approved storyboard (I supply the exact EDL and frame numbers). **No colour corrections, no effects.** Export: HEVC 10-bit, HLG, **Dolby Vision 8.4**, plus a ProRes 422 HQ HLG archive.
2. **Social:**
   - **Instagram:** upload the HDR master from the iPhone app.
   - **YouTube Shorts:** HDR master.
   - **Facebook and TikTok:** test the HDR master with a private upload. Use the Final Cut Pro SDR export only if the platform's HDR handling fails validation.
3. **Clip A:** obtain the **original camera file** from the founder's wife's phone. It removes the 1.5× upscale and may contain a longer, clearer heading moment.
4. **Workflow B** is kept as a fallback if the validation test shows Apple's regenerated metadata changes the look. It needs separate authorization to install tools.

**Why not B first:** it's the most automatable, but it's least proven on Apple playback and adds metadata-editing risk. The goal is visual fidelity, not ease of automation.

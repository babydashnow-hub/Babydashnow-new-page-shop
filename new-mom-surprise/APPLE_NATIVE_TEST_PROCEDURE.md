# Apple-native HDR fidelity test: procedure for approval

**Status:** procedure only. Nothing has been exported, installed or purchased. IMG_7303 stays excluded (private letter body).

**Founder's Mac:** MacBook Air M4, 16 GB, macOS 26.6.2, built-in Liquid Retina 2560×1664, iMovie 10.4.4. **No Final Cut Pro.**

## 1. Which installed tools can produce HDR output

| Tool (already on the Mac) | HDR export? | Dolby Vision 8.4? | Suitable for the test? |
|---|---|---|---|
| **iMovie 10.4.4 (Mac)** | **No.** Imports HDR, **shares SDR only**. Apple: HDR from a Mac iMovie project requires sending it to Final Cut Pro ([Apple Support 102241](https://support.apple.com/en-us/102241)) | No | **No.** It would repeat an SDR conversion |
| **`avconvert`** (built-in command-line tool using Apple's AVFoundation encoder) | **Yes, with HEVC presets.** Apple: "all HEVC presets have been upgraded to support HDR… the output format will match the source format"; H.264 presets convert HDR to SDR ([Apple Developer](https://developer.apple.com/news/?id=rwbholxw), [WWDC20 "Export HDR media"](https://developer.apple.com/videos/play/wwdc2020/10010/), [avconvert man page](https://keith.github.io/xcode-man-pages/avconvert.1.html)) | **Expected, not confirmed.** Apple says output matches source format; no source confirms `avconvert` itself keeps Dolby Vision 8.4 | **Yes: primary test tool** |
| **QuickTime Player** (File → Export As → 4K) | Uses the same AVFoundation HEVC export, so expected to keep HDR | Expected, unverified | Optional GUI alternative |
| **iPhone 16 Pro: Photos trim / iMovie for iOS** | Yes (iMovie iOS: Options → HDR) | Apple-native path | Fallback for the final edit, not this test |

## 2. Is Final Cut Pro necessary?

- **For this fidelity test: no.** `avconvert` uses Apple's own HDR/Dolby Vision-aware encoder. It answers the core question: does an Apple-native re-encode of a trimmed segment preserve HLG, 10-bit and Dolby Vision 8.4, and look identical?
- **For the full V2 edit: probably.** `avconvert` trims one clip at a time; it **cannot assemble** multiple shots into one film. Options for later approval:
  1. **Final Cut Pro** (paid; Apple offers a free trial). Exports HEVC 10-bit HLG with Apple-regenerated Dolby Vision 8.4.
  2. **iMovie on the iPhone 16 Pro** with HDR export (free, already installed). Less control over a vertical 4K timeline.
  3. A small AVFoundation composition script (Apple frameworks only). Needs the Xcode Command Line Tools, which may need installing.

  The test result decides between them.

## 3. How HDR signalling and Dolby Vision will be verified

**On the Mac (read-only, built-in):**
- `mdls -name kMDItemCodecs -name kMDItemPixelHeight -name kMDItemPixelWidth -name kMDItemDurationSeconds <file>`: codec, size, duration.
- QuickTime Player → Window → **Show Movie Inspector**: format, size, frame rate, and an HDR/colour indication.
- Neither shows Dolby Vision RPU detail. That's checked here.

**In this session (definitive):** you upload the exported test files **inside a ZIP** (so the chat app can't transcode them), and I verify with `ffprobe`:

| Check | Original IMG_7321 (my copy, measured) | Test output must show |
|---|---|---|
| Codec / profile / depth | HEVC Main 10, yuv420p10le | **HEVC Main 10, 10-bit** |
| Picture | 3840×2160 + rotation −90 (displays 2160×3840) | **Displays 2160×3840 portrait** (rotation flag or baked in) |
| Frame rate | 30/1 | **30/1** |
| Colour signalling | BT.2020 primaries, HLG (arib-std-b67), BT.2020nc, limited range | **Identical** |
| Dolby Vision configuration | profile 8, bl_compat_id 4 | **profile 8, bl_compat_id 4** |
| Dolby Vision RPU | **203 / 203 displayed frames** | **RPU on every displayed frame** |
| Ambient Viewing Environment | present | Reported (desirable, not required) |
| Duration | 6.765 s | Full test: 6.765 s ±1 frame. Trimmed test: 1.700 s ±1 frame. |

**Fingerprint of my copy of IMG_7321.mov:** 24,528,822 bytes, SHA-256 `32a2cb3817f9ce6c55944f4a06ae14f886927a5e7793b483327d1554ed98ac45`. My copy is a **re-saved trim** (file time 22:01 UTC vs. capture 14:41 EST). If your Mac copy has a different checksum, it may be the longer camera original: tell me before the test.

## 4. Limitations of this MacBook Air display

- **SDR-class panel:** the M4 MacBook Air's Liquid Retina display is about 500 nits. It **decodes and plays HDR** (Dolby Vision, HDR10, HLG) but is not an XDR display. Reviews measured about 470 nits on HDR content, versus up to 1600 nits peak on a MacBook Pro XDR ([Apple newsroom](https://www.apple.com/bw/newsroom/2025/03/apple-introduces-the-new-macbook-air-with-the-m4-chip-and-a-sky-blue-color/), [Tom's Guide](https://www.tomsguide.com/computing/laptops/macbook-air-m4-review), [PetaPixel](https://petapixel.com/2025/03/11/apple-macbook-air-with-m4-review-thin-in-size-price-and-sometimes-performance/)). No published figure exists for its HDR (EDR) headroom.
- **Consequence:**
  - macOS **tone-maps** HDR highlights onto this panel.
  - The Mac shows a compressed version of what the iPhone shows.
  - Highlight differences (white paper, box interior) may be **invisible on the Mac yet visible on the iPhone**, or vice versa.
- **What the Mac is good for:** a **relative A/B** comparison (original and test through the same macOS pipeline), detail and sharpness, colour shifts, artefacts.
- **The primary HDR judge is the iPhone 16 Pro** (HDR OLED), where the footage was shot and where the founder's reference look comes from.
- **Power:** forum reports (unverified) suggest HDR playback differs on battery. Test **on mains power** with "Optimize video streaming while on battery" off.

## 5. Shortest practical test procedure (about 15 minutes, after approval)

**Preparation (Mac, read-only):**

1. Put a **copy** of `IMG_7321.mov` in a new folder, `~/Desktop/BDN_TEST`. Keep the original untouched.
2. In Terminal:

   ```
   cd ~/Desktop/BDN_TEST
   ```

   ```
   shasum -a 256 IMG_7321.mov
   ```

   ```
   avconvert --help
   ```

   Send me the checksum and the help output, which confirms the preset names and the trim options (`--start` / `--duration`) on macOS 26.6.2.

**Export (only once authorized; exact command confirmed from the help output):**

3. Full-length HDR re-encode (isolates the encoder; no trim):

   ```
   avconvert --source IMG_7321.mov --preset PresetHEVCHighestQuality --output T1_IMG_7321_HEVC_full.mov --progress
   ```

4. Trimmed segment, exactly storyboard shot 7 (0.70–2.40 s):

   ```
   avconvert --source IMG_7321.mov --preset PresetHEVCHighestQuality --output T2_IMG_7321_HEVC_0p70-2p40.mov --start 0.70 --duration 1.70 --progress
   ```

5. Re-run `shasum -a 256 IMG_7321.mov` and confirm the original is unchanged.

**Verification:**

6. Zip `T1` and `T2` (Finder → Compress) and upload the ZIP here. I report the §3 table, pass or fail per line.

**Visual A/B: Mac (secondary):**

7. Mains power; auto-brightness, True Tone and Night Shift **off**; brightness fixed at about 75%; dim, constant room light.
8. Open `IMG_7321.mov` and `T1` in **QuickTime Player**, both full-screen on the built-in display. Pause both at **1.00 s, 2.40 s and 5.90 s** (Edit → Go To / arrow keys). Toggle between them (Cmd-`) at each point.

**Visual A/B: iPhone 16 Pro (primary):**

9. AirDrop `T1` and `T2` to the iPhone. In Photos, compare against the original clip at the same brightness (auto-brightness off), same paused moments, swiping between them.

## 6. Acceptance criteria

**Technical (all required):** every line in the §3 table passes, **including a Dolby Vision RPU on every frame**, and the original's checksum is unchanged.

**Visual (founder's judgement; any visible difference = fail):**

| # | Look for | Pass if |
|---|---|---|
| 1 | Cream card and white tissue | Same brightness and tint; no greying, no whitening |
| 2 | Dark green card and kraft box | Same hue and depth; no added contrast |
| 3 | Hand skin tone | Same warmth and hue |
| 4 | Card print and paper texture | Same sharpness at 100% / full screen |
| 5 | Highlights (tissue, light on the box flap) | Detail retained; not clipped or flattened |
| 6 | Smooth areas (box interior) | No banding |
| 7 | T2 playback | No flicker or brightness shift at the start and end; correct length |

**Outcome:**
- **Pass** → Apple's encoder is fidelity-safe. The next decision is the assembly tool (Final Cut Pro trial / iMovie on iPhone / AVFoundation script) for V2.
- **Dolby Vision lost but HLG kept** → test again with QuickTime Player "Export As 4K", or move the assembly to Final Cut Pro / the iPhone.
- **Visible difference** → stop. No V2 until diagnosed.

## 7. Approval requested

1. Approve running steps 1–2 (read-only) now, and steps 3–9 (test export) after reviewing the help output.
2. Confirm whether the Mac copy of IMG_7321.mov matches the checksum above.
3. Note for later: the full V2 edit will likely need Final Cut Pro (trial/purchase), iMovie on the iPhone, or an AVFoundation script. The decision comes after the test.

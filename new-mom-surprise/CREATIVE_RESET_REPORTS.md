# BabyDashNow™ New Mom Surprise: Creative Reset (V1 rejected)

**Read-only research and planning.** Nothing was rendered, converted, edited or overwritten. The V1 deliverables and all sources are untouched. Frames were inspected from temporary thumbnails only.

---

## Report A: Visual fidelity diagnosis

### Source vs V1 (measured)

| Property | Original iPhone footage | V1 HDR master | V1 SDR review |
|---|---|---|---|
| Codec / profile | HEVC Main 10, 10-bit 4:2:0 | HEVC Main 10, 10-bit 4:2:0 | **H.264 High, 8-bit** 4:2:0 |
| Transfer / primaries / matrix | HLG / BT.2020 / BT.2020nc, limited range | HLG / BT.2020 / BT.2020nc ✓ | BT.709 / BT.709 / BT.709 |
| **Dolby Vision** | **Profile 8.4** (HLG-compatible base layer, compatibility ID 4): DOVI configuration record + **per-frame RPU** (checked on 60/60 frames) | **Absent** | Absent (n/a) |
| Ambient Viewing Environment SEI | Present (314 lux) | **Absent** | Absent |
| Apple metadata tracks (`mebx`) | 6 tracks | **Absent** | Absent |
| Resolution | 2160×3840 (A: 1440×2560) | **1080×1920** | **1080×1920** |
| Bitrate | about 25–28 Mbps (4K) | 16.5 Mbps | 24.4 Mbps |
| Tone mapping | (camera-native; Apple renders via DV/HLG) | none | Generic HLG → linear (203-nit reference white, ITU-R BT.2408), Mobius shoulder, BT.2020 → 709 |

### Confirmed findings

1. **The V1 HDR master stripped the iPhone's Dolby Vision 8.4 layer.**
   - The originals carry a per-frame Dolby Vision RPU (frame-by-frame display-mapping metadata) and Apple viewing-environment metadata. Apple devices use these to render the footage as you see it in Photos.
   - V1 kept only the HLG base layer, so on an iPhone it plays as **plain HLG**: a different rendering path from the originals.
   - Cause: ffmpeg 6.1 in this environment re-encodes without carrying or regenerating Dolby Vision (no `dovi_tool`, no standalone x265 with Dolby Vision support).
2. **The SDR conversion was generic, not Apple's.**
   - **25–54% of every frame** is above HLG reference white, measured per shot. Examples: the cream box interior (54%), tissue (45%), seal (47%).
   - The 203-nit / Mobius mapping compresses all of that into the shoulder. **SDR whites peak at only 227–238 / 255, and no pixel in any shot reaches 250.**
   - Result: white paper, tissue and box interiors render **greyer and lower in contrast** than on the iPhone, where they display with HDR headroom.
   - It also ignores the Dolby Vision RPU, which carries the camera's own mapping intent.
3. **8-bit SDR from a 10-bit HDR source**, with no deliberate dithering step. Smooth gradients (walls, paper, box interior) are at risk of banding. *Not yet measured.*
4. **Resolution was reduced 4×** (4K → 1080p). This is inherent to a 1080 deliverable, but it's visible whenever V1 is compared with the originals zoomed in or on a large screen.
5. **My earlier PSNR checks only proved that V1 adds nothing beyond its own pipeline.** They do **not** prove fidelity to how the originals look on an iPhone. That claim is withdrawn.

### Hypotheses (not confirmed)

- **Viewing comparison:** originals viewed in iPhone Photos with HDR/EDR highlights, next to an SDR file, look inherently brighter and punchier. Part of the perceived loss may be display mode, not data. *Need: how and where V1 was viewed.*
- **Transfer path:** earlier deliveries reached you as 512×910 transcodes through the chat app. If V1 was viewed through a chat preview rather than the ZIP, quality would have been further degraded.
- **Visual impact of the missing Dolby Vision:** the metadata loss is confirmed, but **how much it changes the look on your iPhone** has not been measured. It needs an on-device side-by-side.

### Corrective workflow options (not performed)

| Option | What it does | Fidelity | Feasibility |
|---|---|---|---|
| **1. Apple-native edit (recommended)** | Cut the originals in a Dolby Vision-aware Apple editor: iMovie or Final Cut Pro (Mac), or iMovie on iPhone. Export HDR (HEVC 10-bit, Dolby Vision) at 2160×3840. Make any SDR copy with Apple's own HDR → SDR conversion. | Highest: the same rendering pipeline as Photos | Must be done on your Mac or iPhone; I can supply the exact EDL, frame-accurate |
| 2. Dolby Vision-preserving build here | Extract each clip's RPU with `dovi_tool`, cut it to the EDL, and re-encode with x265 Dolby Vision 8.4 injection at 4K | High for HDR; SDR still needs a conversion choice | Needs `dovi_tool` and an x265 build installed (network access); moderate risk |
| 3. Apple-made SDR sources | Export each clip from the iPhone as SDR (Apple's conversion, for example "Most Compatible" or HDR switched off), then cut those with straight cuts only, at 1080 or 4K | Faithful to Apple's own SDR look; no tone mapping by us | Easy; requires the exported files |
| 4. Keep a 4K master | Deliver 2160×3840 and let each platform downscale | Retains source detail | Easy, with any of the above |

**Note:** frame-accurate *lossless* cutting is not possible. The iPhone files have one keyframe per clip, so any cut that doesn't start at frame 0 requires re-encoding. That's why options 1 and 2 matter.

---

## Report B: Three creative concepts (verified footage only)

**Key finding on the letter (A):**
- From about **10.6 s to the end (12.3 s)**, clip A reveals the handwritten heading **"For a special new mom."** as the hand lifts.
- Before that (0–10.5 s) the page is blank or covered by the writing hand: **nothing is readable**.
- The body of the letter is never readable in A. It is fully readable in B, which stays **excluded**.
- The heading is a dedication rather than private content, but **showing it needs your approval.**

### Concept 1: "For a special new mom" (letter-led, chronological)

- **Opening (0–2 s):** A 9.6 → 12.3. A hand finishes a line and lifts away, revealing *"For a special new mom."* Curiosity: who is she, and who is writing?
- **Premise:** one mother taking time for another; the gift is the continuation of that thought.

| # | Source | In → out | Dur | Beat |
|---|---|---|---|---|
| 1 | A | 9.6 → 12.3 | 2.7 | The handwritten heading appears |
| 2 | A | 2.8 → 4.6 | 1.8 | The pen moving: care in progress, not readable *(optional, after shot 1 as a breath)* |
| 3 | D | 3.4 → 4.4 | 1.0 | Empty box |
| 4 | C | 0.0 → 1.8 | 1.8 | Hands make a soft bed of paper |
| 5 | E | 3.0 → 5.0 | 2.0 | Swaddle pressed in gently |
| 6 | G | 2.8 → 4.4 | 1.6 | Lotion |
| 7 | H | 1.8 → 3.6 | 1.8 | Tissue folded over |
| 8 | I | 0.7 → 2.4 | 1.7 | The BabyDashNow card |
| 9 | J | 1.8 → 3.5 | 1.7 | Sealed: the seal itself reads "We show up when it matters" |
| 10 | K | 4.6 → 5.6 | 1.0 | On the way |
| 11 | P | 0.0 → 4.0 | 4.0 | Waiting at her door |

- **Pacing:** about 21 s. Unhurried at the start and end, a little quicker through the packing (1.6–2 s shots).
- **Text (minimal):** none at the start, because the handwriting *is* the title. At P: *"Someone thought of you today."* Then, small: *"Prepared and delivered on their behalf by BabyDashNow™."*
- **Audio and music:** pen scratch and paper sounds from the original audio (if review clears them), with a sparse original felt-piano or nylon-guitar line entering at shot 3.
- **Payoff:** the thought that started on paper arrives at her door.
- **Strengths:** the most human, unique opening; real footage of a real gesture; matches "one mother to another".
- **Weaknesses:** **the letter is never shown going into the box.** If it *was* included, viewers will infer that correctly. If it was not, the concept implies something untrue and **cannot be used**. Also, a mug with a printed logo sits at the top-right edge of A.
- **Privacy:** heading only (approval needed); hands only; the doorstep has no number.

### Concept 2: "Waiting at her door" (bookend)

- **Opening (0–2 s):** P 0.0 → 1.8. A gift waiting quietly at an apartment door. Curiosity: who left this, and why?
- **Premise:** we see the outcome first, then the care that went into it.

| # | Source | In → out | Dur | Beat |
|---|---|---|---|---|
| 1 | P | 0.0 → 1.8 | 1.8 | The gift at the door (question) |
| 2 | A | 9.6 → 12.3 | 2.7 | *"For a special new mom."* (it started with a thought) |
| 3 | D | 3.4 → 4.4 | 1.0 | Empty box |
| 4 | C | 0.0 → 1.8 | 1.8 | Paper bed |
| 5 | E | 3.0 → 5.0 | 2.0 | Swaddle |
| 6 | H | 1.8 → 3.6 | 1.8 | Tissue |
| 7 | I | 0.7 → 2.4 | 1.7 | Card |
| 8 | J | 1.8 → 3.5 | 1.7 | Sealed |
| 9 | K | 4.6 → 5.6 | 1.0 | On the way |
| 10 | P | 1.8 → 4.2 | 2.4 | Back at the door, now understood |

- **Pacing:** about 18 s, or about 20 s with G (2.8–4.4) and F (1.5–3.0) added.
- **Text:** at the start *"Someone thought of her today."* (third person, so authorship isn't attributed). At the end *"We show up when it matters."* plus a small wordmark.
- **Audio:** a held quiet chord at the start, the melody resolving on the return to the door.
- **Payoff:** the same image means more the second time.
- **Strengths:** a clear hook in the feed; a strong, honest structure; no fabricated moment.
- **Weaknesses:** a static product stack is a weaker *moving* hook than a hand writing, and the opening relies on text. The doorstep image is used twice. Same letter-inclusion caveat as Concept 1.
- **Privacy:** same as Concept 1.

### Concept 3: "Hands" (wordless, sound-led)

- **Opening (0–2 s):** A 2.8 → 4.6, extremely close and sound-forward: the scratch of a pen on paper. Curiosity through texture and sound.
- **Premise:** care lives in small, deliberate gestures.
- **Sequence:** A 2.8–4.6 (pen) → C 0.0–2.4 (hands in the paper) → E 3.0–5.2 (pressing the swaddle) → H 1.8–3.8 (laying the tissue) → I 4.4–5.3 (setting the small card) → J 1.5–3.5 (pressing the seal) → K 4.6–5.6 → P 0.0–4.2.
- **Pacing:** about 19 s, rhythmic and tactile.
- **Text:** none until the end. *"Someone thought of you today."* then *"BabyDashNow™, we show up when it matters."*
- **Audio:** **depends on the real recorded sounds** (pen, paper fill, tissue, seal press), with minimal or no music.
- **Payoff:** a quiet accumulation of gestures arriving at a door.
- **Strengths:** the most authentic and premium; avoids the "catalogue" feel by shooting gestures, not products.
- **Weaknesses:** **the source audio has not been reviewed.** Several clips are quiet (−37 to −46 LUFS) or were re-saved, and **A may contain voices.** If the sound doesn't hold up, the concept loses its engine. It's also a slower hook for cold audiences.
- **Privacy:** lowest-risk visuals; audio is the risk.

---

## Report C: Recommended direction

**Concept 1 ("For a special new mom")**, conditional on two confirmations:
1. The letter was genuinely included in the gift.
2. Showing the heading only is approved.

**Why:**
- It's the only opening that is **both moving and meaningful within two seconds:** a real hand revealing words addressed to a new mom.
- It establishes the human motive *before* any product appears, so the packing reads as care rather than a catalogue.
- It ends on a real, privacy-safe outcome.
- BabyDashNow's value ("we show up when it matters") is shown by the seal and the journey, not claimed.

**If either condition fails, use Concept 2** without the letter shots (replace shot 2 with C or H). It still has a clear hook and payoff.

**Ending (all concepts):**
- Hold on the doorstep, then one quiet line of text.
- **Don't use the six-second animated outro here.** Its graphic energy would break the mood.
- A simple static wordmark (or the seal itself, already in the film) is enough.

---

## Report D: Production constraints and decisions

**Missing footage (would strengthen any concept, all filmable without privacy risk):**
- The letter folded and **placed into the box.** This removes the biggest continuity gap.
- A closed-box hero on a neutral surface.
- The gift being set down at the door (hands only, no signage or number in frame).
- A steady, neutral "on the way" shot (no mount, no plates).

**Privacy limits (unchanged):**
- Excluded: B (full letter), IMG_7337 (doormat "Residences at Bedford", entrance and façade), N and O (plates and building), M (mount, traffic).
- **The heading in A needs approval.** The mug logo at A's edge is minor.

**Audio risks:**
- No source audio has been reviewed for speech, radio or music.
- A (the writing clip) is the most likely to contain voices.
- Concept 3 depends on this audio; Concepts 1 and 2 need it only for texture.
- **Music:** an original composition is recommended (solo felt piano or nylon guitar, about 66–72 bpm, no vocals, no swelling strings), produced only after approval.

**Decisions needed before any editing:**
1. Was the handwritten letter **actually included in the gift**?
2. May the heading **"For a special new mom."** appear (body never shown)?
3. **Fidelity route:** Apple-native edit (option 1), Dolby Vision-preserving build here (option 2), Apple-made SDR sources (option 3), and a 4K master (yes/no)?
4. **How was V1 viewed** (iPhone Photos, chat preview or desktop; HDR or SDR display), so the comparison can be repeated properly?
5. **Concept choice:** 1, 2 or 3?
6. Can you film any of the missing inserts?
7. **Audio:** will you review the source audio yourself, or authorise a transcript-free technical check for speech and music?

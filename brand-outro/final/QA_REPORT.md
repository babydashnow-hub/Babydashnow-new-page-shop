# BabyDashNow Official Outro (Version B) - QA Report

## Deliverables
- BabyDashNow_Official_Outro_Final.mp4 - master, H.264 High, 1080x1920, 30 fps, 180 frames, 6.00 s, AAC-LC 48 kHz stereo
- BabyDashNow_Official_Outro_Final_silent.mp4 - same picture, no audio
- BabyDashNow_Chime_Final.wav - original synthesised chime, 48 kHz mono 16-bit
- BabyDashNow_Official_Outro_Final_still.png - final composition, 1080x1920
- Source: ../build_outro_v2.py and ../assets/ (renderer and logo crops)
- Transparent versions (ProRes 4444 .mov, VP9 .webm) are in ../out/

## What changed
Nothing in the approved V2 animation. These files are the V2 renders under final names. V1 and V2 files are unchanged.

## Checks performed on the master
- Specs: 1080x1920, 30 fps, 6.00 s, H.264 High yuv420p, BT.709 tagged.
- Audio: EBU R128 integrated loudness -24.4 LUFS, true peak -14.1 dBFS. No clipping.
- Chime onset: first audible sample at 1.9008 s; circle closes at frame 57 = 1.900 s. Within one frame.
- Circle: at frame 57, every 1-degree sample of the ring is inked (360/360, using a 3x3 neighbourhood). No gap at the 3 o'clock seam.
- Black/blank frames: none detected. Opening frame shows the dot at 50-100% scale on white.
- Frame sequence: dot entrance, orbit, closure, settle, lockup slide, wordmark, mantra, cities, hold - reviewed at contact-sheet level.
- Right-edge clipping during the slide at 2.60 s: none (column 1079 is white).
- Cities spelled: Stamford, Darien, Norwalk, Greenwich.

## Limitations (disclosed)
1. Logo source is the supplied 1200 px JPEG, not vector. The wordmark and mantra are raster crops scaled 1.10x with Lanczos. The brief asks for no upscaled masters. The ring and dot are drawn analytically at full resolution. A vector logo file would remove this limitation; the renderer can be re-run with it.
2. Cities line is set in Inter. The brand typeface is not installed in this environment.
3. Playback was verified from the encoded files and extracted frames, not on a physical phone speaker.
4. The lockup is 10% larger than the reference proportions, applied uniformly. Tell me if you want the reference size back.

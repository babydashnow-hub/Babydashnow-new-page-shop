# Parent Minute: Episode 01 assets

Drop the supplied files here using exactly these names:

| File | Used in |
| --- | --- |
| `01-opening.png` | Scene 1 (0:00–0:03) |
| `02-bag-check.png` | Scene 2 (0:03–0:07) |
| `03-essentials.png` | Scene 3 (0:07–0:13) |
| `04-ready-to-go.png` | Scene 4 (0:13–0:16) |
| `05-end-card.png` | Visual reference only. The end card is rebuilt in code. |
| `babydashnow-logo.png` | End card logo (the real logo; transparent PNG preferred) |

Scene images should be 9:16 portrait. For the sharpest result after the slow push-ins (up to 1.09×), supply them at 1188×2112 or larger. 2160×3840 is ideal.

While a file is missing, Remotion Studio shows a labelled placeholder. A real render fails on purpose, so placeholders never end up in a finished video.

## Audio (optional)

Put audio files in `audio/` and set their paths in Studio's props panel (or with `--props`), e.g. `"parent-minute/audio/zipper.wav"`. Every track defaults to `null` (silent):

- `music`: full-length bed, fades in and out
- `ambience`: soft room tone, looped at low volume
- `zipper`: cued at frame 116 (Scene 2)
- `fabric`: cued at frame 398 (Scene 4, bag lifted)

Use only music and sound effects you have a licence for.

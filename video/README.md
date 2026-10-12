# BabyDashNow™ Parent Minute videos (Remotion)

## Episode 01: `ParentMinuteEpisode01`

1080×1920 · 30 fps · 600 frames (20 s)

```
src/
  ParentMinuteEpisode01.tsx         timeline: scenes, copy, camera moves
  components/ParentMinuteScene.tsx  full-bleed image + slow camera + dissolve
  components/ParentMinuteText.tsx   serif/sans text with soft fade + rise
  components/ParentMinuteEndCard.tsx  end card rebuilt in code, real logo
  components/ParentMinuteAudio.tsx  optional music / ambience / SFX
  parent-minute/theme.ts            palette, fonts, safe zones, easing
  parent-minute/assets.ts           asset paths (public/parent-minute/)
```

Assets: see `public/parent-minute/README.md`.

```
npm install
npm run dev     # Remotion Studio, then pick ParentMinuteEpisode01
npx remotion render src/index.ts ParentMinuteEpisode01 out/parent-minute-episode-01.mp4 --codec=h264 --crf=16
```

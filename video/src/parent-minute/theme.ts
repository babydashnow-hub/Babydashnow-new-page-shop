import { Easing, staticFile } from "remotion";
import { loadFont } from "@remotion/fonts";

// Same typefaces as the BabyDashNow site: Lora (editorial serif) + Inter (sans).
// Self-hosted in public/fonts so rendering never needs network access.
const SERIF_FAMILY = "BDN Lora";
const SANS_FAMILY = "BDN Inter";

loadFont({
  family: SERIF_FAMILY,
  url: staticFile("fonts/Lora-Variable-latin.woff2"),
  weight: "400 700",
  format: "woff2",
});
loadFont({
  family: SANS_FAMILY,
  url: staticFile("fonts/Inter-Variable-latin.woff2"),
  weight: "100 900",
  format: "woff2",
});

export const COLORS = {
  ivory: "#F5F1E8",
  green: "#356B16",
  softBlack: "#1C1B18",
} as const;

export const FONTS = {
  serif: `"${SERIF_FAMILY}", Georgia, "Times New Roman", serif`,
  sans: `"${SANS_FAMILY}", -apple-system, "Segoe UI", sans-serif`,
} as const;

export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 600,
} as const;

// Instagram / Reels UI overlap. Important text stays inside this box.
export const SAFE_ZONE = {
  top: 220,
  bottom: 300,
  side: 96,
} as const;

// Slow, even camera easing (sine in-out) and a soft settle for text.
export const EASE_CAMERA = Easing.bezier(0.37, 0, 0.63, 1);
export const EASE_SETTLE = Easing.bezier(0.22, 1, 0.36, 1);
export const EASE_FADE = Easing.bezier(0.45, 0, 0.55, 1);

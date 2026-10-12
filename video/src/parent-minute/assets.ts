import { staticFile } from "remotion";

// All visual assets live in public/parent-minute/.
export const ASSET_FILES = {
  opening: "parent-minute/01-opening.png",
  bagCheck: "parent-minute/02-bag-check.png",
  essentials: "parent-minute/03-essentials.png",
  readyToGo: "parent-minute/04-ready-to-go.png",
  // Visual reference only. The end card is rebuilt in code for exact branding.
  endCardReference: "parent-minute/05-end-card.png",
  logo: "parent-minute/babydashnow-logo.png",
} as const;

export const asset = (key: keyof typeof ASSET_FILES) =>
  staticFile(ASSET_FILES[key]);

// Entry file. Render with:
// npx remotion render src/index.ts ParentMinuteEpisode01 out/parent-minute-episode-01.mp4

import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

registerRoot(RemotionRoot);

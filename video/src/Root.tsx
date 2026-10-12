import React from "react";
import { Composition } from "remotion";
import {
  ParentMinuteEpisode01,
  parentMinuteEpisode01Defaults,
  parentMinuteEpisode01Schema,
} from "./ParentMinuteEpisode01";
import { VIDEO } from "./parent-minute/theme";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ParentMinuteEpisode01"
      component={ParentMinuteEpisode01}
      schema={parentMinuteEpisode01Schema}
      defaultProps={parentMinuteEpisode01Defaults}
      durationInFrames={VIDEO.durationInFrames}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
    />
  );
};

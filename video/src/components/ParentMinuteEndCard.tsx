import React, { useState } from "react";
import {
  AbsoluteFill,
  getRemotionEnvironment,
  Img,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { asset, ASSET_FILES } from "../parent-minute/assets";
import { COLORS, EASE_CAMERA, EASE_FADE, SAFE_ZONE } from "../parent-minute/theme";
import { MissingAsset } from "./ParentMinuteImage";
import { ParentMinuteText } from "./ParentMinuteText";

type Props = {
  durationInFrames: number;
  /** Frames over which the ivory card dissolves in over the last scene. */
  dissolveIn?: number;
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Rebuilt in code (05-end-card.png is a visual reference only) so the
// branding is exact. Brand is the last thing to arrive: the line first,
// the logo as a quiet sign-off.
const TIMING = {
  title: 12,
  byline: 20,
  rule: 30,
  headline: 34,
  closing: 54,
  logo: 68,
} as const;

export const ParentMinuteEndCard: React.FC<Props> = ({
  durationInFrames,
  dissolveIn = 18,
}) => {
  const frame = useCurrentFrame();

  const cardOpacity = interpolate(frame, [0, dissolveIn], [0, 1], {
    ...clamp,
    easing: EASE_FADE,
  });
  // Barely perceptible settle of the whole layout.
  const settleScale = interpolate(frame, [0, durationInFrames], [1.014, 1], {
    ...clamp,
    easing: EASE_CAMERA,
  });
  const ruleWidth = interpolate(frame, [TIMING.rule, TIMING.rule + 30], [0, 56], {
    ...clamp,
    easing: EASE_FADE,
  });
  const logoOpacity = interpolate(frame, [TIMING.logo, TIMING.logo + 28], [0, 1], {
    ...clamp,
    easing: EASE_FADE,
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.ivory, opacity: cardOpacity }}>
      <AbsoluteFill
        style={{
          padding: `${SAFE_ZONE.top}px ${SAFE_ZONE.side}px ${SAFE_ZONE.bottom}px`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          transform: `scale(${settleScale})`,
        }}
      >
        <ParentMinuteText variant="title" enterAt={TIMING.title} color={COLORS.green}>
          Parent Minute
        </ParentMinuteText>
        <ParentMinuteText
          variant="byline"
          enterAt={TIMING.byline}
          color={COLORS.softBlack}
          opacity={0.62}
          style={{ marginTop: 14 }}
        >
          by BabyDashNow™
        </ParentMinuteText>

        <div
          style={{
            width: ruleWidth,
            height: 2,
            backgroundColor: COLORS.green,
            opacity: 0.45,
            margin: "64px 0 60px",
          }}
        />

        <ParentMinuteText
          variant="headline"
          enterAt={TIMING.headline}
          fadeInFrames={30}
          color={COLORS.softBlack}
          style={{ fontSize: 84, maxWidth: 820 }}
        >
          We show up when it matters.
        </ParentMinuteText>
        <ParentMinuteText
          variant="support"
          enterAt={TIMING.closing}
          color={COLORS.softBlack}
          opacity={0.66}
          style={{ marginTop: 36, fontSize: 32 }}
        >
          A practical reminder for parents.
        </ParentMinuteText>

        <div style={{ marginTop: 120, opacity: logoOpacity }}>
          <Logo />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const LOGO_BOX = { width: 520, height: 150 } as const;

// The real BabyDashNow logo file. Never substituted: a missing file shows a
// labelled placeholder in the Studio and fails a real render.
const Logo: React.FC = () => {
  const [missing, setMissing] = useState(false);
  const { isRendering } = getRemotionEnvironment();

  if (missing) {
    return <MissingAsset label={ASSET_FILES.logo} dark={false} style={LOGO_BOX} />;
  }

  return (
    <Img
      src={asset("logo")}
      maxRetries={isRendering ? 2 : 0}
      onError={isRendering ? undefined : () => setMissing(true)}
      style={{
        maxWidth: LOGO_BOX.width,
        maxHeight: LOGO_BOX.height,
        objectFit: "contain",
        display: "block",
      }}
    />
  );
};

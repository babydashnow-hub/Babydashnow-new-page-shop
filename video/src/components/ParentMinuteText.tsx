import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { COLORS, EASE_FADE, EASE_SETTLE, FONTS } from "../parent-minute/theme";

export type TextVariant = "headline" | "title" | "byline" | "support";

const VARIANTS: Record<TextVariant, React.CSSProperties> = {
  // Editorial serif for emotional / key lines.
  headline: {
    fontFamily: FONTS.serif,
    fontWeight: 400,
    fontSize: 78,
    lineHeight: 1.14,
    letterSpacing: "-0.01em",
  },
  // Series name: quiet, tracked sans caps.
  title: {
    fontFamily: FONTS.sans,
    fontWeight: 500,
    fontSize: 32,
    lineHeight: 1.2,
    letterSpacing: "0.34em",
    textTransform: "uppercase",
  },
  byline: {
    fontFamily: FONTS.sans,
    fontWeight: 400,
    fontSize: 26,
    lineHeight: 1.3,
    letterSpacing: "0.06em",
  },
  support: {
    fontFamily: FONTS.sans,
    fontWeight: 400,
    fontSize: 34,
    lineHeight: 1.4,
    letterSpacing: "0.01em",
  },
};

type Props = {
  children: React.ReactNode;
  variant: TextVariant;
  /** Frame (relative to the parent Sequence) the fade-in starts. */
  enterAt: number;
  /** Frame the fade-out starts. Omit to stay on screen. */
  exitAt?: number;
  fadeInFrames?: number;
  fadeOutFrames?: number;
  /** Distance of the soft upward settle, in px. */
  rise?: number;
  color?: string;
  opacity?: number;
  style?: React.CSSProperties;
};

export const ParentMinuteText: React.FC<Props> = ({
  children,
  variant,
  enterAt,
  exitAt,
  fadeInFrames = 24,
  fadeOutFrames = 14,
  rise = 16,
  color = COLORS.ivory,
  opacity = 1,
  style,
}) => {
  const frame = useCurrentFrame();

  const fadeIn = interpolate(frame, [enterAt, enterAt + fadeInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE_FADE,
  });
  const settle = interpolate(
    frame,
    [enterAt, enterAt + fadeInFrames + 10],
    [rise, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_SETTLE },
  );
  const fadeOut =
    exitAt === undefined
      ? 1
      : interpolate(frame, [exitAt, exitAt + fadeOutFrames], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: EASE_FADE,
        });

  return (
    <div
      style={{
        ...VARIANTS[variant],
        color,
        opacity: fadeIn * fadeOut * opacity,
        transform: `translateY(${settle}px)`,
        textWrap: "balance",
        ...style,
      }}
    >
      {children}
    </div>
  );
};

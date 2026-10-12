import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  COLORS,
  EASE_CAMERA,
  EASE_FADE,
  SAFE_ZONE,
  VIDEO,
} from "../parent-minute/theme";
import { ParentMinuteImage } from "./ParentMinuteImage";

type Point = [x: number, y: number];

export type CameraMove = {
  /** Scale at the first and last frame. Keep both >= 1 so the frame stays covered. */
  scale: [from: number, to: number];
  /** Focus point in % of the frame. Scaling happens toward this point. */
  focus: [from: Point, to: Point];
  /** Optional extra vertical drift in px. Clamped so no edge is ever revealed. */
  driftY?: [from: number, to: number];
};

export type TextPlacement = "upper" | "center" | "lower";

type Props = {
  src: string;
  label: string;
  /** Frames over which this scene dissolves in over the previous one. */
  dissolveIn?: number;
  /** Length of the scene including its overlap with the next one. */
  durationInFrames: number;
  camera: CameraMove;
  /** Only needed when overlaying text (children). */
  textPlacement?: TextPlacement;
  children?: React.ReactNode;
};

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export const ParentMinuteScene: React.FC<Props> = ({
  src,
  label,
  dissolveIn = 0,
  durationInFrames,
  camera,
  textPlacement = "upper",
  children,
}) => {
  const frame = useCurrentFrame();

  const progress = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
    ...clamp,
    easing: EASE_CAMERA,
  });

  const scale = interpolate(progress, [0, 1], camera.scale);
  const fx = interpolate(
    progress,
    [0, 1],
    [camera.focus[0][0], camera.focus[1][0]],
  );
  const fy = interpolate(
    progress,
    [0, 1],
    [camera.focus[0][1], camera.focus[1][1]],
  );

  // Keep any vertical drift inside the slack that the current scale creates,
  // so the image always covers the full 1080x1920 frame.
  const originY = (fy / 100) * VIDEO.height;
  const wantedDrift = camera.driftY
    ? interpolate(progress, [0, 1], camera.driftY)
    : 0;
  const driftY = Math.min(
    originY * (scale - 1),
    Math.max(-(VIDEO.height - originY) * (scale - 1), wantedDrift),
  );

  const opacity =
    dissolveIn > 0
      ? interpolate(frame, [0, dissolveIn], [0, 1], {
          ...clamp,
          easing: EASE_FADE,
        })
      : 1;

  const imageStyle: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  };

  return (
    <AbsoluteFill style={{ opacity, backgroundColor: COLORS.softBlack }}>
      <AbsoluteFill
        style={{
          transform: `translateY(${driftY}px) scale(${scale})`,
          transformOrigin: `${fx}% ${fy}%`,
          willChange: "transform",
        }}
      >
        <ParentMinuteImage src={src} label={label} style={imageStyle} />
      </AbsoluteFill>
      {children ? <Scrim placement={textPlacement} /> : null}
      {children ? (
        <AbsoluteFill
          style={{
            padding: `${SAFE_ZONE.top + 40}px ${SAFE_ZONE.side}px ${SAFE_ZONE.bottom + 40}px`,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            textAlign: "center",
            justifyContent:
              textPlacement === "upper"
                ? "flex-start"
                : textPlacement === "lower"
                  ? "flex-end"
                  : "center",
            gap: 18,
            textShadow: "0 2px 28px rgba(28, 27, 24, 0.35)",
          }}
        >
          {children}
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

// A soft, warm shade behind the text area only — keeps ivory text legible
// without visibly darkening the photograph.
const Scrim: React.FC<{ placement: TextPlacement }> = ({ placement }) => {
  const shade = "rgba(28, 27, 24, 0.50)";
  const clear = "rgba(28, 27, 24, 0)";
  const background =
    placement === "upper"
      ? `linear-gradient(to bottom, ${shade} 0%, ${clear} 48%)`
      : placement === "lower"
        ? `linear-gradient(to top, ${shade} 0%, ${clear} 52%)`
        : `radial-gradient(ellipse 80% 40% at 50% 50%, rgba(28,27,24,0.38) 0%, ${clear} 100%)`;
  return <AbsoluteFill style={{ background, pointerEvents: "none" }} />;
};

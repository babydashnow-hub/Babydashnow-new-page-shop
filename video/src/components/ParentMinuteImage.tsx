import React, { useState } from "react";
import { getRemotionEnvironment, Img } from "remotion";
import { COLORS, FONTS } from "../parent-minute/theme";

type Props = {
  src: string;
  label: string;
  style?: React.CSSProperties;
};

// In the Studio a missing file shows a labelled placeholder so the timing can
// still be reviewed. During a real render a missing file fails the render,
// so a placeholder can never end up in a finished video.
export const ParentMinuteImage: React.FC<Props> = ({ src, label, style }) => {
  const [missing, setMissing] = useState(false);
  const { isRendering } = getRemotionEnvironment();

  if (missing) {
    return <MissingAsset label={label} style={style} />;
  }

  return (
    <Img
      src={src}
      style={style}
      maxRetries={isRendering ? 2 : 0}
      onError={isRendering ? undefined : () => setMissing(true)}
    />
  );
};

export const MissingAsset: React.FC<{
  label: string;
  style?: React.CSSProperties;
  dark?: boolean;
}> = ({ label, style, dark = true }) => (
  <div
    style={{
      ...style,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: dark ? "#2A2925" : "transparent",
      border: dark ? undefined : `2px dashed ${COLORS.softBlack}40`,
      color: dark ? `${COLORS.ivory}99` : `${COLORS.softBlack}99`,
      fontFamily: FONTS.sans,
      fontSize: 26,
      letterSpacing: "0.04em",
      textAlign: "center",
    }}
  >
    Missing asset: public/{label}
  </div>
);

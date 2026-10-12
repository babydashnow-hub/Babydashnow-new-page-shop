import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { z } from "zod";
import { ParentMinuteAudio, audioSchema, defaultAudio } from "./components/ParentMinuteAudio";
import { ParentMinuteEndCard } from "./components/ParentMinuteEndCard";
import { ParentMinuteScene } from "./components/ParentMinuteScene";
import { ParentMinuteText } from "./components/ParentMinuteText";
import { asset, ASSET_FILES } from "./parent-minute/assets";
import { COLORS, VIDEO } from "./parent-minute/theme";

export const parentMinuteEpisode01Schema = z.object({
  audio: audioSchema,
});

export type ParentMinuteEpisode01Props = z.infer<typeof parentMinuteEpisode01Schema>;

export const parentMinuteEpisode01Defaults: ParentMinuteEpisode01Props = {
  audio: defaultAudio,
};

const DISSOLVE = 9;

// Scene starts follow the brief exactly. Each scene runs a little past its
// slot so the next one can dissolve in on top of it.
const SCENES = {
  opening: { from: 0, length: 90 },
  bagCheck: { from: 90, length: 120 },
  essentials: { from: 210, length: 180 },
  readyToGo: { from: 390, length: 90 },
  endCard: { from: 480, length: 120 },
} as const;

const END_CARD_DISSOLVE = 18;

export const ParentMinuteEpisode01: React.FC<ParentMinuteEpisode01Props> = ({
  audio,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.softBlack }}>
      {/* SCENE 1 — 0:00–0:03 */}
      <Sequence
        name="1 · Opening"
        from={SCENES.opening.from}
        durationInFrames={SCENES.opening.length + DISSOLVE}
      >
        <ParentMinuteScene
          src={asset("opening")}
          label={ASSET_FILES.opening}
          durationInFrames={SCENES.opening.length + DISSOLVE}
          camera={{
            scale: [1, 1.035],
            focus: [
              [50, 46],
              [50, 50],
            ],
            driftY: [0, -14],
          }}
          textPlacement="upper"
        >
          <ParentMinuteText variant="title" enterAt={4} exitAt={38}>
            Parent Minute
          </ParentMinuteText>
          <ParentMinuteText variant="byline" enterAt={12} exitAt={38} opacity={0.85}>
            by BabyDashNow™
          </ParentMinuteText>
          <ParentMinuteText
            variant="headline"
            enterAt={48}
            style={{ position: "absolute", top: 260, left: 96, right: 96 }}
          >
            Before you head out...
          </ParentMinuteText>
        </ParentMinuteScene>
      </Sequence>

      {/* SCENE 2 — 0:03–0:07 */}
      <Sequence
        name="2 · Bag check"
        from={SCENES.bagCheck.from}
        durationInFrames={SCENES.bagCheck.length + DISSOLVE}
      >
        <ParentMinuteScene
          src={asset("bagCheck")}
          label={ASSET_FILES.bagCheck}
          dissolveIn={DISSOLVE}
          durationInFrames={SCENES.bagCheck.length + DISSOLVE}
          camera={{
            scale: [1.02, 1.07],
            // Drift toward the parent's hands and the bag (lower centre).
            focus: [
              [50, 55],
              [54, 64],
            ],
          }}
          textPlacement="upper"
        >
          <ParentMinuteText
            variant="headline"
            enterAt={16}
            exitAt={106}
            style={{ fontSize: 64 }}
          >
            A quick diaper-bag check.
          </ParentMinuteText>
        </ParentMinuteScene>
      </Sequence>

      {/* SCENE 3 — 0:07–0:13 */}
      <Sequence
        name="3 · Essentials"
        from={SCENES.essentials.from}
        durationInFrames={SCENES.essentials.length + DISSOLVE}
      >
        <ParentMinuteScene
          src={asset("essentials")}
          label={ASSET_FILES.essentials}
          dissolveIn={DISSOLVE}
          durationInFrames={SCENES.essentials.length + DISSOLVE}
          camera={{
            // Slow macro push into the essentials.
            scale: [1.01, 1.09],
            focus: [
              [50, 58],
              [50, 62],
            ],
          }}
          textPlacement="upper"
        >
          <ParentMinuteText
            variant="headline"
            enterAt={22}
            exitAt={164}
            fadeInFrames={30}
            style={{ maxWidth: 860 }}
          >
            Check the things you never want to discover missing later.
          </ParentMinuteText>
        </ParentMinuteScene>
      </Sequence>

      {/* SCENE 4 — 0:13–0:16 */}
      <Sequence
        name="4 · Ready to go"
        from={SCENES.readyToGo.from}
        durationInFrames={SCENES.readyToGo.length + END_CARD_DISSOLVE}
      >
        <ParentMinuteScene
          src={asset("readyToGo")}
          label={ASSET_FILES.readyToGo}
          dissolveIn={DISSOLVE}
          durationInFrames={SCENES.readyToGo.length + END_CARD_DISSOLVE}
          camera={{
            // Gentle pull-back with an upward drift as the bag is lifted.
            scale: [1.06, 1.015],
            focus: [
              [50, 60],
              [50, 45],
            ],
            driftY: [0, -18],
          }}
          textPlacement="upper"
        >
          <ParentMinuteText variant="headline" enterAt={14} exitAt={78}>
            A practical reminder for parents.
          </ParentMinuteText>
        </ParentMinuteScene>
      </Sequence>

      {/* SCENE 5 — 0:16–0:20 · End card */}
      <Sequence
        name="5 · End card"
        from={SCENES.endCard.from}
        durationInFrames={SCENES.endCard.length}
      >
        <ParentMinuteEndCard
          durationInFrames={SCENES.endCard.length}
          dissolveIn={END_CARD_DISSOLVE}
        />
      </Sequence>

      <ParentMinuteAudio audio={audio} durationInFrames={VIDEO.durationInFrames} />
    </AbsoluteFill>
  );
};

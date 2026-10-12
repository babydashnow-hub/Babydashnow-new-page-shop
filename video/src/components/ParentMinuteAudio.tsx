import React from "react";
import { interpolate, Sequence, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { z } from "zod";

// Every track is optional. Set a path (relative to public/) to enable it,
// e.g. "parent-minute/audio/music.mp3". null = silent, nothing is loaded.
export const audioSchema = z.object({
  music: z.string().nullable(),
  musicVolume: z.number().min(0).max(1),
  ambience: z.string().nullable(),
  zipper: z.string().nullable(),
  fabric: z.string().nullable(),
});

export type AudioProps = z.infer<typeof audioSchema>;

export const defaultAudio: AudioProps = {
  music: null,
  musicVolume: 0.55,
  ambience: null,
  zipper: null,
  fabric: null,
};

// Natural SFX cue points (absolute frames).
export const SFX_CUES = {
  zipper: { from: 116, durationInFrames: 45, volume: 0.45 }, // Scene 2, bag check
  fabric: { from: 398, durationInFrames: 50, volume: 0.35 }, // Scene 4, bag lifted
} as const;

const fadeVolume =
  (total: number, peak: number, fadeIn: number, fadeOut: number) =>
  (frame: number) =>
    interpolate(
      frame,
      [0, fadeIn, total - fadeOut, total],
      [0, peak, peak, 0],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
    );

export const ParentMinuteAudio: React.FC<{
  audio: AudioProps;
  durationInFrames: number;
}> = ({ audio, durationInFrames }) => (
  <>
    {audio.music ? (
      <Audio
        src={staticFile(audio.music)}
        volume={fadeVolume(durationInFrames, audio.musicVolume, 20, 45)}
      />
    ) : null}
    {audio.ambience ? (
      <Audio
        src={staticFile(audio.ambience)}
        loop
        volume={fadeVolume(durationInFrames, 0.18, 30, 45)}
      />
    ) : null}
    {audio.zipper ? (
      <Sequence
        from={SFX_CUES.zipper.from}
        durationInFrames={SFX_CUES.zipper.durationInFrames}
        name="SFX zipper"
      >
        <Audio src={staticFile(audio.zipper)} volume={SFX_CUES.zipper.volume} />
      </Sequence>
    ) : null}
    {audio.fabric ? (
      <Sequence
        from={SFX_CUES.fabric.from}
        durationInFrames={SFX_CUES.fabric.durationInFrames}
        name="SFX fabric"
      >
        <Audio src={staticFile(audio.fabric)} volume={SFX_CUES.fabric.volume} />
      </Sequence>
    ) : null}
  </>
);

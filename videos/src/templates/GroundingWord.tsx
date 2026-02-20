import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Background } from "../components/Background";
import { Particles } from "../components/Particles";
import { GlowWord } from "../components/TextReveal";
import { Footer, Label, AccentLine, GrainOverlay } from "../components/Brand";
import { AMBER, OFF_WHITE, DIM, FONT_LIGHT, FONT_REGULAR } from "../config";

/**
 * Grounding Word of the Day — 8-10 second Story video.
 *
 * Flow:
 * 0-2s: "your grounding word for today" fades in
 * 2-4s: word appears with glow spring animation
 * 4-7s: "say it out loud. say it again." fades in below
 * 7-10s: everything holds, gentle particle drift
 */
export const GroundingWord: React.FC<{
  word: string;
  backgroundSrc?: string;
  accentColor?: string;
  subtext?: string;
}> = ({
  word,
  backgroundSrc,
  accentColor = AMBER,
  subtext = "say it out loud. say it again. let it settle.",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Subtext fade
  const subtextOpacity = interpolate(t, [4, 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subtextY = interpolate(t, [4, 5.5], [15, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <Background src={backgroundSrc} darken={0.45} />
      <GrainOverlay />
      <Particles count={20} color={accentColor} maxOpacity={0.3} />

      <Label text="grounding word" startTime={0.3} top="16%" />
      <AccentLine startTime={1.2} top="20%" width={40} color={accentColor} />

      {/* Main word */}
      <div
        style={{
          position: "absolute",
          top: "42%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
        }}
      >
        <GlowWord word={word} startFrame={Math.round(2 * fps)} fontSize={110} color={accentColor} />
      </div>

      {/* Subtext */}
      <div
        style={{
          position: "absolute",
          top: "55%",
          left: "50%",
          transform: "translateX(-50%)",
          textAlign: "center",
          opacity: subtextOpacity,
          maxWidth: 700,
        }}
      >
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 28,
            color: DIM,
            letterSpacing: 1,
            lineHeight: 1.8,
            transform: `translateY(${subtextY}px)`,
          }}
        >
          {subtext}
        </div>
      </div>

      <Footer />
    </AbsoluteFill>
  );
};

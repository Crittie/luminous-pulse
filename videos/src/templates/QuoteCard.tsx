import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Background } from "../components/Background";
import { Particles } from "../components/Particles";
import { WordByWord } from "../components/TextReveal";
import { Footer, GrainOverlay } from "../components/Brand";
import { AMBER, OFF_WHITE, DIM, FONT_LIGHT } from "../config";

/**
 * Animated Quote Card — 12-18 second video.
 *
 * Flow:
 * 0-1s: background fades in
 * 1-8s: words appear one by one
 * 8-12s: CTA fades in below
 * 12-15s: everything holds
 */
export const QuoteCard: React.FC<{
  text: string;
  backgroundSrc?: string;
  accentColor?: string;
  accentWords?: string[];
  cta?: string;
}> = ({
  text,
  backgroundSrc,
  accentColor = AMBER,
  accentWords = [],
  cta = "save this for when you need it.",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  // CTA timing — appears after all words have appeared
  const wordCount = text.split(" ").length;
  const ctaStartTime = 1.5 + (wordCount * 4) / fps + 1.5;
  const ctaOpacity = interpolate(t, [ctaStartTime, ctaStartTime + 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const ctaY = interpolate(t, [ctaStartTime, ctaStartTime + 1.5], [10, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Subtle vignette
  const vignetteOpacity = interpolate(t, [0, 2], [0, 0.6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <Background src={backgroundSrc} darken={0.4} zoomFrom={1.02} zoomTo={1.1} />
      <GrainOverlay />

      {/* Vignette */}
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(26,26,46,0.5) 100%)",
          opacity: vignetteOpacity,
        }}
      />

      <Particles count={18} color={accentColor} maxOpacity={0.25} />

      {/* Quote text */}
      <div
        style={{
          position: "absolute",
          top: "38%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
          width: "85%",
        }}
      >
        <WordByWord
          text={text}
          startFrame={Math.round(1.5 * fps)}
          fontSize={50}
          accentColor={accentColor}
          accentWords={accentWords}
          lineHeight={1.7}
          maxWidth={900}
          staggerFrames={4}
        />
      </div>

      {/* CTA */}
      <div
        style={{
          position: "absolute",
          bottom: 180,
          left: "50%",
          transform: `translateX(-50%) translateY(${ctaY}px)`,
          textAlign: "center",
          opacity: ctaOpacity,
        }}
      >
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 24,
            color: DIM,
            letterSpacing: 1.5,
          }}
        >
          {cta}
        </div>
      </div>

      <Footer />
    </AbsoluteFill>
  );
};

import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Background } from "../components/Background";
import { Particles } from "../components/Particles";
import { BreathCircle, PATTERNS } from "../components/BreathCircle";
import { Footer, Label, AccentLine, GrainOverlay } from "../components/Brand";
import { AMBER, OFF_WHITE, DIM, FONT_REGULAR, FONT_LIGHT } from "../config";

type PatternName = keyof typeof PATTERNS;

/**
 * Breathing Exercise Follow-Along.
 *
 * Flow:
 * 0-3s: title + subtitle fade in
 * 3-4s: title fades out, circle appears
 * 4-end: breathing cycles with instruction
 * last 3s: outro message
 */
export const BreathExercise: React.FC<{
  patternName?: PatternName;
  title?: string;
  subtitle?: string;
  backgroundSrc?: string;
  accentColor?: string;
  cycles?: number;
  outro?: string;
}> = ({
  patternName = "physiological-sigh",
  title,
  subtitle,
  backgroundSrc,
  accentColor = AMBER,
  cycles = 2,
  outro = "your nervous system just got a reset.",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const totalDuration = durationInFrames / fps;

  const pattern = PATTERNS[patternName];
  const cycleDuration = pattern.reduce((sum, p) => sum + p.duration, 0);

  // Default titles per pattern
  const defaultTitles: Record<PatternName, { title: string; subtitle: string }> = {
    "physiological-sigh": {
      title: "the physiological sigh",
      subtitle: "the 10-second nervous system reset",
    },
    coherent: {
      title: "coherent breathing",
      subtitle: "5.5 breaths per minute calms everything",
    },
    box: {
      title: "box breathing",
      subtitle: "the technique used by navy seals",
    },
    "4-7-8": {
      title: "4-7-8 breathing",
      subtitle: "the natural tranquilizer for your nervous system",
    },
  };

  const displayTitle = title || defaultTitles[patternName].title;
  const displaySubtitle = subtitle || defaultTitles[patternName].subtitle;

  // Title fade in/out
  const titleIn = interpolate(t, [0.3, 1.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const titleOut = interpolate(t, [2.8, 3.5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Outro
  const breathEnd = 3.5 + cycleDuration * cycles + 1;
  const outroIn = interpolate(t, [breathEnd, breathEnd + 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // "Try it with me" between cycles
  const firstCycleEnd = 3.5 + cycleDuration;
  const tryItIn = interpolate(
    t,
    [firstCycleEnd, firstCycleEnd + 0.5, firstCycleEnd + cycleDuration * 0.15 - 0.3, firstCycleEnd + cycleDuration * 0.15],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill>
      <Background src={backgroundSrc} darken={0.5} zoomFrom={1.03} zoomTo={1.12} />
      <GrainOverlay />
      <Particles count={15} color={accentColor} maxOpacity={0.2} />

      {/* Title screen */}
      <div
        style={{
          position: "absolute",
          top: "22%",
          left: "50%",
          transform: "translateX(-50%)",
          textAlign: "center",
          opacity: titleIn * titleOut,
          width: "85%",
        }}
      >
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 24,
            color: DIM,
            letterSpacing: 4,
            textTransform: "uppercase",
            marginBottom: 16,
          }}
        >
          breathe with me
        </div>
        <div
          style={{
            fontFamily: FONT_REGULAR,
            fontSize: 52,
            fontWeight: "bold",
            color: OFF_WHITE,
            lineHeight: 1.3,
          }}
        >
          {displayTitle.split(" ").map((word, i) => {
            // Accent the last word
            const words = displayTitle.split(" ");
            const isLast = i === words.length - 1;
            return (
              <span key={i} style={{ color: isLast ? accentColor : OFF_WHITE }}>
                {word}{" "}
              </span>
            );
          })}
        </div>
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 26,
            color: DIM,
            marginTop: 20,
            letterSpacing: 1,
          }}
        >
          {displaySubtitle}
        </div>
        <div
          style={{
            width: 50,
            height: 3,
            background: accentColor,
            margin: "24px auto 0",
            borderRadius: 2,
          }}
        />
      </div>

      {/* Breathing circle */}
      <BreathCircle
        pattern={pattern}
        startTime={3.5}
        cycles={cycles}
        accentColor={accentColor}
      />

      {/* "Try it with me" between cycles */}
      {cycles > 1 && (
        <div
          style={{
            position: "absolute",
            top: "72%",
            left: "50%",
            transform: "translateX(-50%)",
            textAlign: "center",
            opacity: tryItIn,
          }}
        >
          <div
            style={{
              fontFamily: FONT_REGULAR,
              fontSize: 30,
              color: OFF_WHITE,
              letterSpacing: 2,
            }}
          >
            now try it with me
          </div>
        </div>
      )}

      {/* Header during breathing */}
      <Label
        text={patternName.replace("-", " ")}
        startTime={3.2}
        endTime={breathEnd - 0.5}
        top="12%"
      />

      {/* Outro */}
      <div
        style={{
          position: "absolute",
          top: "38%",
          left: "50%",
          transform: "translateX(-50%)",
          textAlign: "center",
          opacity: outroIn,
          width: "80%",
        }}
      >
        <div
          style={{
            fontFamily: FONT_REGULAR,
            fontSize: 42,
            color: OFF_WHITE,
            lineHeight: 1.5,
          }}
        >
          {outro}
        </div>
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 26,
            color: DIM,
            marginTop: 24,
            letterSpacing: 2,
          }}
        >
          save this for when you need it.
        </div>
      </div>

      <Footer />
    </AbsoluteFill>
  );
};

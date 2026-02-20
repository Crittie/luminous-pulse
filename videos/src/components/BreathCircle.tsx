import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";
import { AMBER, BLUE, LAVENDER, DIM, FONT_LIGHT } from "../config";

/**
 * Breathing circle animation with phase labels.
 * Supports multiple breathing patterns.
 */

interface BreathPhase {
  type: "inhale" | "exhale" | "hold" | "rest";
  duration: number; // seconds
  label?: string;
}

// Pre-built breathing patterns
export const PATTERNS = {
  "physiological-sigh": [
    { type: "inhale" as const, duration: 1.2, label: "inhale" },
    { type: "inhale" as const, duration: 1.0, label: "inhale again" },
    { type: "hold" as const, duration: 0.5 },
    { type: "exhale" as const, duration: 3.5, label: "long exhale" },
    { type: "rest" as const, duration: 1.5 },
  ],
  coherent: [
    { type: "inhale" as const, duration: 5.5, label: "inhale" },
    { type: "exhale" as const, duration: 5.5, label: "exhale" },
    { type: "rest" as const, duration: 0.5 },
  ],
  box: [
    { type: "inhale" as const, duration: 4, label: "inhale" },
    { type: "hold" as const, duration: 4, label: "hold" },
    { type: "exhale" as const, duration: 4, label: "exhale" },
    { type: "hold" as const, duration: 4, label: "hold" },
    { type: "rest" as const, duration: 0.5 },
  ],
  "4-7-8": [
    { type: "inhale" as const, duration: 4, label: "inhale" },
    { type: "hold" as const, duration: 7, label: "hold" },
    { type: "exhale" as const, duration: 8, label: "exhale" },
    { type: "rest" as const, duration: 1 },
  ],
};

export const BreathCircle: React.FC<{
  pattern: BreathPhase[];
  startTime: number; // seconds
  cycles?: number;
  circleSize?: number;
  accentColor?: string;
  showLabel?: boolean;
  showInstruction?: boolean;
  positionY?: string;
}> = ({
  pattern,
  startTime,
  cycles = 2,
  circleSize = 280,
  accentColor = AMBER,
  showLabel = true,
  showInstruction = true,
  positionY = "42%",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  // Calculate total cycle duration
  const cycleDuration = pattern.reduce((sum, p) => sum + p.duration, 0);

  // Find current phase
  let scale = 0.35;
  let labelText = "";
  let labelColor = accentColor;
  let instructionText = "";
  let subText = "";

  const elapsed = t - startTime;
  if (elapsed >= 0 && elapsed < cycleDuration * cycles) {
    const cycleTime = elapsed % cycleDuration;
    let phaseStart = 0;
    let prevScale = 0.35;

    for (const phase of pattern) {
      if (cycleTime >= phaseStart && cycleTime < phaseStart + phase.duration) {
        const progress = (cycleTime - phaseStart) / phase.duration;

        if (phase.type === "inhale") {
          const targetScale = prevScale + (1.0 - 0.35) * (phase.duration / cycleDuration) * 2.5;
          scale = interpolate(progress, [0, 1], [prevScale, Math.min(targetScale, 1.0)], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.out(Easing.cubic),
          });
          labelText = phase.label || "inhale";
          labelColor = accentColor;
          instructionText = "through your nose";
          subText = "breathe in";
        } else if (phase.type === "exhale") {
          scale = interpolate(progress, [0, 1], [1.0, 0.35], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.inOut(Easing.cubic),
          });
          labelText = phase.label || "exhale";
          labelColor = BLUE;
          instructionText = "through your mouth";
          subText = "breathe out";
        } else if (phase.type === "hold") {
          scale = prevScale > 0.7 ? 1.0 : 0.35;
          labelText = phase.label || "hold";
          labelColor = LAVENDER;
          instructionText = "";
          subText = "";
        } else {
          scale = 0.35;
          labelText = "";
          instructionText = "";
          subText = "";
        }
        break;
      }
      // Track what scale we ended at
      if (phase.type === "inhale") {
        const targetScale = prevScale + (1.0 - 0.35) * (phase.duration / cycleDuration) * 2.5;
        prevScale = Math.min(targetScale, 1.0);
      } else if (phase.type === "exhale") {
        prevScale = 0.35;
      }
      phaseStart += phase.duration;
    }
  }

  // Fade in/out
  const fadeIn = interpolate(t, [startTime - 0.5, startTime + 0.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const totalEnd = startTime + cycleDuration * cycles;
  const fadeOut = interpolate(t, [totalEnd - 0.5, totalEnd + 0.5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const visibility = fadeIn * fadeOut;

  const outerGlow = circleSize * scale * 1.5;

  return (
    <>
      {/* Circle */}
      <div
        style={{
          position: "absolute",
          top: positionY,
          left: "50%",
          transform: "translate(-50%, -50%)",
          opacity: visibility,
        }}
      >
        {/* Outer glow */}
        <div
          style={{
            width: outerGlow,
            height: outerGlow,
            borderRadius: "50%",
            background: `radial-gradient(circle, ${accentColor}12 0%, ${accentColor}06 40%, transparent 70%)`,
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
          }}
        />
        {/* Main circle */}
        <div
          style={{
            width: circleSize * scale,
            height: circleSize * scale,
            borderRadius: "50%",
            border: `2.5px solid ${accentColor}`,
            background: `radial-gradient(circle at 40% 35%, ${accentColor}15 0%, ${accentColor}05 50%, transparent 70%)`,
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            boxShadow: `0 0 30px ${accentColor}18, inset 0 0 20px ${accentColor}08`,
          }}
        />
        {/* Center dot */}
        <div
          style={{
            width: 6,
            height: 6,
            borderRadius: "50%",
            background: accentColor,
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            opacity: 0.5,
          }}
        />
      </div>

      {/* Phase label */}
      {showLabel && labelText && (
        <div
          style={{
            position: "absolute",
            top: `calc(${positionY} + ${circleSize * 0.55}px)`,
            left: "50%",
            transform: "translateX(-50%)",
            fontFamily: FONT_LIGHT,
            fontSize: 44,
            letterSpacing: 6,
            color: labelColor,
            opacity: visibility,
            textAlign: "center",
            textTransform: "lowercase",
          }}
        >
          {labelText}
        </div>
      )}

      {/* Instruction */}
      {showInstruction && instructionText && (
        <div
          style={{
            position: "absolute",
            top: `calc(${positionY} + ${circleSize * 0.55 + 55}px)`,
            left: "50%",
            transform: "translateX(-50%)",
            textAlign: "center",
            opacity: visibility * 0.7,
          }}
        >
          <div
            style={{
              fontFamily: FONT_LIGHT,
              fontSize: 24,
              color: DIM,
              letterSpacing: 2,
            }}
          >
            {instructionText}
          </div>
        </div>
      )}
    </>
  );
};

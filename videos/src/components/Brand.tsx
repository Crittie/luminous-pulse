import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { DIM, FONT_REGULAR, FONT_LIGHT, AMBER } from "../config";

/**
 * Brand footer — @luminouspulse.co
 */
export const Footer: React.FC<{
  fadeInTime?: number;
  bottomOffset?: number;
}> = ({ fadeInTime = 1, bottomOffset = 80 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const opacity = interpolate(t, [fadeInTime, fadeInTime + 1], [0, 0.6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: bottomOffset,
        left: "50%",
        transform: "translateX(-50%)",
        fontFamily: FONT_REGULAR,
        fontSize: 22,
        color: DIM,
        opacity,
        letterSpacing: 2,
      }}
    >
      @luminouspulse.co
    </div>
  );
};

/**
 * Section label — small uppercase text
 */
export const Label: React.FC<{
  text: string;
  startTime?: number;
  endTime?: number;
  top?: string;
  color?: string;
  fontSize?: number;
}> = ({
  text,
  startTime = 0,
  endTime,
  top = "12%",
  color = DIM,
  fontSize = 22,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;

  const fadeIn = interpolate(t, [startTime, startTime + 0.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const end = endTime ?? durationInFrames / fps;
  const fadeOut = interpolate(t, [end - 0.5, end], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top,
        left: "50%",
        transform: "translateX(-50%)",
        fontFamily: FONT_LIGHT,
        fontSize,
        color,
        opacity: fadeIn * fadeOut,
        letterSpacing: 4,
        textTransform: "uppercase",
      }}
    >
      {text}
    </div>
  );
};

/**
 * Amber accent line — thin horizontal bar
 */
export const AccentLine: React.FC<{
  width?: number;
  startTime?: number;
  top?: string;
  color?: string;
}> = ({ width = 50, startTime = 0.5, top = "50%", color = AMBER }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  const lineWidth = interpolate(t, [startTime, startTime + 0.6], [0, width], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top,
        left: "50%",
        transform: "translateX(-50%)",
        width: lineWidth,
        height: 3,
        background: color,
        borderRadius: 2,
      }}
    />
  );
};

/**
 * Grain overlay via SVG filter
 */
export const GrainOverlay: React.FC<{ opacity?: number }> = ({
  opacity = 0.4,
}) => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E")`,
      backgroundSize: "128px 128px",
      opacity,
      mixBlendMode: "overlay",
      pointerEvents: "none",
    }}
  />
);

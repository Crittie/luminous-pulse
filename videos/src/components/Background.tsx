import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { NAVY, NAVY_LIGHT } from "../config";

/**
 * Animated background with Ken Burns effect (slow zoom + pan).
 * If backgroundSrc is provided, uses an AI-generated image.
 * Otherwise falls back to navy radial gradient.
 */
export const Background: React.FC<{
  src?: string;
  zoomFrom?: number;
  zoomTo?: number;
  panX?: number;
  panY?: number;
  darken?: number;
}> = ({
  src,
  zoomFrom = 1.05,
  zoomTo = 1.15,
  panX = -20,
  panY = -10,
  darken = 0.35,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const scale = interpolate(frame, [0, durationInFrames], [zoomFrom, zoomTo], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateX = interpolate(frame, [0, durationInFrames], [0, panX], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const translateY = interpolate(frame, [0, durationInFrames], [0, panY], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  if (!src) {
    return (
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 45%, ${NAVY_LIGHT} 0%, ${NAVY} 70%)`,
        }}
      />
    );
  }

  // Use staticFile for relative paths (from public/), keep absolute/data URLs as-is
  const imgSrc = src.startsWith("http") || src.startsWith("data:") || src.startsWith("/")
    ? src
    : staticFile(src);

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: NAVY }}>
      <Img
        src={imgSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
        }}
      />
      {/* Dark overlay to ensure text readability */}
      <AbsoluteFill
        style={{
          background: `rgba(26, 26, 46, ${darken})`,
        }}
      />
    </AbsoluteFill>
  );
};

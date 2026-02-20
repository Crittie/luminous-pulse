import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Background } from "../components/Background";
import { Particles } from "../components/Particles";
import { Typewriter } from "../components/TextReveal";
import { Footer, GrainOverlay } from "../components/Brand";
import { AMBER, LAVENDER, OFF_WHITE, DIM, FONT_REGULAR, FONT_LIGHT } from "../config";

/**
 * Permission Slip Friday — 10-12 second Story video.
 *
 * Flow:
 * 0-1.5s: "permission slip" header fades in
 * 1.5-6s: permission text types out letter by letter
 * 6-9s: "— granted" appears with gentle pulse
 * 9-12s: holds with particles
 */
export const PermissionSlip: React.FC<{
  text: string;
  backgroundSrc?: string;
  accentColor?: string;
}> = ({
  text,
  backgroundSrc,
  accentColor = LAVENDER,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Header
  const headerIn = interpolate(t, [0.3, 1.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // "granted" tag
  const grantedTime = 1.5 + (text.length * 2) / fps + 1;
  const grantedIn = interpolate(t, [grantedTime, grantedTime + 0.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const grantedScale = interpolate(t, [grantedTime, grantedTime + 0.5], [0.9, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Gentle pulse on "granted"
  const pulse = t > grantedTime + 1 ? 1 + 0.015 * Math.sin((t - grantedTime) * 2) : 1;

  return (
    <AbsoluteFill>
      <Background src={backgroundSrc} darken={0.5} />
      <GrainOverlay />
      <Particles count={15} color={accentColor} maxOpacity={0.25} />

      {/* Header */}
      <div
        style={{
          position: "absolute",
          top: "20%",
          left: "50%",
          transform: "translateX(-50%)",
          textAlign: "center",
          opacity: headerIn,
        }}
      >
        <div
          style={{
            fontFamily: FONT_LIGHT,
            fontSize: 22,
            color: DIM,
            letterSpacing: 5,
            textTransform: "uppercase",
          }}
        >
          permission slip friday
        </div>
        <div
          style={{
            width: 40,
            height: 2,
            background: accentColor,
            margin: "16px auto 0",
            borderRadius: 2,
            opacity: 0.7,
          }}
        />
      </div>

      {/* Permission text */}
      <div
        style={{
          position: "absolute",
          top: "40%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
          width: "80%",
        }}
      >
        <Typewriter
          text={text}
          startFrame={Math.round(1.5 * fps)}
          fontSize={40}
          color={OFF_WHITE}
          framesPerChar={2}
          fontWeight="light"
        />
      </div>

      {/* "— granted" */}
      <div
        style={{
          position: "absolute",
          top: "58%",
          left: "50%",
          transform: `translateX(-50%) scale(${grantedScale * pulse})`,
          textAlign: "center",
          opacity: grantedIn,
        }}
      >
        <div
          style={{
            fontFamily: FONT_REGULAR,
            fontSize: 36,
            fontWeight: "bold",
            color: accentColor,
            letterSpacing: 6,
            textShadow: `0 0 30px ${accentColor}40`,
          }}
        >
          — granted.
        </div>
      </div>

      <Footer />
    </AbsoluteFill>
  );
};

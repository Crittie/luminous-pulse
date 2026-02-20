import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { OFF_WHITE, AMBER, FONT_REGULAR, FONT_LIGHT } from "../config";

/**
 * Word-by-word text reveal with optional accent highlighting.
 */
export const WordByWord: React.FC<{
  text: string;
  startFrame: number;
  fontSize?: number;
  color?: string;
  accentColor?: string;
  accentWords?: string[];
  lineHeight?: number;
  maxWidth?: number;
  textAlign?: "center" | "left";
  fontWeight?: "regular" | "light" | "bold";
  letterSpacing?: number;
  staggerFrames?: number;
}> = ({
  text,
  startFrame,
  fontSize = 48,
  color = OFF_WHITE,
  accentColor = AMBER,
  accentWords = [],
  lineHeight = 1.6,
  maxWidth = 850,
  textAlign = "center",
  fontWeight = "regular",
  letterSpacing = 0,
  staggerFrames = 4,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const words = text.split(" ");
  const accentSet = new Set(accentWords.map((w) => w.toLowerCase().replace(/[.,!?;:]/g, "")));

  const fontFamily =
    fontWeight === "light" ? FONT_LIGHT :
    fontWeight === "bold" ? `${FONT_REGULAR}` :
    FONT_REGULAR;

  return (
    <div
      style={{
        maxWidth,
        textAlign,
        lineHeight,
        fontFamily,
        fontSize,
        fontWeight: fontWeight === "bold" ? "bold" : "normal",
        letterSpacing,
      }}
    >
      {words.map((word, i) => {
        const wordFrame = startFrame + i * staggerFrames;
        const opacity = interpolate(frame, [wordFrame, wordFrame + 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const translateY = interpolate(frame, [wordFrame, wordFrame + 10], [12, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        const cleanWord = word.toLowerCase().replace(/[.,!?;:'"]/g, "");
        const isAccent = accentSet.has(cleanWord);

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity,
              transform: `translateY(${translateY}px)`,
              color: isAccent ? accentColor : color,
              marginRight: "0.3em",
              textShadow: isAccent ? `0 0 30px ${accentColor}40` : "none",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

/**
 * Line-by-line text reveal with fade + slide.
 */
export const LineByLine: React.FC<{
  lines: string[];
  startFrame: number;
  fontSize?: number;
  color?: string;
  accentColor?: string;
  accentLineIndex?: number;
  lineHeight?: number;
  maxWidth?: number;
  textAlign?: "center" | "left";
  fontWeight?: "regular" | "light";
  letterSpacing?: number;
  staggerFrames?: number;
}> = ({
  lines,
  startFrame,
  fontSize = 48,
  color = OFF_WHITE,
  accentColor = AMBER,
  accentLineIndex = -1,
  lineHeight = 1.6,
  maxWidth = 850,
  textAlign = "center",
  fontWeight = "regular",
  letterSpacing = 0,
  staggerFrames = 18,
}) => {
  const frame = useCurrentFrame();

  const fontFamily = fontWeight === "light" ? FONT_LIGHT : FONT_REGULAR;

  return (
    <div
      style={{
        maxWidth,
        textAlign,
        fontFamily,
        fontSize,
        letterSpacing,
      }}
    >
      {lines.map((line, i) => {
        const lineFrame = startFrame + i * staggerFrames;
        const opacity = interpolate(frame, [lineFrame, lineFrame + 12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const translateY = interpolate(frame, [lineFrame, lineFrame + 15], [20, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const isAccent = i === accentLineIndex;

        return (
          <div
            key={i}
            style={{
              opacity,
              transform: `translateY(${translateY}px)`,
              color: isAccent ? accentColor : color,
              lineHeight,
              marginBottom: 8,
              textShadow: isAccent ? `0 0 40px ${accentColor}30` : "none",
            }}
          >
            {line}
          </div>
        );
      })}
    </div>
  );
};

/**
 * Single large word reveal with glow effect. Used for grounding words.
 */
export const GlowWord: React.FC<{
  word: string;
  startFrame: number;
  fontSize?: number;
  color?: string;
  glowColor?: string;
}> = ({
  word,
  startFrame,
  fontSize = 120,
  color = AMBER,
  glowColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const glow = glowColor || color;

  // Scale in with spring
  const scaleRaw = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 80, stiffness: 100, mass: 0.8 },
  });
  const scale = frame >= startFrame ? scaleRaw : 0;

  // Opacity
  const opacity = interpolate(frame, [startFrame, startFrame + 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Gentle breathing pulse after appearing
  const t = (frame - startFrame) / fps;
  const pulse = t > 0.5 ? 1 + 0.02 * Math.sin(t * 1.5) : 1;

  // Glow intensity
  const glowSize = interpolate(frame, [startFrame, startFrame + 20], [0, 50], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        fontFamily: FONT_REGULAR,
        fontSize,
        fontWeight: "bold",
        color,
        opacity,
        transform: `scale(${scale * pulse})`,
        textShadow: `0 0 ${glowSize}px ${glow}50, 0 0 ${glowSize * 2}px ${glow}25`,
        letterSpacing: 6,
        textTransform: "lowercase",
      }}
    >
      {word}
    </div>
  );
};

/**
 * Typewriter letter-by-letter reveal.
 */
export const Typewriter: React.FC<{
  text: string;
  startFrame: number;
  fontSize?: number;
  color?: string;
  framesPerChar?: number;
  fontWeight?: "regular" | "light";
}> = ({
  text,
  startFrame,
  fontSize = 42,
  color = OFF_WHITE,
  framesPerChar = 2,
  fontWeight = "light",
}) => {
  const frame = useCurrentFrame();

  const charsVisible = Math.floor(
    Math.max(0, (frame - startFrame) / framesPerChar)
  );
  const displayText = text.slice(0, Math.min(charsVisible, text.length));

  const fontFamily = fontWeight === "light" ? FONT_LIGHT : FONT_REGULAR;

  // Cursor blink
  const cursorVisible =
    frame >= startFrame &&
    charsVisible < text.length &&
    Math.floor((frame - startFrame) / 8) % 2 === 0;

  return (
    <span
      style={{
        fontFamily,
        fontSize,
        color,
        letterSpacing: 2,
      }}
    >
      {displayText}
      {cursorVisible && (
        <span style={{ opacity: 0.6, color: AMBER }}>|</span>
      )}
    </span>
  );
};

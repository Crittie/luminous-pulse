import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

interface Particle {
  x: number;
  y: number;
  size: number;
  speed: number;
  opacity: number;
  delay: number;
  drift: number;
}

/**
 * Floating light particles that drift upward. Creates a sanctuary atmosphere.
 * Particles are deterministic (seeded from index) so renders are reproducible.
 */
export const Particles: React.FC<{
  count?: number;
  color?: string;
  maxOpacity?: number;
}> = ({ count = 25, color = "#F4C430", maxOpacity = 0.4 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const t = frame / fps;

  // Generate deterministic particles
  const particles: Particle[] = React.useMemo(() => {
    const result: Particle[] = [];
    for (let i = 0; i < count; i++) {
      // Simple seeded pseudo-random
      const seed = (i * 7919 + 1) % 10000;
      const r = (n: number) => ((seed * (n + 1) * 9973) % 10000) / 10000;

      result.push({
        x: r(1) * width,
        y: r(2) * height,
        size: 2 + r(3) * 5,
        speed: 15 + r(4) * 25, // pixels per second upward
        opacity: 0.15 + r(5) * (maxOpacity - 0.15),
        delay: r(6) * 4, // stagger appearance
        drift: (r(7) - 0.5) * 30, // horizontal drift
      });
    }
    return result;
  }, [count, width, height, maxOpacity]);

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {particles.map((p, i) => {
        // Fade in
        const fadeIn = interpolate(t, [p.delay, p.delay + 1.5], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        // Fade out at end
        const totalDuration = durationInFrames / fps;
        const fadeOut = interpolate(
          t,
          [totalDuration - 2, totalDuration - 0.5],
          [1, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
        );

        // Movement
        const yOffset = -t * p.speed;
        const xOffset = Math.sin(t * 0.5 + i) * p.drift;

        // Wrap vertically
        const currentY = ((p.y + yOffset) % (height + 40)) - 20;
        const wrappedY = currentY < -20 ? currentY + height + 40 : currentY;

        // Gentle pulse
        const pulse = 0.7 + 0.3 * Math.sin(t * 2 + i * 0.8);

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: p.x + xOffset,
              top: wrappedY,
              width: p.size,
              height: p.size,
              borderRadius: "50%",
              background: color,
              opacity: p.opacity * fadeIn * fadeOut * pulse,
              boxShadow: `0 0 ${p.size * 2}px ${p.size}px ${color}40`,
              filter: "blur(0.5px)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

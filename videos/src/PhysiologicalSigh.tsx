import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";

// ── Brand palette ──────────────────────────────────────────
const NAVY = "#1a1a2e";
const NAVY_LIGHT = "#22283e";
const OFF_WHITE = "#F5F0EB";
const AMBER = "#F4C430";
const BLUE = "#6CB4EE";
const LAVENDER = "#B4A7D6";
const DIM = "#787d8c";

// ── Breathing timing (in seconds) ──────────────────────────
// Physiological sigh: inhale 1 (short) → inhale 2 (short) → long exhale
const INTRO_DURATION = 2.5;
const INHALE_1_START = 3;
const INHALE_1_DURATION = 1.2;
const INHALE_2_START = 4.4;
const INHALE_2_DURATION = 1.0;
const HOLD_START = 5.6;
const HOLD_DURATION = 0.5;
const EXHALE_START = 6.1;
const EXHALE_DURATION = 3.5;
const REST_START = 9.6;
const REST_DURATION = 1.0;

// Second cycle
const CYCLE2_OFFSET = 11;
const INHALE_1_START_2 = CYCLE2_OFFSET;
const INHALE_2_START_2 = CYCLE2_OFFSET + 1.4;
const HOLD_START_2 = CYCLE2_OFFSET + 2.6;
const EXHALE_START_2 = CYCLE2_OFFSET + 3.1;
const EXHALE_END_2 = CYCLE2_OFFSET + 6.6;

const OUTRO_START = 18;

// ── Helper: time in seconds from frame ─────────────────────
function useTime() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return frame / fps;
}

// ── Radial gradient background ─────────────────────────────
const RadialBg: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse at 50% 45%, ${NAVY_LIGHT} 0%, ${NAVY} 70%)`,
    }}
  />
);

// ── Subtle grain overlay ───────────────────────────────────
const GrainOverlay: React.FC = () => (
  <AbsoluteFill
    style={{
      backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E")`,
      backgroundSize: "128px 128px",
      opacity: 0.5,
      mixBlendMode: "overlay",
    }}
  />
);

// ── Breathing circle ───────────────────────────────────────
const BreathCircle: React.FC = () => {
  const t = useTime();

  // Calculate circle scale based on breathing phase
  let scale = 0.4; // resting size

  // Cycle 1
  if (t >= INHALE_1_START && t < INHALE_1_START + INHALE_1_DURATION) {
    // First inhale: grow from 0.4 to 0.65
    const progress = (t - INHALE_1_START) / INHALE_1_DURATION;
    scale = interpolate(progress, [0, 1], [0.4, 0.65], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else if (t >= INHALE_2_START && t < INHALE_2_START + INHALE_2_DURATION) {
    // Second inhale: grow from 0.65 to 1.0
    const progress = (t - INHALE_2_START) / INHALE_2_DURATION;
    scale = interpolate(progress, [0, 1], [0.65, 1.0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else if (t >= HOLD_START && t < HOLD_START + HOLD_DURATION) {
    scale = 1.0; // hold at full
  } else if (t >= EXHALE_START && t < EXHALE_START + EXHALE_DURATION) {
    // Exhale: shrink from 1.0 to 0.4
    const progress = (t - EXHALE_START) / EXHALE_DURATION;
    scale = interpolate(progress, [0, 1], [1.0, 0.4], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.cubic),
    });
  } else if (t >= REST_START && t < CYCLE2_OFFSET) {
    scale = 0.4;
  }

  // Cycle 2
  if (t >= INHALE_1_START_2 && t < INHALE_1_START_2 + INHALE_1_DURATION) {
    const progress = (t - INHALE_1_START_2) / INHALE_1_DURATION;
    scale = interpolate(progress, [0, 1], [0.4, 0.65], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else if (
    t >= INHALE_2_START_2 &&
    t < INHALE_2_START_2 + INHALE_2_DURATION
  ) {
    const progress = (t - INHALE_2_START_2) / INHALE_2_DURATION;
    scale = interpolate(progress, [0, 1], [0.65, 1.0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else if (t >= HOLD_START_2 && t < HOLD_START_2 + HOLD_DURATION) {
    scale = 1.0;
  } else if (t >= EXHALE_START_2 && t < EXHALE_END_2) {
    const progress = (t - EXHALE_START_2) / EXHALE_DURATION;
    scale = interpolate(progress, [0, 1], [1.0, 0.4], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.cubic),
    });
  } else if (t >= EXHALE_END_2 && t < OUTRO_START) {
    scale = 0.4;
  }

  // Intro: circle fades in, then fades out at outro
  const introOpacity = interpolate(t, [1.5, 2.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Fade out circle at outro
  const outroFade = interpolate(t, [OUTRO_START - 0.5, OUTRO_START + 0.3], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const circleSize = 320;
  const outerGlow = circleSize * scale * 1.4;

  return (
    <div
      style={{
        position: "absolute",
        top: "42%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        opacity: introOpacity * outroFade,
      }}
    >
      {/* Outer glow */}
      <div
        style={{
          width: outerGlow,
          height: outerGlow,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${AMBER}15 0%, ${AMBER}08 40%, transparent 70%)`,
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          transition: "width 0.05s, height 0.05s",
        }}
      />
      {/* Main circle */}
      <div
        style={{
          width: circleSize * scale,
          height: circleSize * scale,
          borderRadius: "50%",
          border: `3px solid ${AMBER}`,
          background: `radial-gradient(circle at 40% 35%, ${AMBER}18 0%, ${AMBER}08 50%, transparent 70%)`,
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          boxShadow: `0 0 40px ${AMBER}20, inset 0 0 30px ${AMBER}10`,
          transition: "width 0.05s, height 0.05s",
        }}
      />
      {/* Center dot */}
      <div
        style={{
          width: 8,
          height: 8,
          borderRadius: "50%",
          background: AMBER,
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          opacity: 0.6,
        }}
      />
    </div>
  );
};

// ── Phase label (inhale / exhale) ──────────────────────────
const PhaseLabel: React.FC = () => {
  const t = useTime();

  let text = "";
  let opacity = 0;
  let color = OFF_WHITE;

  // Cycle 1
  if (t >= INHALE_1_START && t < INHALE_1_START + INHALE_1_DURATION) {
    text = "inhale";
    opacity = 1;
    color = AMBER;
  } else if (t >= INHALE_2_START && t < INHALE_2_START + INHALE_2_DURATION) {
    text = "inhale again";
    opacity = 1;
    color = AMBER;
  } else if (t >= HOLD_START && t < HOLD_START + HOLD_DURATION) {
    text = "hold";
    opacity = 1;
    color = LAVENDER;
  } else if (t >= EXHALE_START && t < EXHALE_START + EXHALE_DURATION) {
    text = "long exhale";
    opacity = 1;
    color = BLUE;
  }

  // Cycle 2
  if (t >= INHALE_1_START_2 && t < INHALE_1_START_2 + INHALE_1_DURATION) {
    text = "inhale";
    opacity = 1;
    color = AMBER;
  } else if (
    t >= INHALE_2_START_2 &&
    t < INHALE_2_START_2 + INHALE_2_DURATION
  ) {
    text = "inhale again";
    opacity = 1;
    color = AMBER;
  } else if (t >= HOLD_START_2 && t < HOLD_START_2 + HOLD_DURATION) {
    text = "hold";
    opacity = 1;
    color = LAVENDER;
  } else if (t >= EXHALE_START_2 && t < EXHALE_END_2) {
    text = "long exhale";
    opacity = 1;
    color = BLUE;
  }

  // Fade transitions
  if (opacity > 0) {
    // Don't need extra fade logic — the phase switches handle it
  }

  return (
    <div
      style={{
        position: "absolute",
        top: "62%",
        left: "50%",
        transform: "translateX(-50%)",
        fontFamily:
          "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
        fontSize: 48,
        letterSpacing: 8,
        color,
        opacity,
        textTransform: "lowercase",
        textAlign: "center",
        transition: "opacity 0.3s ease",
      }}
    >
      {text}
    </div>
  );
};

// ── Step indicators (nose/mouth icons as text) ─────────────
const StepIndicator: React.FC = () => {
  const t = useTime();

  let text = "";
  let subtext = "";
  let opacity = 0;

  // Cycle 1
  if (t >= INHALE_1_START && t < INHALE_2_START + INHALE_2_DURATION) {
    text = "through your nose";
    subtext = "two quick breaths in";
    opacity = 1;
  } else if (t >= EXHALE_START && t < EXHALE_START + EXHALE_DURATION) {
    text = "through your mouth";
    subtext = "one long breath out";
    opacity = 1;
  }

  // Cycle 2
  if (t >= INHALE_1_START_2 && t < INHALE_2_START_2 + INHALE_2_DURATION) {
    text = "through your nose";
    subtext = "two quick breaths in";
    opacity = 1;
  } else if (t >= EXHALE_START_2 && t < EXHALE_END_2) {
    text = "through your mouth";
    subtext = "one long breath out";
    opacity = 1;
  }

  return (
    <div
      style={{
        position: "absolute",
        top: "68%",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity,
        transition: "opacity 0.4s ease",
      }}
    >
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 28,
          color: DIM,
          letterSpacing: 2,
          marginTop: 16,
        }}
      >
        {text}
      </div>
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 24,
          color: `${DIM}99`,
          letterSpacing: 1,
          marginTop: 8,
        }}
      >
        {subtext}
      </div>
    </div>
  );
};

// ── Title text ─────────────────────────────────────────────
const TitleText: React.FC = () => {
  const t = useTime();

  // Title fades in at start
  const titleOpacity = interpolate(t, [0.3, 1.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Title fades out when breathing starts
  const titleFadeOut = interpolate(t, [2.5, 3.0], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "18%",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity: titleOpacity * titleFadeOut,
        width: "85%",
      }}
    >
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 30,
          color: DIM,
          letterSpacing: 4,
          textTransform: "uppercase",
          marginBottom: 16,
        }}
      >
        the 10-second reset
      </div>
      <div
        style={{
          fontFamily:
            "HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 56,
          fontWeight: "bold",
          color: OFF_WHITE,
          lineHeight: 1.3,
          letterSpacing: 1,
        }}
      >
        the physiological{" "}
        <span style={{ color: AMBER }}>sigh</span>
      </div>
      <div
        style={{
          width: 60,
          height: 3,
          background: AMBER,
          margin: "24px auto 0",
          borderRadius: 2,
        }}
      />
    </div>
  );
};

// ── Persistent header (shows during breathing) ─────────────
const Header: React.FC = () => {
  const t = useTime();

  const opacity = interpolate(t, [2.8, 3.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Fade out at outro
  const fadeOut = interpolate(t, [OUTRO_START, OUTRO_START + 0.5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "12%",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity: opacity * fadeOut,
      }}
    >
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 26,
          color: DIM,
          letterSpacing: 4,
          textTransform: "uppercase",
        }}
      >
        physiological sigh
      </div>
      {/* Step diagram: ● ● → ○ */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginTop: 20,
          gap: 12,
        }}
      >
        <SmallDot color={AMBER} label="in" t={t} activeStart={INHALE_1_START} activeEnd={INHALE_1_START + INHALE_1_DURATION} activeStart2={INHALE_1_START_2} activeEnd2={INHALE_1_START_2 + INHALE_1_DURATION} />
        <SmallDot color={AMBER} label="in" t={t} activeStart={INHALE_2_START} activeEnd={INHALE_2_START + INHALE_2_DURATION} activeStart2={INHALE_2_START_2} activeEnd2={INHALE_2_START_2 + INHALE_2_DURATION} />
        <div style={{ color: DIM, fontSize: 20, margin: "0 4px" }}>→</div>
        <SmallDot color={BLUE} label="out" t={t} activeStart={EXHALE_START} activeEnd={EXHALE_START + EXHALE_DURATION} activeStart2={EXHALE_START_2} activeEnd2={EXHALE_END_2} />
      </div>
    </div>
  );
};

// Small indicator dot for the step diagram
const SmallDot: React.FC<{
  color: string;
  label: string;
  t: number;
  activeStart: number;
  activeEnd: number;
  activeStart2: number;
  activeEnd2: number;
}> = ({ color, label, t, activeStart, activeEnd, activeStart2, activeEnd2 }) => {
  const isActive =
    (t >= activeStart && t < activeEnd) ||
    (t >= activeStart2 && t < activeEnd2);

  return (
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          width: 14,
          height: 14,
          borderRadius: "50%",
          border: `2px solid ${color}`,
          background: isActive ? color : "transparent",
          margin: "0 auto",
          transition: "background 0.2s",
        }}
      />
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 14,
          color: isActive ? color : DIM,
          marginTop: 4,
          letterSpacing: 1,
        }}
      >
        {label}
      </div>
    </div>
  );
};

// ── "Try it now" text between cycles ───────────────────────
const TryItText: React.FC = () => {
  const t = useTime();

  const opacity = interpolate(
    t,
    [REST_START + 0.2, REST_START + 0.8, CYCLE2_OFFSET - 0.3, CYCLE2_OFFSET],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        position: "absolute",
        top: "72%",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity,
      }}
    >
      <div
        style={{
          fontFamily:
            "HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 32,
          color: OFF_WHITE,
          letterSpacing: 2,
        }}
      >
        now try it with me
      </div>
    </div>
  );
};

// ── Outro ──────────────────────────────────────────────────
const Outro: React.FC = () => {
  const t = useTime();

  const opacity = interpolate(t, [OUTRO_START + 0.5, OUTRO_START + 1.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "35%",
        left: "50%",
        transform: "translateX(-50%)",
        textAlign: "center",
        opacity,
        width: "80%",
      }}
    >
      <div
        style={{
          fontFamily:
            "HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 44,
          color: OFF_WHITE,
          lineHeight: 1.5,
          letterSpacing: 1,
        }}
      >
        your nervous system just got a reset.
      </div>
      <div
        style={{
          fontFamily:
            "HelveticaNeue-Light, Helvetica Neue Light, Helvetica Neue, Helvetica, Arial, sans-serif",
          fontSize: 28,
          color: DIM,
          marginTop: 30,
          letterSpacing: 2,
        }}
      >
        save this for when you need it.
      </div>
    </div>
  );
};

// ── Footer ─────────────────────────────────────────────────
const Footer: React.FC = () => {
  const t = useTime();
  const opacity = interpolate(t, [1, 2], [0, 0.7], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 80,
        left: "50%",
        transform: "translateX(-50%)",
        fontFamily:
          "HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
        fontSize: 24,
        color: DIM,
        opacity,
        letterSpacing: 2,
      }}
    >
      @luminouspulse.co
    </div>
  );
};

// ── Main composition ───────────────────────────────────────
export const PhysiologicalSigh: React.FC = () => {
  return (
    <AbsoluteFill>
      <RadialBg />
      <GrainOverlay />
      <TitleText />
      <Header />
      <BreathCircle />
      <PhaseLabel />
      <StepIndicator />
      <TryItText />
      <Outro />
      <Footer />
    </AbsoluteFill>
  );
};

import React from "react";
import { Composition } from "remotion";
import { GroundingWord } from "./templates/GroundingWord";
import { QuoteCard } from "./templates/QuoteCard";
import { BreathExercise } from "./templates/BreathExercise";
import { PermissionSlip } from "./templates/PermissionSlip";

// Default props for Remotion Studio preview
const defaultProps = {
  word: "steady",
  text: "the part of you that loves cannot be automated.",
  backgroundSrc: "",
  accentColor: "#F4C430",
  accentWords: ["loves"],
  cta: "save this for when you need it.",
  patternName: "physiological-sigh" as const,
  cycles: 2,
  title: "",
  subtitle: "",
  outro: "your nervous system just got a reset.",
  subtext: "say it out loud. say it again. let it settle.",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ── Grounding Word (Story) ── */}
      <Composition
        id="GroundingWord"
        component={GroundingWord}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          word: defaultProps.word,
          backgroundSrc: defaultProps.backgroundSrc,
          accentColor: defaultProps.accentColor,
          subtext: defaultProps.subtext,
        }}
      />

      {/* ── Quote Card (Story) ── */}
      <Composition
        id="QuoteCardStory"
        component={QuoteCard}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          text: defaultProps.text,
          backgroundSrc: defaultProps.backgroundSrc,
          accentColor: defaultProps.accentColor,
          accentWords: defaultProps.accentWords,
          cta: defaultProps.cta,
        }}
      />

      {/* ── Quote Card (Feed 4:5) ── */}
      <Composition
        id="QuoteCardFeed"
        component={QuoteCard}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1350}
        defaultProps={{
          text: defaultProps.text,
          backgroundSrc: defaultProps.backgroundSrc,
          accentColor: defaultProps.accentColor,
          accentWords: defaultProps.accentWords,
          cta: defaultProps.cta,
        }}
      />

      {/* ── Breathing Exercise (Story) ── */}
      <Composition
        id="BreathExercise"
        component={BreathExercise}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          patternName: defaultProps.patternName,
          title: defaultProps.title,
          subtitle: defaultProps.subtitle,
          backgroundSrc: defaultProps.backgroundSrc,
          accentColor: defaultProps.accentColor,
          cycles: defaultProps.cycles,
          outro: defaultProps.outro,
        }}
      />

      {/* ── Permission Slip (Story) ── */}
      <Composition
        id="PermissionSlip"
        component={PermissionSlip}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          text: "you have permission to not apply to a single job today.",
          backgroundSrc: defaultProps.backgroundSrc,
          accentColor: "#B4A7D6",
        }}
      />
    </>
  );
};

import { AbsoluteFill, Sequence, useCurrentFrame, Audio as RemotionAudio, staticFile } from "remotion";
import { Character } from "./components/effects/Character";
import { lyrics } from "./data/lyrics";
import { LyricsDisplay } from "./components/effects/LyricsDisplay";
import { ExplosiveLyrics } from "./components/effects/ExplosiveLyrics";
import { Stamp } from "./components/effects/Stamp";
import { Sparkles } from "./components/effects/Sparkles";

const audioFiles = [
  "01_secret.mp3",
  "02_jimiko.mp3",
  "03_really.mp3",
  "04_noway.mp3",
  "05_awakening.mp3",
  "06_beautiful.mp3",
  "07_strongest.mp3"
];

export const MyComposition = () => {
  const frame = useCurrentFrame();

  // クライマックス判定（最初の8秒以降ずっとクライマックス的な扱いに）
  const isClimax = frame > 240;

  // Switch image based on climax state
  let currentImage = "images/jimiko_final.png";
  if (frame > 345) {
    currentImage = "images/jimiko_climax_2.jpg";
  } else if (isClimax) {
    currentImage = "images/jimiko_intimate.png";
  }

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <RemotionAudio
        src={staticFile("audio/ori_audio_other.wav")}
        volume={1.0}
      />
      {/* <BulletTraces /> */}

      {/* Sparkles (Now throughout the 120s video) */}
      <Sparkles count={120} />

      <Character
        imageSrc={currentImage} // Dynamic image source
        isBreathing={true}
        isShakingHips={!isClimax}
        isClimax={isClimax}
      />

      {/* Stylish Vignette Overlay */}
      <AbsoluteFill
        style={{
          background: "radial-gradient(circle, transparent 40%, rgba(0,0,0,0.4) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* <FeatherBackground /> */}

      {lyrics.map((line, index) => {
        const startFrame = Math.round(line.time * 30);
        const durationInFrames = Math.round(line.duration * 30);
        // Ensure we don't exceed the lyric array if it's shorter than the song
        if (index >= audioFiles.length) return null;

        return (
          <Sequence from={startFrame} durationInFrames={durationInFrames} key={index}>
            <RemotionAudio src={staticFile(`voices/${audioFiles[index]}`)} />
            {line.effect === "explosive" ? (
              <ExplosiveLyrics text={line.text} />
            ) : line.effect === "stamp" ? (
              <Stamp text={line.text} />
            ) : (
              <LyricsDisplay line={line} />
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

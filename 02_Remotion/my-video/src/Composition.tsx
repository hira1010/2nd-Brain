import {
  AbsoluteFill,
  Img,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Audio,
  staticFile,
} from "remotion";

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const globalOpacity = interpolate(
    frame,
    [0, 30, durationInFrames - 60, durationInFrames],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  return (
    <AbsoluteFill className="bg-black text-white font-sans overflow-hidden" style={{ opacity: globalOpacity }}>
      <Audio src={staticFile("audio/Velvet_Hour.mp3")} volume={1} />
      <MainImage />
      <Particles />
      <TypographyOverlay />
      <Letterbox />
      <BeatSync />
    </AbsoluteFill>
  );
};

const MainImage = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Slow Ken Burns zoom in over 60 seconds
  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.15]);
  // Slight pan upwards
  const translateY = interpolate(frame, [0, durationInFrames], [20, -20]);

  return (
    <AbsoluteFill className="items-center justify-center bg-black pointer-events-none">
      <Img 
        src={staticFile(`images/main_girl.jpg`)} 
        className="absolute w-[150%] h-[150%] object-cover blur-3xl opacity-30"
        style={{ transform: `scale(1.5)` }}
      />
      <Img 
        src={staticFile(`images/main_girl.jpg`)} 
        className="relative w-full h-full object-contain drop-shadow-2xl"
        style={{
          transform: `scale(${scale}) translateY(${translateY}px)`,
        }}
      />
    </AbsoluteFill>
  );
};

const Particles = () => {
  const frame = useCurrentFrame();
  
  // A simple way to create a few floating particles using pseudo-random logic
  const particles = Array.from({ length: 30 }).map((_, i) => {
    const seed = i * 1234.5;
    const speed = 0.5 + (seed % 2);
    const startX = (seed % 100); // 0 to 100vw
    const startY = 110 + (seed % 50); // Start below screen
    
    const y = startY - (frame * speed) / 10;
    const x = startX + Math.sin(frame / 30 + seed) * 2;
    
    const opacity = interpolate(
      frame % (200 + (seed % 100)),
      [0, 50, 150, 200 + (seed % 100)],
      [0, 0.6, 0.6, 0]
    );

    return (
      <div
        key={i}
        className="absolute rounded-full bg-white blur-[1px]"
        style={{
          left: `${x}vw`,
          top: `${y}vh`,
          width: `${2 + (seed % 4)}px`,
          height: `${2 + (seed % 4)}px`,
          opacity,
          mixBlendMode: 'screen'
        }}
      />
    );
  });

  return <AbsoluteFill className="pointer-events-none z-20">{particles}</AbsoluteFill>;
};

const TypographyOverlay = () => {
  const frame = useCurrentFrame();
  
  // Show only during chorus
  const opacity = interpolate(frame, [900, 930, 1400, 1430], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  
  return (
    <AbsoluteFill className="justify-center items-center pointer-events-none z-30" style={{ opacity }}>
      <div className="border-4 border-white p-6 mix-blend-overlay">
        <h1 className="text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-yellow-400 tracking-[0.2em] uppercase">
          Velvet Hour
        </h1>
      </div>
    </AbsoluteFill>
  );
};

const Letterbox = () => {
  const frame = useCurrentFrame();
  const barHeight = interpolate(frame, [0, 60], [0, 60], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill className="pointer-events-none z-40">
      <div className="absolute top-0 left-0 right-0 bg-black" style={{ height: barHeight }} />
      <div className="absolute bottom-0 left-0 right-0 bg-black" style={{ height: barHeight }} />
    </AbsoluteFill>
  );
};

const BeatSync = () => {
  const frame = useCurrentFrame();
  
  // Only pulse during build-up and chorus
  if (frame < 450 || frame > 1500) return null;
  
  // Faster beat during chorus
  const beatInterval = frame > 900 ? 15 : 30;
  const beat = frame % beatInterval;
  const pulse = interpolate(beat, [0, 2, beatInterval], [0.15, 0, 0]);

  return (
    <AbsoluteFill className="pointer-events-none z-50">
      <div className="absolute inset-0 bg-white" style={{ opacity: pulse, mixBlendMode: 'overlay' }} />
    </AbsoluteFill>
  );
};

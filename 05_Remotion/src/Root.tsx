import "./index.css";
import React from "react";
import { Composition } from "remotion";
import { MyComposition } from "./Composition";
import { ConversationScene } from "./ConversationScene";
import { loadFont as loadRocknRollOne } from "@remotion/google-fonts/RocknRollOne";
// import { loadFont as loadMochiyPopOne } from "@remotion/google-fonts/MochiyPopOne";
// import { loadFont as loadZenMaruGothic } from "@remotion/google-fonts/ZenMaruGothic";
// import { loadFont as loadShipporiMincho } from "@remotion/google-fonts/ShipporiMincho";
// import { loadFont as loadDotGothic16 } from "@remotion/google-fonts/DotGothic16";

// Loading fonts as per guidelines
loadRocknRollOne();
// loadMochiyPopOne();
// loadZenMaruGothic();
// loadShipporiMincho();
// loadDotGothic16();

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyComp"
        component={MyComposition}
        durationInFrames={3600} // 120秒に延長
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ConversationScene"
        component={ConversationScene}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

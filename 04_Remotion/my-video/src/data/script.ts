export type CharacterId = "zundamon" | "metan" | "ryusei";

// アニメーションの型定義
export type AnimationType = "none" | "fadeIn" | "slideUp" | "slideLeft" | "zoomIn" | "bounce";

// ビジュアルの型定義
export interface VisualContent {
  type: "image" | "text" | "none";
  src?: string;
  text?: string;
  fontSize?: number;
  color?: string;
  animation?: AnimationType;
}

// 効果音の型定義
export interface SoundEffect {
  src: string;
  volume?: number;
}

// BGM設定
export interface BGMConfig {
  src: string;
  volume?: number;
  loop?: boolean;
}

// BGM設定（動画全体で使用）
export const bgmConfig: BGMConfig | null = null;

// セリフデータの型定義
export interface ScriptLine {
  id: number;
  character: CharacterId;
  text: string;
  displayText?: string;
  scene: number;
  voiceFile: string;
  durationInFrames: number;
  pauseAfter: number;
  emotion?: "normal" | "happy" | "surprised" | "thinking" | "sad";
  visual?: VisualContent;
  se?: SoundEffect;
}

// シーン定義
export interface SceneInfo {
  id: number;
  title: string;
  background: string;
}

export const scenes: SceneInfo[] = [
  { id: 1, title: "オープニング", background: "gradient" },
  { id: 2, title: "メインコンテンツ", background: "solid" },
  { id: 3, title: "エンディング", background: "gradient" },
];

// このファイルは config/script.yaml から自動生成されます
// 編集する場合は config/script.yaml を編集して npm run sync-script を実行してください
export const scriptData: ScriptLine[] = [
  {
    "id": 1,
    "character": "zundamon",
    "text": "株式投資とわ、単なる金儲けの手段でわありませんなのだ。企業の成長という未来の価値に、自分のお金を託す行為なのだ。",
    "displayText": "株式投資とは、単なる金儲けの手段ではないのだ。\n未来の価値に、自分のお金を託す行為なのだ。",
    "scene": 1,
    "pauseAfter": 15,
    "visual": {
      "type": "image",
      "src": "stock_market_pro_01.png",
      "animation": "fadeIn"
    },
    "voiceFile": "01_zundamon.wav",
    "durationInFrames": 376
  },
  {
    "id": 2,
    "character": "zundamon",
    "text": "多くの人は暴落を恐れますが、真に価値ある企業わ、不況という荒波を超えてさらなる高みへと昇っていくのだ。",
    "displayText": "暴落を恐れる必要わまったくないのだ。\n不況を超えて、さらなる高みへ昇るのだ！",
    "scene": 2,
    "pauseAfter": 15,
    "visual": {
      "type": "image",
      "src": "stock_market_pro_02.png",
      "animation": "fadeIn"
    },
    "voiceFile": "02_zundamon.wav",
    "durationInFrames": 324
  },
  {
    "id": 3,
    "character": "zundamon",
    "text": "数字の向こう側にある本質を見極めること。それこそが、一流の投資家に求められる唯一の素養なのだ。",
    "displayText": "数字の向こうにある本質を見極めるのだ。\nそれこそが、一流の投資家への第一歩なのだ！",
    "scene": 3,
    "pauseAfter": 30,
    "visual": {
      "type": "image",
      "src": "stock_market_pro_03.png",
      "animation": "fadeIn"
    },
    "voiceFile": "03_zundamon.wav",
    "durationInFrames": 318
  }
];

// VOICEVOXスクリプト生成用
export const generateVoicevoxScript = (
  data: ScriptLine[],
  characterSpeakerMap: Record<CharacterId, number>
) => {
  return data.map((line) => ({
    id: line.id,
    character: line.character,
    speakerId: characterSpeakerMap[line.character],
    text: line.text,
    outputFile: line.voiceFile,
  }));
};

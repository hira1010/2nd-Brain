// ===== 型定義 =====

export type Point = { x: number; y: number };

export type MosaicKeyframe = {
  time: number;
  x: number; // 画面幅に対する割合 (0-100)
  y: number; // 画面高さに対する割合 (0-100)
};

export type MosaicTrack = {
  id: string;
  keyframes: MosaicKeyframe[];
  size: number; // モザイクの半径 (0-50、画面短辺に対する%)
};

export type Tool = 'select' | '1point' | '2point';

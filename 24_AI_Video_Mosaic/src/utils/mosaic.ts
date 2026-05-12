import type { MosaicKeyframe } from '../types';

/**
 * キーフレーム配列から指定時刻の位置を線形補間で求める
 */
export function interpolatePosition(
  keyframes: MosaicKeyframe[],
  time: number
): { x: number; y: number } | null {
  if (keyframes.length === 0) return null;

  const sorted = [...keyframes].sort((a, b) => a.time - b.time);

  // 範囲外はクランプ
  if (time <= sorted[0].time) return { x: sorted[0].x, y: sorted[0].y };
  if (time >= sorted[sorted.length - 1].time) {
    const last = sorted[sorted.length - 1];
    return { x: last.x, y: last.y };
  }

  // 前後のキーフレームを見つけて補間
  for (let i = 0; i < sorted.length - 1; i++) {
    const a = sorted[i];
    const b = sorted[i + 1];
    if (time >= a.time && time <= b.time) {
      const t = (time - a.time) / (b.time - a.time);
      return {
        x: a.x + (b.x - a.x) * t,
        y: a.y + (b.y - a.y) * t,
      };
    }
  }
  return null;
}

/**
 * 指定した円形領域にモザイク（ピクセル化）を適用する
 */
export function applyCircularMosaic(
  ctx: CanvasRenderingContext2D,
  cx: number,  // ピクセル座標
  cy: number,
  radius: number,
  blockSize = 16
) {
  const x = Math.max(0, Math.floor(cx - radius));
  const y = Math.max(0, Math.floor(cy - radius));
  const w = Math.min(ctx.canvas.width - x, Math.ceil(radius * 2));
  const h = Math.min(ctx.canvas.height - y, Math.ceil(radius * 2));
  if (w <= 0 || h <= 0) return;

  const img = ctx.getImageData(x, y, w, h);
  const d = img.data;

  // ブロックごとに平均色を計算してピクセル化
  for (let by = 0; by < h; by += blockSize) {
    for (let bx = 0; bx < w; bx += blockSize) {
      let r = 0, g = 0, b = 0, count = 0;
      for (let py = by; py < Math.min(by + blockSize, h); py++) {
        for (let px = bx; px < Math.min(bx + blockSize, w); px++) {
          const i = (py * w + px) * 4;
          r += d[i]; g += d[i + 1]; b += d[i + 2];
          count++;
        }
      }
      r = r / count | 0; g = g / count | 0; b = b / count | 0;
      for (let py = by; py < Math.min(by + blockSize, h); py++) {
        for (let px = bx; px < Math.min(bx + blockSize, w); px++) {
          const i = (py * w + px) * 4;
          d[i] = r; d[i + 1] = g; d[i + 2] = b;
        }
      }
    }
  }
  ctx.putImageData(img, x, y);
}

/** ランダムなIDを生成 */
export const genId = () => Math.random().toString(36).substr(2, 9);

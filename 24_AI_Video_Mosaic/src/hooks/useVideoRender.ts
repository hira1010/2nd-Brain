import { useEffect, useRef } from 'react';
import type { MosaicTrack } from '../types';
import { interpolatePosition, applyCircularMosaic } from '../utils/mosaic';

/**
 * 動画フレームをCanvasに描画し、モザイクを適用し続けるフック
 * useRefで最新のtracksを参照するためループが止まらない設計
 */
export function useVideoRender(
  videoRef: React.RefObject<HTMLVideoElement | null>,
  canvasRef: React.RefObject<HTMLCanvasElement | null>,
  tracks: MosaicTrack[],
  selectedTrackId: string | null,
  videoUrl: string | null
) {
  const tracksRef = useRef(tracks);
  const selectedRef = useRef(selectedTrackId);

  // 最新状態をrefに同期（ループが古い値を使わないように）
  useEffect(() => { tracksRef.current = tracks; }, [tracks]);
  useEffect(() => { selectedRef.current = selectedTrackId; }, [selectedTrackId]);

  useEffect(() => {
    if (!videoUrl) return;
    let active = true;
    let rafId = 0;

    const loop = () => {
      if (!active) return;
      const video = videoRef.current;
      const canvas = canvasRef.current;

      if (video && canvas) {
        const ctx = canvas.getContext('2d', { willReadFrequently: true });

        if (ctx) {
          // 動画が再生可能な状態か確認
          if (video.videoWidth > 0 && video.videoHeight > 0) {
            // canvasサイズを動画に合わせる
            if (canvas.width !== video.videoWidth) canvas.width = video.videoWidth;
            if (canvas.height !== video.videoHeight) canvas.height = video.videoHeight;

            // 動画フレームを描画（失敗しても次フレームで再挑戦）
            try {
              ctx.drawImage(video, 0, 0);
            } catch (_) {
              // 描画できない場合はスキップ
            }

            const t = video.currentTime;
            const cw = canvas.width;
            const ch = canvas.height;
            const shortSide = Math.min(cw, ch);

            // 各トラックにモザイクを適用
            tracksRef.current.forEach(track => {
              const pos = interpolatePosition(track.keyframes, t);
              if (!pos) return;

              const px = (pos.x / 100) * cw;
              const py = (pos.y / 100) * ch;
              const radius = (track.size / 100) * shortSide;

              // 円形クリップ → モザイク
              ctx.save();
              ctx.beginPath();
              ctx.ellipse(px, py, radius, radius, 0, 0, Math.PI * 2);
              ctx.clip();
              applyCircularMosaic(ctx, px, py, radius);
              ctx.restore();

              // 選択中のトラックに枠を表示
              if (track.id === selectedRef.current) {
                ctx.save();
                ctx.strokeStyle = 'rgba(255,255,255,0.85)';
                ctx.lineWidth = 3;
                ctx.setLineDash([6, 4]);
                ctx.beginPath();
                ctx.ellipse(px, py, radius, radius, 0, 0, Math.PI * 2);
                ctx.stroke();
                ctx.restore();
              }
            });
          } else {
            // 動画未ロード中のプレースホルダー
            if (canvas.width < 640) canvas.width = 1280;
            if (canvas.height < 360) canvas.height = 720;
            ctx.fillStyle = '#111827';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#6b7280';
            ctx.font = 'bold 22px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('⏳ 動画を読み込み中...', canvas.width / 2, canvas.height / 2);
          }
        }
      }

      rafId = requestAnimationFrame(loop);
    };

    rafId = requestAnimationFrame(loop);
    return () => { active = false; cancelAnimationFrame(rafId); };
  }, [videoUrl, videoRef, canvasRef]);
}

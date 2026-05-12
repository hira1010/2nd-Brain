import React from 'react';
import { Play, Pause, Video } from 'lucide-react';
import type { Tool, Point } from '../types';

interface VideoCanvasProps {
  videoRef: React.RefObject<HTMLVideoElement | null>;
  canvasRef: React.RefObject<HTMLCanvasElement | null>;
  videoUrl: string | null;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  tool: Tool;
  firstPoint: Point | null;
  onOpenFile: () => void;
  onPlayPause: () => void;
  onSeek: (ratio: number) => void;
  onCanvasClick: (e: React.MouseEvent<HTMLCanvasElement>) => void;
  onCanvasMouseDown: (e: React.MouseEvent<HTMLCanvasElement>) => void;
  onCanvasMouseMove: (e: React.MouseEvent<HTMLCanvasElement>) => void;
  onCanvasMouseUp: () => void;
}

/** ツールに対応するヒントテキスト */
const hintText: Record<Tool, (hasFirst: boolean) => string> = {
  '1point': () => '🎯 隠したい場所をクリック → 動画を進めてまたクリック（繰り返して追跡）',
  '2point': (hasFirst) => hasFirst ? '📍 2点目をクリック（反対側）' : '📍 1点目をクリック（顔の片側）',
  'select': () => '✋ モザイクをドラッグして移動 ｜ AI追跡ONで経路を自動記録',
};

export const VideoCanvas: React.FC<VideoCanvasProps> = ({
  videoRef, canvasRef,
  videoUrl, isPlaying, currentTime, duration,
  tool, firstPoint,
  onOpenFile, onPlayPause, onSeek,
  onCanvasClick, onCanvasMouseDown, onCanvasMouseMove, onCanvasMouseUp,
}) => {
  if (!videoUrl) {
    return (
      <div className="empty-state" onClick={onOpenFile}>
        <Video size={48} className="text-slate-700 mb-4" />
        <p className="text-slate-400 font-bold">クリックして動画を選択</p>
        <p className="text-slate-600 text-sm mt-2">MP4, MOV, WebM など対応</p>
      </div>
    );
  }

  const progressPct = duration ? (currentTime / duration) * 100 : 0;

  return (
    <div className="video-area">
      {/* 操作ガイド */}
      <div className="hint-bar">
        {hintText[tool](!!firstPoint)}
      </div>

      {/* 非表示の動画要素（音声再生のみ担当） */}
      <video
        ref={videoRef}
        src={videoUrl}
        preload="auto"
        style={{ display: 'none' }}
      />

      {/* モザイク適用済みキャンバス */}
      <canvas
        ref={canvasRef}
        className="mosaic-canvas"
        onClick={onCanvasClick}
        onMouseDown={onCanvasMouseDown}
        onMouseMove={onCanvasMouseMove}
        onMouseUp={onCanvasMouseUp}
        onMouseLeave={onCanvasMouseUp}
      />

      {/* 再生コントロール */}
      <div className="playback-bar">
        <button className="play-btn" onClick={onPlayPause}>
          {isPlaying
            ? <Pause size={18} fill="white" />
            : <Play size={18} fill="white" className="ml-0.5" />
          }
        </button>

        <div className="flex flex-col gap-1 flex-1">
          <div className="flex justify-between text-[10px] font-mono text-slate-400">
            <span>{currentTime.toFixed(2)}s</span>
            <span>{duration.toFixed(2)}s</span>
          </div>
          <div
            className="w-full h-2 bg-slate-800 rounded-full cursor-pointer overflow-hidden"
            onClick={e => {
              const r = e.currentTarget.getBoundingClientRect();
              onSeek((e.clientX - r.left) / r.width);
            }}
          >
            <div className="h-full bg-indigo-500 transition-none" style={{ width: `${progressPct}%` }} />
          </div>
        </div>
      </div>
    </div>
  );
};

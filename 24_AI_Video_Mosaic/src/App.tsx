import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Sidebar } from './components/Sidebar';
import { VideoCanvas } from './components/VideoCanvas';
import { Timeline } from './components/Timeline';
import { useVideoRender } from './hooks/useVideoRender';
import { useMosaicTracks } from './hooks/useMosaicTracks';

const App: React.FC = () => {
  // ===== 動画の基本状態 =====
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // ===== モザイクのロジック（カスタムフック） =====
  const mosaic = useMosaicTracks();

  // ===== Canvas描画ループ（カスタムフック） =====
  useVideoRender(videoRef, canvasRef, mosaic.tracks, mosaic.activeId, videoUrl);

  // ===== 動画の時間監視 =====
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const onTime = () => setCurrentTime(video.currentTime);
    const onMeta = () => setDuration(video.duration);
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    video.addEventListener('timeupdate', onTime);
    video.addEventListener('loadedmetadata', onMeta);
    video.addEventListener('play', onPlay);
    video.addEventListener('pause', onPause);
    return () => {
      video.removeEventListener('timeupdate', onTime);
      video.removeEventListener('loadedmetadata', onMeta);
      video.removeEventListener('play', onPlay);
      video.removeEventListener('pause', onPause);
    };
  }, [videoUrl]);

  // ===== ファイル読込 =====
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setVideoUrl(URL.createObjectURL(file));
      mosaic.clearAll();
    }
  };

  const handlePlayPause = useCallback(() => {
    const v = videoRef.current;
    if (!v) return;
    if (isPlaying) v.pause(); else v.play();
  }, [isPlaying]);

  const handleSeek = useCallback((ratio: number) => {
    if (videoRef.current) videoRef.current.currentTime = ratio * duration;
  }, [duration]);

  // ===== Canvas上のマウスイベントをパーセント座標に変換して渡す =====
  const toPercent = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const r = e.currentTarget.getBoundingClientRect();
    return {
      x: ((e.clientX - r.left) / r.width) * 100,
      y: ((e.clientY - r.top) / r.height) * 100,
      t: videoRef.current?.currentTime ?? 0,
    };
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const { x, y, t } = toPercent(e);
    mosaic.handleClick(x, y, t);
  };

  const handleCanvasMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const { x, y, t } = toPercent(e);
    mosaic.handleMouseDown(x, y, t, mosaic.tracks);
  };

  const handleCanvasMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const { x, y, t } = toPercent(e);
    mosaic.handleMouseMove(x, y, t);
  };

  // ===== キーフレームの個別削除（hookに委譲） =====
  const handleDeleteKeyframe = mosaic.deleteKeyframe;

  return (
    <div className="app-container">
      {/* 非表示ファイル入力 */}
      <input
        ref={fileInputRef}
        type="file"
        accept="video/*"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />

      {/* 左サイドバー */}
      <Sidebar
        tool={mosaic.tool}
        onChangeTool={mosaic.changeTool}
        isAutoTracking={mosaic.isAutoTracking}
        onToggleAutoTracking={() => mosaic.setIsAutoTracking(!mosaic.isAutoTracking)}
        tracks={mosaic.tracks}
        activeId={mosaic.activeId}
        onSelectTrack={mosaic.setActiveId}
        onDeleteTrack={mosaic.deleteTrack}
        onNewTrack={mosaic.startNewTrack}
        mosaicSize={mosaic.mosaicSize}
        onSizeChange={mosaic.setMosaicSize}
        onOpenFile={() => fileInputRef.current?.click()}
      />

      {/* 中央 動画エリア */}
      <main className="main-area">
        <VideoCanvas
          videoRef={videoRef}
          canvasRef={canvasRef}
          videoUrl={videoUrl}
          isPlaying={isPlaying}
          currentTime={currentTime}
          duration={duration}
          tool={mosaic.tool}
          firstPoint={mosaic.firstPoint}
          onOpenFile={() => fileInputRef.current?.click()}
          onPlayPause={handlePlayPause}
          onSeek={handleSeek}
          onCanvasClick={handleCanvasClick}
          onCanvasMouseDown={handleCanvasMouseDown}
          onCanvasMouseMove={handleCanvasMouseMove}
          onCanvasMouseUp={mosaic.stopDragging}
        />
      </main>

      {/* 下部タイムライン */}
      {videoUrl && (
        <Timeline
          tracks={mosaic.tracks}
          onSeekTo={t => { if (videoRef.current) videoRef.current.currentTime = t; }}
          onDeleteKeyframe={handleDeleteKeyframe}
          onClearAll={mosaic.clearAll}
        />
      )}
    </div>
  );
};

export default App;

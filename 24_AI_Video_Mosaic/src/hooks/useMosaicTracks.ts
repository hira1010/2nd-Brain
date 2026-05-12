import { useState, useCallback, useRef } from 'react';
import type { MosaicTrack, MosaicKeyframe, Tool, Point } from '../types';
import { genId, interpolatePosition } from '../utils/mosaic';

/**
 * モザイクトラックの状態管理ロジックをまとめたフック
 *
 * ドラッグ判定には useRef を使う。
 * useState だと「マウスダウン直後の最初のMouseMove」では
 * 更新前の値（null）が見えてしまいドラッグが始まらないバグを防ぐため。
 */
export function useMosaicTracks() {
  const [tracks, setTracks] = useState<MosaicTrack[]>([]);
  const [activeId, setActiveId] = useState<string>(genId());
  const [mosaicSize, setMosaicSize] = useState(12);
  const [tool, setTool] = useState<Tool>('1point');
  const [firstPoint, setFirstPoint] = useState<Point | null>(null);
  const [isAutoTracking, setIsAutoTracking] = useState(false);

  // ドラッグ中のトラックID（refで即座に更新 → ラグなしにドラッグ開始）
  const draggingIdRef = useRef<string | null>(null);
  // ドラッグが発生したか（クリックイベントとの競合防止）
  const hasDraggedRef = useRef(false);

  /** 新しいトラックにキーフレームを追加（既存なら更新） */
  const addKeyframe = useCallback((x: number, y: number, time: number) => {
    const kf: MosaicKeyframe = { time, x, y };
    setTracks(prev => {
      const idx = prev.findIndex(t => t.id === activeId);
      if (idx !== -1) {
        const arr = [...prev];
        const kfs = [...arr[idx].keyframes];
        const ki = kfs.findIndex(k => Math.abs(k.time - time) < 0.05);
        if (ki !== -1) kfs[ki] = kf; else kfs.push(kf);
        arr[idx] = { ...arr[idx], keyframes: kfs };
        return arr;
      }
      return [...prev, { id: activeId, keyframes: [kf], size: mosaicSize }];
    });
  }, [activeId, mosaicSize]);

  /** キャンバスクリック（ドラッグ後は無視） */
  const handleClick = useCallback((x: number, y: number, time: number) => {
    // ドラッグが起きていたらクリックとして扱わない
    if (hasDraggedRef.current) { hasDraggedRef.current = false; return; }

    if (tool === '1point') {
      addKeyframe(x, y, time);
    } else if (tool === '2point') {
      if (!firstPoint) {
        setFirstPoint({ x, y });
      } else {
        addKeyframe((firstPoint.x + x) / 2, (firstPoint.y + y) / 2, time);
        setFirstPoint(null);
      }
    }
  }, [tool, firstPoint, addKeyframe]);

  /** マウス押下 ― モザイクの上なら即ドラッグ開始（refで即時反映） */
  const handleMouseDown = useCallback((x: number, y: number, time: number, tracksSnapshot: MosaicTrack[]) => {
    hasDraggedRef.current = false;
    const hit = tracksSnapshot.find(tr => {
      const pos = interpolatePosition(tr.keyframes, time);
      if (!pos) return false;
      return Math.sqrt((pos.x - x) ** 2 + (pos.y - y) ** 2) < 15;
    });
    if (hit) {
      draggingIdRef.current = hit.id;
      setActiveId(hit.id);
    }
  }, []);

  /** マウス移動 ― refを使ってラグなしでドラッグ */
  const handleMouseMove = useCallback((x: number, y: number, time: number) => {
    if (!draggingIdRef.current) return;
    hasDraggedRef.current = true;
    const id = draggingIdRef.current;

    setTracks(prev => prev.map(tr => {
      if (tr.id !== id) return tr;
      const kfs = [...tr.keyframes];
      if (isAutoTracking) {
        const kf: MosaicKeyframe = { time, x, y };
        const ki = kfs.findIndex(k => Math.abs(k.time - time) < 0.05);
        if (ki !== -1) kfs[ki] = kf; else kfs.push(kf);
      } else {
        // 最も時刻が近いキーフレームだけ位置を変える
        const si = kfs.reduce((best, _k, i) =>
          Math.abs(kfs[i].time - time) < Math.abs(kfs[best].time - time) ? i : best, 0);
        kfs[si] = { ...kfs[si], x, y };
      }
      return { ...tr, keyframes: kfs };
    }));
  }, [isAutoTracking]);

  const stopDragging = useCallback(() => {
    draggingIdRef.current = null;
  }, []);

  const deleteTrack = useCallback((id: string) => {
    setTracks(prev => prev.filter(t => t.id !== id));
    if (activeId === id) setActiveId(genId());
  }, [activeId]);

  /** キーフレーム単体を削除（最後の1点なら全トラック削除） */
  const deleteKeyframe = useCallback((trackId: string, keyframeIndex: number) => {
    setTracks(prev => {
      const idx = prev.findIndex(t => t.id === trackId);
      if (idx === -1) return prev;
      const newKfs = prev[idx].keyframes.filter((_, i) => i !== keyframeIndex);
      if (newKfs.length === 0) {
        // キーフレームが0になったらトラックごと削除
        return prev.filter(t => t.id !== trackId);
      }
      const arr = [...prev];
      arr[idx] = { ...arr[idx], keyframes: newKfs };
      return arr;
    });
  }, []);

  const clearAll = useCallback(() => setTracks([]), []);

  const startNewTrack = useCallback(() => {
    setActiveId(genId());
    setTool('1point');
  }, []);

  const changeTool = useCallback((t: Tool) => {
    setTool(t);
    setFirstPoint(null);
  }, []);

  return {
    tracks, activeId, setActiveId,
    mosaicSize, setMosaicSize,
    tool, changeTool,
    firstPoint,
    isAutoTracking, setIsAutoTracking,
    handleClick, handleMouseDown, handleMouseMove, stopDragging,
    deleteTrack, deleteKeyframe, clearAll, startNewTrack,
  };
}

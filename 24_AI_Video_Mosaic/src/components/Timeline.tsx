import React from 'react';
import { Clock, Trash2, Settings2 } from 'lucide-react';
import { motion } from 'framer-motion';
import type { MosaicTrack } from '../types';

interface TimelineProps {
  tracks: MosaicTrack[];
  onSeekTo: (time: number) => void;
  onDeleteKeyframe: (trackId: string, timeIndex: number) => void;
  onClearAll: () => void;
}

export const Timeline: React.FC<TimelineProps> = ({
  tracks, onSeekTo, onDeleteKeyframe, onClearAll,
}) => {
  // 全トラックのキーフレームを時刻順に並べて表示
  const allKeyframes = tracks.flatMap(tr =>
    tr.keyframes.map((kf, ki) => ({ ...kf, trackId: tr.id, ki, size: tr.size }))
  ).sort((a, b) => a.time - b.time);

  return (
    <footer className="timeline">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Clock size={13} className="text-indigo-400" />
          <span className="text-xs font-bold uppercase tracking-wider">タイムライン（クリックでジャンプ）</span>
        </div>
        <button
          className="text-[10px] bg-slate-800 hover:bg-red-900/50 px-3 py-1 rounded transition-colors"
          onClick={onClearAll}
        >
          全消去
        </button>
      </div>

      <div className="flex gap-3 overflow-x-auto pb-1">
        {allKeyframes.length === 0 ? (
          <div className="w-full h-12 border-2 border-dashed border-slate-800 rounded-xl flex items-center justify-center text-slate-600 text-xs">
            動画上をクリックしてモザイクを追加
          </div>
        ) : (
          allKeyframes.map((kf, i) => (
            <motion.div
              key={`${kf.trackId}-${kf.ki}`}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.03 }}
              className="flex-shrink-0 w-32 premium-card !p-3 border-l-4 cursor-pointer hover:brightness-125"
              style={{ borderLeftColor: '#6366f1' }}
              onClick={() => onSeekTo(kf.time)}
            >
              <div className="flex justify-between items-start mb-1">
                <p className="text-sm font-mono font-bold">{kf.time.toFixed(2)}s</p>
                <button
                  onClick={e => { e.stopPropagation(); onDeleteKeyframe(kf.trackId, kf.ki); }}
                  className="text-slate-600 hover:text-red-400 p-0.5"
                >
                  <Trash2 size={10} />
                </button>
              </div>
              <p className="text-[10px] text-slate-500 flex items-center gap-1">
                <Settings2 size={9} /> {kf.size}%
              </p>
            </motion.div>
          ))
        )}
      </div>
    </footer>
  );
};

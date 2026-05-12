import React from 'react';
import { Plus, CircleDot, MoveHorizontal, MousePointer2, Trash2, Video, Settings2 } from 'lucide-react';
import type { MosaicTrack, Tool } from '../types';

interface SidebarProps {
  tool: Tool;
  onChangeTool: (t: Tool) => void;
  isAutoTracking: boolean;
  onToggleAutoTracking: () => void;
  tracks: MosaicTrack[];
  activeId: string;
  onSelectTrack: (id: string) => void;
  onDeleteTrack: (id: string) => void;
  onNewTrack: () => void;
  mosaicSize: number;
  onSizeChange: (v: number) => void;
  onOpenFile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  tool, onChangeTool,
  isAutoTracking, onToggleAutoTracking,
  tracks, activeId, onSelectTrack, onDeleteTrack, onNewTrack,
  mosaicSize, onSizeChange,
  onOpenFile,
}) => {
  const toolButtons: { id: Tool; icon: React.ReactNode; label: string }[] = [
    { id: '1point', icon: <CircleDot size={15} />, label: '1点追跡（クリック1回）' },
    { id: '2point', icon: <MoveHorizontal size={15} />, label: '2点追跡（中心を自動計算）' },
    { id: 'select', icon: <MousePointer2 size={15} />, label: '選択・移動' },
  ];

  return (
    <aside className="sidebar">
      {/* ヘッダー */}
      <div className="sidebar-header">
        <Video size={18} className="text-indigo-400" />
        <span className="font-bold text-sm">AIモザイクエディター</span>
      </div>

      {/* ファイル読込 */}
      <button
        className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all"
        onClick={onOpenFile}
      >
        <Plus size={16} /> 動画を読み込む
      </button>

      {/* 追跡モード */}
      <section>
        <p className="section-label">追跡モード</p>
        <div className="flex flex-col gap-2">
          {toolButtons.map(t => (
            <button
              key={t.id}
              className={`tool-button ${tool === t.id ? 'active' : ''}`}
              onClick={() => onChangeTool(t.id)}
            >
              {t.icon} {t.label}
            </button>
          ))}
        </div>
      </section>

      {/* AI自動追跡トグル */}
      <div
        className={`flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all ${isAutoTracking ? 'bg-emerald-500/10 border-emerald-500/50' : 'bg-slate-800/50 border-slate-700'}`}
        onClick={onToggleAutoTracking}
      >
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isAutoTracking ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`} />
          <span className="text-xs font-bold">AI自動追跡モード</span>
        </div>
        <div className={`w-8 h-4 rounded-full relative transition-colors ${isAutoTracking ? 'bg-emerald-500' : 'bg-slate-700'}`}>
          <div className={`absolute top-1 w-2 h-2 bg-white rounded-full transition-all ${isAutoTracking ? 'left-5' : 'left-1'}`} />
        </div>
      </div>

      {/* モザイク管理 */}
      <section>
        <p className="section-label">モザイク管理</p>
        <button
          className="w-full py-2 mb-2 bg-slate-700 hover:bg-slate-600 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all"
          onClick={onNewTrack}
        >
          <Plus size={12} /> 別のモザイクを追加
        </button>
        <div className="flex flex-col gap-2 max-h-48 overflow-y-auto">
          {tracks.map((tr, i) => (
            <div
              key={tr.id}
              onClick={() => onSelectTrack(tr.id)}
              className={`flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all ${activeId === tr.id ? 'bg-indigo-600/20 border-indigo-500' : 'bg-slate-800/30 border-slate-700'}`}
            >
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${activeId === tr.id ? 'bg-indigo-400' : 'bg-slate-600'}`} />
                <span className="text-xs font-bold">モザイク #{i + 1}</span>
                <span className="text-[10px] text-slate-500">{tr.keyframes.length}点</span>
              </div>
              <button
                onClick={e => { e.stopPropagation(); onDeleteTrack(tr.id); }}
                className="text-slate-500 hover:text-red-400 p-1"
              >
                <Trash2 size={12} />
              </button>
            </div>
          ))}
          {tracks.length === 0 && (
            <div className="text-[10px] text-slate-600 italic text-center py-4 border border-dashed border-slate-800 rounded-xl">
              まだモザイクがありません
            </div>
          )}
        </div>
      </section>

      {/* 詳細設定 */}
      <section>
        <p className="section-label">詳細設定</p>
        <div className="premium-card">
          <div className="flex justify-between mb-2">
            <span className="text-xs text-slate-400 flex items-center gap-1"><Settings2 size={11} /> モザイクサイズ</span>
            <span className="text-xs font-mono">{mosaicSize}%</span>
          </div>
          <input
            type="range" min="3" max="40" value={mosaicSize}
            onChange={e => onSizeChange(parseInt(e.target.value))}
            className="w-full h-1 bg-slate-700 rounded appearance-none cursor-pointer accent-indigo-500"
          />
        </div>
      </section>
    </aside>
  );
};

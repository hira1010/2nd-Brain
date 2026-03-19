import { useCurrentFrame, useVideoConfig, Img, interpolate, spring, staticFile, Audio } from 'remotion';
import React from 'react';

export const JimiPV: React.FC = () => {
    const frame = useCurrentFrame();
    const { fps, durationInFrames, width, height } = useVideoConfig();

    // 進行率 (0〜1)
    const progress = frame / durationInFrames;

    // Ken Burns効果: ズームとパン
    const zoom = interpolate(frame, [0, durationInFrames], [1, 1.3], {
        extrapolateRight: 'clamp',
    });

    const panX = Math.sin(progress * Math.PI * 2) * 50;
    const panY = progress * 100;

    // カラーオーバーレイの透明度
    const overlayOpacity = interpolate(
        frame,
        [0, durationInFrames / 3, durationInFrames * 2 / 3, durationInFrames],
        [0.1, 0.08, 0.12, 0.1]
    );

    // カラートーン（時間経過で変化）
    let overlayColor;
    if (progress < 0.33) {
        overlayColor = 'rgba(255, 200, 150, 0.1)'; // ウォーム
    } else if (progress < 0.66) {
        overlayColor = 'rgba(120, 160, 200, 0.08)'; // ティール
    } else {
        overlayColor = 'rgba(255, 180, 200, 0.12)'; // ピンク
    }

    // タイトルアニメーション
    const titleOpacity = interpolate(
        frame,
        [0, 30, 150, 180],
        [0, 1, 1, 0],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );

    const titleScale = spring({
        frame: frame - 10,
        fps,
        config: {
            damping: 100,
            stiffness: 200,
            mass: 0.5,
        },
    });

    return (
        <div style={{
            width,
            height,
            backgroundColor: '#000',
            position: 'relative',
            overflow: 'hidden',
        }}>
            {/* BGM: Pythonで自動生成したアンビエント音楽 */}
            <Audio src={staticFile('bgm.wav')} volume={0.5} />

            {/* 画像レイヤー */}
            <div style={{
                width: '100%',
                height: '100%',
                transform: `scale(${zoom}) translate(${panX}px, ${-panY}px)`,
                transformOrigin: 'center center',
            }}>
                <Img
                    src={staticFile('jimi_source.jpg')}
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                    }}
                />
            </div>

            {/* カラーオーバーレイ */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                backgroundColor: overlayColor,
                pointerEvents: 'none',
            }} />

            {/* ビネット効果 */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 0%, rgba(0,0,0,0.6) 100%)',
                pointerEvents: 'none',
            }} />

            {/* タイトル */}
            <div style={{
                position: 'absolute',
                bottom: 80,
                left: '50%',
                transform: `translateX(-50%) scale(${titleScale})`,
                color: 'white',
                fontSize: 64,
                fontWeight: 'bold',
                textShadow: '0 4px 20px rgba(0,0,0,0.8)',
                opacity: titleOpacity,
                fontFamily: 'Arial, sans-serif',
                letterSpacing: '8px',
            }}>
                地味子
            </div>

            {/* クレジット */}
            <div style={{
                position: 'absolute',
                bottom: 20,
                right: 30,
                color: 'rgba(255,255,255,0.7)',
                fontSize: 14,
                textShadow: '0 2px 10px rgba(0,0,0,0.8)',
                opacity: interpolate(frame, [durationInFrames - 120, durationInFrames - 60], [0, 1], {
                    extrapolateLeft: 'clamp',
                    extrapolateRight: 'clamp',
                }),
            }}>
                Presented by Remi Investment
            </div>
        </div>
    );
};


import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from 'remotion';

// Character Component with Lip Sync
const SpeakingCharacter: React.FC<{
    side: 'left' | 'right';
    imageSrcClosed: string; // 口閉じ（通常）
    imageSrcOpen?: string;  // 口開け（差分があれば）
    isSpeaking?: boolean;
}> = ({ side, imageSrcClosed, imageSrcOpen, isSpeaking = false }) => {
    const frame = useCurrentFrame();

    // Lip Sync Logic
    // 6フレームごとに口を開閉する (少しゆっくりに)
    const lipState = isSpeaking && imageSrcOpen
        ? (Math.floor(frame / 6) % 2 === 0 ? 'open' : 'closed')
        : 'closed';

    const currentImage = lipState === 'open' && imageSrcOpen ? imageSrcOpen : imageSrcClosed;

    // Simple "breathe" animation
    const breathe = Math.sin(frame * 0.05) * 5;

    const style: React.CSSProperties = {
        position: 'absolute',
        bottom: 0, // 底辺に合わせる
        [side]: -50, // 少し画面端に寄せる
        width: 800, // サイズ倍増
        height: 800, // サイズ倍増
        objectFit: 'contain',
        transform: `translateY(${breathe}px) ${side === 'right' ? 'scaleX(-1)' : ''}`, // Flip right character
        filter: isSpeaking ? 'brightness(1.1) drop-shadow(0 0 10px rgba(255,255,255,0.5))' : 'brightness(0.6)', // 話してない方は暗くする
        transition: 'filter 0.2s',
        zIndex: 10,
    };

    return <Img src={currentImage} style={style} />;
};

// Subtitle Component
const Subtitle: React.FC<{ text: string }> = ({ text }) => {
    return (
        <div
            style={{
                position: 'absolute',
                bottom: 30,
                left: 0,
                right: 0,
                textAlign: 'center',
                padding: '20px',
            }}
        >
            <h2
                style={{
                    fontFamily: '"RocknRoll One", sans-serif',
                    fontSize: 50,
                    color: 'white',
                    textShadow: '0px 0px 10px rgba(0,0,0,0.8), 4px 4px 0px rgba(0,0,0,1)',
                    margin: 0,
                    background: 'rgba(0,0,0,0.5)',
                    display: 'inline-block',
                    padding: '10px 40px',
                    borderRadius: 50,
                }}
            >
                {text}
            </h2>
        </div>
    );
};

// Screen/Content Component
const ScreenShare: React.FC = () => {
    return (
        <div style={{
            position: 'absolute',
            top: 50,
            left: '50%',
            transform: 'translateX(-50%)',
            width: '80%',
            height: '60%',
            backgroundColor: 'white',
            borderRadius: 20,
            boxShadow: '0 10px 50px rgba(0,0,0,0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            overflow: 'hidden'
        }}>
            {/* Dummy Terminal Content */}
            <div style={{ width: '100%', height: '100%', padding: 40, fontFamily: 'monospace', fontSize: 24, boxSizing: 'border-box', color: '#333' }}>
                <div style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
                    <span style={{ width: 15, height: 15, borderRadius: '50%', background: '#ff5f56' }}></span>
                    <span style={{ width: 15, height: 15, borderRadius: '50%', background: '#ffbd2e' }}></span>
                    <span style={{ width: 15, height: 15, borderRadius: '50%', background: '#27c93f' }}></span>
                </div>
                <div>~ $ npx skills add remotion-dev<span className="cursor">_</span></div>
            </div>
        </div>
    )
}

export const ConversationScene: React.FC = () => {
    // --- Stock Investment Dialogue Script ---
    const dialogues = [
        {
            character: 'remi',
            text: "優斗、あなたまだ貯金なんてしてるの？ これからは『株式投資』の時代よ。",
            duration: 120
        },
        {
            character: 'yuto',
            text: "ええっ！？ か、株ですか！？ 暴落して借金背負うのが怖いです…！",
            duration: 120
        },
        {
            character: 'remi',
            text: "フフッ、貧弱な発想ね。リスクを管理してこそ、巨万の富は得られるの。",
            duration: 120
        },
        {
            character: 'yuto',
            text: "さすがレミさん…！ 僕にもその極意、教えてください！",
            duration: 90
        }
    ];

    // Calculate current dialogue based on frame
    const frame = useCurrentFrame();
    let currentDialogueIndex = 0;
    let accumulatedFrames = 0;

    for (let i = 0; i < dialogues.length; i++) {
        accumulatedFrames += dialogues[i].duration;
        if (frame < accumulatedFrames) {
            currentDialogueIndex = i;
            break;
        }
        // If frame exceeds total duration, keep showing the last one (or stop)
        if (i === dialogues.length - 1) currentDialogueIndex = i;
    }

    const currentLine = dialogues[currentDialogueIndex];
    const isRemiSpeaking = currentLine.character === 'remi';
    const isYutoSpeaking = currentLine.character === 'yuto';

    // Updated image paths
    const remiClosed = staticFile("images/remi_close.png");
    const remiOpen = staticFile("images/remi_open.png");

    const yutoClosed = staticFile("images/yuto_close.png");
    const yutoOpen = staticFile("images/yuto_open.png");

    return (
        <AbsoluteFill style={{ backgroundColor: '#2d3436' }}>

            {/* Background decoration */}
            <AbsoluteFill style={{ background: 'linear-gradient(135deg, #2d3436 0%, #000000 100%)' }} />

            {/* Center Screen */}
            <ScreenShare />

            {/* Characters */}
            {/* Left: Remi */}
            <SpeakingCharacter
                side="left"
                imageSrcClosed={remiClosed}
                imageSrcOpen={remiOpen}
                isSpeaking={isRemiSpeaking}
            />

            {/* Right: Yuto */}
            <SpeakingCharacter
                side="right"
                imageSrcClosed={yutoClosed}
                imageSrcOpen={yutoOpen}
                isSpeaking={isYutoSpeaking}
            />

            {/* Subtitles */}
            <Subtitle text={currentLine.text} />

        </AbsoluteFill>
    );
};

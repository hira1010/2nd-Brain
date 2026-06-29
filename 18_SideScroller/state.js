export const state = {
    isGameOver: false,
    score: 0,
    frameCount: 0,
    sp: 0,
    maxSp: 100,
    currentStage: 1,
    stageThresholds: [100, 300, 600, 1000], // Stage 5 はスコアではなくボス討伐でクリア
    keys: { ArrowLeft: false, ArrowRight: false, Space: false, KeyZ: false, ArrowUp: false }
};

export const assets = {
    playerImg: null,
    enemyImg: null,
    itemImg: null
};

// オブジェクトのリストを保持
export const gameObjects = {
    enemies: [],
    items: [],
    platforms: [],
    boss: null
};

// UI要素の取得
export const ui = {
    hpFill: () => document.getElementById('hp-fill'),
    spFill: () => document.getElementById('sp-fill'),
    spHint: () => document.getElementById('sp-hint'),
    scoreDisplay: () => document.getElementById('score'),
    gameOverScreen: () => document.getElementById('game-over-screen'),
    finalScoreDisplay: () => document.getElementById('final-score'),
    stageDisplay: () => document.getElementById('stage-display'),
    stageClearScreen: () => document.getElementById('stage-clear-screen'),
    stageClearText: () => document.getElementById('stage-clear-text')
};

export const getCanvas = () => document.getElementById('gameCanvas');
export const getCtx = () => getCanvas().getContext('2d');

const character = document.getElementById('character');
const container = document.getElementById('game-container');

// 初期位置
let posX = 300 - 24;
let posY = 200 - 24;
const speed = 3;

// スプライトの行と列の設定 (1コマ 48x48)
// 行: 0=前, 1=左, 2=右, 3=後ろ
const directions = {
    'ArrowDown': { row: 0, dx: 0, dy: 1 },
    's': { row: 0, dx: 0, dy: 1 },
    'ArrowLeft': { row: 1, dx: -1, dy: 0 },
    'a': { row: 1, dx: -1, dy: 0 },
    'ArrowRight': { row: 2, dx: 1, dy: 0 },
    'd': { row: 2, dx: 1, dy: 0 },
    'ArrowUp': { row: 3, dx: 0, dy: -1 },
    'w': { row: 3, dx: 0, dy: -1 }
};

let currentRow = 0;
let currentFrame = 1; // 0=左足, 1=直立(止まる), 2=右足
let isMoving = false;
let moveInterval = null;
let animationInterval = null;
let currentKey = null;

const keys = {};

window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if (directions[e.key] && currentKey !== e.key) {
        currentKey = e.key;
        startMoving(e.key);
    }
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
    if (e.key === currentKey) {
        // 現在押されているキーが離されたら、他に押されている方向キーを探す
        currentKey = Object.keys(keys).find(k => keys[k] && directions[k]) || null;
        if (currentKey) {
            startMoving(currentKey);
        } else {
            stopMoving();
        }
    }
});

function startMoving(key) {
    clearInterval(moveInterval);
    clearInterval(animationInterval);
    
    currentRow = directions[key].row;
    isMoving = true;
    
    moveInterval = setInterval(() => moveCharacter(key), 1000 / 60); // 60FPSで移動
    
    // アニメーション (0 -> 1 -> 2 -> 1 の繰り返し)
    let animStep = 0;
    const frames = [0, 1, 2, 1];
    animationInterval = setInterval(() => {
        currentFrame = frames[animStep];
        updateSprite();
        animStep = (animStep + 1) % 4;
    }, 150); // 歩く早さ
}

function stopMoving() {
    isMoving = false;
    clearInterval(moveInterval);
    clearInterval(animationInterval);
    currentFrame = 1; // 止まるポーズに戻す
    updateSprite();
}

function moveCharacter(key) {
    const dir = directions[key];
    posX += dir.dx * speed;
    posY += dir.dy * speed;
    
    // 画面外に出ないように制限
    posX = Math.max(0, Math.min(container.clientWidth - 48, posX));
    posY = Math.max(0, Math.min(container.clientHeight - 48, posY));
    
    character.style.left = posX + 'px';
    character.style.top = posY + 'px';
}

function updateSprite() {
    const xOffset = -(currentFrame * 48);
    const yOffset = -(currentRow * 48);
    character.style.backgroundPosition = `${xOffset}px ${yOffset}px`;
}

// 初期化
character.style.left = posX + 'px';
character.style.top = posY + 'px';
updateSprite();

import { state, assets, gameObjects, ui, getCanvas, getCtx } from './state.js';
import { loadImage, checkCollision } from './utils.js';
import { player, Enemy, Boss, Platform, spawnItem } from './entities.js';
import { initThreeJS, updateThreeJS } from './three_bg.js';

// キー入力リスナー
window.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') state.keys.ArrowLeft = true;
    if (e.code === 'ArrowRight') state.keys.ArrowRight = true;
    if (e.code === 'ArrowUp') state.keys.ArrowUp = true;
    if (e.code === 'Space' || e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
        if (!state.keys.Space && !state.isGameOver) player.attack();
        state.keys.Space = true;
    }
    if (e.code === 'KeyZ' || e.key.toLowerCase() === 'z') {
        if (!state.keys.KeyZ && !state.isGameOver && state.sp >= state.maxSp) {
            player.ultimate();
        }
        state.keys.KeyZ = true;
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') state.keys.ArrowLeft = false;
    if (e.code === 'ArrowRight') state.keys.ArrowRight = false;
    if (e.code === 'ArrowUp') state.keys.ArrowUp = false;
    if (e.code === 'Space' || e.code === 'ShiftLeft' || e.code === 'ShiftRight') state.keys.Space = false;
    if (e.code === 'KeyZ' || e.key.toLowerCase() === 'z') state.keys.KeyZ = false;
});

export function checkStageProgress() {
    if (state.currentStage < 5 && state.score >= state.stageThresholds[state.currentStage - 1]) {
        nextStage();
    }
}

function nextStage() {
    state.isGameOver = true;
    state.currentStage++;
    
    const stageDisplay = ui.stageDisplay();
    if (stageDisplay) {
        if (state.currentStage === 5) {
            stageDisplay.innerHTML = `STAGE: 5 / 5 <span id="next-score" style="font-size: 14px; color: #ff0000;">(DEFEAT THE BOSS!!)</span>`;
        } else {
            stageDisplay.innerHTML = `STAGE: ${state.currentStage} / 5 <span id="next-score" style="font-size: 14px; color: #ccc;">(Next: ${state.stageThresholds[state.currentStage - 1]})</span>`;
        }
    }
    
    const screen = ui.stageClearScreen();
    const text = ui.stageClearText();
    if (text) text.innerText = state.currentStage === 5 ? "WARNING! BOSS APPROACHING!" : "STAGE CLEAR!!";
    if (state.currentStage === 5 && text) text.style.color = "red";
    if (screen) screen.classList.remove('hidden');
    
    setTimeout(() => {
        if (screen) screen.classList.add('hidden');
        state.isGameOver = false;
        gameObjects.enemies.length = 0; 
        gameObjects.items.length = 0;
        player.hp = player.maxHp;
        ui.hpFill().style.width = '100%';
        if (state.currentStage === 5) {
            gameObjects.boss = new Boss();
        }
        requestAnimationFrame(gameLoop);
    }, 2000);
}

export function gameClear() {
    state.isGameOver = true;
    const screen = ui.stageClearScreen();
    const text = ui.stageClearText();
    if (text) text.innerText = "GAME CLEAR!!";
    if (screen) screen.classList.remove('hidden');
}

export function gameOver() {
    state.isGameOver = true;
    ui.finalScoreDisplay().innerText = state.score;
    ui.gameOverScreen().classList.remove('hidden');
}

function spawnPlatform() {
    const canvas = getCanvas();
    if (Math.random() < 0.02) {
        gameObjects.platforms.push(new Platform(canvas.width, 180 + Math.random() * 120, 100 + Math.random() * 150));
    }
}

function updateItems() {
    const ctx = getCtx();
    for (let i = gameObjects.items.length - 1; i >= 0; i--) {
        const item = gameObjects.items[i];
        item.x -= 2;
        item.y += item.vy;
        if (item.vy < 5) item.vy += 0.5;
        if (item.y > 350) item.y = 350;
        
        if (assets.itemImg) {
            ctx.drawImage(assets.itemImg, item.x, item.y, 40, 40);
        } else {
            ctx.fillStyle = '#00ffff';
            ctx.beginPath();
            ctx.arc(item.x + 20, item.y + 20, 15, 0, Math.PI*2);
            ctx.fill();
        }
        
        if (item.x + 40 < 0) {
            gameObjects.items.splice(i, 1);
            continue;
        }
        
        const itemRect = { x: item.x, y: item.y, width: 40, height: 40 };
        if (checkCollision(player, itemRect)) {
            player.gainSp(20);
            state.score += 5;
            ui.scoreDisplay().innerText = state.score;
            gameObjects.items.splice(i, 1);
            checkStageProgress();
        }
    }
}

function gameLoop() {
    if (state.isGameOver) return;
    
    const canvas = getCanvas();
    const ctx = getCtx();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    updateThreeJS();
    
    player.update();
    player.draw();
    
    spawnPlatform();
    for (let i = gameObjects.platforms.length - 1; i >= 0; i--) {
        const p = gameObjects.platforms[i];
        p.update();
        p.draw();
        if (p.x + p.width < 0) gameObjects.platforms.splice(i, 1);
    }
    
    updateItems();
    
    if (gameObjects.boss && !gameObjects.boss.isDead) {
        gameObjects.boss.update();
        gameObjects.boss.draw();
        
        if (checkCollision(player, gameObjects.boss)) {
            player.takeDamage(2);
        }
        
        if (Math.random() < 0.05) {
            const minion = new Enemy();
            minion.x = gameObjects.boss.x;
            minion.y = gameObjects.boss.y + gameObjects.boss.height / 2;
            gameObjects.enemies.push(minion);
        }
    }
    
    const spawnRate = gameObjects.boss ? 0.01 : 0.01 + (state.currentStage * 0.005);
    if (Math.random() < spawnRate) {
        gameObjects.enemies.push(new Enemy());
    }
    
    for (let i = gameObjects.enemies.length - 1; i >= 0; i--) {
        const enemy = gameObjects.enemies[i];
        enemy.update();
        enemy.draw();
        
        if (enemy.x + enemy.width < 0) {
            gameObjects.enemies.splice(i, 1);
            continue;
        }
        
        if (checkCollision(player, enemy)) {
            player.takeDamage(15);
            gameObjects.enemies.splice(i, 1);
        }
    }
    
    state.frameCount++;
    requestAnimationFrame(gameLoop);
}

async function init() {
    assets.playerImg = await loadImage('player.png');
    assets.enemyImg = await loadImage('enemy.png');
    assets.itemImg = await loadImage('item_crystal.png');
    
    initThreeJS();
    
    gameLoop();
}

init();

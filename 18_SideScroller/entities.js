import { state, assets, gameObjects, ui, getCanvas, getCtx } from './state.js';
import { checkCollision } from './utils.js';
import { checkStageProgress, gameOver, gameClear } from './main.js';

export function spawnItem(x, y) {
    gameObjects.items.push({ x, y, vy: -5 });
}

export const player = {
    x: 100,
    y: 250,
    width: 120,
    height: 180,
    speed: 5,
    hp: 100,
    maxHp: 100,
    isAttacking: false,
    attackTimer: 0,
    vy: 0,
    gravity: 0.8,
    isJumping: false,
    jumpPower: -15,
    groundY: 250,
    
    update() {
        const canvas = getCanvas();
        if (state.keys.ArrowLeft) this.x -= this.speed;
        if (state.keys.ArrowRight) this.x += this.speed;
        if (this.x < 0) this.x = 0;
        if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;
        
        // ジャンプ処理
        if (state.keys.ArrowUp && !this.isJumping) {
            this.vy = this.jumpPower;
            this.isJumping = true;
        }
        
        this.y += this.vy;
        this.vy += this.gravity;
        
        let landed = false;
        if (this.vy > 0) {
            for (let p of gameObjects.platforms) {
                // 足場との当たり判定
                if (this.x + this.width - 40 > p.x && this.x + 40 < p.x + p.width && 
                    this.y + this.height >= p.y && this.y + this.height - this.vy <= p.y + 15) {
                    this.y = p.y - this.height;
                    this.vy = 0;
                    this.isJumping = false;
                    landed = true;
                    break;
                }
            }
        }
        
        if (!landed && this.y >= this.groundY) {
            this.y = this.groundY;
            this.vy = 0;
            this.isJumping = false;
        }
        
        if (this.isAttacking) {
            this.attackTimer--;
            if (this.attackTimer <= 0) this.isAttacking = false;
        }
    },
    
    attack() {
        if (!this.isAttacking) {
            this.isAttacking = true;
            this.attackTimer = 15;
            
            const attackBox = { x: this.x + this.width, y: this.y + 40, width: 80, height: 100 };
            
            // ボスとの当たり判定
            if (gameObjects.boss && !gameObjects.boss.isDead && checkCollision(attackBox, gameObjects.boss)) {
                gameObjects.boss.takeDamage(20);
                this.gainSp(5);
            }
            
            // 敵との当たり判定
            for (let i = gameObjects.enemies.length - 1; i >= 0; i--) {
                const enemy = gameObjects.enemies[i];
                if (checkCollision(attackBox, enemy)) {
                    state.score += 10;
                    ui.scoreDisplay().innerText = state.score;
                    this.gainSp(10);
                    gameObjects.enemies.splice(i, 1);
                    checkStageProgress();
                }
            }
        }
    },
    
    draw() {
        const ctx = getCtx();
        // 残像（アフターイメージ）の描画
        if (this.isAttacking && assets.playerImg) {
            for (let i = 1; i <= 3; i++) {
                ctx.save();
                ctx.globalAlpha = 0.5 - (i * 0.15); // 徐々に薄く
                const offsetX = this.x - (i * 20); // 過去の位置っぽく
                
                // 傾きも少しずつ戻す
                ctx.translate(offsetX + this.width / 2 + 20, this.y + this.height);
                ctx.rotate((Math.PI / 180) * (15 - i * 5));
                ctx.translate(-(offsetX + this.width / 2), -(this.y + this.height));
                
                ctx.drawImage(assets.playerImg, offsetX, this.y, this.width, this.height);
                ctx.restore();
            }
        }

        // 本体描画
        ctx.save();
        if (this.isAttacking) {
            ctx.translate(this.x + this.width / 2 + 40, this.y + this.height);
            ctx.rotate((Math.PI / 180) * 15);
            ctx.translate(-(this.x + this.width / 2), -(this.y + this.height));
        } else if (!this.isJumping) {
            // 歩行アニメーション (上下に揺らす) 地面にいる時のみ
            if (state.keys.ArrowLeft || state.keys.ArrowRight) {
                this.y = this.groundY + (Math.sin(state.frameCount / 3) * 5); 
            } else {
                this.y = this.groundY;
            }
        }

        if (assets.playerImg) {
            ctx.drawImage(assets.playerImg, this.x, this.y, this.width, this.height);
        } else {
            ctx.fillStyle = '#4a90e2';
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
        ctx.restore();
        
        // 攻撃エフェクト (三日月型の斬撃)
        if (this.isAttacking) {
            const progress = (15 - this.attackTimer) / 15; 
            const radius = 60 + progress * 40;
            ctx.beginPath();
            ctx.arc(this.x + this.width, this.y + this.height / 2, radius, -Math.PI / 3, Math.PI / 3);
            ctx.lineWidth = 15;
            ctx.strokeStyle = `rgba(0, 255, 255, ${1 - progress})`;
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(this.x + this.width, this.y + this.height / 2, radius - 10, -Math.PI / 4, Math.PI / 4);
            ctx.lineWidth = 5;
            ctx.strokeStyle = `rgba(255, 255, 255, ${1 - progress})`;
            ctx.stroke();
        }
    },
    
    takeDamage(amount) {
        const canvas = getCanvas();
        this.hp -= amount;
        if (this.hp <= 0) {
            this.hp = 0;
            gameOver();
        }
        ui.hpFill().style.width = (this.hp / this.maxHp * 100) + '%';
        canvas.style.transform = `translateX(${(Math.random()-0.5)*10}px)`;
        setTimeout(() => canvas.style.transform = 'none', 50);
    },
    
    gainSp(amount) {
        state.sp += amount;
        if (state.sp > state.maxSp) state.sp = state.maxSp;
        ui.spFill().style.width = (state.sp / state.maxSp * 100) + '%';
        if (state.sp === state.maxSp) {
            ui.spHint().style.opacity = '1';
        }
    },
    
    ultimate() {
        const canvas = getCanvas();
        const ctx = getCtx();
        state.sp = 0;
        ui.spFill().style.width = '0%';
        ui.spHint().style.opacity = '0';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        gameObjects.enemies.forEach(enemy => {
            state.score += 30;
            if (Math.random() > 0.5) spawnItem(enemy.x, enemy.y);
        });
        gameObjects.enemies.length = 0;
        ui.scoreDisplay().innerText = state.score;
    }
};

export class Enemy {
    constructor() {
        const canvas = getCanvas();
        this.x = canvas.width;
        this.y = 330;
        this.width = 60;
        this.height = 60;
        
        if (Math.random() > 0.5) {
            this.y = 150 + Math.random() * 150; // 空中敵
        }
        
        if (state.currentStage >= 3) this.type = Math.floor(Math.random() * 3);
        else if (state.currentStage >= 2) this.type = Math.floor(Math.random() * 2);
        else this.type = 0;
        
        this.speed = (3 + Math.random() * 3) + (state.currentStage * 0.5);
        if (this.type === 1) this.speed += 3;
    }
    
    update() {
        this.x -= this.speed;
        if (this.type === 2) {
            this.y = 250 + Math.sin(state.frameCount / 10) * 80;
        }
    }
    
    draw() {
        const ctx = getCtx();
        if (assets.enemyImg) {
            ctx.save();
            if (this.type === 1) ctx.filter = 'hue-rotate(90deg)';
            if (this.type === 2) ctx.filter = 'hue-rotate(180deg)';
            ctx.drawImage(assets.enemyImg, this.x, this.y, this.width, this.height);
            ctx.restore();
        } else {
            ctx.fillStyle = this.type === 1 ? '#ff0000' : '#d0021b';
            ctx.beginPath();
            ctx.arc(this.x + this.width/2, this.y + this.height/2, this.width/2, 0, Math.PI*2);
            ctx.fill();
        }
    }
}

export class Boss {
    constructor() {
        const canvas = getCanvas();
        this.x = canvas.width + 100; // 画面外から登場
        this.y = 100;
        this.width = 250;
        this.height = 250;
        this.hp = 500;
        this.maxHp = 500;
        this.isDead = false;
    }
    
    update() {
        if (this.isDead) return;
        const canvas = getCanvas();
        // 定位置まで移動
        if (this.x > canvas.width - this.width - 20) {
            this.x -= 2;
        }
        // ふわふわ浮かぶ
        this.y = 100 + Math.sin(state.frameCount / 20) * 50;
    }
    
    draw() {
        if (this.isDead) return;
        const ctx = getCtx();
        ctx.save();
        ctx.filter = 'hue-rotate(270deg) contrast(1.5)';
        if (assets.enemyImg) {
            ctx.drawImage(assets.enemyImg, this.x, this.y, this.width, this.height);
        } else {
            ctx.fillStyle = '#ff00ff';
            ctx.beginPath();
            ctx.arc(this.x + this.width/2, this.y + this.height/2, this.width/2, 0, Math.PI*2);
            ctx.fill();
        }
        ctx.restore();
        
        // HPバー
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(this.x, this.y - 20, this.width, 10);
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(this.x, this.y - 20, this.width * (this.hp / this.maxHp), 10);
    }
    
    takeDamage(amount) {
        this.hp -= amount;
        state.score += 50;
        ui.scoreDisplay().innerText = state.score;
        if (this.hp <= 0) {
            this.hp = 0;
            this.isDead = true;
            state.score += 1000;
            ui.scoreDisplay().innerText = state.score;
            gameClear();
        }
    }
}

export class Platform {
    constructor(x, y, w) {
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = 20;
    }
    update() {
        this.x -= 3 + (state.currentStage * 0.5); 
    }
    draw() {
        const ctx = getCtx();
        ctx.fillStyle = 'rgba(0, 255, 255, 0.4)'; 
        ctx.fillRect(this.x, this.y, this.width, this.height);
        ctx.strokeStyle = '#00ffff';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
    }
}

const GameView = {
    effectTimer: null,

    showScreen: function(screenId) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById('screen-' + screenId).classList.add('active');
    },

    updateCostumeSelectionUI: function(state) {
        const place = state.currentPlace;
        for(let i = 1; i <= 5; i++) {
            document.getElementById(`cos-img-${i}`).src = `img/cos${place}-${i}.jpg`;
            const isCleared = state.clearStatus[place][i-1];
            document.getElementById(`badge-${i}`).classList.toggle('hidden', !isCleared);
        }
    },

    updateDialogue: function(message) {
        document.getElementById('game-message').textContent = message;
    },

    updateHearts: function(playerLife, cpuLife) {
        const cpuH = document.getElementById('cpu-hearts');
        const plyH = document.getElementById('player-hearts');
        
        const renderHearts = (life) => {
            return Array(5).fill(0).map((_, i) => `<span class="heart ${i < life ? 'filled' : 'empty'}">${i < life ? '❤️' : '🤍'}</span>`).join('');
        };
        
        const prevCpuLife = cpuH.querySelectorAll('.filled').length;
        
        cpuH.innerHTML = renderHearts(cpuLife);
        plyH.innerHTML = renderHearts(playerLife);
        
        // ライフが減ったときの演出（画面・ライフバーの揺れ）
        if (cpuLife < prevCpuLife && prevCpuLife > 0) {
            cpuH.classList.add('heart-damage');
            setTimeout(() => cpuH.classList.remove('heart-damage'), 500);
        }
        
        // ピンチ演出（残りライフ1でドクドクさせる＆集中線）
        const speedLines = document.getElementById('speed-lines');
        if (cpuLife === 1) {
            cpuH.classList.add('heart-pinch');
            if (speedLines) speedLines.classList.add('active');
        } else {
            cpuH.classList.remove('heart-pinch');
            if (speedLines) speedLines.classList.remove('active');
        }
    },

    updateCharacter: function(place, costume, wins) {
        const img = document.getElementById('main-character');
        const container = document.getElementById('char-container');
        const winIdx = Math.min(wins, 5);
        img.src = `img/${place}-${costume}-${winIdx}.jpg`;
        
        // 場所と進行度（勝利数）に応じたクラスを付与（個別演出用）
        if (container) {
            container.className = `text-center place-${place} wins-${winIdx}`;
        }
    },

    showJankenEffect: function(result) {
        const oldLayer = document.getElementById('janken-effect-layer');
        if (oldLayer) oldLayer.remove();
        if (this.effectTimer) clearTimeout(this.effectTimer);

        const layer = document.createElement('div');
        layer.id = 'janken-effect-layer';
        layer.className = 'janken-effect-layer';

        const effect = document.createElement('div');
        effect.className = `janken-effect ${result}`;
        effect.innerHTML = result === 'win'
            ? '<span class="effect-title">勝ち！</span><span class="effect-sub">やったね！</span>'
            : '<span class="effect-title">負け...</span><span class="effect-sub">いたた...</span>';

        const vectors = [
            [-330, -210], [-280, -40], [-250, 170], [-150, -250],
            [-80, 250], [60, -270], [120, 240], [210, -190],
            [280, -20], [330, 170], [-370, 70], [365, 75],
            [-40, -330], [45, 330]
        ];
        vectors.forEach(([x, y], i) => {
            const spark = document.createElement('span');
            spark.className = 'spark';
            spark.style.left = `${48 + (i % 3) * 3}%`;
            spark.style.top = `${46 + Math.floor(i / 3) * 4}%`;
            spark.style.setProperty('--dx', `${x}px`);
            spark.style.setProperty('--dy', `${y}px`);
            effect.appendChild(spark);
        });

        layer.appendChild(effect);
        document.body.appendChild(layer);
        this.effectTimer = setTimeout(() => layer.remove(), 1200);
    },

    playRandomWinAudio: function() {
        if (typeof winAudioFiles !== 'undefined' && winAudioFiles.length > 0) {
            const randomFile = winAudioFiles[Math.floor(Math.random() * winAudioFiles.length)];
            const audio = new Audio(`audio/win/${randomFile}`);
            audio.volume = 1.0;
            audio.play().catch(e => console.error("Audio play failed:", e));
        }
    },

    playSE: function(type) {
        const audio = new Audio(`audio/${type}.mp3`);
        audio.volume = 1.0;
        audio.play().catch(e => console.error("Audio play failed:", e));
    },

    showResultDisplay: function(playerHand, cpuHand) {
        const plyEl = document.getElementById('player-hand');
        const cpuEl = document.getElementById('cpu-hand');
        const display = document.getElementById('result-display');
        
        // 最初は両方グーで揺らす（じゃん、けん、のタメ）
        plyEl.textContent = '✊';
        cpuEl.textContent = '✊';
        display.classList.remove('invisible');
        
        plyEl.classList.add('hand-shake');
        cpuEl.classList.add('hand-shake');
        
        // 0.8秒後に実際の手を出す（ぽん！）
        setTimeout(() => {
            plyEl.classList.remove('hand-shake');
            cpuEl.classList.remove('hand-shake');
            
            plyEl.textContent = playerHand;
            cpuEl.textContent = cpuHand;
            
            plyEl.classList.add('hand-pop');
            cpuEl.classList.add('hand-pop');
            
            setTimeout(() => {
                plyEl.classList.remove('hand-pop');
                cpuEl.classList.remove('hand-pop');
            }, 500);
        }, 800);
    },

    hideResultDisplay: function() {
        document.getElementById('result-display').classList.add('invisible');
    },

    setControlsState: function(enabled) {
        const controls = document.getElementById('controls');
        if (enabled) {
            controls.style.opacity = "1";
            controls.style.pointerEvents = "auto";
        } else {
            controls.style.opacity = "0.3";
            controls.style.pointerEvents = "none";
        }
    },

    setNextButtonState: function(enabled) {
        document.getElementById('next-btn').disabled = !enabled;
    },

    showGameOver: function(titleText, subText, showNextCostumeBtn) {
        document.getElementById('msg-window-container').classList.add('hidden');
        document.getElementById('controls').classList.add('hidden');
        document.getElementById('game-over-area').classList.remove('hidden');
        document.getElementById('final-result-text').textContent = titleText;
        document.getElementById('final-sub-text').textContent = subText;
    },

    hideGameOver: function() {
        document.getElementById('msg-window-container').classList.remove('hidden');
        document.getElementById('controls').classList.remove('hidden');
        document.getElementById('game-over-area').classList.add('hidden');
    },

    updatePlaceButtons: function(unlockedPlaces) {
        for (let i = 1; i <= 3; i++) {
            const btn = document.getElementById(`gal-btn-${i}`);
            btn.disabled = !unlockedPlaces[i];
        }
    },

    showOmake: function(place, idx) {
        document.getElementById('omake-display').src = `img/omake${place}-${idx}.jpg`;
        document.getElementById('omake-label').textContent = `No. ${idx}`;
    },

    updateSettingsUI: function(mode) {
        const modes = ['normal', 'player', 'cousin'];
        modes.forEach(m => {
            const btn = document.getElementById('btn-mode-' + m);
            btn.style.borderWidth = (m === mode) ? '4px' : '2px';
            btn.style.borderColor = (m === mode) ? '#f472b6' : '#fcc2d7';
        });
    },

    initMagnifier: function() {
        const img = document.getElementById('omake-display');
        const glass = document.getElementById('magnifier');
        
        if (!img || !glass) return;
        
        img.addEventListener('mousemove', moveMagnifier);
        img.addEventListener('mouseenter', () => glass.classList.add('active'));
        img.addEventListener('mouseleave', () => glass.classList.remove('active'));
        
        function moveMagnifier(e) {
            const rect = img.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const w = glass.offsetWidth / 2;
            const h = glass.offsetHeight / 2;
            
            // ガラスの位置を設定
            glass.style.left = (x - w) + "px";
            glass.style.top = (y - h) + "px";
            
            // ズーム倍率
            const zoom = 2;
            
            // 背景画像と位置を設定
            glass.style.backgroundImage = `url('${img.src}')`;
            glass.style.backgroundSize = `${img.width * zoom}px ${img.height * zoom}px`;
            glass.style.backgroundPosition = `-${(x * zoom) - w}px -${(y * zoom) - h}px`;
        }
    }
};

const GamePresenter = {
    init: function() {
        this.setMode('normal');
        window.showScreen = this.showScreen.bind(this);
        window.selectCostumePhase = this.selectCostumePhase.bind(this);
        window.startGame = this.startGame.bind(this);
        window.setMode = this.setMode.bind(this);
        window.nextStep = this.nextStep.bind(this);
        window.play = this.play.bind(this);
        window.resetGame = this.resetGame.bind(this);
        window.openGallery = this.openGallery.bind(this);
        window.nextOmake = this.nextOmake.bind(this);
        window.prevOmake = this.prevOmake.bind(this);
        window.exitGame = this.exitGame.bind(this);
        window.useSkill = this.useSkill.bind(this);
    },

    showScreen: function(screenId) {
        GameView.showScreen(screenId);
        if (screenId === 'select-place-gallery') {
            GameView.updatePlaceButtons(GameModel.state.unlockedPlaces);
        }
        if (screenId === 'select-costume') {
            GameView.updateCostumeSelectionUI(GameModel.state);
        }
    },

    selectCostumePhase: function(place) {
        GameModel.state.currentPlace = place;
        GameView.updateCostumeSelectionUI(GameModel.state);
        this.showScreen('select-costume');
    },

    startGame: function(costume) {
        GameModel.state.currentCostume = costume;
        GameModel.state.dialogueIdx = 0; 
        GameModel.state.step = 'intro';  
        this.resetGameUI(); 
        this.showScreen('game');
        this.updateDialogue(); 
        
        // BGMの再生
        const bgm = document.getElementById('bgm');
        if (bgm) {
            bgm.volume = 0.1; // BGMの音量を10%に下げる
            bgm.play().catch(e => console.error("BGM play failed:", e));
        } 
        
        // スキルボタンの初期化
        const btn = document.getElementById('skill-btn');
        if (btn) {
            btn.textContent = `おねだり（のこり${GameModel.state.skillsLeft}回）`;
            btn.classList.remove('hidden', 'opacity-50', 'cursor-not-allowed');
            btn.disabled = false;
        }
    },

    updateDialogue: function() {
        const currentList = GameModel.introDialogues[GameModel.state.currentPlace];
        GameView.updateDialogue(currentList[GameModel.state.dialogueIdx]);
    },

    setMode: function(mode) {
        GameModel.setDifficulty(mode);
        GameView.updateSettingsUI(mode);
        this.resetGame();
    },

    nextStep: function() {
        if (GameModel.state.step === 'intro') {
            GameModel.state.dialogueIdx++;
            const currentList = GameModel.introDialogues[GameModel.state.currentPlace];
            if (GameModel.state.dialogueIdx < currentList.length) {
                this.updateDialogue();
            } else {
                GameModel.state.step = 'ready';
                const hint = GameModel.getHintDialogue();
                GameView.updateDialogue(`${hint} ・・・じゃんけ～ん！`);
                GameView.setControlsState(true);
                GameView.setNextButtonState(false);
                GameView.hideResultDisplay();
            }
            return;
        }

        if (GameModel.state.step === 'start' || GameModel.state.step === 'result') {
            if (GameModel.state.playerLife <= 0 || GameModel.state.cpuLife <= 0) {
                this.endGame();
                return;
            }
            const hint = GameModel.getHintDialogue();
            GameView.updateDialogue(`${hint} ・・・じゃんけ～ん！`);
            GameModel.state.step = 'ready';
            GameView.setControlsState(true);
            GameView.setNextButtonState(false);
            GameView.hideResultDisplay();
        }
    },
    play: function(playerIdx) {
        GameView.playSE('click');
        const cpuIdx = GameModel.determineCpuHand(playerIdx);
        
        GameView.showResultDisplay(GameModel.hands[playerIdx], GameModel.hands[cpuIdx]);
        GameView.setControlsState(false);
        GameView.setNextButtonState(false); // 演出中は進めない
        GameModel.state.step = 'result';

        setTimeout(() => {
            const result = GameModel.checkResult(playerIdx, cpuIdx);
            
            if (result === 'draw') {
                GameModel.state.drawCount++;
                GameView.updateDialogue(`あいこ！もう一回！（あいこボーナス：次勝つと＋${GameModel.state.drawCount}ダメージ！）`);
            } else if (result === 'win') {
                // コンボ（連勝）のカウント
                GameModel.state.combo = (GameModel.state.combo || 0) + 1;
                
                let damage = 1;
                let isCritical = Math.random() < 0.2;

                if (GameModel.state.drawCount > 0) {
                    damage += GameModel.state.drawCount; // あいこボーナス追加
                    isCritical = true; // あいこ後は確定クリティカル演出
                } else if (isCritical) {
                    damage += 1;
                }
                
                if (isCritical || damage > 1) {
                    GameView.updateDialogue(`★クリティカルヒット！★ ${damage}ダメージ！！`);
                    GameView.showJankenEffect('win');
                    for (let i = 0; i < damage; i++) GameModel.decreaseCpuLife();
                } else {
                    if (GameModel.state.combo >= 2) {
                        GameView.updateDialogue(`${GameModel.state.combo}連勝！あーあ、まけちゃった`);
                    } else {
                        GameView.updateDialogue("あーあ、まけちゃった");
                    }
                    GameView.showJankenEffect('win');
                    GameModel.decreaseCpuLife();
                }
                
                GameModel.state.drawCount = 0; // ボーナスリセット
                
                GameView.playRandomWinAudio();
                GameView.playSE('win');
                GameView.updateHearts(GameModel.state.playerLife, GameModel.state.cpuLife);
                GameView.updateCharacter(GameModel.state.currentPlace, GameModel.state.currentCostume, GameModel.state.wins);
            } else {
                // 負けたらコンボとボーナスリセット
                GameModel.state.combo = 0;
                GameModel.state.drawCount = 0;
                GameView.updateDialogue("あたしのかちだね！");
                GameView.showJankenEffect('lose');
                GameView.playSE('lose');
                GameModel.decreasePlayerLife();
                GameView.updateHearts(GameModel.state.playerLife, GameModel.state.cpuLife);
            }
            
            GameView.setNextButtonState(true); // 演出が終わったら進める
        }, 1000);
    },

    useSkill: function() {
        if (GameModel.state.skillsLeft > 0 && GameModel.state.step === 'ready') {
            GameModel.state.skillsLeft--;
            GameModel.state.guaranteedWin = true;
            GameView.updateDialogue("ももは「えっ、お兄ちゃんのお願い？ しょうがないなぁ…（次は勝てるよ！）」");
            const btn = document.getElementById('skill-btn');
            if (btn) {
                btn.textContent = `おねだり（のこり${GameModel.state.skillsLeft}回）`;
                btn.disabled = true;
                btn.classList.add('opacity-50', 'cursor-not-allowed');
            }
        }
    },

    endGame: function() {
        GameModel.state.step = 'end';
        
        let title = "";
        let sub = "";

        if (GameModel.state.cpuLife <= 0) {
            const place = GameModel.state.currentPlace;
            const costume = GameModel.state.currentCostume;
            GameModel.state.clearStatus[place][costume - 1] = true;
            
            const allCleared = GameModel.state.clearStatus[place].every(c => c === true);
            const clearCount = GameModel.state.clearStatus[place].filter(c => c === true).length;

            if (allCleared) {
                title = "完全制覇おめでとう！！";
                sub = `${GameModel.placeNames[place]}のギャラリーが解放されたよ！`;
                GameModel.state.unlockedPlaces[place] = true;
            } else {
                title = `${costume}番目の衣装クリア！`;
                sub = `あと${5 - clearCount}つの衣装で全クリだよ！`;
            }
        } else {
            title = "ざんねん...";
            sub = "また挑戦してね！";
        }
        
        GameView.showGameOver(title, sub, true);
    },

    resetGameUI: function() {
        GameModel.resetLife();
        GameView.updateHearts(GameModel.state.playerLife, GameModel.state.cpuLife);
        GameView.updateCharacter(GameModel.state.currentPlace, GameModel.state.currentCostume, GameModel.state.wins);
        GameView.hideGameOver();
        GameView.setNextButtonState(true);
        GameView.hideResultDisplay();
        GameView.setControlsState(false);
    },

    resetGame: function() {
        GameModel.state.step = 'start';
        this.resetGameUI();
        GameView.updateDialogue("これからはじめるよ？");
    },

    openGallery: function(place) {
        GameModel.state.currentPlace = place;
        GameModel.state.currentOmakeIdx = 0;
        document.getElementById('gallery-title').textContent = `${GameModel.placeNames[place]}のぎゃらりー`;
        this.showScreen('gallery');
        GameView.showOmake(place, GameModel.state.currentOmakeIdx);
    },

    nextOmake: function() {
        GameModel.state.currentOmakeIdx = (GameModel.state.currentOmakeIdx + 1) % 15;
        GameView.showOmake(GameModel.state.currentPlace, GameModel.state.currentOmakeIdx);
    },

    prevOmake: function() {
        GameModel.state.currentOmakeIdx = (GameModel.state.currentOmakeIdx - 1 + 15) % 15;
        GameView.showOmake(GameModel.state.currentPlace, GameModel.state.currentOmakeIdx);
    },

    exitGame: function() {
        if (window.close) window.close();
        else alert("ゲームを終了します");
    }
};

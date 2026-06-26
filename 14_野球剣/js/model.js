const GameModel = {
    state: {
        playerLife: 5,
        cpuLife: 5,
        wins: 0,
        difficulty: 'normal',
        unlockedPlaces: { 1: false, 2: false, 3: false },
        clearStatus: {
            1: [false, false, false, false, false],
            2: [false, false, false, false, false],
            3: [false, false, false, false, false]
        },
        currentPlace: 1,
        currentCostume: 1,
        step: 'start',
        currentOmakeIdx: 0,
        dialogueIdx: 0,
        skillsLeft: 1,
        guaranteedWin: false,
        drawCount: 0
    },
    hands: ['✊', '✌️', '✋'],
    placeNames: { 1: 'おへや', 2: 'きょうしつ', 3: 'こうえん' },
    introDialogues: {
        1: ["おにいちゃん。ようこそあたしのへやに", "また、むかしのようにじゃんけんしようね", "はじめるけどいい？"],
        2: ["えっ！がっこうまできたの？", "ともだちがみてるかもしれないよ", "しょうがないな～"],
        3: ["ここならしずかだしへいきだよね？", "まわりにだれもいなそうだね！", "じゃあ、はじめようか"]
    },
    
    resetLife: function() {
        this.state.playerLife = 5;
        this.state.cpuLife = 5;
        this.state.wins = 0;
        this.state.skillsLeft = 1;
        this.state.guaranteedWin = false;
        this.state.drawCount = 0;
    },
    decreaseCpuLife: function() {
        this.state.cpuLife--;
        this.state.wins++;
    },
    decreasePlayerLife: function() {
        this.state.playerLife--;
    },
    setDifficulty: function(mode) {
        this.state.difficulty = mode;
    },
    determineCpuHand: function(playerIdx) {
        if (this.state.guaranteedWin) {
            this.state.guaranteedWin = false; // 使用後はリセット
            return (playerIdx + 1) % 3; // プレイヤーが勝つ手
        }
        if (this.state.difficulty === 'player') return (playerIdx + 1) % 3;
        if (this.state.difficulty === 'cousin') return (playerIdx + 2) % 3;
        // normalモード: 完全ランダム（あいこも出る）
        return Math.floor(Math.random() * 3);
    },
    getHintDialogue: function() {
        const hands = ['グー', 'チョキ', 'パー'];
        const randomHand = hands[Math.floor(Math.random() * 3)];
        const hints = [
            `次は${randomHand}をだそうかな〜？`,
            `えっとね、たぶん${randomHand}をだすよ！`,
            `ふふっ、${randomHand}には気をつけてね？`,
            `ん〜、${randomHand}を出したい気分かも。`
        ];
        return hints[Math.floor(Math.random() * hints.length)];
    },
    checkResult: function(playerIdx, cpuIdx) {
        if (playerIdx === cpuIdx) return 'draw';
        if ((playerIdx === 0 && cpuIdx === 1) || (playerIdx === 1 && cpuIdx === 2) || (playerIdx === 2 && cpuIdx === 0)) return 'win';
        return 'lose';
    }
};

class YakyukenGame {
    constructor() {
        this.images = [];
        this.currentStage = 0;
        this.isProcessing = false;
        
        this.confettiManager = new ConfettiManager('win-confetti');
        this.init();
    }

    async init() {
        // 画像リストの読み込み（サーバー側ではなくブラウザ側でフォルダ内のファイルを取得するのは難しいため、
        // 今回はコピーしたファイル名の規則性からリストを生成します）
        // 00000.png から 00118.png まで
        for (let i = 0; i <= 118; i++) {
            // パディング処理（00000 の形式にする）
            const num = String(i).padStart(5, '0');
            // 注意: Copy-Itemでファイル名が変わっていないことを前提としています。
            // 実際は 00000-xxxx.png という形式なので、後で調整が必要かもしれません。
            // ここでは簡易的に、実際に存在するファイルを推測するためのロジックを入れます。
            this.images.push(num); 
        }

        // 要素の取得
        this.imgElement = document.getElementById('main-image');
        this.imgContainer = document.getElementById('image-container');
        this.stageText = document.getElementById('current-stage');
        this.totalText = document.getElementById('total-stages');
        this.progressBar = document.getElementById('progress-bar');
        this.resultText = document.getElementById('result-text');
        this.opponentHand = document.getElementById('opponent-hand');
        this.flashEffect = document.getElementById('flash-effect');
        this.viewport = document.querySelector('.image-viewport');

        // 実際の画像ファイル名リストを取得
        if (typeof ACTUAL_FILES !== 'undefined') {
            this.setFileList(ACTUAL_FILES);
        } else {
            // フォールバック（念のため）
            this.fileList = this.images.map(num => `${num}.png`);
        }
        
        this.updateDisplay();
    }

    setFileList(list) {
        this.fileList = list;
        this.totalText.innerText = this.fileList.length;
        this.updateDisplay();
    }

    updateDisplay() {
        if (this.fileList.length === 0) return;

        const fileName = this.fileList[this.currentStage];
        const fullPath = `assets/${fileName}`;

        // フェードアウト
        this.imgContainer.classList.add('fade-out');

        setTimeout(() => {
            this.imgElement.src = fullPath;
            this.imgElement.onload = () => {
                this.imgContainer.classList.remove('fade-out');
            };
            
            this.stageText.innerText = this.currentStage + 1;
            const progress = ((this.currentStage + 1) / this.fileList.length) * 100;
            this.progressBar.style.width = `${progress}%`;
        }, 300);
    }

    play(userChoice) {
        if (this.isProcessing) return;
        this.isProcessing = true;

        const choices = ['rock', 'scissors', 'paper'];
        const aiChoice = choices[Math.floor(Math.random() * 3)];
        
        // 相手の手を表示
        const icons = { 'rock': '✊', 'scissors': '✌️', 'paper': '🖐️' };
        this.opponentHand.innerText = icons[aiChoice];
        this.opponentHand.classList.add('show');

        // 勝敗判定
        let result = ''; // 'win', 'lose', 'draw'
        if (userChoice === aiChoice) {
            result = 'draw';
        } else if (
            (userChoice === 'rock' && aiChoice === 'scissors') ||
            (userChoice === 'scissors' && aiChoice === 'paper') ||
            (userChoice === 'paper' && aiChoice === 'rock')
        ) {
            result = 'win';
        } else {
            result = 'lose';
        }

        this.showResult(result);
    }

    showResult(result) {
        const resultMessages = {
            'win': 'WIN!',
            'lose': 'LOSE...',
            'draw': 'DRAW'
        };

        this.resultText.innerText = resultMessages[result];
        this.resultText.className = '';
        this.resultText.classList.add(result);
        this.resultText.classList.add('show');

        // 勝利時の演出
        if (result === 'win') {
            this.flashEffect.classList.add('active');
            setTimeout(() => this.flashEffect.classList.remove('active'), 500);
            
            // 追加演出
            this.confettiManager.spawn();
            this.viewport.classList.add('shake');
            setTimeout(() => this.viewport.classList.remove('shake'), 500);

            if (this.currentStage < this.fileList.length - 1) {
                this.currentStage++;
                this.updateDisplay();
            }
        }

        // しばらくしたらメッセージを消す
        setTimeout(() => {
            this.resultText.classList.remove('show');
            this.opponentHand.classList.remove('show');
            this.isProcessing = false;
        }, 1500);
    }
}

class ConfettiManager {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    spawn() {
        this.particles = [];
        const count = 150;
        const colors = ['#ff4757', '#ffa502', '#2ed573', '#1e90ff', '#ffffff'];
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: -20,
                size: Math.random() * 8 + 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                speed: Math.random() * 6 + 4,
                angle: Math.random() * Math.PI * 2,
                spin: Math.random() * 0.2 - 0.1,
                vx: Math.random() * 4 - 2
            });
        }
        this.animate();
    }

    animate() {
        if (this.particles.length === 0) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        let alive = false;
        this.particles.forEach(p => {
            p.y += p.speed;
            p.x += p.vx;
            p.angle += p.spin;
            if (p.y < this.canvas.height) {
                alive = true;
                this.ctx.save();
                this.ctx.translate(p.x, p.y);
                this.ctx.rotate(p.angle);
                this.ctx.fillStyle = p.color;
                this.ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
                this.ctx.restore();
            }
        });
        if (alive) requestAnimationFrame(() => this.animate());
        else this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

const game = new YakyukenGame();

import * as THREE from 'three';

// --- 初期設定 ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050505);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// --- ライティング ---
const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0x00ffff, 2, 50);
pointLight.position.set(0, 10, 0);
scene.add(pointLight);

const neonLight = new THREE.RectAreaLight(0xff00ff, 5, 12, 12);
neonLight.position.set(0, 0.1, 0);
neonLight.rotation.x = -Math.PI / 2;
scene.add(neonLight);

// --- リングの作成 ---
// マット
const matGeometry = new THREE.BoxGeometry(10, 0.5, 10);
const matMaterial = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.8 });
const mat = new THREE.Mesh(matGeometry, matMaterial);
mat.position.y = -0.25;
scene.add(mat);

// コーナーポスト
const postGeometry = new THREE.CylinderGeometry(0.2, 0.2, 3);
const postMaterial = new THREE.MeshStandardMaterial({ color: 0x444444 });

const createPost = (x: number, z: number) => {
    const post = new THREE.Mesh(postGeometry, postMaterial);
    post.position.set(x, 1.5, z);
    scene.add(post);
};

createPost(4.8, 4.8);
createPost(-4.8, 4.8);
createPost(4.8, -4.8);
createPost(-4.8, -4.8);

// ロープ (簡易版)
const ropeMaterial = new THREE.LineBasicMaterial({ color: 0xff00ff });
const createRope = (y: number) => {
    const points = [
        new THREE.Vector3(4.8, y, 4.8),
        new THREE.Vector3(-4.8, y, 4.8),
        new THREE.Vector3(-4.8, y, -4.8),
        new THREE.Vector3(4.8, y, -4.8),
        new THREE.Vector3(4.8, y, 4.8),
    ];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geometry, ropeMaterial);
    scene.add(line);
};

createRope(1.0);
createRope(1.8);
createRope(2.6);

// --- レスラーの作成 (ボクセルスタイル) ---
const createWrestler = (color: number, x: number) => {
    const group = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: color, emissive: color, emissiveIntensity: 0.2 });

    // 胴体 (Torso)
    const torso = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.5, 0.8), mat);
    torso.position.y = 1.75;
    group.add(torso);

    // 頭 (Head)
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.7), mat);
    head.position.y = 2.85;
    group.add(head);

    // 右腕 (Right Arm)
    const rArm = new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.2, 0.4), mat);
    rArm.position.set(0.85, 1.8, 0);
    group.add(rArm);

    // 左腕 (Left Arm)
    const lArm = new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.2, 0.4), mat);
    lArm.position.set(-0.85, 1.8, 0);
    group.add(lArm);

    // 右足 (Right Leg)
    const rLeg = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.2, 0.5), mat);
    rLeg.position.set(0.35, 0.6, 0);
    group.add(rLeg);

    // 左足 (Left Leg)
    const lLeg = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.2, 0.5), mat);
    lLeg.position.set(-0.35, 0.6, 0);
    group.add(lLeg);

    group.position.x = x;
    scene.add(group);
    return group;
};

const player1 = createWrestler(0x00ffff, -2);
const player2 = createWrestler(0xff0088, 2);
player2.rotation.y = Math.PI; // 向き合わせ

// --- 入力管理 ---
const keys: { [key: string]: boolean } = {};
window.addEventListener('keydown', (e) => keys[e.code] = true);
window.addEventListener('keyup', (e) => keys[e.code] = false);

// --- ステータス管理 ---
const state = {
    p1: { hp: 100, isAttacking: false, isSpecial: false, attackCooldown: 0 },
    p2: { hp: 100, isAttacking: false, attackCooldown: 0 },
    cameraRotation: 0,
    isCameraRotating: false,
    isGameOver: false
};

const updateHP = () => {
    const hp1 = document.getElementById('hp-1p');
    const hp2 = document.getElementById('hp-2p');
    if (hp1) hp1.style.width = `${state.p1.hp}%`;
    if (hp2) hp2.style.width = `${state.p2.hp}%`;

    if (state.p1.hp <= 0 || state.p2.hp <= 0) {
        showResult();
    }
};

const showResult = () => {
    state.isGameOver = true;
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    if (resultDiv && resultText) {
        resultText.innerText = state.p1.hp > 0 ? "YOU WIN" : "YOU LOSE";
        resultText.style.color = state.p1.hp > 0 ? "#00ffff" : "#ff0088";
        resultDiv.style.display = "block";
    }
};

// リトライ機能
const retryBtn = document.getElementById('retry-btn');
retryBtn?.addEventListener('click', () => {
    state.p1.hp = 100;
    state.p2.hp = 100;
    state.isGameOver = false;
    state.p1.isAttacking = false;
    state.p1.isSpecial = false;
    state.p2.isAttacking = false;
    updateHP();

    player1.position.set(-2, 0, 0);
    player1.scale.set(1, 1, 1);
    player2.position.set(2, 0, 0);

    const resultDiv = document.getElementById('result');
    if (resultDiv) resultDiv.style.display = "none";
});

// --- アニメーションループ ---
const moveSpeed = 0.1;
const ringLimit = 4.5;

function animate() {
    requestAnimationFrame(animate);

    if (!state.isGameOver) {
        // 1Pの移動 (攻撃・必殺技中でない時のみ)
        if (!state.p1.isAttacking && !state.p1.isSpecial) {
            if (keys['ArrowUp'] || keys['KeyW']) player1.position.z -= moveSpeed;
            if (keys['ArrowDown'] || keys['KeyS']) player1.position.z += moveSpeed;
            if (keys['ArrowLeft'] || keys['KeyA']) player1.position.x -= moveSpeed;
            if (keys['ArrowRight'] || keys['KeyD']) player1.position.x += moveSpeed;
        }

        // 必殺技処理 (Lキー)
        if (keys['KeyL'] && !state.p1.isSpecial && !state.p1.isAttacking) {
            state.p1.isSpecial = true;
            state.p1.attackCooldown = 60;
            state.isCameraRotating = true;
            state.cameraRotation = 0;

            const dist = player1.position.distanceTo(player2.position);
            if (dist < 3.0) {
                state.p2.hp = Math.max(0, state.p2.hp - 30);
                updateHP();
            }
        }

        // 攻撃処理 (Jキー: パンチ)
        if (keys['KeyJ'] && !state.p1.isAttacking && !state.p1.isSpecial) {
            state.p1.isAttacking = true;
            state.p1.attackCooldown = 20;
            
            const dist = player1.position.distanceTo(player2.position);
            if (dist < 2.0) {
                state.p2.hp = Math.max(0, state.p2.hp - 5);
                updateHP();
            }
        }

        // CPUの行動
        if (!state.p2.isAttacking && state.p2.hp > 0) {
            const dx = player1.position.x - player2.position.x;
            const dz = player1.position.z - player2.position.z;
            const dist = Math.sqrt(dx * dx + dz * dz);

            if (dist > 1.5) {
                player2.position.x += (dx / dist) * moveSpeed * 0.5;
                player2.position.z += (dz / dist) * moveSpeed * 0.5;
            } else {
                state.p2.isAttacking = true;
                state.p2.attackCooldown = 30;
                state.p1.hp = Math.max(0, state.p1.hp - 3);
                updateHP();
            }
        }

        // 演出管理
        if (state.p1.isAttacking) {
            state.p1.attackCooldown--;
            player1.children[2].position.z = -0.8;
            if (state.p1.attackCooldown <= 0) {
                state.p1.isAttacking = false;
                player1.children[2].position.z = 0;
            }
        }
        if (state.p1.isSpecial) {
            state.p1.attackCooldown--;
            player1.scale.set(1.5, 1.5, 1.5);
            if (state.p1.attackCooldown <= 0) {
                state.p1.isSpecial = false;
                player1.scale.set(1, 1, 1);
            }
        }
        if (state.p2.isAttacking) {
            state.p2.attackCooldown--;
            player2.children[2].position.z = -0.8;
            if (state.p2.attackCooldown <= 0) {
                state.p2.isAttacking = false;
                player2.children[2].position.z = 0;
            }
        }

        // カメラ回転
        if (state.isCameraRotating) {
            state.cameraRotation += 0.15;
            const radius = 10;
            camera.position.x = Math.sin(state.cameraRotation) * radius;
            camera.position.z = Math.cos(state.cameraRotation) * radius;
            camera.lookAt(0, 0, 0);
            if (state.cameraRotation >= Math.PI * 2) {
                state.isCameraRotating = false;
                camera.position.set(0, 5, 10);
                camera.lookAt(0, 0, 0);
            }
        }

        // リング内制限
        const limitPos = (obj: THREE.Object3D) => {
            obj.position.x = Math.max(-ringLimit, Math.min(ringLimit, obj.position.x));
            obj.position.z = Math.max(-ringLimit, Math.min(ringLimit, obj.position.z));
        };
        limitPos(player1);
        limitPos(player2);
    }

    renderer.render(scene, camera);
}

// リサイズ対応
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();
console.log('Pro Wrestling Game Initialized!');

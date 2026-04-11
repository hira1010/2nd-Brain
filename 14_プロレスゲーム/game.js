/* game.js */

let scene, camera, renderer, clock;
let players = { p1: null, p2: null };
let ring, ropes = [], crowd;
let specialGauge = 0;
let isSpecialExecuting = false;
let hitStop = 0;
let particles = [];


// Input state
const input = {
    joyX: 0, joyY: 0,
    btns: { strike: false, dash: false, throw: false, defend: false, joint: false, special: false }
};

init();
animate();

function init() {
    // Basic Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x050510); // 深い夜

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 5, 12);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.getElementById('game-container').appendChild(renderer.domElement);

    clock = new THREE.Clock();

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
    scene.add(ambientLight);

    const spotlight = new THREE.SpotLight(0xffffff, 1);
    spotlight.position.set(0, 15, 0);
    spotlight.castShadow = true;
    scene.add(spotlight);

    // Ring (真青なマット - より質感高く)
    const ringGeo = new THREE.BoxGeometry(10, 0.5, 10);
    const ringMat = new THREE.MeshStandardMaterial({ 
        color: 0x0000ff,
        roughness: 0.8,
        metalness: 0.2
    });
    ring = new THREE.Mesh(ringGeo, ringMat);
    ring.position.y = -0.25;
    ring.receiveShadow = true;
    scene.add(ring);

    // Crowd (観客席の追加)
    createCrowd();


    // Ropes (黒の3本線)
    const ropeMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
    const posts = [[5, 5], [5, -5], [-5, 5], [-5, -5]];
    posts.forEach(p => {
        const postGeo = new THREE.CylinderGeometry(0.1, 0.1, 2.5);
        const post = new THREE.Mesh(postGeo, ropeMat);
        post.position.set(p[0], 1, p[1]);
        scene.add(post);

        for (let i = 0; i < 3; i++) {
            const ropeGeo = new THREE.CylinderGeometry(0.04, 0.04, 10.1);
            const rope = new THREE.Mesh(ropeGeo, ropeMat);
            rope.position.y = 0.6 + i * 0.6;
            if (p[0] === 5 && p[1] === 5) {
                const r1 = rope.clone(); r1.rotation.z = Math.PI / 2; r1.position.z = 5; r1.position.x = 0; scene.add(r1);
                const r2 = rope.clone(); r2.rotation.x = Math.PI / 2; r2.position.x = 5; r2.position.z = 0; scene.add(r2);
            }
            if (p[0] === -5 && p[1] === -5) {
                const r1 = rope.clone(); r1.rotation.z = Math.PI / 2; r1.position.z = -5; r1.position.x = 0; scene.add(r1);
                const r2 = rope.clone(); r2.rotation.x = Math.PI / 2; r2.position.x = -5; r2.position.z = 0; scene.add(r2);
            }
        }
    });

    // Players
    players.p1 = createPlayer(0xff0000, "P1", -2);
    players.p2 = createPlayer(0x00ff00, "P2", 2);

    setupControls();
    window.addEventListener('resize', onWindowResize, false);
}

function createPlayer(color, name, x) {
    const group = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.8, 0.5), new THREE.MeshPhongMaterial({ color }));
    body.position.y = 0.9;
    body.castShadow = true;
    group.add(body);

    const head = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), new THREE.MeshPhongMaterial({ color: 0xffdbac }));
    head.position.y = 2.0;
    group.add(head);

    group.position.set(x, 0, 0);
    scene.add(group);

    return {
        mesh: group,
        state: 'IDLE',
        hp: 100,
        name: name,
        velocity: new THREE.Vector3(),
        lastAttackTime: 0
    };
}

function setupControls() {
    const stick = document.getElementById('joystick-container');
    const handle = document.getElementById('joystick-handle');
    let isDragging = false;

    const updateStick = (e) => {
        if (!isDragging) return;
        const rect = stick.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const touch = e.touches ? e.touches[0] : e;

        let dx = touch.clientX - centerX;
        let dy = touch.clientY - centerY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const maxDist = 60;

        if (dist > maxDist) {
            dx = dx * maxDist / dist;
            dy = dy * maxDist / dist;
        }

        handle.style.left = `calc(50% + ${dx}px)`;
        handle.style.top = `calc(50% + ${dy}px)`;

        input.joyX = dx / maxDist;
        input.joyY = dy / maxDist;
    };

    const handleStart = (e) => { isDragging = true; updateStick(e); if (e.preventDefault) e.preventDefault(); };

    stick.addEventListener('touchstart', handleStart);
    window.addEventListener('touchmove', updateStick);
    window.addEventListener('touchend', () => {
        isDragging = false;
        handle.style.left = '50%'; handle.style.top = '50%';
        input.joyX = 0; input.joyY = 0;
    });

    stick.addEventListener('mousedown', handleStart);
    window.addEventListener('mousemove', updateStick);
    window.addEventListener('mouseup', () => {
        isDragging = false;
        handle.style.left = '50%'; handle.style.top = '50%';
        input.joyX = 0; input.joyY = 0;
    });

    const bindBtn = (id, key) => {
        const btn = document.getElementById(id);
        const setVal = (v) => (e) => { input.btns[key] = v; if (e.preventDefault) e.preventDefault(); };
        btn.addEventListener('touchstart', setVal(true));
        btn.addEventListener('touchend', setVal(false));
        btn.addEventListener('mousedown', setVal(true));
        btn.addEventListener('mouseup', setVal(false));
    };

    bindBtn('btn-strike', 'strike');
    bindBtn('btn-dash', 'dash');
    bindBtn('btn-throw', 'throw');
    bindBtn('btn-defend', 'defend');
    bindBtn('btn-joint', 'joint');
    bindBtn('btn-special', 'special');

    document.getElementById('btn-fall').addEventListener('click', startFall);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    const elapsed = clock.getElapsedTime();
    
    if (hitStop > 0) {
        hitStop -= delta;
        return;
    }

    updateCrowd(elapsed);
    updateParticles(delta);
    updatePhysics(delta);
    updateCamera();
    updateUI();
    renderer.render(scene, camera);
}


function updateParticles(delta) {
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.life -= delta;
        if (p.life <= 0) {
            scene.remove(p.mesh);
            particles.splice(i, 1);
        } else {
            p.mesh.position.add(p.velocity.clone().multiplyScalar(delta));
            p.mesh.scale.multiplyScalar(0.95);
        }
    }
}

function createHitEffect(pos, color = 0xffff00) {
    for (let i = 0; i < 10; i++) {
        const geo = new THREE.SphereGeometry(0.1, 4, 4);
        const mat = new THREE.MeshBasicMaterial({ color });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.copy(pos);
        scene.add(mesh);
        particles.push({
            mesh,
            velocity: new THREE.Vector3((Math.random() - 0.5) * 5, Math.random() * 5, (Math.random() - 0.5) * 5),
            life: 0.5
        });
    }
}

function createCrowd() {
    crowd = new THREE.Group();
    const crowdGeo = new THREE.BoxGeometry(0.3, 0.3, 0.3);
    for (let i = 0; i < 500; i++) {
        const mat = new THREE.MeshStandardMaterial({ color: Math.random() > 0.5 ? 0x444444 : 0x222222 });
        const p = new THREE.Mesh(crowdGeo, mat);
        
        const angle = Math.random() * Math.PI * 2;
        const radius = 7 + Math.random() * 5;
        p.position.set(Math.cos(angle) * radius, Math.random() * 3, Math.sin(angle) * radius);
        p.initialY = p.position.y;
        crowd.add(p);
    }
    scene.add(crowd);
}

function updateCrowd(time) {
    if (!crowd) return;
    crowd.children.forEach((p, i) => {
        p.position.y = p.initialY + Math.sin(time * 5 + i) * 0.1;
    });
}



function updatePhysics(delta) {
    const p1 = players.p1;
    if (!p1 || isSpecialExecuting) return;

    const speed = input.btns.dash ? 6 : 3;
    const moveX = input.joyX * speed * delta;
    const moveZ = input.joyY * speed * delta;

    p1.mesh.position.x += moveX;
    p1.mesh.position.z += moveZ;

    const limit = 4.8;
    if (Math.abs(p1.mesh.position.x) > limit) {
        const sign = Math.sign(p1.mesh.position.x);
        p1.mesh.position.x = sign * limit;
        if (input.btns.dash) {
            input.joyX = -sign;
            shakeMatt();
        }
    }
    if (Math.abs(p1.mesh.position.z) > limit) {
        p1.mesh.position.z = Math.sign(p1.mesh.position.z) * limit;
    }

    if (Math.abs(input.joyX) > 0.1 || Math.abs(input.joyY) > 0.1) {
        p1.mesh.rotation.y = Math.atan2(input.joyX, input.joyY);
    }

    if (input.btns.strike && Date.now() - p1.lastAttackTime > 500) {
        p1.lastAttackTime = Date.now();
        const dist = p1.mesh.position.distanceTo(players.p2.mesh.position);
        if (dist < 1.8) {
            hitStop = 0.1;
            createHitEffect(players.p2.mesh.position.clone().add(new THREE.Vector3(0, 1.2, 0)));
            shakeMatt();
            // 相手を少し吹っ飛ばす
            const dir = players.p2.mesh.position.clone().sub(p1.mesh.position).normalize();
            players.p2.mesh.position.add(dir.multiplyScalar(0.5));
        }
    }
    if (input.btns.special && specialGauge >= 100) executeSpecial();
}


function updateCamera() {
    if (isSpecialExecuting) {
        const time = clock.getElapsedTime() * 4;
        camera.position.x = Math.sin(time) * 10;
        camera.position.z = Math.cos(time) * 10;
        camera.position.y = 4;
        camera.lookAt(0, 1, 0);
        return;
    }
    const p1 = players.p1.mesh.position;
    const p2 = players.p2.mesh.position;
    const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
    camera.position.lerp(new THREE.Vector3(mid.x, 6, mid.z + 8), 0.1);
    camera.lookAt(mid.x, 1, mid.z);
}

function updateUI() {
    document.getElementById('special-gauge').style.width = `${specialGauge}%`;
    const p1 = players.p1, p2 = players.p2;
    const dist = p1.mesh.position.distanceTo(p2.mesh.position);

    // 相手がダウンしているか、テスト用に常にフォール可能か（簡易化）
    if (dist < 1.5 && !isFalling) document.getElementById('fall-container').classList.remove('hidden');
    else document.getElementById('fall-container').classList.add('hidden');

    if (specialGauge < 100) specialGauge += 0.2;
}

let isFalling = false;
function startFall() {
    if (isFalling) return;
    isFalling = true;
    let count = 0;
    const el = document.getElementById('fall-count');
    const interval = setInterval(() => {
        count++;
        el.textContent = count;
        if (count === 3) {
            clearInterval(interval);
            el.textContent = "3!!! FINISH!";
            setTimeout(() => { location.reload(); }, 3000);
        }
        if (count === 2 && Math.random() > 0.5) {
            setTimeout(() => {
                if (isFalling && count < 3) {
                    clearInterval(interval);
                    el.textContent = "2.9!!";
                    setTimeout(() => { el.textContent = ""; isFalling = false; }, 1000);
                }
            }, 900);
        }
    }, 1000);
}

function shakeMatt() {
    document.body.classList.add('shake');
    setTimeout(() => document.body.classList.remove('shake'), 300);
}

function executeSpecial() {
    if (specialGauge < 100 || isSpecialExecuting) return;
    isSpecialExecuting = true;
    specialGauge = 0;
    document.getElementById('action-buttons').classList.add('hidden');
    document.getElementById('announcer-cutin').classList.remove('hidden');
    document.getElementById('crowd-cutin').classList.remove('hidden');
    setTimeout(() => {
        isSpecialExecuting = false;
        document.getElementById('action-buttons').classList.remove('hidden');
        document.getElementById('announcer-cutin').classList.add('hidden');
        document.getElementById('crowd-cutin').classList.add('hidden');
    }, 4000);
}

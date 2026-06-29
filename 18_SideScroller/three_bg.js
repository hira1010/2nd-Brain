import { state } from './state.js';

let scene, camera, renderer, t_cubes = [];

export function initThreeJS() {
    if (!window.THREE) return;
    
    const threeCanvas = document.getElementById('threeCanvas');
    renderer = new THREE.WebGLRenderer({ canvas: threeCanvas, alpha: true, antialias: true });
    renderer.setSize(800, 600);
    
    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x001133, 10, 60);
    
    camera = new THREE.PerspectiveCamera(60, 800/600, 0.1, 100);
    camera.position.set(0, 5, 20);
    
    const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
    scene.add(ambientLight);
    
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(10, 20, 10);
    scene.add(dirLight);
    
    // サイバーなグリッド地面
    const grid = new THREE.GridHelper(200, 40, 0x00ffff, 0x004444);
    grid.position.y = -5;
    scene.add(grid);
    
    // ビルディング群の生成
    const geo = new THREE.BoxGeometry(1, 1, 1);
    for(let i=0; i<60; i++) {
        const mat = new THREE.MeshPhongMaterial({ 
            color: 0x333333,
            emissive: Math.random() > 0.8 ? 0x00ffff : 0x000000 
        });
        const mesh = new THREE.Mesh(geo, mat);
        
        mesh.position.set(
            (Math.random() > 0.5 ? 1 : -1) * (10 + Math.random() * 40), // 中央を避ける
            (Math.random() * 10) - 5,
            (Math.random() - 0.5) * 80 - 20
        );
        mesh.scale.set(
            2 + Math.random() * 3,
            10 + Math.random() * 20,
            2 + Math.random() * 3
        );
        scene.add(mesh);
        t_cubes.push(mesh);
    }
}

export function updateThreeJS() {
    if (!scene) return;
    
    // スクロールに合わせてカメラを少し揺らしつつビルを奥から手前へ流す
    t_cubes.forEach(c => {
        c.position.z += 0.3 + (state.currentStage * 0.05);
        if (c.position.z > 20) {
            c.position.z -= 100;
            c.position.x = (Math.random() > 0.5 ? 1 : -1) * (10 + Math.random() * 40);
        }
    });
    
    // ステージごとのフォグ（霧）色の変化
    if (state.currentStage === 2) scene.fog.color.setHex(0xaa4400);      // 夕方
    else if (state.currentStage === 3) scene.fog.color.setHex(0x000022); // 夜
    else if (state.currentStage === 4) scene.fog.color.setHex(0x114411); // 毒沼
    else if (state.currentStage === 5) scene.fog.color.setHex(0x550055); // 異空間
    else scene.fog.color.setHex(0x001133); // 初期
    
    renderer.render(scene, camera);
}

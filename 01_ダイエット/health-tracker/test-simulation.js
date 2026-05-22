const fs = require('fs');
const path = require('path');

// グローバルオブジェクトのモック
global.window = global;

const elementCache = {};
global.document = {
    addEventListener: (event, callback) => {
        if (event === 'DOMContentLoaded') {
            global.domContentLoadedCallback = callback;
        }
    },
    getElementById: (id) => {
        if (!elementCache[id]) {
            const listeners = {};
            elementCache[id] = {
                id: id,
                value: '',
                textContent: '',
                style: {},
                classList: {
                    add: () => {},
                    remove: () => {},
                    contains: () => false,
                    toggle: () => {}
                },
                addEventListener: (event, callback) => {
                    listeners[event] = callback;
                },
                click: () => {
                    if (listeners['click']) {
                        listeners['click']();
                    }
                },
                querySelector: () => ({ textContent: '' }),
                getContext: () => ({}),
                appendChild: () => {},
                append: () => {},
                innerHTML: ''
            };
        }
        return elementCache[id];
    },
    createElement: (tag) => {
        return {
            value: '',
            textContent: '',
            style: {},
            className: '',
            appendChild: () => {},
            append: () => {},
            addEventListener: () => {},
            classList: {
                add: () => {},
                remove: () => {},
                contains: () => false,
                toggle: () => {}
            }
        };
    },
    querySelectorAll: () => []
};

global.prompt = (msg, def) => "250"; // カロリー入力ダイアログのモック

global.localStorageStore = {};
global.localStorage = {
    getItem: (key) => global.localStorageStore[key] || null,
    setItem: (key, val) => { global.localStorageStore[key] = val; }
};
global.lucide = {
    createIcons: () => {}
};
global.Chart = function() {
    return { destroy: () => {} };
};

// script.jsの読み込みと実行
const scriptContent = fs.readFileSync(path.join(__dirname, 'script.js'), 'utf8') +
    '\nglobal.getDOM = () => DOM;\nglobal.triggerAutoSave = triggerAutoSave;';
eval(scriptContent);

// DOMContentLoadedの実行
global.domContentLoadedCallback();

const DOM = global.getDOM();

console.log("--- 非同期自動保存シミュレーションテスト開始 ---");

// 1. 朝食入力欄に「トースト」を入力し、追加ボタンをクリック
console.log("\n1. 朝食に入力欄から 'トースト' を追加します。");
DOM.mealBreakfast.value = 'トースト';
const addBreakfastBtn = elementCache['add-breakfast-btn'];
if (addBreakfastBtn) {
    addBreakfastBtn.click();
}

// 2. 600ms 待つ
setTimeout(() => {
    console.log("600ms経過後のローカルストレージ内容（朝食に toast が入っているはず）:");
    console.log(localStorage.getItem('health_tracker_data'));

    // 3. 昼食に新規メニュー「ステーキ」を入力し、追加ボタンをクリック
    console.log("\n2. 昼食に入力欄から新規メニュー 'ステーキ' (カロリーはモックで250) を追加します。");
    DOM.mealLunch.value = 'ステーキ';
    const addLunchBtn = elementCache['add-lunch-btn'];
    if (addLunchBtn) {
        addLunchBtn.click();
    }

    // 4. さらに 600ms 待つ
    setTimeout(() => {
        console.log("さらに600ms経過後のローカルストレージ内容（朝食と昼食の両方が保存されているはず）:");
        console.log(localStorage.getItem('health_tracker_data'));
        console.log("食事メニューのストレージ内容（ステーキが記憶されているはず）:");
        console.log(localStorage.getItem('health_tracker_meals'));
        console.log("\n--- テスト終了 ---");
    }, 600);

}, 600);


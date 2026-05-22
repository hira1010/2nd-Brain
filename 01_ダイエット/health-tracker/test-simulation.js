const fs = require('fs');
const path = require('path');

// グローバルオブジェクトのモック
global.window = global;
global.document = {
    addEventListener: (event, callback) => {
        if (event === 'DOMContentLoaded') {
            global.domContentLoadedCallback = callback;
        }
    },
    getElementById: (id) => {
        return {
            id: id,
            value: 'none',
            textContent: '',
            style: {},
            classList: {
                add: () => {},
                remove: () => {},
                contains: () => false,
                toggle: () => {}
            },
            addEventListener: () => {},
            querySelector: () => ({ textContent: '' }),
            getContext: () => ({}),
            appendChild: () => {},
            innerHTML: ''
        };
    },
    createElement: (tag) => {
        return {
            value: '',
            textContent: '',
            style: {},
            className: '',
            appendChild: () => {},
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

// 1. 朝食を toast に変更し自動保存をトリガー
console.log("\n1. 朝食を 'toast' に変更します。");
DOM.mealBreakfast.value = 'toast';
global.triggerAutoSave(DOM.mealBreakfast);

// 2. 600ms 待つ
setTimeout(() => {
    console.log("600ms経過後のローカルストレージ内容（朝食のみ保存されているはず）:");
    console.log(localStorage.getItem('health_tracker_data'));

    // 3. 昼食を salad に変更し自動保存をトリガー
    console.log("\n2. 昼食を 'salad' に変更します。");
    DOM.mealLunch.value = 'salad';
    global.triggerAutoSave(DOM.mealLunch);

    // 4. さらに 600ms 待つ
    setTimeout(() => {
        console.log("さらに600ms経過後のローカルストレージ内容（朝食と昼食の両方が保存されているはず）:");
        console.log(localStorage.getItem('health_tracker_data'));
        console.log("\n--- テスト終了 ---");
    }, 600);

}, 600);

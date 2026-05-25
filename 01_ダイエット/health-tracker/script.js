/**
 * ヘルスケア記録サイト - メインスクリプト
 *
 * 構造:
 *   [1] 定数・設定データ
 *   [2] アプリケーション状態
 *   [3] 初期化
 *   [4] データ層（読み書き）
 *   [5] 食事リスト管理
 *   [6] 水分管理
 *   [7] 自動保存
 *   [8] ダッシュボード表示
 *   [9] グラフ
 *   [10] カレンダー・履歴
 *   [11] ユーティリティ
 */

// ============================================================
// [1] 定数・設定データ
// ============================================================

/** デフォルトの食事メニューデータ（P:たんぱく質, F:脂質, C:炭水化物, kcal:カロリー） */
const DEFAULT_MEAL_MENU = {
    // 朝食・乳製品・卵
    toast:      { name: '🍞 トースト (6枚切1枚)', p: 5.6,  f: 2.0,  c: 28.0,  kcal: 160 },
    egg:        { name: '🍳 スクランブルエッグ', p: 7.0,  f: 6.0,  c: 1.0,   kcal: 90  },
    boiled_egg: { name: '🥚 ゆで卵 (1個)',        p: 6.5,  f: 5.0,  c: 0.2,   kcal: 76  },
    fried_egg:  { name: '🍳 目玉焼き (1個)',      p: 6.5,  f: 6.0,  c: 0.3,   kcal: 90  },
    yogurt:     { name: '🥣 ヨーグルト (プレーン)', p: 3.6,  f: 3.0,  c: 4.9,   kcal: 62  },
    yogurt_sw:  { name: '🥣 加糖ヨーグルト',      p: 3.0,  f: 2.0,  c: 12.0,  kcal: 80  },
    milk:       { name: '🥛 牛乳 (200ml)',       p: 6.8,  f: 7.8,  c: 9.9,   kcal: 138 },
    soymilk:    { name: '🥛 無調整豆乳 (200ml)',  p: 8.3,  f: 4.4,  c: 3.8,   kcal: 92  },
    cheese:     { name: '🧀 スライスチーズ (1枚)', p: 4.0,  f: 5.0,  c: 0.3,   kcal: 60  },
    cottage:    { name: '🧀 カッテージチーズ(100g)',p: 13.3, f: 4.5,  c: 1.9,   kcal: 101 },

    // 定番・おかず・健康食品
    natto:      { name: '🥢 納豆 (1パック)',      p: 8.0,  f: 5.0,  c: 6.0,   kcal: 100 },
    tofu:       { name: '🥢 豆腐 (半丁)',        p: 7.0,  f: 4.5,  c: 2.5,   kcal: 80  },
    chicken:    { name: '🍗 サラダチキン',       p: 25.0, f: 1.5,  c: 0.5,   kcal: 120 },
    salmon:     { name: '🐟 鮭の塩焼き (1切れ)',  p: 20.0, f: 8.0,  c: 0.1,   kcal: 150 },
    mackerel:   { name: '🐟 鯖の塩焼き (1切れ)',  p: 18.0, f: 16.0, c: 0.2,   kcal: 220 },
    sashimi:    { name: '🐟 刺身盛り合わせ',      p: 22.0, f: 3.0,  c: 0.2,   kcal: 120 },
    beef_steak: { name: '🥩 牛ヒレステーキ(100g)', p: 20.5, f: 4.8,  c: 0.3,   kcal: 130 },
    pork_ginger:{ name: '🐖 豚の生姜焼き (1人前)', p: 18.0, f: 20.0, c: 8.0,   kcal: 300 },
    yakitori:   { name: '🍢 焼き鳥 (もも塩3本)',  p: 15.0, f: 6.0,  c: 0.5,   kcal: 180 },
    karage:     { name: '🍗 鶏の唐揚げ (3個)',    p: 12.0, f: 15.0, c: 6.0,   kcal: 210 },
    hamburg:    { name: '🥩 ハンバーグ (1人前)',  p: 18.0, f: 22.0, c: 12.0,  kcal: 320 },
    gyoza:      { name: '🥟 餃子 (5個)',         p: 8.0,  f: 10.0, c: 20.0,  kcal: 200 },
    nugget:     { name: '🍗 チキンナゲット (5個)', p: 12.0, f: 15.0, c: 12.0,  kcal: 230 },
    tuna_can:   { name: '🐟 ツナ缶 (水煮1缶)',    p: 12.5, f: 0.2,  c: 0.1,   kcal: 53  },
    saba_can:   { name: '🐟 鯖の味噌煮缶 (1缶)',  p: 26.0, f: 18.0, c: 10.0,  kcal: 310 },
    chikuwa:    { name: '🍢 ちくわ (2本)',        p: 6.0,  f: 1.0,  c: 7.0,   kcal: 60  },
    sasakama:   { name: '🐟 笹かまぼこ (2枚)',    p: 7.0,  f: 0.5,  c: 4.0,   kcal: 50  },

    // 主食・ご飯・麺
    rice:       { name: '🍚 白米 (普通盛1杯)',     p: 3.8,  f: 0.4,  c: 55.7,  kcal: 240 },
    rice_large: { name: '🍚 白米 (大盛1杯)',       p: 4.0,  f: 0.5,  c: 55.0,  kcal: 240 },
    brown_rice: { name: '🍚 玄米 (普通盛1杯)',     p: 4.2,  f: 1.5,  c: 51.3,  kcal: 230 },
    oats:       { name: '🥣 オートミール (30g)',  p: 4.4,  f: 2.0,  c: 20.5,  kcal: 110 },
    onigiri_ume:{ name: '🍙 梅おにぎり',         p: 3.0,  f: 0.5,  c: 40.0,  kcal: 180 },
    onigiri_sha:{ name: '🍙 鮭おにぎり',         p: 4.5,  f: 1.0,  c: 40.0,  kcal: 190 },
    onigiri_may:{ name: '🍙 ツナマヨおにぎり',    p: 4.8,  f: 5.0,  c: 39.0,  kcal: 220 },
    curry:      { name: '🍛 カレーライス',       p: 15.0, f: 18.0, c: 90.0,  kcal: 650 },
    beef_bowl:  { name: '🐂 牛丼 (並盛)',         p: 20.0, f: 22.0, c: 95.0,  kcal: 700 },
    ramen:      { name: '🍜 醤油ラーメン',       p: 20.0, f: 20.0, c: 70.0,  kcal: 550 },
    udon:       { name: '🥢 かけうどん',         p: 8.0,  f: 1.0,  c: 55.0,  kcal: 280 },
    soba:       { name: '🥢 かけそば',           p: 12.0, f: 2.0,  c: 55.0,  kcal: 290 },
    pasta_toma: { name: '🍝 トマトパスタ',       p: 12.0, f: 8.0,  c: 75.0,  kcal: 450 },
    pasta_carb: { name: '🍝 カルボナーラ',       p: 20.0, f: 30.0, c: 70.0,  kcal: 680 },
    pizza:      { name: '🍕 ピザ (Mサイズ1切れ)', p: 8.0,  f: 8.0,  c: 24.0,  kcal: 200 },
    sandwich:   { name: '🥪 ミックスサンド',     p: 10.0, f: 12.0, c: 25.0,  kcal: 250 },
    croissant:  { name: '🥐 クロワッサン',       p: 4.0,  f: 11.0, c: 20.0,  kcal: 200 },

    // スープ・サラダ・野菜
    salad:      { name: '🥗 グリーンサラダ',     p: 1.0,  f: 0.2,  c: 4.0,   kcal: 20  },
    miso_soup:  { name: '🥣 味噌汁',             p: 1.5,  f: 0.8,  c: 3.5,   kcal: 35  },
    broccoli:   { name: '🥦 ブロッコリー (100g)', p: 4.3,  f: 0.5,  c: 5.2,   kcal: 33  },
    spinach:    { name: '🥬 ほうれん草 (100g)',   p: 2.2,  f: 0.4,  c: 3.1,   kcal: 20  },
    tomato:     { name: '🍅 トマト (中1個)',      p: 1.1,  f: 0.2,  c: 7.2,   kcal: 30  },
    avocado:    { name: '🥑 アボカド (半分)',     p: 1.3,  f: 13.0, c: 4.0,   kcal: 130 },
    konjac:     { name: '🥢 こんにゃく (100g)',   p: 0.1,  f: 0.0,  c: 2.3,   kcal: 7   },
    shirataki:  { name: '🥢 しらたき (100g)',     p: 0.2,  f: 0.0,  c: 3.0,   kcal: 6   },
    kimchi:     { name: '🥢 キムチ (50g)',       p: 1.0,  f: 0.2,  c: 2.6,   kcal: 23  },

    // 果物・おやつ・サプリ
    banana:     { name: '🍌 バナナ (1本)',        p: 1.1,  f: 0.2,  c: 22.5,  kcal: 86  },
    apple:      { name: '🍎 りんご (半分)',       p: 0.3,  f: 0.1,  c: 15.0,  kcal: 60  },
    orange:     { name: '🍊 オレンジ (1個)',      p: 1.0,  f: 0.1,  c: 20.0,  kcal: 80  },
    sweet_pot:  { name: '🍠 さつまいも (150g)',   p: 1.8,  f: 0.3,  c: 45.0,  kcal: 190 },
    nuts:       { name: '🥜 ミックスナッツ(25g)',  p: 5.0,  f: 15.0, c: 4.0,   kcal: 150 },
    chocolate:  { name: '🍫 チョコレート (25g)',   p: 2.0,  f: 15.0, c: 28.0,  kcal: 250 },
    protein:    { name: '🥤 プロテイン (ホエイ)',  p: 20.0, f: 1.5,  c: 3.0,   kcal: 120 },
    pudding:    { name: '🍮 プリン',             p: 5.0,  f: 5.0,  c: 20.0,  kcal: 150 },
    ice_cream:  { name: '🍨 バニラアイス',       p: 3.5,  f: 8.0,  c: 23.0,  kcal: 180 },

    // 飲み物・調味料
    yakult:     { name: '🍼 乳酸菌飲料 (1本)',    p: 0.8,  f: 0.1,  c: 11.5,  kcal: 50  },
    coffee:     { name: '☕ ブラックコーヒー',     p: 0.2,  f: 0.0,  c: 0.7,   kcal: 4   },
    latte:      { name: '☕ カフェラテ (200ml)',   p: 4.0,  f: 4.5,  c: 8.0,   kcal: 90  },
    green_tea:  { name: '🍵 緑茶',               p: 0.0,  f: 0.0,  c: 0.0,   kcal: 0   },
    coke:       { name: '🥤 コーラ (350ml)',     p: 0.0,  f: 0.0,  c: 40.0,  kcal: 160 },
    beer:       { name: '🍺 ビール (350ml缶)',    p: 1.0,  f: 0.0,  c: 10.5,  kcal: 140 },
    highball:   { name: '🥃 ハイボール',         p: 0.0,  f: 0.0,  c: 0.0,   kcal: 70  },
    olive_oil:  { name: '🧴 オリーブオイル(大1)', p: 0.0,  f: 12.0, c: 0.0,   kcal: 110 },
    butter:     { name: '🧈 バター (10g)',       p: 0.1,  f: 8.1,  c: 0.0,   kcal: 73  },
    mayonnaise: { name: '🧴 マヨネーズ (大1)',    p: 0.2,  f: 11.2, c: 0.1,   kcal: 100 },
    soy_sauce:  { name: '🧴 醤油 (大さじ1)',      p: 1.4,  f: 0.0,  c: 1.8,   kcal: 13  },
};

/** 食事メニューデータ（ロードされたデータがマージされます） */
let MEAL_MENU = {
    none:       { name: '選択しない',           p: 0,    f: 0,    c: 0,    kcal: 0   },
};

/** 食事の時間帯リスト（このリストを使い、同じタイプ名を何度も書かない） */
const MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack'];

/**
 * 1日の目標摂取栄養素（身長180cm・体重94kg・43歳・-20kgダイエット目標に基づいて計算）
 * 基礎代謞: 1,855 kcal / TDEE: 2,550 kcal / 赤字-750kcal = 目標 1,800 kcal
 * PFC配分: P:30% F:25% C:45%（ダイエット中の筋肉維持のためたんぱく質多め）
 */
let DAILY_TARGET = {
    kcal: 1800,
    p:    135,  // 1800 × 30% ÷ 4kcal/g
    f:    50,   // 1800 × 25% ÷ 9kcal/g
    c:    203,  // 1800 × 45% ÷ 4kcal/g
    water: 2000, // 1日の目標水分摂取量 (ml)
};

/** バイタル・活動の入力項目定義（ID・保存キー・型） */
const VITAL_FIELDS = [
    { id: 'weight-input',           key: 'weight',          type: 'float'  },
    { id: 'bodyfat-input',          key: 'bodyfat',         type: 'float'  },
    { id: 'bp-input',               key: 'bp',              type: 'string' },
    { id: 'bmi-input',              key: 'bmi',             type: 'float'  },
    { id: 'waist-input',            key: 'waist',           type: 'float'  },
    { id: 'visceral-fat-input',     key: 'visceralFat',     type: 'float'  },
    { id: 'subcutaneous-fat-input', key: 'subcutaneousFat', type: 'float'  },
    { id: 'muscle-input',           key: 'muscle',          type: 'float'  },
    { id: 'metabolism-input',       key: 'metabolism',      type: 'float'  },
    { id: 'body-age-input',         key: 'bodyAge',         type: 'int'    },
    { id: 'exercise-input',         key: 'exercise',        type: 'string' },
];

/**
 * グラフの各タブ設定（タブID → 描画に必要な設定をまとめた定義）
 * ここを追加・変更するだけでグラフタブを増減できる。
 */
const CHART_TAB_CONFIG = {
    weight: {
        label: '体重 (kg)',
        showWater: true,
        buildDatasets: (dates, data) => [{
            ...lineDatasetBase('体重 (kg)', '#ec4899', 'rgba(236, 72, 153, 0.08)'),
            data: dates.map(d => (data[d] || {}).weight || null),
        }],
    },
    bodyfat: {
        label: '体脂肪率 (%)',
        showWater: true,
        buildDatasets: (dates, data) => [{
            ...lineDatasetBase('体脂肪率 (%)', '#a855f7', 'rgba(168, 85, 247, 0.08)'),
            data: dates.map(d => (data[d] || {}).bodyfat || null),
        }],
    },
    bp: {
        label: '血圧 (mmHg)',
        showWater: false,
        buildDatasets: (dates, data) => {
            const systolic = [], diastolic = [];
            dates.forEach(d => {
                const bp = (data[d] || {}).bp || '';
                const m  = bp.match(/^(\d+)\s*\/\s*(\d+)$/);
                systolic.push(m  ? parseInt(m[1], 10) : null);
                diastolic.push(m ? parseInt(m[2], 10) : null);
            });
            return [
                { ...lineDatasetBase('最高血圧 (mmHg)', '#f97316', 'rgba(249, 115, 22, 0.08)'),  data: systolic  },
                { ...lineDatasetBase('最低血圧 (mmHg)', '#06b6d4', 'rgba(6, 182, 212, 0.08)'),   data: diastolic },
            ];
        },
    },
    waist: {
        label: 'ウエスト (cm)',
        showWater: true,
        buildDatasets: (dates, data) => [{
            ...lineDatasetBase('ウエスト (cm)', '#10b981', 'rgba(16, 185, 129, 0.08)'),
            data: dates.map(d => (data[d] || {}).waist || null),
        }],
    },
    bmi: {
        label: 'BMI',
        showWater: true,
        buildDatasets: (dates, data) => [{
            ...lineDatasetBase('BMI', '#3b82f6', 'rgba(59, 130, 246, 0.08)'),
            data: dates.map(d => (data[d] || {}).bmi || null),
        }],
    },
    muscle: {
        label: '割合 (%)',
        showWater: false,
        buildDatasets: (dates, data) => [
            { ...lineDatasetBase('骨格筋率 (%)',  '#10b981', 'rgba(16, 185, 129, 0.08)'), data: dates.map(d => (data[d] || {}).muscle         || null) },
            { ...lineDatasetBase('皮下脂肪率 (%)', '#ec4899', 'rgba(236, 72, 153, 0.08)'), data: dates.map(d => (data[d] || {}).subcutaneousFat || null) },
        ],
    },
    metabolism: {
        label: '基礎代謝 (kcal)',
        showWater: true,
        buildDatasets: (dates, data) => [{
            ...lineDatasetBase('基礎代謝 (kcal)', '#f59e0b', 'rgba(245, 158, 11, 0.08)'),
            data: dates.map(d => (data[d] || {}).metabolism || null),
        }],
    },
};

// ============================================================
// [2] アプリケーション状態（変わる値はここにまとめる）
// ============================================================

let selectedDate   = getFormattedDate(new Date()); // 選択中の日付（YYYY-MM-DD）
let weightChart    = null;                          // Chart.js インスタンス
let currentChartTab = 'weight';                    // 現在表示中のグラフタブ
let saveTimeout    = null;                          // 自動保存の遅延タイマー
let DOM            = {};                            // DOM要素キャッシュ
let lastActiveMealInputType = null;                 // 直前に「新しい食事を追加」を押した食事タイプ


// ============================================================
// [3] 初期化
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    cacheDOM();
    loadTargetSettings(); // 目標設定のロード
    loadMeals();          // 食事メニュー全体のロード
    generateMealOptions();

    if (DOM.datePicker) DOM.datePicker.value = selectedDate;

    setupEventListeners();
    loadDateData(selectedDate);
    updateDashboard();
});

/**
 * 主要なDOM要素を1か所でまとめてキャッシュする。
 * 画面の動作中は、この DOM オブジェクトを通じて要素にアクセスする。
 */
function cacheDOM() {
    DOM = {
        // 日付ナビゲーション
        datePicker: document.getElementById('date-picker'),
        prevBtn:    document.getElementById('prev-date-btn'),
        nextBtn:    document.getElementById('next-date-btn'),

        // 食事プルダウン
        mealBreakfast: document.getElementById('meal-breakfast'),
        mealLunch:     document.getElementById('meal-lunch'),
        mealDinner:    document.getElementById('meal-dinner'),
        mealSnack:     document.getElementById('meal-snack'),

        // 食事「追加」ボタン
        addBreakfastBtn: document.getElementById('add-breakfast-btn'),
        addLunchBtn:     document.getElementById('add-lunch-btn'),
        addDinnerBtn:    document.getElementById('add-dinner-btn'),
        addSnackBtn:     document.getElementById('add-snack-btn'),

        // 食事リスト表示エリア
        breakfastList: document.getElementById('breakfast-list'),
        lunchList:     document.getElementById('lunch-list'),
        dinnerList:    document.getElementById('dinner-list'),
        snackList:     document.getElementById('snack-list'),

        // 水分
        waterCurrent:  document.getElementById('water-current'),
        waterResetBtn: document.getElementById('water-reset-btn'),
        waterPctText:  document.getElementById('water-pct-text'),
        waterProgress: document.getElementById('water-progress'),

        // 今日のサマリー
        summaryWeight:  document.getElementById('summary-weight'),
        summaryBodyfat: document.getElementById('summary-bodyfat'),
        summaryBp:      document.getElementById('summary-bp'),
        summaryBmi:     document.getElementById('summary-bmi'),
        summaryWaist:   document.getElementById('summary-waist'),

        // PFC・カロリー
        totalCalories: document.getElementById('total-calories'),
        totalP:        document.getElementById('total-p'),
        totalF:        document.getElementById('total-f'),
        totalC:        document.getElementById('total-c'),
        pBar:          document.getElementById('p-bar'),
        fBar:          document.getElementById('f-bar'),
        cBar:          document.getElementById('c-bar'),

        // その他
        autosaveBadge: document.getElementById('autosave-badge'),
        chartCanvas:   document.getElementById('weightChart'),

        // PFC目標超過判定用のラベル要素
        labelP: document.getElementById('label-p'),
        labelF: document.getElementById('label-f'),
        labelC: document.getElementById('label-c'),

        // 設定トグルとパネル
        toggleSettingsBtn: document.getElementById('toggle-settings-btn'),
        settingsPanel:     document.getElementById('settings-panel'),
        
        // 目標設定の入力項目
        targetKcal:  document.getElementById('target-kcal-input'),
        targetP:     document.getElementById('target-p-input'),
        targetF:     document.getElementById('target-f-input'),
        targetC:     document.getElementById('target-c-input'),
        targetWater: document.getElementById('target-water-input'),
        
        // カスタム食事の入力項目
        customMealName:    document.getElementById('custom-meal-name'),
        customMealKcal:    document.getElementById('custom-meal-kcal'),
        customMealP:       document.getElementById('custom-meal-p'),
        customMealF:       document.getElementById('custom-meal-f'),
        customMealC:       document.getElementById('custom-meal-c'),
        saveCustomMealBtn: document.getElementById('save-custom-meal-btn'),
        customMealsTags:   document.getElementById('custom-meals-tags'),
    };

    // バイタル入力欄をキャッシュ（VITAL_FIELDSの定義から自動生成）
    VITAL_FIELDS.forEach(({ id, key }) => {
        DOM[key] = document.getElementById(id);
    });

    // 各食事タイプのメモリ上リスト（保存前のバッファ）
    // 例: DOM.mealLists.breakfast = ['toast', 'egg']
    DOM.mealLists = Object.fromEntries(MEAL_TYPES.map(t => [t, []]));
}

/**
 * 食事プルダウンの選択肢をMEAL_MENUから動的に生成する
 */
/**
 * 食事プルダウンの選択肢を再生成する
 * (カスタムドロップダウンになったため、すべてのドロップダウンを再レンダリングします)
 */
function generateMealOptions() {
    MEAL_TYPES.forEach(type => {
        const input = DOM[`meal${type.charAt(0).toUpperCase() + type.slice(1)}`];
        renderDropdown(type, input ? input.value : '');
    });
}

/**
 * カスタムドロップダウンの表示内容をレンダリングする
 * @param {string} type - 食事タイプ ('breakfast', 'lunch', 'dinner', 'snack')
 * @param {string} filterText - 絞り込みテキスト
 */
function renderDropdown(type, filterText = '') {
    const dropdown = document.getElementById(`dropdown-${type}`);
    if (!dropdown) return;

    dropdown.innerHTML = '';
    const cleanedFilter = cleanMealName(filterText);

    let hasItems = false;

    Object.entries(MEAL_MENU).forEach(([key, meal]) => {
        if (key === 'none') return;

        // 絞り込み処理
        if (cleanedFilter) {
            const cleanedName = cleanMealName(meal.name);
            if (!cleanedName.includes(cleanedFilter) && !key.toLowerCase().includes(cleanedFilter)) {
                return;
            }
        }

        hasItems = true;

        const item = document.createElement('div');
        item.className = 'meal-dropdown-item';
        
        // 項目が選択された時の処理 (mousedown を使い、input の blur より先に発火させる)
        item.addEventListener('mousedown', (e) => {
            // 削除ボタンがクリックされた場合は処理をスキップ
            if (e.target.classList.contains('meal-dropdown-item-delete')) {
                return;
            }
            addMealItem(type, key);
            const input = DOM[`meal${type.charAt(0).toUpperCase() + type.slice(1)}`];
            if (input) input.value = '';
            dropdown.classList.add('hidden');
            showToast(`「${meal.name}」を${getMealTypeName(type)}に追加しました`);
        });

        // 食べ物の名前とカロリーを表示するエリア
        const info = document.createElement('div');
        info.className = 'meal-dropdown-item-info';
        
        const nameSpan = document.createElement('span');
        nameSpan.textContent = meal.name;
        
        const kcalSpan = document.createElement('span');
        kcalSpan.className = 'meal-dropdown-item-kcal';
        kcalSpan.textContent = `(${meal.kcal} kcal)`;
        
        info.appendChild(nameSpan);
        info.appendChild(kcalSpan);
        item.appendChild(info);

        // 削除用の「×」ボタン
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'meal-dropdown-item-delete';
        deleteBtn.textContent = '×';
        deleteBtn.title = 'この食事をマイメニューから削除';
        deleteBtn.addEventListener('mousedown', (e) => {
            e.stopPropagation(); // 親要素の選択処理が走らないようにする
            e.preventDefault();  // フォーカスが外れないようにする
            removeCustomMeal(key, true); // ドロップダウン内からの削除は確認を省略
        });

        item.appendChild(deleteBtn);
        dropdown.appendChild(item);
    });

    // 検索結果がない場合
    if (!hasItems && cleanedFilter) {
        const noResult = document.createElement('div');
        noResult.style.padding = '0.75rem 1rem';
        noResult.style.color = 'var(--text-muted)';
        noResult.style.fontSize = '0.85rem';
        noResult.textContent = '一致する食事がありません';
        dropdown.appendChild(noResult);
    }

    // 最下部の「＋ 新しい食事を追加」ボタン
    const actionItem = document.createElement('div');
    actionItem.className = 'meal-dropdown-action-item';
    actionItem.innerHTML = `➕ 新しい食事を追加`;
    actionItem.addEventListener('mousedown', (e) => {
        e.stopPropagation();
        e.preventDefault(); // 入力欄からのフォーカス移動を防ぐ
        dropdown.classList.add('hidden');
        
        // どの食事タイプから新しい食事追加を押したかを記録
        lastActiveMealInputType = type;
        
        // 設定パネルを開く
        if (DOM.settingsPanel) {
            DOM.settingsPanel.classList.remove('hidden');
            // 目標値の設定を反映
            if (DOM.targetKcal)  DOM.targetKcal.value  = DAILY_TARGET.kcal;
            if (DOM.targetP)     DOM.targetP.value     = DAILY_TARGET.p;
            if (DOM.targetF)     DOM.targetF.value     = DAILY_TARGET.f;
            if (DOM.targetC)     DOM.targetC.value     = DAILY_TARGET.c;
            if (DOM.targetWater) DOM.targetWater.value = DAILY_TARGET.water;
        }
        
        // 新規登録の入力欄までスクロールして自動フォーカス
        if (DOM.customMealName) {
            DOM.customMealName.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => {
                DOM.customMealName.focus();
            }, 300);
        }
    });
    dropdown.appendChild(actionItem);
}

/**
 * 全てのイベントリスナーをセットアップする
 */
function setupEventListeners() {
    // 日付変更
    DOM.datePicker?.addEventListener('change', e => {
        selectedDate = e.target.value;
        loadDateData(selectedDate);
        updateDashboard();
    });

    // 前日・翌日ボタン
    DOM.prevBtn?.addEventListener('click', () => changeDate(-1));
    DOM.nextBtn?.addEventListener('click', () => changeDate(1));

    // 水分加算ボタン（+200ml / +500ml）
    document.querySelectorAll('.water-btn[data-amount]').forEach(btn => {
        btn.addEventListener('click', () => addWater(parseInt(btn.dataset.amount, 10)));
    });

    // 水分リセットボタン
    DOM.waterResetBtn?.addEventListener('click', resetWater);

    // バイタル入力（自動保存トリガー）
    VITAL_FIELDS.forEach(({ key }) => {
        DOM[key]?.addEventListener('input', e => triggerAutoSave(e.target));
    });

    // 食事入力フィールドとドロップダウンの制御イベント
    MEAL_TYPES.forEach(type => {
        const cap = type.charAt(0).toUpperCase() + type.slice(1);
        const input = DOM[`meal${cap}`];
        const dropdown = document.getElementById(`dropdown-${type}`);

        if (input && dropdown) {
            // フォーカス時にドロップダウンを表示
            input.addEventListener('focus', () => {
                document.querySelectorAll('.meal-dropdown-menu').forEach(menu => {
                    menu.classList.add('hidden');
                });
                renderDropdown(type, input.value);
                dropdown.classList.remove('hidden');
            });

            // 文字入力時に絞り込んで表示
            input.addEventListener('input', () => {
                renderDropdown(type, input.value);
                dropdown.classList.remove('hidden');
            });

            // フォーカスが外れたときに遅延して非表示にする (mousedownイベントの処理を確実に走らせるため)
            input.addEventListener('blur', () => {
                setTimeout(() => {
                    dropdown.classList.add('hidden');
                }, 200);
            });
        }
    });

    // 画面のどこかをクリックしたときにドロップダウンを閉じる処理
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.meal-add-row-wrapper')) {
            document.querySelectorAll('.meal-dropdown-menu').forEach(menu => {
                menu.classList.add('hidden');
            });
        }
    });

    // 食事「追加」ボタン（MEAL_TYPESをベースに対応を自動生成）
    MEAL_TYPES.forEach(type => {
        const cap    = type.charAt(0).toUpperCase() + type.slice(1);
        const btn    = DOM[`add${cap}Btn`];
        const input  = DOM[`meal${cap}`]; // input要素
        btn?.addEventListener('click', () => {
            const inputText = input?.value?.trim();
            if (!inputText) return;

            const existingKey = findMealKey(inputText);
            if (existingKey) {
                // 既存の食事が見つかった場合
                addMealItem(type, existingKey);
                const meal = MEAL_MENU[existingKey];
                showToast(`「${meal.name}」を${getMealTypeName(type)}に追加しました`);
                if (input) input.value = ''; // 入力欄をクリア
            } else {
                // 新規食事の場合、カロリーを聞く
                const cleanedName = inputText.replace(/\s*\(.*\)\s*/g, '').trim();
                if (!cleanedName) return;

                const calorieInput = prompt(`「${cleanedName}」のカロリー(kcal)を入力してください：`, "200");
                if (calorieInput === null) return; // キャンセルされた場合

                const kcal = parseFloat(calorieInput) || 0;
                const newKey = `custom_${Date.now()}`;
                
                // 入力されたカロリー値からPFC（タンパク質20%、脂質25%、炭水化物55%）を自動推定して入力
                const p = round1((kcal * 0.20) / 4);
                const f = round1((kcal * 0.25) / 9);
                const c = round1((kcal * 0.55) / 4);

                MEAL_MENU[newKey] = {
                    name: `⭐ ${cleanedName}`,
                    kcal: kcal,
                    p: p,
                    f: f,
                    c: c
                };

                saveMealsToStorage(); // 食事メニュー全体を保存
                generateMealOptions();
                renderCustomMealsTags();
                addMealItem(type, newKey);
                showToast(`「${cleanedName}」を新しく登録し、${getMealTypeName(type)}に追加しました`);
                if (input) input.value = ''; // 入力欄をクリア
            }
        });
    });

    // グラフ切り替えタブ
    const chartTabs = document.querySelectorAll('.chart-tab');
    chartTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            chartTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentChartTab = tab.dataset.tab;
            updateChart();
        });
    });

    // 設定トグルのイベント
    DOM.toggleSettingsBtn?.addEventListener('click', toggleSettingsPanel);

    // 目標設定 of 入力イベント
    [DOM.targetKcal, DOM.targetP, DOM.targetF, DOM.targetC, DOM.targetWater].forEach(input => {
        input?.addEventListener('input', saveTargetSettings);
    });

    // カスタム食事の登録ボタン
    DOM.saveCustomMealBtn?.addEventListener('click', addCustomMeal);

    // マイ食事メニュー追加の「食事の名前」入力時に、既存メニューからカロリーやPFCを自動補完する
    DOM.customMealName?.addEventListener('input', () => {
        const nameVal = DOM.customMealName.value.trim();
        if (!nameVal) return;
        
        const existingKey = findMealKey(nameVal);
        if (existingKey) {
            const meal = MEAL_MENU[existingKey];
            if (DOM.customMealKcal) DOM.customMealKcal.value = meal.kcal;
            if (DOM.customMealP)    DOM.customMealP.value = meal.p;
            if (DOM.customMealF)    DOM.customMealF.value = meal.f;
            if (DOM.customMealC)    DOM.customMealC.value = meal.c;
        }
    });

    // カスタム食事入力欄での Enter キー押下で登録
    [DOM.customMealName, DOM.customMealKcal, DOM.customMealP, DOM.customMealF, DOM.customMealC].forEach(input => {
        input?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // フォーム送信を防ぐ
                addCustomMeal();
            }
        });
    });

}

// ============================================================
// [4] データ層（読み書き）
// ============================================================

/** ローカルストレージから全記録データを取得する */
function getAllData() {
    const raw = localStorage.getItem('health_tracker_data');
    return raw ? JSON.parse(raw) : {};
}

/** ローカルストレージに全記録データを保存する */
function saveAllData(data) {
    localStorage.setItem('health_tracker_data', JSON.stringify(data));
}

/**
 * 選択中の日付のデータを読み込み、画面の各入力欄に反映する
 */
function loadDateData(dateStr) {
    const dayData = getAllData()[dateStr] || {};

    // 食事リストを復元（旧形式の文字列も自動でリスト変換して引き継ぐ）
    MEAL_TYPES.forEach(type => {
        DOM.mealLists[type] = normalizeMealData(dayData[type]);
        renderMealList(type);
    });

    // バイタル入力欄の復元
    VITAL_FIELDS.forEach(({ key }) => {
        const val = dayData[key];
        if (DOM[key]) DOM[key].value = (val !== undefined && val !== null) ? val : '';
    });

    // 水分の復元
    updateWaterDisplay(dayData.water || 0);
}

/**
 * フォーム全体のデータを収集してローカルストレージへ保存する
 */
function saveCurrentData(changedElement) {
    const allData = getAllData();
    const dayData = {};

    // 食事データ（リスト形式）
    MEAL_TYPES.forEach(type => {
        dayData[type] = DOM.mealLists[type] || [];
    });

    // 水分
    dayData.water = parseInt(DOM.waterCurrent?.textContent || '0', 10) || 0;

    // バイタル・活動
    VITAL_FIELDS.forEach(({ key, type }) => {
        const input = DOM[key];
        if (!input) return;
        const val = input.value;
        if (val === '') {
            dayData[key] = type === 'string' ? '' : null;
        } else {
            dayData[key] = type === 'float' ? parseFloat(val)
                         : type === 'int'   ? parseInt(val, 10)
                         : val.trim();
        }
    });

    allData[selectedDate] = dayData;
    saveAllData(allData);

    // 自動保存バッジを「保存済み」表示に戻す
    setAutosaveBadge(false);
    applySaveGlow(changedElement);

    // 軽量モードで更新（カレンダー・履歴の重い再描画はスキップ）
    updateDashboard(true);
}

// ============================================================
// [5] 食事リスト管理
// ============================================================

/**
 * 保存データの形式を正規化する。
 * 旧形式（文字列）→ リスト変換、新形式（配列）→ そのまま利用。
 * @param {string|string[]|undefined} saved
 * @returns {string[]}
 */
function normalizeMealData(saved) {
    if (Array.isArray(saved))                                    return saved.filter(k => k && k !== 'none');
    if (typeof saved === 'string' && saved !== 'none' && saved)  return [saved];
    return [];
}

/**
 * 指定した食事タイプのリストにメニューを1件追加する
 */
function addMealItem(type, key) {
    DOM.mealLists[type] = DOM.mealLists[type] || [];
    DOM.mealLists[type].push(key);
    renderMealList(type);
    triggerAutoSave(null);
}

/**
 * 指定した食事タイプのリストから指定位置のメニューを削除する
 */
function removeMealItem(type, index) {
    DOM.mealLists[type]?.splice(index, 1);
    renderMealList(type);
    triggerAutoSave(null);
}

/**
 * 指定した食事タイプの「選んだ食事カード」と「合計栄養タグ」を再描画する
 */
function renderMealList(type) {
    const cap          = type.charAt(0).toUpperCase() + type.slice(1);
    const listDiv      = DOM[`${type}List`];
    const nutritionDiv = document.getElementById(`${type}-nutrition`);
    const items        = DOM.mealLists[type] || [];

    // --- 食事カード（タグ）の描画 ---
    if (listDiv) {
        listDiv.innerHTML = '';
        items.forEach((key, idx) => {
            const meal = MEAL_MENU[key];
            if (!meal) return;

            const tag       = document.createElement('span');
            tag.className   = 'meal-item-tag';

            const nameSpan  = document.createElement('span');
            nameSpan.textContent = meal.name;

            const removeBtn = document.createElement('button');
            removeBtn.className   = 'meal-item-remove';
            removeBtn.textContent = '×';
            removeBtn.title       = `${meal.name} を削除`;
            removeBtn.addEventListener('click', () => removeMealItem(type, idx));

            tag.append(nameSpan, removeBtn);
            listDiv.appendChild(tag);
        });
    }

    // --- 合計栄養タグの描画 ---
    if (nutritionDiv) {
        if (items.length === 0) {
            nutritionDiv.innerHTML = '';
        } else {
            const totals = sumNutrition(items);
            nutritionDiv.innerHTML = `
                <span class="nutri-tag cal">🔥 ${totals.kcal} kcal</span>
                <span class="nutri-tag p">P 🥩 たんぱく質: ${round1(totals.p)}g</span>
                <span class="nutri-tag f">F 🧈 脂質: ${round1(totals.f)}g</span>
                <span class="nutri-tag c">C 🍚 炭水化物: ${round1(totals.c)}g</span>
            `;
        }
    }
}

// ============================================================
// [6] 水分管理
// ============================================================

/**
 * 水分摂取量の表示（数値・パーセントバー）を更新する
 */
function updateWaterDisplay(value) {
    const goal = DAILY_TARGET.water || 2000;
    const pct  = Math.min(Math.round((value / goal) * 100), 100);
    if (DOM.waterCurrent)  DOM.waterCurrent.textContent  = value;
    if (DOM.waterPctText)  DOM.waterPctText.textContent  = `${pct}%`;
    if (DOM.waterProgress) DOM.waterProgress.style.width = `${pct}%`;
    // 画面の目標水分量表示も更新する
    const unitEl = DOM.waterCurrent?.nextElementSibling;
    if (unitEl && unitEl.classList.contains('unit')) {
        unitEl.textContent = `/ ${goal} ml`;
    }
}

/** 水分摂取量を加算する */
function addWater(amount) {
    const current = parseInt(DOM.waterCurrent?.textContent || '0', 10) || 0;
    updateWaterDisplay(current + amount);
    saveCurrentData();
}

/** 水分摂取量をゼロにリセットする */
function resetWater() {
    updateWaterDisplay(0);
    saveCurrentData();
}

// ============================================================
// [7] 自動保存
// ============================================================

/**
 * 入力の手が止まってから500ms後に保存を実行するタイマーを設定する
 */
function triggerAutoSave(changedElement) {
    setAutosaveBadge(true);
    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => saveCurrentData(changedElement), 500);
}

/**
 * 自動保存バッジの表示を切り替える
 * @param {boolean} isSaving - true: 「保存中…」, false: 「自動保存済」
 */
function setAutosaveBadge(isSaving) {
    if (!DOM.autosaveBadge) return;
    const span = DOM.autosaveBadge.querySelector('span');
    if (isSaving) {
        DOM.autosaveBadge.classList.add('saving');
        if (span) span.textContent = '保存中...';
    } else {
        DOM.autosaveBadge.classList.remove('saving');
        if (span) span.textContent = '自動保存済';
    }
}

/**
 * 自動保存時、入力欄を一瞬光らせるエフェクトを適用する。
 * SELECT要素はプルダウンが閉じるバグを防ぐため対象外とする。
 */
function applySaveGlow(el) {
    if (el && el.tagName !== 'SELECT') {
        el.classList.remove('autosave-glow');
        void el.offsetWidth; // アニメーション再実行のトリガー
        el.classList.add('autosave-glow');
    }
}

// ============================================================
// [8] ダッシュボード表示
// ============================================================

/**
 * ダッシュボード全体（サマリー・グラフ・カレンダー・履歴）を更新する
 * @param {boolean} lightweight - true の場合、カレンダー・履歴の重い再描画をスキップ
 */
function updateDashboard(lightweight = false) {
    const todayData = getAllData()[selectedDate] || {};

    // サマリーカードの各値を更新
    setSummary(DOM.summaryWeight,  todayData.weight,  'weight',  ' kg');
    setSummary(DOM.summaryBodyfat, todayData.bodyfat, 'bodyfat', ' %');
    setSummary(DOM.summaryBp,      todayData.bp,      'bp',      ' mmHg');
    setSummary(DOM.summaryBmi,     todayData.bmi,     'bmi',     '');
    setSummary(DOM.summaryWaist,   todayData.waist,   'waist',   ' cm');

    updatePfcSummary(todayData);
    updateChart();

    if (!lightweight) {
        renderCalendar();
        renderHistoryList();
    }
}

/**
 * サマリーカードの1要素を更新する。
 * 今日のデータがなければ直近の記録値を「(直近)」付きで表示する。
 */
function setSummary(el, currentVal, key, suffix) {
    if (!el) return;
    if (currentVal !== undefined && currentVal !== null && currentVal !== '') {
        el.textContent = `${currentVal}${suffix}`;
    } else {
        const latest = findLatestValue(key);
        el.textContent = latest !== null ? `${latest}${suffix} (直近)` : `- ${suffix}`.trim();
    }
}

/**
 * 全記録の中から、指定キーの最新の記録値を返す
 */
function findLatestValue(key) {
    const data   = getAllData();
    const sorted = Object.keys(data).sort((a, b) => new Date(b) - new Date(a));
    for (const d of sorted) {
        const val = data[d]?.[key];
        if (val !== undefined && val !== null && val !== '') return val;
    }
    return null;
}

/**
 * 今日の総カロリー・PFCバランスバーを更新する。
 * 目標値（DAILY_TARGET）を超えた項目は赤色（over-limit）に切り替える。
 */
function updatePfcSummary(dayData) {
    // 全食事タイプのメニューキーを1つの配列に集める（旧形式・新形式の両方に対応）
    const allKeys = MEAL_TYPES.flatMap(type => normalizeMealData(dayData[type]));
    const totals  = sumNutrition(allKeys);

    // カロリー表示（実績 / 目標 kcal）＋ 超過時に赤色
    if (DOM.totalCalories) {
        DOM.totalCalories.textContent = `${Math.round(totals.kcal)} / ${DAILY_TARGET.kcal} kcal`;
        DOM.totalCalories.classList.toggle('over-limit', totals.kcal > DAILY_TARGET.kcal);
    }

    // PFCの目標表示と実績の更新
    if (DOM.labelP) DOM.labelP.innerHTML = `P 🥩 たんぱく質: <b id="total-p">${round1(totals.p)}</b> / ${DAILY_TARGET.p}g`;
    if (DOM.labelF) DOM.labelF.innerHTML = `F 🧈 脂質: <b id="total-f">${round1(totals.f)}</b> / ${DAILY_TARGET.f}g`;
    if (DOM.labelC) DOM.labelC.innerHTML = `C 🍚 炭水化物: <b id="total-c">${round1(totals.c)}</b> / ${DAILY_TARGET.c}g`;

    // innerHTMLで再構築されたID要素をキャッシュに再ロード
    DOM.totalP = document.getElementById('total-p');
    DOM.totalF = document.getElementById('total-f');
    DOM.totalC = document.getElementById('total-c');

    // 目標超過時にラベル全体を赤色に切り替える
    DOM.labelP?.classList.toggle('over-limit', totals.p > DAILY_TARGET.p);
    DOM.labelF?.classList.toggle('over-limit', totals.f > DAILY_TARGET.f);
    DOM.labelC?.classList.toggle('over-limit', totals.c > DAILY_TARGET.c);

    // PFC割合バー（摂取したP:F:C の比率を表示）
    const totalGrams = totals.p + totals.f + totals.c;
    if (totalGrams > 0) {
        if (DOM.pBar) DOM.pBar.style.width = `${(totals.p / totalGrams) * 100}%`;
        if (DOM.fBar) DOM.fBar.style.width = `${(totals.f / totalGrams) * 100}%`;
        if (DOM.cBar) DOM.cBar.style.width = `${(totals.c / totalGrams) * 100}%`;
    } else {
        [DOM.pBar, DOM.fBar, DOM.cBar].forEach(b => { if (b) b.style.width = '0%'; });
    }
}


/**
 * 日付の選択を指定した日数分ずらす
 */
function changeDate(daysOffset) {
    const d = new Date(selectedDate);
    d.setDate(d.getDate() + daysOffset);
    selectedDate = getFormattedDate(d);
    if (DOM.datePicker) DOM.datePicker.value = selectedDate;
    loadDateData(selectedDate);
    updateDashboard();
}

// ============================================================
// [9] グラフ
// ============================================================

/**
 * 過去7日間の推移グラフを描画する。
 * CHART_TAB_CONFIG の設定に基づき、各タブのデータセットを構築する。
 */
function updateChart() {
    if (!DOM.chartCanvas) return;

    const data    = getAllData();
    const base    = new Date(selectedDate);
    const dates   = Array.from({ length: 7 }, (_, i) => {
        const d = new Date(base);
        d.setDate(base.getDate() - (6 - i));
        return getFormattedDate(d);
    });
    const labels  = dates.map(d => { const dt = new Date(d); return `${dt.getMonth() + 1}/${dt.getDate()}`; });

    const config  = CHART_TAB_CONFIG[currentChartTab] || CHART_TAB_CONFIG.weight;
    const datasets = config.buildDatasets(dates, data).map(ds => ({
        borderWidth: 3, pointRadius: 4, pointHoverRadius: 6,
        tension: 0.3, spanGaps: true, yAxisID: 'yPrimary',
        ...ds,
    }));

    // 水分の棒グラフは一部のタブにのみ表示する
    if (config.showWater) {
        datasets.push({
            label: '水分 (ml)',
            type: 'bar',
            data: dates.map(d => (data[d] || {}).water || 0),
            backgroundColor: 'rgba(59, 130, 246, 0.12)',
            borderColor:     'rgba(59, 130, 246, 0.25)',
            borderWidth: 1, borderRadius: 5,
            yAxisID: 'ySecondary',
        });
    }

    weightChart?.destroy();

    const scalesConfig = {
        x:        { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
        yPrimary: {
            type: 'linear', position: 'left',
            grid:  { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#94a3b8' },
            title: { display: true, text: config.label, color: '#94a3b8' },
        },
    };
    if (config.showWater) {
        scalesConfig.ySecondary = {
            type: 'linear', position: 'right',
            grid:  { drawOnChartArea: false },
            ticks: { color: '#94a3b8' },
            title: { display: true, text: '水分 (ml)', color: '#3b82f6' },
            min: 0, max: Math.max((DAILY_TARGET.water || 2000) + 1000, 3000),
        };
    }

    weightChart = new Chart(DOM.chartCanvas.getContext('2d'), {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend:  { labels: { color: '#94a3b8', font: { family: 'Outfit, Noto Sans JP' } } },
                tooltip: { mode: 'index', intersect: false },
            },
            scales: scalesConfig,
        },
    });
}

/**
 * 線グラフのデータセットに共通するプロパティを返す（CHART_TAB_CONFIGの内部で使用）
 */
function lineDatasetBase(label, color, bgColor) {
    return { label, borderColor: color, backgroundColor: bgColor, pointBackgroundColor: color };
}

// ============================================================
// [10] カレンダー・履歴
// ============================================================

/**
 * 月カレンダーを描画する
 */
function renderCalendar() {
    const grid = document.getElementById('calendar-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const data  = getAllData();
    const d     = new Date(selectedDate);
    const year  = d.getFullYear();
    const month = d.getMonth();

    // 月ヘッダー
    const title = document.createElement('div');
    title.className = 'calendar-title-wrapper';
    Object.assign(title.style, { gridColumn: 'span 7', textAlign: 'center', fontWeight: '700', marginBottom: '0.5rem' });
    title.textContent = `${year}年 ${month + 1}月`;
    grid.appendChild(title);

    // 曜日ヘッダー
    ['日', '月', '火', '水', '木', '金', '土'].forEach(day => {
        const h = document.createElement('div');
        h.className   = 'calendar-header';
        h.textContent = day;
        grid.appendChild(h);
    });

    // 月初の空白セル
    const startDow = new Date(year, month, 1).getDay();
    for (let i = 0; i < startDow; i++) {
        const e = document.createElement('div');
        e.className = 'calendar-day empty';
        grid.appendChild(e);
    }

    // 日付セル
    const totalDays = new Date(year, month + 1, 0).getDate();
    for (let day = 1; day <= totalDays; day++) {
        const dateStr = getFormattedDate(new Date(year, month, day));
        const cell    = document.createElement('div');
        cell.className = 'calendar-day';
        if (dateStr === selectedDate) cell.classList.add('active');
        if (data[dateStr])            cell.classList.add('has-data');

        const num = document.createElement('span');
        num.className   = 'day-number';
        num.textContent = day;
        cell.appendChild(num);

        cell.addEventListener('click', () => {
            selectedDate = dateStr;
            if (DOM.datePicker) DOM.datePicker.value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });

        grid.appendChild(cell);
    }
}

/**
 * 最近5件の記録を履歴リストに描画する
 */
function renderHistoryList() {
    const list = document.getElementById('history-list');
    if (!list) return;
    list.innerHTML = '';

    const data   = getAllData();
    const sorted = Object.keys(data).sort((a, b) => new Date(b) - new Date(a));

    if (sorted.length === 0) {
        const msg = document.createElement('div');
        Object.assign(msg.style, { color: 'var(--text-muted)', textAlign: 'center', padding: '2rem 0' });
        msg.textContent = '記録がまだありません';
        list.appendChild(msg);
        return;
    }

    sorted.slice(0, 5).forEach(dateStr => {
        const dayData = data[dateStr];
        const dObj    = new Date(dateStr);

        const hasMeals = MEAL_TYPES.some(type => {
            const val = dayData[type];
            return Array.isArray(val) ? val.length > 0 : (val && val !== 'none');
        });

        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div class="history-item-header">
                <span class="history-item-date">${dObj.getMonth() + 1}月${dObj.getDate()}日</span>
                <span class="history-item-weight">${dayData.weight ? `${dayData.weight}kg` : '-- kg'}</span>
            </div>
            <div class="history-item-summary">
                <div class="history-summary-tag">
                    <i data-lucide="utensils" style="color: var(--accent-orange)"></i>
                    <span>${hasMeals ? '食事あり' : '未記録'}</span>
                </div>
                <div class="history-summary-tag">
                    <i data-lucide="droplet" style="color: var(--accent-blue)"></i>
                    <span>${dayData.water || 0}ml</span>
                </div>
                <div class="history-summary-tag">
                    <i data-lucide="activity" style="color: var(--accent-emerald)"></i>
                    <span>${dayData.exercise ? '運動あり' : 'なし'}</span>
                </div>
            </div>
        `;
        item.addEventListener('click', () => {
            selectedDate = dateStr;
            if (DOM.datePicker) DOM.datePicker.value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });
        list.appendChild(item);
    });

    lucide.createIcons();
}

// ============================================================
// [11] ユーティリティ
// ============================================================

/**
 * Dateオブジェクトを YYYY-MM-DD 形式の文字列に変換する
 */
function getFormattedDate(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

/**
 * メニューキーの配列から栄養素の合計を計算して返す
 * @param {string[]} keys
 * @returns {{ kcal: number, p: number, f: number, c: number }}
 */
function sumNutrition(keys) {
    return keys.reduce((acc, key) => {
        const meal = MEAL_MENU[key];
        if (meal) {
            acc.kcal += meal.kcal;
            acc.p    += meal.p;
            acc.f    += meal.f;
            acc.c    += meal.c;
        }
        return acc;
    }, { kcal: 0, p: 0, f: 0, c: 0 });
}

/**
 * 小数点第1位で四捨五入する（例: 1.25 → 1.3）
 */
function round1(x) {
    return Math.round(x * 10) / 10;
}

// ============================================================
// [12] 設定パネル機能（目標設定とカスタム食事）
// ============================================================

/**
 * 設定パネルの表示・非表示を切り替える
 */
function toggleSettingsPanel() {
    if (!DOM.settingsPanel) return;
    DOM.settingsPanel.classList.toggle('hidden');
    
    // 開いた際、現在の設定値を入力を反映する
    if (!DOM.settingsPanel.classList.contains('hidden')) {
        if (DOM.targetKcal)  DOM.targetKcal.value  = DAILY_TARGET.kcal;
        if (DOM.targetP)     DOM.targetP.value     = DAILY_TARGET.p;
        if (DOM.targetF)     DOM.targetF.value     = DAILY_TARGET.f;
        if (DOM.targetC)     DOM.targetC.value     = DAILY_TARGET.c;
        if (DOM.targetWater) DOM.targetWater.value = DAILY_TARGET.water;
    }
}

/**
 * 画面から変更された目標設定をローカルストレージに保存する
 */
function saveTargetSettings() {
    DAILY_TARGET.kcal  = parseFloat(DOM.targetKcal?.value) || 1800;
    DAILY_TARGET.p     = parseFloat(DOM.targetP?.value) || 135;
    DAILY_TARGET.f     = parseFloat(DOM.targetF?.value) || 50;
    DAILY_TARGET.c     = parseFloat(DOM.targetC?.value) || 203;
    DAILY_TARGET.water = parseFloat(DOM.targetWater?.value) || 2000;

    localStorage.setItem('health_tracker_target_settings', JSON.stringify(DAILY_TARGET));
    
    // 水分表示とダッシュボード・グラフを即座に更新する
    const currentWater = parseInt(DOM.waterCurrent?.textContent || '0', 10) || 0;
    updateWaterDisplay(currentWater);
    updateDashboard(true);
}

/**
 * 目標設定をローカルストレージから読み込む
 */
function loadTargetSettings() {
    const raw = localStorage.getItem('health_tracker_target_settings');
    if (raw) {
        try {
            DAILY_TARGET = JSON.parse(raw);
        } catch (e) {
            console.error('目標設定の読み込みに失敗しました:', e);
        }
    }
}

/**
 * 食事メニューをローカルストレージから読み込み、MEAL_MENUにマージする
 */
function loadMeals() {
    const raw = localStorage.getItem('health_tracker_meals');
    if (raw) {
        try {
            const savedMeals = JSON.parse(raw);
            // 最新の DEFAULT_MEAL_MENU と保存されているマイメニュー・カスタムメニューをマージする
            MEAL_MENU = {
                none: { name: '選択しない', p: 0, f: 0, c: 0, kcal: 0 },
                ...DEFAULT_MEAL_MENU,
                ...savedMeals
            };
        } catch (e) {
            console.error('食事メニューの読み込みに失敗しました:', e);
            MEAL_MENU = {
                none: { name: '選択しない', p: 0, f: 0, c: 0, kcal: 0 },
                ...DEFAULT_MEAL_MENU
            };
        }
    } else {
        // 初回起動時はデフォルト値を設定して保存
        MEAL_MENU = {
            none: { name: '選択しない', p: 0, f: 0, c: 0, kcal: 0 },
            ...DEFAULT_MEAL_MENU
        };
        saveMealsToStorage();
    }
    renderCustomMealsTags();
}

/**
 * 画面で入力されたマイ食事メニューを登録して保存する
 */
function addCustomMeal() {
    const name = DOM.customMealName?.value?.trim();
    const kcal = parseFloat(DOM.customMealKcal?.value) || 0;
    const p    = parseFloat(DOM.customMealP?.value) || 0;
    const f    = parseFloat(DOM.customMealF?.value) || 0;
    const c    = parseFloat(DOM.customMealC?.value) || 0;

    if (!name) {
        alert('食事の名前を入力してください。');
        return;
    }

    // 重複を避けるための識別キーを生成
    const key = `custom_${Date.now()}`;
    
    // 新しいメニューオブジェクトを作成
    const newMeal = {
        name: `⭐ ${name}`, // マイメニューであることが分かりやすいように星マークを付与
        kcal: kcal,
        p: p,
        f: f,
        c: c
    };

    // メモリ上のメニューデータにマージ
    MEAL_MENU[key] = newMeal;

    // ローカルストレージに食事メニュー全体を保存
    saveMealsToStorage();

    // 入力フォームをクリア
    if (DOM.customMealName) DOM.customMealName.value = '';
    if (DOM.customMealKcal) DOM.customMealKcal.value = '';
    if (DOM.customMealP)    DOM.customMealP.value = '';
    if (DOM.customMealF)    DOM.customMealF.value = '';
    if (DOM.customMealC)    DOM.customMealC.value = '';

    // プルダウンの選択肢を再生成
    generateMealOptions();
    // 登録済みタグ一覧を更新
    renderCustomMealsTags();

    // 自動追加と自動スクロールバックの制御
    if (lastActiveMealInputType) {
        // 元の食事タイプに自動追加
        addMealItem(lastActiveMealInputType, key);
        showToast(`マイメニュー「${name}」を登録し、${getMealTypeName(lastActiveMealInputType)}に追加しました`);
        
        // 設定パネルを閉じる
        if (DOM.settingsPanel) {
            DOM.settingsPanel.classList.add('hidden');
        }
        
        // 元の食事入力欄までスクロール
        const cap = lastActiveMealInputType.charAt(0).toUpperCase() + lastActiveMealInputType.slice(1);
        const input = DOM[`meal${cap}`];
        if (input) {
            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => {
                input.focus();
            }, 300);
        }
        
        // 状態をリセット
        lastActiveMealInputType = null;
    } else {
        showToast(`マイメニュー「${name}」を追加しました`);
    }
}

/**
 * 食事メニュー全体（noneを除く）をローカルストレージに保存する
 */
function saveMealsToStorage() {
    const mealsToSave = {};
    Object.entries(MEAL_MENU).forEach(([key, meal]) => {
        if (key !== 'none') {
            mealsToSave[key] = meal;
        }
    });
    localStorage.setItem('health_tracker_meals', JSON.stringify(mealsToSave));
}

/**
 * 登録済みの食事メニューを削除する
 * @param {string} key - 削除するメニューの識別キー
 * @param {boolean} bypassConfirm - 確認ダイアログをスキップするかどうか
 */
function removeCustomMeal(key, bypassConfirm = false) {
    const meal = MEAL_MENU[key];
    if (!meal) return;
    const name = meal.name.replace('⭐ ', '');
    if (bypassConfirm || confirm(`この食事メニュー「${name}」を削除しますか？\n(すでにその日の食事として記録されている項目は、そのまま計算に残ります)`)) {
        delete MEAL_MENU[key];
        saveMealsToStorage();
        generateMealOptions();
        renderCustomMealsTags();
        showToast(`マイメニュー「${name}」を削除しました`);
    }
}

/**
 * 登録されているすべての食事メニュー（noneを除く）をタグで描画する
 */
function renderCustomMealsTags() {
    if (!DOM.customMealsTags) return;
    DOM.customMealsTags.innerHTML = '';

    let hasMeals = false;
    Object.entries(MEAL_MENU).forEach(([key, meal]) => {
        if (key === 'none') return;
        hasMeals = true;

        const tag = document.createElement('span');
        tag.className = 'custom-meal-tag';
        tag.textContent = `${meal.name.replace('⭐ ', '')} (${meal.kcal}kcal)`;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'custom-meal-tag-remove';
        removeBtn.textContent = '×';
        removeBtn.title = 'このメニューを削除';
        removeBtn.addEventListener('click', () => removeCustomMeal(key));

        tag.appendChild(removeBtn);
        DOM.customMealsTags.appendChild(tag);
    });

    if (!hasMeals) {
        const msg = document.createElement('span');
        msg.style.color = 'var(--text-muted)';
        msg.style.fontSize = '0.85rem';
        msg.textContent = '登録済みのマイメニューはありません';
        DOM.customMealsTags.appendChild(msg);
    }
}

// ============================================================
// [13] あいまい検索とトースト通知ヘルパー関数
// ============================================================

/**
 * 比較のために食事名から絵文字、余計な記号、スペース、括弧書きを除去する
 */
function cleanMealName(name) {
    if (!name) return '';
    return name
        .replace(/[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDC00-\uDFFF]/g, '') // 絵文字除去
        .replace(/\s+/g, '') // 全半角空白除去
        .replace(/\([^)]*\)/g, '') // 半角カッコとその中身除去
        .replace(/（[^）]*）/g, '') // 全角カッコとその中身除去
        .toLowerCase()
        .trim();
}

/**
 * 入力されたテキストから既存メニュー(MEAL_MENU)のキーを特定する（あいまい検索）
 */
function findMealKey(inputText) {
    if (!inputText) return null;
    const cleanedInput = cleanMealName(inputText);
    if (!cleanedInput) return null;

    // 1. クリーンアップ後の完全一致、またはキー名との完全一致を探す
    for (const [key, meal] of Object.entries(MEAL_MENU)) {
        if (key === 'none') continue;
        if (key.toLowerCase() === cleanedInput) return key;
        if (cleanMealName(meal.name) === cleanedInput) return key;
    }

    // 2. 部分一致を探す（入力値がメニュー名に含まれる、またはメニュー名が入力値に含まれる）
    for (const [key, meal] of Object.entries(MEAL_MENU)) {
        if (key === 'none') continue;
        const cleanedMenuName = cleanMealName(meal.name);
        if (cleanedMenuName.includes(cleanedInput) || cleanedInput.includes(cleanedMenuName)) {
            return key;
        }
    }

    return null;
}

/**
 * 画面にフワッとお知らせを表示するトースト通知機能
 */
function showToast(message) {
    const toast = document.getElementById('toast-notification');
    const toastMsg = document.getElementById('toast-message');
    if (toast && toastMsg) {
        toastMsg.textContent = message;
        toast.classList.add('show');
        
        if (window.toastTimer) {
            clearTimeout(window.toastTimer);
        }
        window.toastTimer = setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

/**
 * 食事の時間帯を日本語名に変換する
 */
function getMealTypeName(type) {
    switch (type) {
        case 'breakfast': return '朝食';
        case 'lunch':     return '昼食';
        case 'dinner':    return '晩御飯';
        case 'snack':     return 'おやつ';
        default:          return '食事';
    }
}

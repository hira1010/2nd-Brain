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

/** 食事メニューデータ（P:たんぱく質, F:脂質, C:炭水化物, kcal:カロリー） */
const MEAL_MENU = {
    none:       { name: '選択しない',           p: 0,    f: 0,    c: 0,    kcal: 0   },
    toast:      { name: '🍞 トースト',           p: 6,    f: 4,    c: 30,   kcal: 180 },
    egg:        { name: '🍳 スクランブルエッグ', p: 7,    f: 6,    c: 1,    kcal: 90  },
    salad:      { name: '🥗 グリーンサラダ',     p: 1,    f: 0.2,  c: 4,    kcal: 20  },
    chicken:    { name: '🍗 サラダチキン',       p: 25,   f: 1.5,  c: 0.5,  kcal: 120 },
    curry:      { name: '🍛 カレーライス',       p: 15,   f: 18,   c: 90,   kcal: 650 },
    fish_set:   { name: '🐟 焼き魚定食',         p: 25,   f: 12,   c: 60,   kcal: 480 },
    beef_bowl:  { name: '🐂 牛丼',               p: 20,   f: 22,   c: 95,   kcal: 700 },
    ramen:      { name: '🍜 醤油ラーメン',       p: 20,   f: 20,   c: 70,   kcal: 550 },
    udon:       { name: '🥢 かけうどん',         p: 8,    f: 1,    c: 55,   kcal: 280 },
    rice:       { name: '🍚 白米 (大盛1杯)',     p: 4,    f: 0.5,  c: 55,   kcal: 240 },
    chocolate:  { name: '🍫 チョコレート',       p: 2,    f: 15,   c: 28,   kcal: 250 },
    apple:      { name: '🍎 りんご (半分)',       p: 0.3,  f: 0.1,  c: 15,   kcal: 60  },
    protein:    { name: '🥤 プロテイン',         p: 20,   f: 1.5,  c: 3,    kcal: 120 },
};

/** 食事の時間帯リスト（このリストを使い、同じタイプ名を何度も書かない） */
const MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack'];

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

// ============================================================
// [3] 初期化
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    cacheDOM();
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
function generateMealOptions() {
    const selects = [DOM.mealBreakfast, DOM.mealLunch, DOM.mealDinner, DOM.mealSnack];
    selects.forEach(select => {
        if (!select) return;
        select.innerHTML = '';
        Object.entries(MEAL_MENU).forEach(([key, meal]) => {
            const opt = document.createElement('option');
            opt.value       = key;
            opt.textContent = key === 'none' ? meal.name : `${meal.name} (${meal.kcal} kcal)`;
            select.appendChild(opt);
        });
    });
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

    // 食事「追加」ボタン（MEAL_TYPESをベースに対応を自動生成）
    MEAL_TYPES.forEach(type => {
        const cap    = type.charAt(0).toUpperCase() + type.slice(1);
        const btn    = DOM[`add${cap}Btn`];
        const select = DOM[`meal${cap}`];
        btn?.addEventListener('click', () => {
            const key = select?.value;
            if (key && key !== 'none') addMealItem(type, key);
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
                <span class="nutri-tag p">🥩 たんぱく質: ${round1(totals.p)}g</span>
                <span class="nutri-tag f">🧈 脂質: ${round1(totals.f)}g</span>
                <span class="nutri-tag c">🍚 炭水化物: ${round1(totals.c)}g</span>
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
    const goal = 2000;
    const pct  = Math.min(Math.round((value / goal) * 100), 100);
    if (DOM.waterCurrent)  DOM.waterCurrent.textContent  = value;
    if (DOM.waterPctText)  DOM.waterPctText.textContent  = `${pct}%`;
    if (DOM.waterProgress) DOM.waterProgress.style.width = `${pct}%`;
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
 * 今日の総カロリー・PFCバランスバーを更新する
 */
function updatePfcSummary(dayData) {
    // 全食事タイプのメニューキーを1つの配列に集める（旧形式・新形式の両方に対応）
    const allKeys = MEAL_TYPES.flatMap(type => normalizeMealData(dayData[type]));
    const totals  = sumNutrition(allKeys);

    if (DOM.totalCalories) DOM.totalCalories.textContent = `${Math.round(totals.kcal)} kcal`;
    if (DOM.totalP)        DOM.totalP.textContent        = round1(totals.p);
    if (DOM.totalF)        DOM.totalF.textContent        = round1(totals.f);
    if (DOM.totalC)        DOM.totalC.textContent        = round1(totals.c);

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
            min: 0, max: 3000,
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

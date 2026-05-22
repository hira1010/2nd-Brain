/**
 * ヘルスケア記録サイト - メインスクリプト (リファクタリング版)
 */

// 食事メニューデータの定義（P:たんぱく質, F:脂質, C:炭水化物）
const MEAL_MENU = {
    "none": { name: "選択しない", p: 0, f: 0, c: 0, kcal: 0 },
    "toast": { name: "🍞 トースト", p: 6, f: 4, c: 30, kcal: 180 },
    "egg": { name: "🍳 スクランブルエッグ", p: 7, f: 6, c: 1, kcal: 90 },
    "salad": { name: "🥗 グリーンサラダ", p: 1, f: 0.2, c: 4, kcal: 20 },
    "chicken": { name: "🍗 サラダチキン", p: 25, f: 1.5, c: 0.5, kcal: 120 },
    "curry": { name: "🍛 カレーライス", p: 15, f: 18, c: 90, kcal: 650 },
    "fish_set": { name: "🐟 焼き魚定食", p: 25, f: 12, c: 60, kcal: 480 },
    "beef_bowl": { name: "🐂 牛丼", p: 20, f: 22, c: 95, kcal: 700 },
    "ramen": { name: "🍜 醤油ラーメン", p: 20, f: 20, c: 70, kcal: 550 },
    "udon": { name: "🥢 かけうどん", p: 8, f: 1, c: 55, kcal: 280 },
    "rice": { name: "🍚 白米 (大盛1杯)", p: 4, f: 0.5, c: 55, kcal: 240 },
    "chocolate": { name: "🍫 チョコレート", p: 2, f: 15, c: 28, kcal: 250 },
    "apple": { name: "🍎 りんご (半分)", p: 0.3, f: 0.1, c: 15, kcal: 60 },
    "protein": { name: "🥤 プロテイン", p: 20, f: 1.5, c: 3, kcal: 120 }
};

// バイタルおよび活動入力項目の定義（ID、データキー、型の指定）
const VITAL_FIELDS = [
    { id: 'weight-input', key: 'weight', type: 'float' },
    { id: 'bodyfat-input', key: 'bodyfat', type: 'float' },
    { id: 'bp-input', key: 'bp', type: 'string' },
    { id: 'bmi-input', key: 'bmi', type: 'float' },
    { id: 'waist-input', key: 'waist', type: 'float' },
    { id: 'visceral-fat-input', key: 'visceralFat', type: 'float' },
    { id: 'subcutaneous-fat-input', key: 'subcutaneousFat', type: 'float' },
    { id: 'muscle-input', key: 'muscle', type: 'float' },
    { id: 'metabolism-input', key: 'metabolism', type: 'float' },
    { id: 'body-age-input', key: 'bodyAge', type: 'int' },
    { id: 'exercise-input', key: 'exercise', type: 'string' }
];

// 選択中の日付 (デフォルトは今日の日付: YYYY-MM-DD形式)
let selectedDate = getFormattedDate(new Date());

// Chart.js のインスタンスを保持する変数
let weightChart = null;

// 現在選択されているグラフのタブ
let currentChartTab = 'weight';

// 自動保存のデバウンス用タイマー
let saveTimeout = null;

// DOM要素のキャッシュ用オブジェクト
let DOM = {};

// アプリケーション起動時の初期化
document.addEventListener('DOMContentLoaded', () => {
    cacheDOM();
    generateMealOptions();

    if (DOM.datePicker) {
        DOM.datePicker.value = selectedDate;
    }

    setupEventListeners();
    loadDateData(selectedDate);
    updateDashboard();
});

/**
 * 主要なDOM要素を1箇所で取得してキャッシュする
 */
function cacheDOM() {
    DOM = {
        datePicker: document.getElementById('date-picker'),
        prevBtn: document.getElementById('prev-date-btn'),
        nextBtn: document.getElementById('next-date-btn'),
        mealBreakfast: document.getElementById('meal-breakfast'),
        mealLunch: document.getElementById('meal-lunch'),
        mealDinner: document.getElementById('meal-dinner'),
        mealSnack: document.getElementById('meal-snack'),
        waterCurrent: document.getElementById('water-current'),
        waterResetBtn: document.getElementById('water-reset-btn'),
        waterPctText: document.getElementById('water-pct-text'),
        waterProgress: document.getElementById('water-progress'),
        summaryWeight: document.getElementById('summary-weight'),
        summaryBodyfat: document.getElementById('summary-bodyfat'),
        summaryBp: document.getElementById('summary-bp'),
        summaryBmi: document.getElementById('summary-bmi'),
        summaryWaist: document.getElementById('summary-waist'),
        totalCalories: document.getElementById('total-calories'),
        totalP: document.getElementById('total-p'),
        totalF: document.getElementById('total-f'),
        totalC: document.getElementById('total-c'),
        pBar: document.getElementById('p-bar'),
        fBar: document.getElementById('f-bar'),
        cBar: document.getElementById('c-bar'),
        autosaveBadge: document.getElementById('autosave-badge'),
        chartCanvas: document.getElementById('weightChart')
    };

    // バイタル入力項目もキャッシュに追加
    VITAL_FIELDS.forEach(field => {
        DOM[field.key] = document.getElementById(field.id);
    });
}

/**
 * Dateオブジェクトを YYYY-MM-DD 形式の文字列に変換する
 */
function getFormattedDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * 食事プルダウンメニューの選択肢を動的に生成する
 */
function generateMealOptions() {
    const selects = [DOM.mealBreakfast, DOM.mealLunch, DOM.mealDinner, DOM.mealSnack];
    
    selects.forEach(select => {
        if (!select) return;
        select.innerHTML = ''; // クリア
        
        Object.entries(MEAL_MENU).forEach(([key, meal]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = key === 'none' ? meal.name : `${meal.name} (${meal.kcal} kcal)`;
            select.appendChild(option);
        });
    });
}

/**
 * 各種イベントリスナーをセットアップする
 */
function setupEventListeners() {
    // 日付変更イベント
    if (DOM.datePicker) {
        DOM.datePicker.addEventListener('change', (e) => {
            selectedDate = e.target.value;
            loadDateData(selectedDate);
            updateDashboard();
        });
    }

    // 前日・翌日ボタン
    if (DOM.prevBtn) DOM.prevBtn.addEventListener('click', () => changeDate(-1));
    if (DOM.nextBtn) DOM.nextBtn.addEventListener('click', () => changeDate(1));

    // 水分クイック加算ボタン
    const waterButtons = document.querySelectorAll('.water-btn[data-amount]');
    waterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const amount = parseInt(btn.dataset.amount, 10);
            addWater(amount);
        });
    });

    // 水分リセットボタン
    if (DOM.waterResetBtn) {
        DOM.waterResetBtn.addEventListener('click', () => resetWater());
    }

    // 各バイタル項目の入力イベント（自動保存トリガー）
    VITAL_FIELDS.forEach(field => {
        const input = DOM[field.key];
        if (input) {
            input.addEventListener('input', () => triggerAutoSave());
        }
    });

    // 食事プルダウンの変更イベント
    const mealSelects = [DOM.mealBreakfast, DOM.mealLunch, DOM.mealDinner, DOM.mealSnack];
    mealSelects.forEach(select => {
        if (!select) return;
        select.addEventListener('change', (e) => {
            updateSingleMealNutrition(e.target.id, e.target.value);
            triggerAutoSave();
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

/**
 * 指定した日数分、選択日付を変更する
 */
function changeDate(daysOffset) {
    const currentDate = new Date(selectedDate);
    currentDate.setDate(currentDate.getDate() + daysOffset);
    selectedDate = getFormattedDate(currentDate);
    
    if (DOM.datePicker) {
        DOM.datePicker.value = selectedDate;
    }
    loadDateData(selectedDate);
    updateDashboard();
}

/**
 * ローカルストレージから全データを取得する
 */
function getAllData() {
    const dataJSON = localStorage.getItem('health_tracker_data');
    return dataJSON ? JSON.parse(dataJSON) : {};
}

/**
 * ローカルストレージに全データを保存する
 */
function saveAllData(data) {
    localStorage.setItem('health_tracker_data', JSON.stringify(data));
}

/**
 * 選択された日付のデータを読み込み、フォームにセットする
 */
function loadDateData(dateStr) {
    const data = getAllData();
    const dayData = data[dateStr] || {};

    // 食事プルダウンへの反映
    const mealTypes = ['breakfast', 'lunch', 'dinner', 'snack'];
    mealTypes.forEach(type => {
        const key = `meal${type.charAt(0).toUpperCase() + type.slice(1)}`;
        const select = DOM[key];
        const val = dayData[type] || 'none';
        if (select) {
            select.value = val;
            updateSingleMealNutrition(select.id, val);
        }
    });

    // バイタル項目の入力欄へ反映
    VITAL_FIELDS.forEach(field => {
        const input = DOM[field.key];
        if (input) {
            const val = dayData[field.key];
            input.value = (val !== undefined && val !== null) ? val : '';
        }
    });

    // 水分データの反映
    updateWaterDisplay(dayData.water || 0);
}

/**
 * 単体の食事メニューに対するPFC・カロリー表示を更新する
 */
function updateSingleMealNutrition(selectId, mealKey) {
    const type = selectId.split('-')[1]; // 'breakfast', 'lunch' など
    const targetDiv = document.getElementById(`${type}-nutrition`);
    const meal = MEAL_MENU[mealKey];

    if (!targetDiv) return;
    if (!meal || mealKey === 'none') {
        targetDiv.innerHTML = '';
        return;
    }

    targetDiv.innerHTML = `
        <span class="nutri-tag cal"><i data-lucide="flame" style="width: 0.8rem; height: 0.8rem"></i>${meal.kcal} kcal</span>
        <span class="nutri-tag p">P: ${meal.p}g</span>
        <span class="nutri-tag f">F: ${meal.f}g</span>
        <span class="nutri-tag c">C: ${meal.c}g</span>
    `;

    lucide.createIcons();
}

/**
 * 水分摂取量の表示を更新する
 */
function updateWaterDisplay(value) {
    if (DOM.waterCurrent) DOM.waterCurrent.textContent = value;
    
    const goal = 2000;
    const pct = Math.min(Math.round((value / goal) * 100), 100);
    
    if (DOM.waterPctText) DOM.waterPctText.textContent = `${pct}%`;
    if (DOM.waterProgress) DOM.waterProgress.style.width = `${pct}%`;
}

/**
 * 水分摂取量を加算する
 */
function addWater(amount) {
    const currentWater = parseInt(DOM.waterCurrent ? DOM.waterCurrent.textContent : '0', 10) || 0;
    updateWaterDisplay(currentWater + amount);
    saveCurrentData();
}

/**
 * 水分摂取量をリセットする
 */
function resetWater() {
    updateWaterDisplay(0);
    saveCurrentData();
}

/**
 * 自動保存のデバウンス処理（キー入力後、手が止まってから実行）
 */
function triggerAutoSave() {
    if (DOM.autosaveBadge) {
        DOM.autosaveBadge.classList.add('saving');
        const span = DOM.autosaveBadge.querySelector('span');
        if (span) span.textContent = '保存中...';
    }

    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
        saveCurrentData();
    }, 500);
}

/**
 * フォーム全体のデータを収集してローカルストレージに自動保存する
 */
function saveCurrentData() {
    const data = getAllData();
    const dayData = {};
    
    // 食事データの取得
    dayData.breakfast = DOM.mealBreakfast ? DOM.mealBreakfast.value : 'none';
    dayData.lunch = DOM.mealLunch ? DOM.mealLunch.value : 'none';
    dayData.dinner = DOM.mealDinner ? DOM.mealDinner.value : 'none';
    dayData.snack = DOM.mealSnack ? DOM.mealSnack.value : 'none';
    
    // 水分データの取得
    dayData.water = parseInt(DOM.waterCurrent ? DOM.waterCurrent.textContent : '0', 10) || 0;

    // バイタル項目の自動収集
    VITAL_FIELDS.forEach(field => {
        const input = DOM[field.key];
        if (!input) return;

        const val = input.value;
        if (val === '') {
            dayData[field.key] = field.type === 'string' ? '' : null;
        } else {
            if (field.type === 'float') {
                dayData[field.key] = parseFloat(val);
            } else if (field.type === 'int') {
                dayData[field.key] = parseInt(val, 10);
            } else {
                dayData[field.key] = val.trim();
            }
        }
    });

    data[selectedDate] = dayData;
    saveAllData(data);
    
    // 自動保存完了表示
    if (DOM.autosaveBadge) {
        DOM.autosaveBadge.classList.remove('saving');
        const span = DOM.autosaveBadge.querySelector('span');
        if (span) span.textContent = '自動保存済';
    }
    
    applySaveGlow();
    updateDashboard();
}

/**
 * 自動保存された際、入力欄を一瞬光らせるエフェクト
 */
function applySaveGlow() {
    const inputs = [
        DOM.mealBreakfast, DOM.mealLunch, DOM.mealDinner, DOM.mealSnack
    ];
    
    VITAL_FIELDS.forEach(field => {
        inputs.push(DOM[field.key]);
    });

    inputs.forEach(input => {
        if (input) {
            input.classList.remove('autosave-glow');
            void input.offsetWidth; // リフロー
            input.classList.add('autosave-glow');
        }
    });
}

/**
 * ダッシュボード全体の表示（サマリー、グラフ、カレンダー、履歴）を更新する
 */
function updateDashboard() {
    const data = getAllData();
    const todayData = data[selectedDate] || {};

    // 各サマリー要素のテキスト設定（データがなければ直近値を表示）
    const updateSummaryElement = (elem, val, latestVal, suffix = '') => {
        if (!elem) return;
        if (val !== undefined && val !== null && val !== '') {
            elem.textContent = `${val}${suffix}`;
        } else if (latestVal !== null && latestVal !== undefined && latestVal !== '') {
            elem.textContent = `${latestVal}${suffix} (直近)`;
        } else {
            elem.textContent = `- ${suffix}`.trim();
        }
    };

    updateSummaryElement(DOM.summaryWeight, todayData.weight, findLatestValue('weight'), ' kg');
    updateSummaryElement(DOM.summaryBodyfat, todayData.bodyfat, findLatestValue('bodyfat'), ' %');
    updateSummaryElement(DOM.summaryBp, todayData.bp, findLatestValue('bp'), ' mmHg');
    updateSummaryElement(DOM.summaryBmi, todayData.bmi, findLatestValue('bmi'));
    updateSummaryElement(DOM.summaryWaist, todayData.waist, findLatestValue('waist'), ' cm');

    updatePfcSummary(todayData);
    updateChart();
    renderCalendar();
    renderHistoryList();
}

/**
 * 特定のキーの直近の記録値を取得する
 */
function findLatestValue(key) {
    const data = getAllData();
    const sortedDates = Object.keys(data).sort((a, b) => new Date(b) - new Date(a));
    
    for (const dStr of sortedDates) {
        const val = data[dStr] ? data[dStr][key] : null;
        if (val !== undefined && val !== null && val !== '') {
            return val;
        }
    }
    return null;
}

/**
 * PFCとカロリーのサマリー表示を更新する
 */
function updatePfcSummary(dayData) {
    const meals = [
        dayData.breakfast || 'none',
        dayData.lunch || 'none',
        dayData.dinner || 'none',
        dayData.snack || 'none'
    ];

    let totalCal = 0, totalP = 0, totalF = 0, totalC = 0;

    meals.forEach(key => {
        const meal = MEAL_MENU[key];
        if (meal) {
            totalCal += meal.kcal;
            totalP += meal.p;
            totalF += meal.f;
            totalC += meal.c;
        }
    });

    if (DOM.totalCalories) DOM.totalCalories.textContent = `${totalCal} kcal`;
    if (DOM.totalP) DOM.totalP.textContent = totalP;
    if (DOM.totalF) DOM.totalF.textContent = totalF;
    if (DOM.totalC) DOM.totalC.textContent = totalC;

    const totalGrams = totalP + totalF + totalC;
    if (totalGrams > 0) {
        const pPct = (totalP / totalGrams) * 100;
        const fPct = (totalF / totalGrams) * 100;
        const cPct = (totalC / totalGrams) * 100;

        if (DOM.pBar) DOM.pBar.style.width = `${pPct}%`;
        if (DOM.fBar) DOM.fBar.style.width = `${fPct}%`;
        if (DOM.cBar) DOM.cBar.style.width = `${cPct}%`;
    } else {
        if (DOM.pBar) DOM.pBar.style.width = `0%`;
        if (DOM.fBar) DOM.fBar.style.width = `0%`;
        if (DOM.cBar) DOM.cBar.style.width = `0%`;
    }
}

/**
 * Chart.js用の線グラフデータセット作成用の共通関数
 */
function createLineDataset(label, data, color, bgColor, yAxisID) {
    return {
        label,
        data,
        borderColor: color,
        backgroundColor: bgColor,
        borderWidth: 3,
        pointBackgroundColor: color,
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.3,
        yAxisID,
        spanGaps: true
    };
}

/**
 * 過去7日間の各種推移グラフを描画する
 */
function updateChart() {
    if (!DOM.chartCanvas) return;
    
    const data = getAllData();
    const labels = [];
    const datasets = [];
    
    const baseDate = new Date(selectedDate);
    const dates = [];
    
    for (let i = 6; i >= 0; i--) {
        const d = new Date(baseDate);
        d.setDate(baseDate.getDate() - i);
        const dStr = getFormattedDate(d);
        dates.push(dStr);
        labels.push(`${d.getMonth() + 1}/${d.getDate()}`);
    }

    // 水分の棒グラフ（背景用）
    const waterData = dates.map(dStr => (data[dStr] || {}).water || 0);
    const waterDataset = {
        label: '水分 (ml)',
        data: waterData,
        type: 'bar',
        backgroundColor: 'rgba(59, 130, 246, 0.12)',
        borderColor: 'rgba(59, 130, 246, 0.25)',
        borderWidth: 1,
        borderRadius: 5,
        yAxisID: 'ySecondary'
    };

    let yPrimaryLabel = '';
    let ySecondaryLabel = '水分 (ml)';
    let ySecondaryMax = 3000;
    let showWater = true;

    // 各種タブごとのデータセット構成
    if (currentChartTab === 'weight') {
        const weightData = dates.map(dStr => (data[dStr] || {}).weight || null);
        yPrimaryLabel = '体重 (kg)';
        datasets.push(createLineDataset('体重 (kg)', weightData, '#ec4899', 'rgba(236, 72, 153, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'bodyfat') {
        const bodyfatData = dates.map(dStr => (data[dStr] || {}).bodyfat || null);
        yPrimaryLabel = '体脂肪率 (%)';
        datasets.push(createLineDataset('体脂肪率 (%)', bodyfatData, '#a855f7', 'rgba(168, 85, 247, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'bp') {
        const systolicData = [];
        const diastolicData = [];
        dates.forEach(dStr => {
            const bpStr = (data[dStr] || {}).bp || '';
            const match = bpStr.match(/^(\d+)\s*\/\s*(\d+)$/);
            if (match) {
                systolicData.push(parseInt(match[1], 10));
                diastolicData.push(parseInt(match[2], 10));
            } else {
                systolicData.push(null);
                diastolicData.push(null);
            }
        });
        
        yPrimaryLabel = '血圧 (mmHg)';
        showWater = false;
        
        datasets.push(createLineDataset('最高血圧 (mmHg)', systolicData, '#f97316', 'rgba(249, 115, 22, 0.08)', 'yPrimary'));
        datasets.push(createLineDataset('最低血圧 (mmHg)', diastolicData, '#06b6d4', 'rgba(6, 182, 212, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'waist') {
        const waistData = dates.map(dStr => (data[dStr] || {}).waist || null);
        yPrimaryLabel = 'ウエスト (cm)';
        datasets.push(createLineDataset('ウエスト (cm)', waistData, '#10b981', 'rgba(16, 185, 129, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'bmi') {
        const bmiData = dates.map(dStr => (data[dStr] || {}).bmi || null);
        yPrimaryLabel = 'BMI';
        datasets.push(createLineDataset('BMI', bmiData, '#3b82f6', 'rgba(59, 130, 246, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'muscle') {
        const muscleData = dates.map(dStr => (data[dStr] || {}).muscle || null);
        const subcutaneousData = dates.map(dStr => (data[dStr] || {}).subcutaneousFat || null);
        
        yPrimaryLabel = '割合 (%)';
        showWater = false;
        
        datasets.push(createLineDataset('骨格筋率 (%)', muscleData, '#10b981', 'rgba(16, 185, 129, 0.08)', 'yPrimary'));
        datasets.push(createLineDataset('皮下脂肪率 (%)', subcutaneousData, '#ec4899', 'rgba(236, 72, 153, 0.08)', 'yPrimary'));
    } else if (currentChartTab === 'metabolism') {
        const metabolismData = dates.map(dStr => (data[dStr] || {}).metabolism || null);
        yPrimaryLabel = '基礎代謝 (kcal)';
        datasets.push(createLineDataset('基礎代謝 (kcal)', metabolismData, '#f59e0b', 'rgba(245, 158, 11, 0.08)', 'yPrimary'));
    }

    if (showWater) {
        datasets.push(waterDataset);
    }

    if (weightChart) {
        weightChart.destroy();
    }

    const ctx = DOM.chartCanvas.getContext('2d');
    const scalesConfig = {
        x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' }
        },
        yPrimary: {
            type: 'linear',
            position: 'left',
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#94a3b8' },
            title: {
                display: true,
                text: yPrimaryLabel,
                color: '#94a3b8'
            }
        }
    };

    if (showWater) {
        scalesConfig.ySecondary = {
            type: 'linear',
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: '#94a3b8' },
            title: {
                display: true,
                text: ySecondaryLabel,
                color: '#3b82f6'
            },
            min: 0,
            max: ySecondaryMax
        };
    }

    weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#94a3b8',
                        font: { family: 'Outfit, Noto Sans JP' }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: scalesConfig
        }
    });
}

/**
 * カレンダーをレンダリングする
 */
function renderCalendar() {
    const calendarGrid = document.getElementById('calendar-grid');
    if (!calendarGrid) return;
    calendarGrid.innerHTML = '';

    const data = getAllData();
    const currentDate = new Date(selectedDate);
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    const headerTitle = document.createElement('div');
    headerTitle.className = 'calendar-title-wrapper';
    headerTitle.style.gridColumn = 'span 7';
    headerTitle.style.textAlign = 'center';
    headerTitle.style.fontWeight = '700';
    headerTitle.style.marginBottom = '0.5rem';
    headerTitle.textContent = `${year}年 ${month + 1}月`;
    calendarGrid.appendChild(headerTitle);

    const weekDays = ['日', '月', '火', '水', '木', '金', '土'];
    weekDays.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'calendar-header';
        dayHeader.textContent = day;
        calendarGrid.appendChild(dayHeader);
    });

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    const startDayOfWeek = firstDay.getDay();
    const totalDays = lastDay.getDate();

    for (let i = 0; i < startDayOfWeek; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day empty';
        calendarGrid.appendChild(emptyCell);
    }

    for (let day = 1; day <= totalDays; day++) {
        const dateObj = new Date(year, month, day);
        const dateStr = getFormattedDate(dateObj);
        const hasData = !!data[dateStr];

        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day';
        if (dateStr === selectedDate) dayCell.classList.add('active');
        if (hasData) dayCell.classList.add('has-data');

        const dayNumSpan = document.createElement('span');
        dayNumSpan.className = 'day-number';
        dayNumSpan.textContent = day;
        dayCell.appendChild(dayNumSpan);

        dayCell.addEventListener('click', () => {
            selectedDate = dateStr;
            if (DOM.datePicker) DOM.datePicker.value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });

        calendarGrid.appendChild(dayCell);
    }
}

/**
 * 履歴リストをレンダリングする
 */
function renderHistoryList() {
    const historyList = document.getElementById('history-list');
    if (!historyList) return;
    historyList.innerHTML = '';

    const data = getAllData();
    const sortedDates = Object.keys(data).sort((a, b) => new Date(b) - new Date(a));

    if (sortedDates.length === 0) {
        const emptyMsg = document.createElement('div');
        emptyMsg.style.color = 'var(--text-muted)';
        emptyMsg.style.textAlign = 'center';
        emptyMsg.style.padding = '2rem 0';
        emptyMsg.textContent = '記録がまだありません';
        historyList.appendChild(emptyMsg);
        return;
    }

    const recentDates = sortedDates.slice(0, 5);

    recentDates.forEach(dateStr => {
        const dayData = data[dateStr];
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const dObj = new Date(dateStr);
        const displayDate = `${dObj.getMonth() + 1}月${dObj.getDate()}日`;
        const displayWeight = dayData.weight ? `${dayData.weight}kg` : '-- kg';

        const hasMeals = ['breakfast', 'lunch', 'dinner', 'snack'].some(type => dayData[type] && dayData[type] !== 'none');
        const hasExercise = !!dayData.exercise;
        
        item.innerHTML = `
            <div class="history-item-header">
                <span class="history-item-date">${displayDate}</span>
                <span class="history-item-weight">${displayWeight}</span>
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
                    <span>${hasExercise ? '運動あり' : 'なし'}</span>
                </div>
            </div>
        `;

        item.addEventListener('click', () => {
            selectedDate = dateStr;
            if (DOM.datePicker) DOM.datePicker.value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });

        historyList.appendChild(item);
    });

    lucide.createIcons();
}

/**
 * ヘルスケア記録サイト - メインスクリプト
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

// 選択中の日付 (デフォルトは今日の日付: YYYY-MM-DD形式)
let selectedDate = getFormattedDate(new Date());

// Chart.js のインスタンスを保持する変数
let weightChart = null;

// 自動保存のデバウンス用タイマー
let saveTimeout = null;

// アプリケーション起動時の初期化
document.addEventListener('DOMContentLoaded', () => {
    // プルダウンメニューのオプションを生成
    generateMealOptions();

    // 日付選択フォームに初期日付を設定
    const datePicker = document.getElementById('date-picker');
    datePicker.value = selectedDate;

    // イベントリスナーの登録
    setupEventListeners();

    // データの読み込みと画面の更新
    loadDateData(selectedDate);
    updateDashboard();
});

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
    const selects = ['meal-breakfast', 'meal-lunch', 'meal-dinner', 'meal-snack'];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        select.innerHTML = ''; // クリア
        
        Object.entries(MEAL_MENU).forEach(([key, meal]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = `${meal.name} (${meal.kcal} kcal)`;
            if (key === 'none') {
                option.textContent = meal.name;
            }
            select.appendChild(option);
        });
    });
}

/**
 * 各種イベントリスナーをセットアップする
 */
function setupEventListeners() {
    const datePicker = document.getElementById('date-picker');
    const prevBtn = document.getElementById('prev-date-btn');
    const nextBtn = document.getElementById('next-date-btn');
    
    const weightInput = document.getElementById('weight-input');
    const exerciseInput = document.getElementById('exercise-input');
    
    const mealSelects = document.querySelectorAll('.meal-select');
    const waterButtons = document.querySelectorAll('.water-btn[data-amount]');
    const waterResetBtn = document.getElementById('water-reset-btn');

    // 日付手動変更時
    datePicker.addEventListener('change', (e) => {
        selectedDate = e.target.value;
        loadDateData(selectedDate);
        updateDashboard();
    });

    // 前日ボタン
    prevBtn.addEventListener('click', () => {
        changeDate(-1);
    });

    // 翌日ボタン
    nextBtn.addEventListener('click', () => {
        changeDate(1);
    });

    // 水分クイック加算ボタン
    waterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const amount = parseInt(btn.dataset.amount, 10);
            addWater(amount);
        });
    });

    // 水分リセットボタン
    waterResetBtn.addEventListener('click', () => {
        resetWater();
    });

    // 体重・運動の入力イベントで自動保存（デバウンス処理）
    weightInput.addEventListener('input', () => {
        triggerAutoSave();
    });
    
    exerciseInput.addEventListener('input', () => {
        triggerAutoSave();
    });

    // 食事プルダウンの変更イベントで自動保存＆PFC表示更新
    mealSelects.forEach(select => {
        select.addEventListener('change', (e) => {
            const selectId = e.target.id;
            const mealKey = e.target.value;
            
            // 選択した食事の栄養素を表示
            updateSingleMealNutrition(selectId, mealKey);
            
            // 自動保存の実行
            triggerAutoSave();
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
    
    document.getElementById('date-picker').value = selectedDate;
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

    // 各プルダウンに値を反映（なければ 'none'）
    document.getElementById('meal-breakfast').value = dayData.breakfast || 'none';
    document.getElementById('meal-lunch').value = dayData.lunch || 'none';
    document.getElementById('meal-dinner').value = dayData.dinner || 'none';
    document.getElementById('meal-snack').value = dayData.snack || 'none';

    // 各食事の栄養素表示を更新
    updateSingleMealNutrition('meal-breakfast', dayData.breakfast || 'none');
    updateSingleMealNutrition('meal-lunch', dayData.lunch || 'none');
    updateSingleMealNutrition('meal-dinner', dayData.dinner || 'none');
    updateSingleMealNutrition('meal-snack', dayData.snack || 'none');

    // 体重と運動の入力欄
    document.getElementById('weight-input').value = dayData.weight || '';
    document.getElementById('exercise-input').value = dayData.exercise || '';

    // 水分の表示更新
    const waterVal = dayData.water || 0;
    updateWaterDisplay(waterVal);
}

/**
 * 単体の食事メニューに対するPFC・カロリー表示を更新する
 */
function updateSingleMealNutrition(selectId, mealKey) {
    const type = selectId.split('-')[1]; // 'breakfast', 'lunch' など
    const targetDiv = document.getElementById(`${type}-nutrition`);
    const meal = MEAL_MENU[mealKey];

    if (!meal || mealKey === 'none') {
        targetDiv.innerHTML = '';
        return;
    }

    // PFCとカロリーのバッジ風HTMLを作成
    targetDiv.innerHTML = `
        <span class="nutri-tag cal"><i data-lucide="flame" style="width: 0.8rem; height: 0.8rem"></i>${meal.kcal} kcal</span>
        <span class="nutri-tag p">P: ${meal.p}g</span>
        <span class="nutri-tag f">F: ${meal.f}g</span>
        <span class="nutri-tag c">C: ${meal.c}g</span>
    `;

    // アイコンの初期化
    lucide.createIcons();
}

/**
 * 水分摂取量の表示を更新する
 */
function updateWaterDisplay(value) {
    document.getElementById('water-current').textContent = value;
    
    // サマリー部分の更新
    const goal = 2000; // 水分目標 2000ml
    const pct = Math.min(Math.round((value / goal) * 100), 100);
    
    document.getElementById('water-pct-text').textContent = `${pct}%`;
    document.getElementById('water-progress').style.width = `${pct}%`;
}

/**
 * 水分摂取量を加算する
 */
function addWater(amount) {
    const currentWater = parseInt(document.getElementById('water-current').textContent, 10) || 0;
    const newWater = currentWater + amount;
    updateWaterDisplay(newWater);
    
    // 水分は変更後、即座に自動保存
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
    // 自動保存バッジを「保存中...」にする
    const badge = document.getElementById('autosave-badge');
    badge.classList.add('saving');
    badge.querySelector('span').textContent = '保存中...';

    clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
        saveCurrentData();
    }, 500); // 500ミリ秒後に実行
}

/**
 * フォーム全体のデータをローカルストレージに自動保存する
 */
function saveCurrentData() {
    const data = getAllData();
    
    const breakfast = document.getElementById('meal-breakfast').value;
    const lunch = document.getElementById('meal-lunch').value;
    const dinner = document.getElementById('meal-dinner').value;
    const snack = document.getElementById('meal-snack').value;
    
    const weightVal = document.getElementById('weight-input').value;
    const weight = weightVal !== '' ? parseFloat(weightVal) : null;
    
    const exercise = document.getElementById('exercise-input').value.trim();
    const water = parseInt(document.getElementById('water-current').textContent, 10) || 0;

    // データの組み立て
    data[selectedDate] = {
        breakfast,
        lunch,
        dinner,
        snack,
        weight,
        exercise,
        water
    };

    saveAllData(data);
    
    // 自動保存完了アニメーション表示
    const badge = document.getElementById('autosave-badge');
    badge.classList.remove('saving');
    badge.querySelector('span').textContent = '自動保存済';
    
    // 入力欄に一瞬光るエフェクトを適用
    applySaveGlow();

    // 各表示コンポーネントの更新
    updateDashboard();
}

/**
 * 自動保存された際、入力欄を一瞬光らせるエフェクト
 */
function applySaveGlow() {
    const inputs = [
        document.getElementById('weight-input'),
        document.getElementById('exercise-input'),
        document.getElementById('meal-breakfast'),
        document.getElementById('meal-lunch'),
        document.getElementById('meal-dinner'),
        document.getElementById('meal-snack')
    ];

    inputs.forEach(input => {
        input.classList.remove('autosave-glow');
        // リフローを起こしてアニメーションを再トリガーする
        void input.offsetWidth;
        input.classList.add('autosave-glow');
    });
}

/**
 * ダッシュボード全体の表示（サマリー、グラフ、カレンダー、履歴）を更新する
 */
function updateDashboard() {
    const data = getAllData();
    const todayData = data[selectedDate] || {};

    // 1. 体重サマリーの更新
    const summaryWeight = document.getElementById('summary-weight');
    if (todayData.weight) {
        summaryWeight.textContent = `${todayData.weight} kg`;
    } else {
        const latestWeight = findLatestWeight();
        if (latestWeight) {
            summaryWeight.textContent = `${latestWeight} kg (直近)`;
        } else {
            summaryWeight.textContent = '- kg';
        }
    }

    // 2. 今日の総カロリー＆PFCバランスの計算と更新
    updatePfcSummary(todayData);

    // 3. グラフの更新
    updateChart();

    // 4. カレンダーの描画
    renderCalendar();

    // 5. 履歴リストの更新
    renderHistoryList();
}

/**
 * 直近で記録されている体重を取得する
 */
function findLatestWeight() {
    const data = getAllData();
    const sortedDates = Object.keys(data).sort((a, b) => new Date(b) - new Date(a));
    
    for (const dStr of sortedDates) {
        if (data[dStr] && data[dStr].weight) {
            return data[dStr].weight;
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

    let totalCal = 0;
    let totalP = 0;
    let totalF = 0;
    let totalC = 0;

    meals.forEach(key => {
        const meal = MEAL_MENU[key];
        if (meal) {
            totalCal += meal.kcal;
            totalP += meal.p;
            totalF += meal.f;
            totalC += meal.c;
        }
    });

    // カロリー数値更新
    document.getElementById('total-calories').textContent = `${totalCal} kcal`;
    
    // PFC数値更新
    document.getElementById('total-p').textContent = totalP;
    document.getElementById('total-f').textContent = totalF;
    document.getElementById('total-c').textContent = totalC;

    // PFC割合バーの更新
    const totalGrams = totalP + totalF + totalC;
    const pBar = document.getElementById('p-bar');
    const fBar = document.getElementById('f-bar');
    const c-bar = document.getElementById('c-bar'); // 注意: IDは 'c-bar'

    if (totalGrams > 0) {
        const pPct = (totalP / totalGrams) * 100;
        const fPct = (totalF / totalGrams) * 100;
        const cPct = (totalC / totalGrams) * 100;

        pBar.style.width = `${pPct}%`;
        fBar.style.width = `${fPct}%`;
        document.getElementById('c-bar').style.width = `${cPct}%`;
    } else {
        pBar.style.width = `0%`;
        fBar.style.width = `0%`;
        document.getElementById('c-bar').style.width = `0%`;
    }
}

/**
 * Chart.jsを使用して過去7日間の体重と水分の複合グラフを描画する
 */
function updateChart() {
    const data = getAllData();
    
    const labels = [];
    const weightDataset = [];
    const waterDataset = [];
    
    const baseDate = new Date(selectedDate);
    for (let i = 6; i >= 0; i--) {
        const d = new Date(baseDate);
        d.setDate(baseDate.getDate() - i);
        const dStr = getFormattedDate(d);
        
        labels.push(`${d.getMonth() + 1}/${d.getDate()}`);
        
        const dayVal = data[dStr] || {};
        weightDataset.push(dayVal.weight || null);
        waterDataset.push(dayVal.water || 0);
    }

    if (weightChart) {
        weightChart.destroy();
    }

    const ctx = document.getElementById('weightChart').getContext('2d');
    
    weightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '体重 (kg)',
                    data: weightDataset,
                    borderColor: '#ec4899',
                    backgroundColor: 'rgba(236, 72, 153, 0.1)',
                    borderWidth: 3,
                    pointBackgroundColor: '#ec4899',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.3,
                    yAxisID: 'yWeight',
                    spanGaps: true
                },
                {
                    label: '水分 (ml)',
                    data: waterDataset,
                    type: 'bar',
                    backgroundColor: 'rgba(59, 130, 246, 0.3)',
                    borderColor: 'rgba(59, 130, 246, 0.6)',
                    borderWidth: 1,
                    borderRadius: 5,
                    yAxisID: 'yWater'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#94a3b8',
                        font: {
                            family: 'Outfit, Noto Sans JP'
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                yWeight: {
                    type: 'linear',
                    position: 'left',
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    },
                    title: {
                        display: true,
                        text: '体重 (kg)',
                        color: '#ec4899'
                    }
                },
                yWater: {
                    type: 'linear',
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    },
                    title: {
                        display: true,
                        text: '水分 (ml)',
                        color: '#3b82f6'
                    },
                    min: 0,
                    max: 3000
                }
            }
        }
    });
}

/**
 * カレンダーをレンダリングする
 */
function renderCalendar() {
    const calendarGrid = document.getElementById('calendar-grid');
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
        if (dateStr === selectedDate) {
            dayCell.classList.add('active');
        }
        if (hasData) {
            dayCell.classList.add('has-data');
        }

        const dayNumSpan = document.createElement('span');
        dayNumSpan.className = 'day-number';
        dayNumSpan.textContent = day;
        dayCell.appendChild(dayNumSpan);

        dayCell.addEventListener('click', () => {
            selectedDate = dateStr;
            document.getElementById('date-picker').value = selectedDate;
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

        // 食事があるかのチェック
        let hasMeals = false;
        if (
            (dayData.breakfast && dayData.breakfast !== 'none') ||
            (dayData.lunch && dayData.lunch !== 'none') ||
            (dayData.dinner && dayData.dinner !== 'none') ||
            (dayData.snack && dayData.snack !== 'none')
        ) {
            hasMeals = true;
        }
        let hasExercise = dayData.exercise ? true : false;
        
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
            document.getElementById('date-picker').value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });

        historyList.appendChild(item);
    });

    lucide.createIcons();
}

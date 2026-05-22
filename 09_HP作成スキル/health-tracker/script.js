/**
 * ヘルスケア記録サイト - メインスクリプト
 */

// データの構造定義
// localStorageのキー: 'health_tracker_data'
// 値の形式: { "YYYY-MM-DD": { breakfast, lunch, dinner, snack, water, weight, exercise } }

// 選択中の日付 (デフォルトは今日の日付: YYYY-MM-DD形式)
let selectedDate = getFormattedDate(new Date());

// Chart.js のインスタンスを保持する変数
let weightChart = null;

// アプリケーション起動時の初期化
document.addEventListener('DOMContentLoaded', () => {
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
 * 各種イベントリスナーをセットアップする
 */
function setupEventListeners() {
    const datePicker = document.getElementById('date-picker');
    const prevBtn = document.getElementById('prev-date-btn');
    const nextBtn = document.getElementById('next-date-btn');
    const trackerForm = document.getElementById('tracker-form');
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

    // フォーム送信（保存）
    trackerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        saveCurrentData();
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

    // 各フォーム要素に値を反映（データがなければ空にする）
    document.getElementById('meal-breakfast').value = dayData.breakfast || '';
    document.getElementById('meal-lunch').value = dayData.lunch || '';
    document.getElementById('meal-dinner').value = dayData.dinner || '';
    document.getElementById('meal-snack').value = dayData.snack || '';
    document.getElementById('weight-input').value = dayData.weight || '';
    document.getElementById('exercise-input').value = dayData.exercise || '';

    // 水分の表示更新
    const waterVal = dayData.water || 0;
    updateWaterDisplay(waterVal);
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
    
    // 水分は即時仮保存するようにすると使いやすい
    autoSaveField('water', newWater);
}

/**
 * 水分摂取量をリセットする
 */
function resetWater() {
    updateWaterDisplay(0);
    autoSaveField('water', 0);
}

/**
 * 特定のフィールドのみを自動でバックグラウンド保存する（水分など）
 */
function autoSaveField(fieldName, value) {
    const data = getAllData();
    if (!data[selectedDate]) {
        data[selectedDate] = {};
    }
    data[selectedDate][fieldName] = value;
    saveAllData(data);
    updateDashboard();
}

/**
 * フォーム全体のデータをローカルストレージに保存する
 */
function saveCurrentData() {
    const data = getAllData();
    
    const breakfast = document.getElementById('meal-breakfast').value.trim();
    const lunch = document.getElementById('meal-lunch').value.trim();
    const dinner = document.getElementById('meal-dinner').value.trim();
    const snack = document.getElementById('meal-snack').value.trim();
    
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
    
    // トースト通知を表示
    showToast('記録を保存しました！');
    
    // 各表示コンポーネントの更新
    updateDashboard();
}

/**
 * トースト通知を表示する関数
 */
function showToast(message) {
    // 既存のトーストがあれば削除
    const oldToast = document.querySelector('.toast');
    if (oldToast) {
        oldToast.remove();
    }

    // トースト要素の作成
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i data-lucide="check-circle"></i><span>${message}</span>`;
    document.body.appendChild(toast);
    
    // アイコンの有効化
    lucide.createIcons();

    // アニメーション表示
    setTimeout(() => {
        toast.classList.add('show');
    }, 50);

    // 3秒後に消去
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 400);
    }, 3000);
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
        // 今日が未入力の場合、直近に入力された体重を探して表示する
        const latestWeight = findLatestWeight();
        if (latestWeight) {
            summaryWeight.textContent = `${latestWeight} kg (直近)`;
        } else {
            summaryWeight.textContent = '- kg';
        }
    }

    // 2. グラフの更新
    updateChart();

    // 3. カレンダーの描画
    renderCalendar();

    // 4. 履歴リストの更新
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
 * Chart.jsを使用して過去7日間の体重と水分の複合グラフを描画する
 */
function updateChart() {
    const data = getAllData();
    
    // 選択された日付から遡って過去7日分の日付リストを作成
    const labels = [];
    const weightDataset = [];
    const waterDataset = [];
    
    const baseDate = new Date(selectedDate);
    for (let i = 6; i >= 0; i--) {
        const d = new Date(baseDate);
        d.setDate(baseDate.getDate() - i);
        const dStr = getFormattedDate(d);
        
        // ラベルは「月/日」形式
        labels.push(`${d.getMonth() + 1}/${d.getDate()}`);
        
        const dayVal = data[dStr] || {};
        weightDataset.push(dayVal.weight || null);
        waterDataset.push(dayVal.water || 0);
    }

    // 既存のグラフがあれば破棄して再作成
    if (weightChart) {
        weightChart.destroy();
    }

    const ctx = document.getElementById('weightChart').getContext('2d');
    
    // Chart.js グラフの設定
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
                    spanGaps: true // データが抜けている日も線を繋ぐ
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
                        drawOnChartArea: false // 左右のグリッド線が重複して見づらくなるのを防ぐ
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
                    max: 3000 // 最大3リットルに固定して視覚的に分かりやすく
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
    const month = currentDate.getMonth(); // 0-11

    // カレンダーヘッダー（年月表示と曜日）
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

    // 月の最初の日と最後の日を取得
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    const startDayOfWeek = firstDay.getDay(); // 初日の曜日 (0: 日曜日 〜 6: 土曜日)
    const totalDays = lastDay.getDate();

    // 初日の曜日までの空白セルを作成
    for (let i = 0; i < startDayOfWeek; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'calendar-day empty';
        calendarGrid.appendChild(emptyCell);
    }

    // 日付セルの作成
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

        // クリックでその日に移動
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
    
    // 日付の降順（新しい順）にソート
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

    // 直近の5件を表示
    const recentDates = sortedDates.slice(0, 5);

    recentDates.forEach(dateStr => {
        const dayData = data[dateStr];
        
        const item = document.createElement('div');
        item.className = 'history-item';
        
        // 日付のフォーマット（M月D日）
        const dObj = new Date(dateStr);
        const displayDate = `${dObj.getMonth() + 1}月${dObj.getDate()}日`;

        // 体重の表示
        const displayWeight = dayData.weight ? `${dayData.weight}kg` : '-- kg';

        // 食事等の有無タグ
        let hasMeals = (dayData.breakfast || dayData.lunch || dayData.dinner || dayData.snack) ? true : false;
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

        // クリックしたらその日のデータを読み込む
        item.addEventListener('click', () => {
            selectedDate = dateStr;
            document.getElementById('date-picker').value = selectedDate;
            loadDateData(selectedDate);
            updateDashboard();
        });

        historyList.appendChild(item);
    });

    // Lucideアイコンの再適用
    lucide.createIcons();
}

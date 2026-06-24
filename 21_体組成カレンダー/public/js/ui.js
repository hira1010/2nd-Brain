function saveEntry(message = "記録しました") {
  const entry = readEntry();
  const hasValue = METRICS.some(({ key }) => Number.isFinite(entry[key]));

  if (!hasValue) {
    setStatus("記録できる数値がありません");
    return;
  }

  logs[refs.date.value || getTodayKey()] = {
    ...entry,
    updatedAt: new Date().toISOString(),
  };
  persistLogs();
  saveLogToApi(refs.date.value || getTodayKey(), entry);
  render();
  clearEntryInputs();
  setStatus(message);
}

function readEntry() {
  return Object.fromEntries(METRICS.map(({ key }) => [key, toNumber(fieldRefs[key].value)]));
}

function render() {
  renderStats();
  renderGoals();
  renderWeeklyReview();
  renderFoodList();
  renderHistory();
  renderCalendar();

  drawChart();
}

function renderMetricTabs() {
  refs.metricTabs.innerHTML = getVisibleTabMetrics().map((metric) => {
    const active = metric.key === activeMetric ? " active" : "";
    return `<button class="metric-tab${active}" type="button" data-metric="${metric.key}">${metric.label}</button>`;
  }).join("");
}

function renderChartMetricSelect() {
  refs.chartMetricSelect.innerHTML = getVisibleTabMetrics().map((metric) => {
    return `<option value="${metric.key}">${metric.label}</option>`;
  }).join("");
  refs.chartMetricSelect.value = activeMetric;

}

function handleMetricTabClick(event) {
  const button = event.target.closest("[data-metric]");
  if (!button || !refs.metricTabs.contains(button)) {
    return;
  }

  setActiveMetric(button.dataset.metric);
}

function setActiveMetric(metricKey) {
  if (!getVisibleTabMetrics().some(({ key }) => key === metricKey)) {
    return;
  }

  activeMetric = metricKey;
  renderMetricTabs();
  refs.chartMetricSelect.value = activeMetric;

  renderStats();
  renderMetricComment();
  drawChart();
}

function getVisibleTabMetrics() {
  return METRICS.filter(({ key }) => !HIDDEN_TAB_KEYS.has(key));
}

function renderStats() {
  const entries = getSortedEntries("asc");

  refs.statsGrid.innerHTML = STAT_METRIC_KEYS.map((metricKey) => {
    const metric = getMetric(metricKey);
    const validEntries = entries.filter(({ entry }) => Number.isFinite(getMetricValue(entry, metric.key)));
    const latest = validEntries.at(-1);
    const previous = validEntries.at(-2);
    
    const value = getMetricValue(latest?.entry, metric.key);
    const oldValue = getMetricValue(previous?.entry, metric.key);
    const unit = getMetricUnit(metric.key, latest?.entry);
    const diff = Number.isFinite(value) && Number.isFinite(oldValue) ? value - oldValue : null;
    const diffText = diff == null ? "前回比 -" : `前回比 ${diff > 0 ? "+" : ""}${round(diff)}${unit}`;
    return `
      <article class="stat-card">
        <span>${metric.label}</span>
        <strong>${Number.isFinite(value) ? `${round(value)}${unit}` : "-"}</strong>
        <em>${diffText}</em>
        <button class="secondary stat-target-button" type="button" data-target-metric="${metric.key}">目標線</button>
      </article>
    `;
  }).join("");

  refs.statusText.textContent = entries.length ? `${entries.length}件の記録を保存中` : "記録を追加するとグラフが表示されます";
  renderMetricComment(entries);
}

function renderMetricComment(entries = getSortedEntries("asc")) {
  const metric = getMetric(activeMetric) || METRICS[0];
  const comparable = entries.filter(({ entry }) => Number.isFinite(getMetricValue(entry, metric.key)));

  if (comparable.length < 2) {
    refs.metricComment.textContent = `${metric.label}は比較できる前回データがまだありません。`;
    return;
  }

  const latest = comparable.at(-1);
  const previous = comparable.at(-2);
  const currentValue = getMetricValue(latest.entry, metric.key);
  const previousValue = getMetricValue(previous.entry, metric.key);
  const unit = getMetricUnit(metric.key, latest.entry);
  const diff = round(currentValue - previousValue);
  const relation = getDateGapLabel(previous.dateKey, latest.dateKey);

  if (diff === 0) {
    refs.metricComment.textContent = `${metric.label}は${relation}と同じ${round(currentValue)}${unit}です。キープできています。`;
    return;
  }

  const direction = diff > 0 ? "増えました" : "減りました";
  const absoluteDiff = Math.abs(diff);
  const tone = getMetricTone(metric.key, diff);
  refs.metricComment.textContent = `${metric.label}は${relation}より${absoluteDiff}${unit}${direction}。${tone}`;
}

function getMetricValue(entry, key) {
  if (!entry) {
    return NaN;
  }

  if (Number.isFinite(entry[key])) {
    return entry[key];
  }

  if (key === "skeletalMuscleMass" && Number.isFinite(entry.skeletalMuscleRate)) {
    return entry.skeletalMuscleRate;
  }

  return NaN;
}

function getMetricUnit(key, entry) {
  if (key === "skeletalMuscleMass" && entry && !Number.isFinite(entry.skeletalMuscleMass) && Number.isFinite(entry.skeletalMuscleRate)) {
    return "%";
  }

  return getMetric(key)?.unit || "";
}

function getDateGapLabel(previousDate, latestDate) {
  const previous = new Date(`${previousDate}T00:00:00`);
  const latest = new Date(`${latestDate}T00:00:00`);
  const diffDays = Math.round((latest - previous) / MS_PER_DAY);
  return diffDays === 1 ? "前日" : "前回";
}

function getMetricTone(metricKey, diff) {
  if (LOWER_IS_BETTER_KEYS.has(metricKey)) {
    return diff < 0 ? "いい流れです。" : "増えた理由を食事・水分・睡眠から見直しましょう。";
  }

  if (isHigherBetterMetric(metricKey)) {
    return diff > 0 ? "筋肉を守れていていい傾向です。" : "たんぱく質と筋トレ量を少し意識しましょう。";
  }

  return diff < 0 ? "少し下がりました。" : "少し上がりました。";
}

function getMetric(metricKey) {
  return METRICS.find(({ key }) => key === metricKey);
}

function isHigherBetterMetric(metricKey) {
  return HIGHER_IS_BETTER_KEYS.has(metricKey);
}

function isImprovedMetricDiff(metricKey, diff) {
  return isHigherBetterMetric(metricKey) ? diff > 0 : diff < 0;
}

function renderGoals() {
  const currentWeight = getCurrentWeightForGoal();
  const targetWeight = toNumber(refs.targetWeight.value);

  if (!Number.isFinite(currentWeight) || !Number.isFinite(targetWeight)) {
    refs.showAllGoalsButton.hidden = true;
    refs.goalTrack.classList.remove("goal-track-selected");
    refs.goalStatus.textContent = "現在体重と最終目標を入力してください";
    refs.goalTrack.innerHTML = `<p class="empty-state">体重を入力すると、2kgごとの中間目標を作ります。</p>`;
    return;
  }

  if (currentWeight <= targetWeight) {
    setSelectedGoalWeight(null);
    refs.showAllGoalsButton.hidden = true;
    refs.goalTrack.classList.remove("goal-track-selected");
    refs.goalStatus.textContent = `現在 ${round(currentWeight)}kg / 目標 ${round(targetWeight)}kg`;
    refs.goalTrack.innerHTML = `
      <button class="goal-step current" type="button" data-goal="${round(currentWeight)}">
        <span>現在</span>
        <strong>${round(currentWeight)}kg</strong>
      </button>
      <button class="goal-step final" type="button" data-goal="${round(targetWeight)}">
        <span>最終目標</span>
        <strong>${round(targetWeight)}kg</strong>
      </button>
    `;
    return;
  }

  const milestones = buildWeightMilestones(currentWeight, targetWeight, WEIGHT_GOAL_STEP_KG);
  const visibleMilestones = selectedGoalWeight == null ? milestones : milestones.filter((weight) => weight === selectedGoalWeight);
  if (selectedGoalWeight != null && visibleMilestones.length === 0) {
    visibleMilestones.push(selectedGoalWeight);
  }

  const remaining = round(currentWeight - targetWeight);
  refs.showAllGoalsButton.hidden = selectedGoalWeight == null;
  refs.goalTrack.classList.toggle("goal-track-selected", selectedGoalWeight != null);
  refs.goalStatus.textContent = selectedGoalWeight == null
    ? `現在 ${round(currentWeight)}kg / 最終目標 ${round(targetWeight)}kg / 残り ${remaining}kg`
    : `選択中 ${round(selectedGoalWeight)}kg / 最終目標 ${round(targetWeight)}kg`;
  refs.goalTrack.innerHTML = visibleMilestones.map((weight) => {
    const index = milestones.indexOf(weight);
    const isCurrent = index === 0;
    const isFinal = index === milestones.length - 1;
    const label = index === -1 ? "選択目標" : isCurrent ? "現在" : isFinal ? "最終目標" : `目標 ${index}`;
    const isSelected = selectedGoalWeight === weight;
    const className = `goal-step${isCurrent ? " current" : ""}${isFinal ? " final" : ""}${isSelected ? " selected" : ""}`;
    return `
      <button class="${className}" type="button" data-goal="${weight}">
        <span>${label}</span>
        <strong>${round(weight)}kg</strong>
      </button>
    `;
  }).join("");
}

function handleGoalClick(event) {
  const button = event.target.closest("[data-goal]");
  if (!button || !refs.goalTrack.contains(button)) {
    return;
  }

  setSelectedGoalWeight(toNumber(button.dataset.goal));
  renderGoals();
  drawChart();
}

function showAllGoals() {
  setSelectedGoalWeight(null);
  renderGoals();
  drawChart();
}

function loadSelectedGoalWeight() {
  const saved = toNumber(localStorage.getItem(SELECTED_GOAL_KEY));
  return Number.isFinite(saved) ? saved : null;
}

function setSelectedGoalWeight(value) {
  selectedGoalWeight = Number.isFinite(value) ? value : null;

  if (selectedGoalWeight == null) {
    localStorage.removeItem(SELECTED_GOAL_KEY);
    delete metricTargets.weight;
  } else {
    localStorage.setItem(SELECTED_GOAL_KEY, String(selectedGoalWeight));
    metricTargets.weight = selectedGoalWeight;
  }
  persistMetricTargets();
  saveSettingsToApi({ selectedGoalWeight });

}



function handleStatTargetClick(event) {
  const button = event.target.closest("[data-target-metric]");
  if (!button || !refs.statsGrid.contains(button)) {
    return;
  }

  const metricKey = button.dataset.targetMetric;
  const metric = getMetric(metricKey);
  if (!metric) {
    return;
  }

  const currentTarget = getTargetLineValue(metricKey);
  const suggestedTarget = getSuggestedTarget(metricKey);
  if (!Number.isFinite(currentTarget) && !Number.isFinite(suggestedTarget)) {
    return;
  }

  setActiveMetric(metricKey);
  setMetricTarget(metricKey, Number.isFinite(currentTarget) ? currentTarget : suggestedTarget);
}

function promptActiveMetricTarget() {
  const inputTarget = toNumber(refs.metricTargetInput.value);
  const currentTarget = getTargetLineValue(activeMetric);
  const suggestedTarget = getSuggestedTarget(activeMetric);
  const target = Number.isFinite(inputTarget) ? inputTarget : Number.isFinite(currentTarget) ? currentTarget : suggestedTarget;
  if (!Number.isFinite(target)) {
    return;
  }

  setMetricTarget(activeMetric, target);
}

function setMetricTarget(metricKey, value) {
  if (Number.isFinite(value)) {
    metricTargets[metricKey] = value;
    if (metricKey === "weight") {
      selectedGoalWeight = value;
      localStorage.setItem(SELECTED_GOAL_KEY, String(value));
      saveSettingsToApi({ selectedGoalWeight });
    }
  } else {
    delete metricTargets[metricKey];
    if (metricKey === "weight") {
      selectedGoalWeight = null;
      localStorage.removeItem(SELECTED_GOAL_KEY);
      saveSettingsToApi({ selectedGoalWeight });
    }
  }

  persistMetricTargets();
  renderMetricTargetInput();
  renderGoals();
  drawChart();
}



function getSuggestedTarget(metricKey) {
  const latestEntryWithMetric = getSortedEntries("asc").reverse().find(({ entry }) => Number.isFinite(getMetricValue(entry, metricKey)))?.entry;
  const latestValue = getMetricValue(latestEntryWithMetric, metricKey);
  if (!Number.isFinite(latestValue)) {
    return "";
  }

  const step = TARGET_STEP_BY_METRIC[metricKey] || 1;
  const direction = isHigherBetterMetric(metricKey) ? 1 : -1;
  return round(latestValue + step * direction);
}

function loadMetricTargets() {
  try {
    const parsed = JSON.parse(localStorage.getItem(METRIC_TARGETS_KEY) || "{}");
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return {};
    }

    return Object.fromEntries(
      Object.entries(parsed)
        .map(([key, value]) => [key, toNumber(value)])
        .filter(([key, value]) => getMetric(key) && Number.isFinite(value))
    );
  } catch {
    return {};
  }
}

function persistMetricTargets() {
  localStorage.setItem(METRIC_TARGETS_KEY, JSON.stringify(metricTargets));
}

function getCurrentWeightForGoal() {
  const inputWeight = toNumber(fieldRefs.weight.value);
  if (Number.isFinite(inputWeight)) {
    return inputWeight;
  }

  const latest = getSortedEntries("asc").reverse().find(({ entry }) => Number.isFinite(entry.weight));
  return latest?.entry.weight;
}

function buildWeightMilestones(currentWeight, targetWeight, stepKg) {
  const milestones = [round(currentWeight)];
  let next = currentWeight - stepKg;

  while (next > targetWeight) {
    milestones.push(round(next));
    next -= stepKg;
  }

  if (milestones.at(-1) !== round(targetWeight)) {
    milestones.push(round(targetWeight));
  }

  return milestones;
}

function renderHistory() {
  const entries = getSortedEntries("desc");
  if (!entries.length) {
    refs.historyList.innerHTML = `<p class="empty-state">画像を読み取るか、文字データを貼って「文字から記録」を押してください。</p>`;
    return;
  }

  refs.historyList.innerHTML = entries.map(({ dateKey, entry }) => `
    <article class="history-item" data-date="${dateKey}">
      <strong>${formatDate(dateKey)}</strong>
      <span>${formatEntry(entry)}</span>
      <button class="secondary delete-entry" type="button" data-delete="${dateKey}" aria-label="${dateKey}を削除">削除</button>
    </article>
  `).join("");
}

function saveMealLog() {
  const dateKey = refs.date.value || getTodayKey();
  const meal = readMealInputs();

  if (!hasAnyMeal(meal)) {
    setStatus("食事欄が空です。朝食・昼食・晩御飯・間食のどれかを入れてください");
    return;
  }

  foodLogs[dateKey] = {
    ...meal,
    updatedAt: new Date().toISOString(),
  };
  persistFoodLogs();
  saveFoodLogToApi(dateKey, foodLogs[dateKey]);
  renderFoodList();
  renderCalendar();
  setStatus(`${formatDate(dateKey)}の食事を保存しました`);
}

function readMealInputs() {
  return {
    ...Object.fromEntries(MEAL_FIELDS.map(({ key }) => [key, mealRefs[key].value.trim()])),
  };
}

function clearMealInputs() {
  MEAL_FIELDS.forEach(({ key }) => {
    mealRefs[key].value = "";
  });
}

function writeMealInputs(meal) {
  MEAL_FIELDS.forEach(({ key }) => {
    if (typeof meal[key] === "string" && meal[key].trim()) {
      mealRefs[key].value = meal[key].trim();
    }
  });
}



function loadMealInputsForDate(dateKey) {
  const meal = foodLogs[dateKey] || {};
  MEAL_FIELDS.forEach(({ key }) => {
    mealRefs[key].value = meal[key] || "";
  });
}

function renderFoodList() {
  const entries = getSortedFoodEntries("desc");
  if (!entries.length) {
    refs.foodList.innerHTML = `<p class="empty-state">日付を選んで、朝食・昼食・晩御飯・間食を保存すると一覧に表示されます。</p>`;
    return;
  }

  refs.foodList.innerHTML = entries.map(({ dateKey, meal }) => `
    <article class="food-item" data-food-date="${dateKey}">
      <strong>${formatDate(dateKey)}</strong>
      <div class="food-lines">
        ${MEAL_FIELDS.map(({ key, label }) => `
          <p>
            <b>${label}</b>
            <span>${escapeHtml(meal[key] || "-")}</span>
          </p>
        `).join("")}
      </div>
      <button class="secondary delete-food" type="button" data-delete-food="${dateKey}" aria-label="${dateKey}の食事を削除">削除</button>
    </article>
  `).join("");
}

function handleFoodListClick(event) {
  const deleteButton = event.target.closest("[data-delete-food]");
  if (deleteButton) {
    delete foodLogs[deleteButton.dataset.deleteFood];
    persistFoodLogs();
    deleteFoodLogFromApi(deleteButton.dataset.deleteFood);
    renderFoodList();
    renderCalendar();
    loadMealInputsForDate(refs.date.value);
    setStatus("食事メモを削除しました");
    return;
  }

  const item = event.target.closest("[data-food-date]");
  if (!item) {
    return;
  }

  refs.date.value = item.dataset.foodDate;
  loadMealInputsForDate(item.dataset.foodDate);
  setStatus("食事メモを入力欄に読み込みました");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderWeeklyReview() {
  const entries = getSortedEntries("asc").slice(-WEEKLY_REVIEW_DAYS);
  if (entries.length < 2) {
    refs.weeklyReviewContent.innerHTML = `<p class="empty-state">2件以上記録すると週刊レビューを作れます。</p>`;
    return;
  }

  const startDate = formatDate(entries[0].dateKey);
  const endDate = formatDate(entries.at(-1).dateKey);
  const rows = WEEKLY_REVIEW_METRIC_KEYS
    .map((metricKey) => buildWeeklyReviewRow(metricKey, entries))
    .filter(Boolean);

  refs.weeklyReviewContent.innerHTML = `
    <div class="weekly-review-summary">
      <span>${startDate}〜${endDate} / ${entries.length}件</span>
      <strong>${buildWeeklyLead(entries)}</strong>
    </div>
    <div class="weekly-review-grid">
      ${rows.join("")}
    </div>
  `;
}

async function createWeeklyAiPrompt() {
  const weekRange = getCurrentMondaySundayRange();
  const entries = getEntriesInDateRange(weekRange.startKey, weekRange.endKey);

  if (!entries.length) {
    setStatus(`${formatDate(weekRange.startKey)}〜${formatDate(weekRange.endKey)}の記録がありません`);
    return;
  }

  const prompt = buildWeeklyAiPrompt(entries, weekRange);
  refs.rawInput.value = prompt;
  await copyTextToClipboard(prompt);
  refs.rawInput.focus();
  setStatus(`AIプロンプトを作成しました（${formatDate(weekRange.startKey)}〜${formatDate(weekRange.endKey)} / ${entries.length}件）`);
}

function getCurrentMondaySundayRange() {
  const latestDateKey = getSortedEntries("asc").at(-1)?.dateKey || getTodayKey();
  const latestDate = new Date(`${latestDateKey}T00:00:00`);
  const day = latestDate.getDay();
  const diffToMonday = day === 0 ? -6 : 1 - day;
  const monday = new Date(latestDate);
  monday.setDate(latestDate.getDate() + diffToMonday);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  return { startKey: toDateKey(monday), endKey: toDateKey(sunday) };
}

function getEntriesInDateRange(startKey, endKey) {
  return getSortedEntries("asc").filter(({ dateKey }) => dateKey >= startKey && dateKey <= endKey);
}

function buildWeeklyAiPrompt(entries, weekRange) {
  const startDate = formatDate(weekRange.startKey);
  const endDate = formatDate(weekRange.endKey);
  const summaryRows = WEEKLY_REVIEW_METRIC_KEYS
    .map((metricKey) => buildPromptMetricSummary(metricKey, entries))
    .filter(Boolean)
    .join("\n");
  const dailyRows = entries.map(({ dateKey, entry }) => {
    return [
      `- ${formatDate(dateKey)}`,
      `  体組成: ${formatEntry(entry)}`,
      `  食事: ${formatMealEntry(foodLogs[dateKey])}`,
    ].join("\n");
  }).join("\n");

  return [
    "以下は体組成の1週間データです。",
    `期間: ${startDate}〜${endDate}（月曜始まり・日曜終わり）`,
    "",
    "お願い:",
    "1. 体重・体脂肪率・筋肉量・BMI・内臓脂肪・基礎代謝・体内年齢の変化をわかりやすく要約してください。",
    "2. 良かった点を3つ、注意点を3つ出してください。",
    "3. 来週やることを食事・運動・睡眠の3項目で具体的に提案してください。",
    "4. 朝食・昼食・晩御飯・間食と体組成の関係も見てください。",
    "5. 数字の増減に一喜一憂しすぎない、続けやすいコメントにしてください。",
    "",
    "週の変化:",
    summaryRows || "- 比較できる項目が不足しています。",
    "",
    "日別データ:",
    dailyRows,
  ].join("\n");
}

function buildPromptMetricSummary(metricKey, entries) {
  const metric = getMetric(metricKey);
  const comparable = entries
    .map(({ entry }) => ({ value: getMetricValue(entry, metricKey), entry }))
    .filter(({ value }) => Number.isFinite(value));

  if (!metric || comparable.length < 2) {
    return "";
  }

  const first = comparable[0];
  const latest = comparable.at(-1);
  const unit = getMetricUnit(metricKey, latest.entry);
  const diff = round(latest.value - first.value);
  return `- ${metric.label}: ${round(first.value)}${unit} → ${round(latest.value)}${unit}（${diff > 0 ? "+" : ""}${diff}${unit}）`;
}

async function copyTextToClipboard(text) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
    }
  } catch {
    // Clipboard access is optional; the prompt remains in the text area.
  }
}

function buildWeeklyReviewRow(metricKey, entries) {
  const metric = getMetric(metricKey);
  const comparable = entries
    .map(({ entry }) => ({ value: getMetricValue(entry, metricKey), entry }))
    .filter(({ value }) => Number.isFinite(value));

  if (!metric || comparable.length < 2) {
    return "";
  }

  const first = comparable[0];
  const latest = comparable.at(-1);
  const unit = getMetricUnit(metricKey, latest.entry);
  const diff = round(latest.value - first.value);
  const diffText = diff === 0 ? "変化なし" : `${diff > 0 ? "+" : ""}${diff}${unit}`;
  const tone = getWeeklyMetricTone(metricKey, diff);
  const reviewClass = getWeeklyReviewClass(metricKey, diff);

  return `
    <article class="weekly-review-item ${reviewClass} metric-${metricKey}">
      <div class="weekly-review-item-head">
        <span>${metric.label}</span>
        <b>${diffText}</b>
      </div>
      <div class="weekly-review-values">
        <strong>${round(first.value)}${unit}</strong>
        <span>→</span>
        <strong>${round(latest.value)}${unit}</strong>
      </div>
      <p>${tone}</p>
    </article>
  `;
}

function getWeeklyReviewClass(metricKey, diff) {
  if (diff === 0) {
    return "neutral";
  }

  return isImprovedMetricDiff(metricKey, diff) ? "good" : "watch";
}

function getWeeklyMetricTone(metricKey, diff) {
  if (diff === 0) {
    return "大きな変化はありません。今の生活リズムを崩さず、次の記録で同じ水準を保てるか見ていきましょう。";
  }

  const improved = isImprovedMetricDiff(metricKey, diff);
  const comments = {
    weight: improved
      ? "体重はしっかり下がっています。急ぎすぎず、食事量と睡眠を安定させてこのペースを続けましょう。"
      : "体重が増えています。食べすぎだけでなく、水分・塩分・睡眠不足でも増えるので、数日単位で見直しましょう。",
    bodyFat: improved
      ? "体脂肪率は下がっています。減量の方向は良いので、たんぱく質を落とさず筋肉を守りましょう。"
      : "体脂肪率が上がっています。間食・夜の炭水化物・運動量を見直し、まずは前週水準に戻しましょう。",
    skeletalMuscleMass: improved
      ? "筋肉量は増えています。たんぱく質と筋トレの流れが良いので、体重を落としながら維持を狙いましょう。"
      : "筋肉量が少し下がっています。食事を減らしすぎず、たんぱく質と軽い筋トレを優先しましょう。",
    visceralFat: improved
      ? "内臓脂肪は下がっています。体重管理と食事改善が効いている可能性があるので、この流れを続けましょう。"
      : "内臓脂肪が上がっています。飲酒・脂質・夜遅い食事を見直し、まずは増加を止めることを目標にしましょう。",
    basalMetabolism: improved
      ? "基礎代謝は上がっています。筋肉量や活動量を守れているサインなので、運動習慣を続けましょう。"
      : "基礎代謝が下がっています。筋肉量低下や活動量不足の影響もあるので、歩数と筋トレを少し足しましょう。",
  };

  return comments[metricKey] || (improved ? "良い方向に動いています。この調子で次の記録も確認しましょう。" : "注意したい変化です。生活リズムを一つだけ見直して様子を見ましょう。");
}

function buildWeeklyLead(entries) {
  const weight = getWeeklyDiff("weight", entries);
  const bodyFat = getWeeklyDiff("bodyFat", entries);
  const muscle = getWeeklyDiff("skeletalMuscleMass", entries);

  if (weight && weight.diff < 0 && muscle && muscle.diff >= 0) {
    return "体重を落としながら筋肉量を守れている良い週です。";
  }

  if (weight && weight.diff < 0 && bodyFat && bodyFat.diff <= 0) {
    return "体重と体脂肪が下がっていて、減量の流れは良好です。";
  }

  if (weight && weight.diff > 0) {
    return "体重が増えているので、食事量・水分・睡眠の影響を見直しましょう。";
  }

  return "大きく崩れていないので、次の記録も同じペースで見ていきましょう。";
}

function getWeeklyDiff(metricKey, entries) {
  const comparable = entries
    .map(({ entry }) => getMetricValue(entry, metricKey))
    .filter((value) => Number.isFinite(value));

  if (comparable.length < 2) {
    return null;
  }

  return { first: comparable[0], latest: comparable.at(-1), diff: round(comparable.at(-1) - comparable[0]) };
}


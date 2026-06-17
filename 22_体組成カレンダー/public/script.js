const STORAGE_KEY = "body-composition-logs-v1";
const FOOD_STORAGE_KEY = "body-composition-food-logs-v1";
const SELECTED_GOAL_KEY = "body-composition-selected-goal-v1";
const METRIC_TARGETS_KEY = "body-composition-metric-targets-v1";

const WEEKLY_REVIEW_DAYS = 7;
const WEIGHT_GOAL_STEP_KG = 2;
const CHART_MIN_WIDTH = 600;
const CHART_MIN_HEIGHT = 320;
const CHART_GRID_LINES = 4;
const CHART_PAD = { left: 58, right: 24, top: 42, bottom: 52 };
const MAX_X_AXIS_LABELS = 6;
const MS_PER_DAY = 86400000;
const API_LOGS_PATH = "/api/logs";
const API_FOOD_LOGS_PATH = "/api/food-logs";
const API_SETTINGS_PATH = "/api/settings";
const API_BASE_URL = location.protocol === "file:" || location.hostname === "127.0.0.1" || location.hostname === "localhost"
  ? "https://still-snow-35c8.hirakura10.workers.dev"
  : "";

const METRICS = [
  { key: "weight", label: "体重", unit: "kg", color: "#0f766e", patterns: ["体重", "weight"] },
  { key: "bodyFat", label: "体脂肪率", unit: "%", color: "#b43333", patterns: ["体脂肪率", "体脂肪", "body fat", "fat"] },
  { key: "bodyFatMass", label: "体脂肪量", unit: "kg", color: "#8f3a3a", patterns: ["体脂肪量"] },
  { key: "subcutaneousFat", label: "皮下脂肪率", unit: "%", color: "#d06b4c", patterns: ["皮下脂肪率", "皮下脂肪"] },
  { key: "skeletalMuscleRate", label: "骨格筋率", unit: "%", color: "#2764b3", patterns: ["骨格筋率", "骨格筋"] },
  { key: "skeletalMuscleMass", label: "筋肉量", unit: "kg", color: "#1d7a9a", patterns: ["骨格筋量", "筋肉量", "muscle"] },
  { key: "bmi", label: "BMI", unit: "", color: "#7c4d1d", patterns: ["bmi"] },
  { key: "visceralFat", label: "内臓脂肪", unit: "", color: "#7b3fb4", patterns: ["内臓脂肪レベル", "内臓脂肪", "内蔵脂肪レベル", "内蔵脂肪", "visceral"] },
  { key: "basalMetabolism", label: "基礎代謝", unit: "kcal", color: "#5a6c21", patterns: ["基礎代謝", "basal metabolism"] },
  { key: "bodyAge", label: "体内年齢", unit: "歳", color: "#4b5563", patterns: ["体内年齢", "体年齢", "body age"] },
];
const HIDDEN_TAB_KEYS = new Set(["bodyFatMass", "subcutaneousFat", "skeletalMuscleRate"]);
const STAT_METRIC_KEYS = ["weight", "bodyFat", "skeletalMuscleMass", "bmi", "visceralFat", "basalMetabolism", "bodyAge"];
const WEEKLY_REVIEW_METRIC_KEYS = ["weight", "bodyFat", "skeletalMuscleMass", "visceralFat", "basalMetabolism"];
const LOWER_IS_BETTER_KEYS = new Set(["weight", "bodyFat", "bodyFatMass", "subcutaneousFat", "bmi", "visceralFat", "bodyAge"]);
const HIGHER_IS_BETTER_KEYS = new Set(["skeletalMuscleRate", "skeletalMuscleMass", "basalMetabolism"]);
const TARGET_STEP_BY_METRIC = {
  basalMetabolism: 50,
  bodyAge: 1,
  bodyFat: 1,
  bmi: 0.5,
  skeletalMuscleMass: 0.5,
  visceralFat: 0.5,
  weight: 2,
};
const MEAL_FIELDS = [
  { key: "breakfast", label: "朝食" },
  { key: "lunch", label: "昼食" },
  { key: "dinner", label: "晩御飯" },
  { key: "snack", label: "間食" },
];


const refs = {
  date: document.getElementById("entryDate"),

  rawInput: document.getElementById("rawInput"),
  parseButton: document.getElementById("parseButton"),
  saveButton: document.getElementById("saveButton"),

  saveMealButton: document.getElementById("saveMealButton"),
  clearMealButton: document.getElementById("clearMealButton"),
  exportButton: document.getElementById("exportButton"),
  resetButton: document.getElementById("resetButton"),
  cloudSyncButton: document.getElementById("cloudSyncButton"),
  metricTabs: document.getElementById("metricTabs"),
  chartMetricSelect: document.getElementById("chartMetricSelect"),

  metricComment: document.getElementById("metricComment"),
  statsGrid: document.getElementById("statsGrid"),
  targetWeight: document.getElementById("targetWeight"),
  goalStatus: document.getElementById("goalStatus"),
  goalTrack: document.getElementById("goalTrack"),
  showAllGoalsButton: document.getElementById("showAllGoalsButton"),
  weeklyReviewButton: document.getElementById("weeklyReviewButton"),
  aiPromptButton: document.getElementById("aiPromptButton"),
  weeklyReviewContent: document.getElementById("weeklyReviewContent"),
  calendarMonthLabel: document.getElementById("calendarMonthLabel"),
  prevMonthButton: document.getElementById("prevMonthButton"),
  nextMonthButton: document.getElementById("nextMonthButton"),
  calendarGrid: document.getElementById("calendarGrid"),
  chart: document.getElementById("trendChart"),
  chartLatestValue: document.getElementById("chartLatestValue"),
  statusText: document.getElementById("statusText"),
  foodList: document.getElementById("foodList"),
  historyList: document.getElementById("historyList"),
};

const fieldRefs = Object.fromEntries(METRICS.map(({ key }) => [key, document.getElementById(key)]));
const mealRefs = Object.fromEntries(MEAL_FIELDS.map(({ key }) => [key, document.getElementById(key)]));


let logs = loadLogs();
let foodLogs = loadFoodLogs();
let activeMetric = "weight";
let currentCalendarDate = new Date();


let selectedGoalWeight = loadSelectedGoalWeight();
let metricTargets = loadMetricTargets();

window.bodyCompositionParser = { parseText };
initialize();

function initialize() {
  refs.date.value = getTodayKey();


  loadMealInputsForDate(refs.date.value);
  bindEvents();
  renderMetricTabs();
  renderChartMetricSelect();
  render();
  syncAllFromApi();
  syncSettingsFromApi();
}

function bindEvents() {
  refs.parseButton.addEventListener("click", parseRawInput);
  refs.saveButton.addEventListener("click", () => saveEntry("入力内容を記録しました"));

  refs.saveMealButton.addEventListener("click", saveMealLog);
  refs.clearMealButton.addEventListener("click", clearMealInputs);
  refs.exportButton.addEventListener("click", exportCsv);
  refs.resetButton.addEventListener("click", resetAll);
  refs.cloudSyncButton.addEventListener("click", () => syncAllFromApi({ showResult: true }));
  refs.metricTabs.addEventListener("click", handleMetricTabClick);
  refs.chartMetricSelect.addEventListener("change", () => setActiveMetric(refs.chartMetricSelect.value));

  refs.statsGrid.addEventListener("click", handleStatTargetClick);
  refs.weeklyReviewButton.addEventListener("click", renderWeeklyReview);
  refs.aiPromptButton.addEventListener("click", createWeeklyAiPrompt);
  refs.historyList.addEventListener("click", handleHistoryClick);
  refs.foodList.addEventListener("click", handleFoodListClick);
  refs.goalTrack.addEventListener("click", handleGoalClick);
  refs.showAllGoalsButton.addEventListener("click", showAllGoals);
  refs.prevMonthButton.addEventListener("click", () => {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
    renderCalendar();
  });
  refs.nextMonthButton.addEventListener("click", () => {
    currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
    renderCalendar();
  });
  refs.calendarGrid.addEventListener("click", handleCalendarClick);
  refs.targetWeight.addEventListener("input", () => {
    setSelectedGoalWeight(null);
    renderGoals();
  });
  refs.date.addEventListener("change", () => {
    loadMealInputsForDate(refs.date.value);
    refs.mealImageStatus.textContent = getMealImageStatusText();
  });
  fieldRefs.weight.addEventListener("input", renderGoals);
  window.addEventListener("resize", drawChart);
}


function parseRawInput() {
  const { text, date, entry, meal } = parseText(refs.rawInput.value);
  if (!text) {
    setStatus("文字データが空です");
    return;
  }

  if (date) {
    refs.date.value = date;
    loadMealInputsForDate(date);
  }

  let count = 0;
  METRICS.forEach(({ key }) => {
    if (entry[key] != null && Number.isFinite(entry[key])) {
      fieldRefs[key].value = String(entry[key]);
      count += 1;
    }
  });

  const hasMeal = hasAnyMeal(meal);
  if (hasMeal) {
    writeMealInputs(meal);
  }

  if (count > 0 || hasMeal) {
    if (count > 0) {
      saveEntry(`${count}項目を読み取って記録しました`);
    }
    if (hasMeal) {
      saveMealLog();
    }
    refs.rawInput.value = "";
    setStatus(`${count + (hasMeal ? 1 : 0)}件を読み取って保存しました`);
    return;
  }

  if (count === 0) {
    setStatus("読み取れる数値が見つかりませんでした");
  }
}

function parseText(value) {
  const text = normalizeText(value);
  return {
    text,
    date: extractDate(text),
    entry: parseCsvLike(text) || parseKeyValueText(text),
    meal: parseMealText(text),
  };
}

function parseCsvLike(text) {
  const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  if (lines.length < 2 || !lines[0].includes(",")) {
    return null;
  }

  const headers = splitCsvLine(lines[0]);
  const values = splitCsvLine(lines[1]);
  const entry = {};

  headers.forEach((header, index) => {
    const metric = findMetricByLabel(header);
    if (metric) {
      entry[metric.key] = toNumber(values[index]);
    }
  });

  return Object.keys(entry).length ? entry : null;
}

function parseKeyValueText(text) {
  const entry = {};
  const compact = text.replace(/\s+/g, " ");

  METRICS.forEach((metric) => {
    for (const pattern of metric.patterns) {
      const escaped = pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const match = compact.match(new RegExp(`${escaped}\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)`, "i"));
      if (match) {
        entry[metric.key] = toNumber(match[1]);
        break;
      }
    }
  });

  if (!Object.keys(entry).length) {
    const numbers = compact.match(/-?\d+(?:\.\d+)?/g) || [];
    ["weight", "bodyFat", "skeletalMuscleRate", "bmi", "visceralFat", "bodyAge"].forEach((key, index) => {
      if (numbers[index] != null) {
        entry[key] = toNumber(numbers[index]);
      }
    });
  }

  applyBodyCompositionSpecialCases(compact, entry);
  applySectionBodyCompositionCases(text, entry);
  return entry;
}

function parseMealText(text) {
  const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  const meal = {};

  lines.forEach((line, index) => {
    const match = line.match(/^(朝食|昼食|晩御飯|晩ご飯|夕食|夜ご飯|間食|おやつ)\s*[:：]?\s*(.*)$/);
    if (!match) {
      return;
    }

    const key = getMealKeyByLabel(match[1]);
    if (!key) {
      return;
    }

    const inlineValue = match[2].trim();
    const valueLines = inlineValue
      ? [inlineValue, ...collectMealValueLines(lines, index + 1)]
      : collectMealValueLines(lines, index + 1);
    meal[key] = valueLines.join(" / ");
  });

  return normalizeMeal(meal);
}


function collectMealValueLines(lines, startIndex) {
  const values = [];
  for (let index = startIndex; index < lines.length; index += 1) {
    const line = lines[index];
    if (isMealLabelLine(line) || isBodyMetricLabelLine(line) || isDateLikeLine(line)) {
      break;
    }
    values.push(line);
  }
  return values;
}

function getMealKeyByLabel(label) {
  const normalized = label.replace(/\s/g, "");
  if (normalized === "朝食") return "breakfast";
  if (normalized === "昼食") return "lunch";
  if (["晩御飯", "晩ご飯", "夕食", "夜ご飯"].includes(normalized)) return "dinner";
  if (["間食", "おやつ"].includes(normalized)) return "snack";
  return "";
}

function isMealLabelLine(line) {
  return /^(朝食|昼食|晩御飯|晩ご飯|夕食|夜ご飯|間食|おやつ)\s*[:：]?/.test(line);
}

function isBodyMetricLabelLine(line) {
  return /^(体重|体脂肪|体脂肪率|皮下脂肪率|骨格筋|骨格筋率|内[臓蔵]脂肪|内[臓蔵]脂肪レベル|基礎代謝|体(?:内)?年齢|BMI)\s*[:：]?/i.test(line);
}

function isDateLikeLine(line) {
  return /^(記録日|測定日時|測定情報|20\d{2}[\/\-.年]\d{1,2}[\/\-.月]\d{1,2}|\d{1,2}[\/\-.月]\d{1,2})/.test(line);
}

function applyBodyCompositionSpecialCases(text, entry) {
  const bodyFatPair = text.match(new RegExp(`${flexLabel("体脂肪率")}\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)\\s*%?\\s*[（(]\\s*(-?\\d+(?:\\.\\d+)?)\\s*k?g?\\s*[）)]`, "i"));
  if (bodyFatPair) {
    entry.bodyFat = toNumber(bodyFatPair[1]);
    entry.bodyFatMass = toNumber(bodyFatPair[2]);
  }

  const skeletalPair = text.match(new RegExp(`(?:${flexLabel("骨格筋率")}|${flexLabel("骨格筋")})\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)\\s*%?\\s*[（(]\\s*(-?\\d+(?:\\.\\d+)?)\\s*k?g?\\s*[）)]`, "i"));
  if (skeletalPair) {
    entry.skeletalMuscleRate = toNumber(skeletalPair[1]);
    entry.skeletalMuscleMass = toNumber(skeletalPair[2]);
  }

  assignMatchedNumber(entry, "skeletalMuscleMass", text, new RegExp(`(?:${flexLabel("骨格筋量")}|${flexLabel("筋肉量")})\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)\\s*k?g?`, "i"));
  assignMatchedNumber(entry, "skeletalMuscleRate", text, new RegExp(`(?:${flexLabel("骨格筋率")}|${flexLabel("骨格筋")})\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)\\s*%?`, "i"));
  assignMatchedNumber(entry, "subcutaneousFat", text, new RegExp(`${flexLabel("皮下脂肪率")}\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)`));
  assignMatchedNumber(entry, "visceralFat", text, new RegExp(`(?:${flexLabel("内臓脂肪")}|${flexLabel("内蔵脂肪")})\\s*(?:${flexLabel("レベル")})?\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)`, "i"));
  assignMatchedNumber(entry, "basalMetabolism", text, new RegExp(`${flexLabel("基礎代謝")}\\s*[:：]?\\s*([0-9,]+(?:\\.\\d+)?)`, "i"));
  assignMatchedNumber(entry, "bodyAge", text, new RegExp(`(?:${flexLabel("体内年齢")}|${flexLabel("体年齢")})\\s*[:：]?\\s*(-?\\d+(?:\\.\\d+)?)`, "i"));
}

function assignMatchedNumber(entry, key, text, pattern) {
  const match = text.match(pattern);
  if (match) {
    entry[key] = toNumber(match[1]);
  }
}

function flexLabel(label) {
  return label.split("").map((char) => char.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("\\s*");
}

function applySectionBodyCompositionCases(text, entry) {
  const lines = text.split(/\n+/).map((line) => cleanSectionLine(line)).filter(Boolean);

  lines.forEach((line, index) => {
    const next = lines[index + 1] || "";
    const afterNext = lines[index + 2] || "";

    applySimpleSectionValue(entry, line, next);
    applyBodyFatSection(entry, line, next);
    applyMuscleSection(entry, line, next, afterNext);
  });
}

function cleanSectionLine(line) {
  return line
    .trim()
    .replace(/\uFE0F/g, "")
    .replace(/^[^0-9A-Za-zぁ-んァ-ン一-龯]+/, "")
    .trim();
}

function applySimpleSectionValue(entry, label, valueLine) {
  const sectionMap = [
    { pattern: /^体重$/, key: "weight", valuePattern: /(-?\d+(?:\.\d+)?)\s*kg/i },
    { pattern: /^皮下脂肪率$/, key: "subcutaneousFat", valuePattern: /(?:全体\s*[:：]?\s*)?(-?\d+(?:\.\d+)?)\s*%?/ },
    { pattern: /^内[臓蔵]脂肪レベル$/, key: "visceralFat", valuePattern: /(-?\d+(?:\.\d+)?)/ },
    { pattern: /^基礎代謝$/, key: "basalMetabolism", valuePattern: /([0-9,]+(?:\.\d+)?)/ },
    { pattern: /^体(?:内)?年齢$/, key: "bodyAge", valuePattern: /(-?\d+(?:\.\d+)?)/ },
    { pattern: /^BMI$/i, key: "bmi", valuePattern: /(-?\d+(?:\.\d+)?)/ },
  ];
  const section = sectionMap.find(({ pattern }) => pattern.test(label));
  if (section) {
    assignMatchedNumber(entry, section.key, valueLine, section.valuePattern);
  }
}

function applyBodyFatSection(entry, label, valueLine) {
  if (!/^体脂肪(?:率)?$/.test(label)) {
    return;
  }

  assignPercentMassPair(entry, valueLine, "bodyFat", "bodyFatMass");
}

function applyMuscleSection(entry, label, nextLine, afterNextLine) {
  if (!/^骨格筋(?:率)?$/.test(label)) {
    return;
  }

  const valueLine = /骨格筋率|^全体/.test(nextLine) ? nextLine : afterNextLine;
  assignPercentMassPair(entry, valueLine, "skeletalMuscleRate", "skeletalMuscleMass");
  assignMatchedNumber(entry, "skeletalMuscleMass", afterNextLine, /(?:骨格筋量|筋肉量)\s*[:：]?\s*(-?\d+(?:\.\d+)?)\s*k?g?/i);
}

function assignPercentMassPair(entry, text, rateKey, massKey) {
  const value = text.match(/(?:全体\s*[:：]?\s*)?(-?\d+(?:\.\d+)?)\s*%?\s*[（(]?\s*(-?\d+(?:\.\d+)?)?\s*k?g?/i);
  if (!value) {
    return;
  }

  entry[rateKey] = toNumber(value[1]);
  if (value[2] != null) {
    entry[massKey] = toNumber(value[2]);
  }
}

function findMetricByLabel(label) {
  const normalized = String(label).toLowerCase();
  return METRICS.find((metric) => {
    return metric.key.toLowerCase() === normalized || metric.patterns.some((pattern) => normalized.includes(pattern.toLowerCase()));
  });
}

function splitCsvLine(line) {
  return line.split(",").map((cell) => cell.trim().replace(/^"|"$/g, ""));
}

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

function drawChart() {
  const canvas = refs.chart;
  const context = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.max(CHART_MIN_WIDTH, Math.floor(rect.width * scale));
  canvas.height = Math.max(CHART_MIN_HEIGHT, Math.floor(rect.height * scale));
  context.setTransform(scale, 0, 0, scale, 0, 0);

  const width = canvas.width / scale;
  const height = canvas.height / scale;
  context.clearRect(0, 0, width, height);

  const metric = getMetric(activeMetric) || METRICS[0];
  const points = getSortedEntries("asc")
    .map(({ dateKey, entry }) => ({ dateKey, value: getMetricValue(entry, metric.key), entry }))
    .filter(({ value }) => Number.isFinite(value) && value > 0);
  const unit = points.length ? getMetricUnit(metric.key, points.at(-1).entry) : metric.unit;
  refs.chartLatestValue.textContent = points.length ? `最新 ${round(points.at(-1).value)}${unit}` : "最新 -";

  drawChartFrame(context, width, height);

  if (points.length === 0) {
    drawEmptyChart(context, width, height, `${metric.label}の記録がありません`);
    return;
  }

  const pad = CHART_PAD;
  const targetLineValue = getTargetLineValue(metric.key);
  const values = points.map(({ value }) => value);
  if (Number.isFinite(targetLineValue) && targetLineValue > 0) {
    values.push(targetLineValue);
  }
  let min = Math.min(...values);
  let max = Math.max(...values);
  const dataMin = min;
  const range = max - min || Math.max(1, max * 0.08);
  min -= range * 0.18;
  max += range * 0.18;

  if (dataMin >= 0 && min < 0) {
    min = 0;
  }

  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const xFor = (index) => pad.left + (points.length === 1 ? plotW / 2 : (plotW * index) / (points.length - 1));
  const yFor = (value) => pad.top + plotH - ((value - min) / (max - min)) * plotH;

  context.strokeStyle = "#e3e9ee";
  context.lineWidth = 1;
  context.fillStyle = "#697784";
  context.font = "12px sans-serif";

  for (let i = 0; i <= CHART_GRID_LINES; i += 1) {
    const y = pad.top + (plotH * i) / CHART_GRID_LINES;
    const value = max - ((max - min) * i) / CHART_GRID_LINES;
    context.beginPath();
    context.moveTo(pad.left, y);
    context.lineTo(width - pad.right, y);
    context.stroke();
    context.fillText(`${round(value)}${unit}`, 10, y + 4);
  }

  context.strokeStyle = metric.color;
  context.lineWidth = 3;
  context.beginPath();
  points.forEach((point, index) => {
    const x = xFor(index);
    const y = yFor(point.value);
    if (index === 0) {
      context.moveTo(x, y);
    } else {
      context.lineTo(x, y);
    }
  });
  context.stroke();

  points.forEach((point, index) => {
    const x = xFor(index);
    const y = yFor(point.value);
    context.fillStyle = "#ffffff";
    context.strokeStyle = metric.color;
    context.lineWidth = 3;
    context.beginPath();
    context.arc(x, y, 5, 0, Math.PI * 2);
    context.fill();
    context.stroke();

    if (index === 0 || index === points.length - 1 || points.length <= 8) {
      context.fillStyle = "#16202a";
      context.font = "700 12px sans-serif";
      context.fillText(`${round(point.value)}${unit}`, x - 18, y - 12);
    }
  });

  drawXAxisLabels(context, points, xFor, height);

  if (Number.isFinite(targetLineValue)) {
    drawTargetLine(context, targetLineValue, yFor, pad, width, unit);
  }
}

function drawXAxisLabels(context, points, xFor, height) {
  const visibleIndexes = getVisibleXAxisIndexes(points.length);
  context.fillStyle = "#697784";
  context.font = "12px sans-serif";
  context.textAlign = "right";

  visibleIndexes.forEach((index) => {
    const label = points[index].dateKey.slice(5).replace("-", "/");
    const x = xFor(index);
    context.save();
    context.translate(x, height - 18);
    context.rotate(-Math.PI / 8);
    context.fillText(label, 0, 0);
    context.restore();
  });

  context.textAlign = "left";
}

function getVisibleXAxisIndexes(pointCount) {
  if (pointCount <= MAX_X_AXIS_LABELS) {
    return Array.from({ length: pointCount }, (_, index) => index);
  }

  const indexes = new Set([0, pointCount - 1]);
  const step = Math.ceil((pointCount - 1) / (MAX_X_AXIS_LABELS - 1));
  for (let index = step; index < pointCount - 1; index += step) {
    indexes.add(index);
  }
  return [...indexes].sort((a, b) => a - b);
}

function getTargetLineValue(metricKey) {
  if (metricKey === "weight" && Number.isFinite(selectedGoalWeight)) {
    return selectedGoalWeight;
  }

  if (Number.isFinite(metricTargets[metricKey])) {
    return metricTargets[metricKey];
  }

  const suggestedTarget = getSuggestedTarget(metricKey);
  return Number.isFinite(suggestedTarget) ? suggestedTarget : NaN;
}

function drawTargetLine(context, targetValue, yFor, pad, width, unit) {
  const y = yFor(targetValue);
  context.save();
  context.strokeStyle = "#d3322f";
  context.fillStyle = "#d3322f";
  context.lineWidth = 4;
  context.shadowColor = "rgba(255, 255, 255, 0.95)";
  context.shadowBlur = 3;
  context.setLineDash([8, 6]);
  context.beginPath();
  context.moveTo(pad.left, y);
  context.lineTo(width - pad.right, y);
  context.stroke();
  context.setLineDash([]);
  context.font = "800 12px sans-serif";
  context.fillText(`目標 ${round(targetValue)}${unit}`, pad.left + 8, Math.max(pad.top + 12, y - 8));
  context.restore();
}

function drawChartFrame(context, width, height) {
  context.fillStyle = "#ffffff";
  context.fillRect(0, 0, width, height);
  context.strokeStyle = "#d7e0e6";
  context.strokeRect(0.5, 0.5, width - 1, height - 1);
}

function drawEmptyChart(context, width, height, message) {
  context.fillStyle = "#697784";
  context.font = "700 16px sans-serif";
  context.textAlign = "center";
  context.fillText(message, width / 2, height / 2);
  context.textAlign = "left";
}

function handleHistoryClick(event) {
  const deleteButton = event.target.closest("[data-delete]");
  if (deleteButton) {
    delete logs[deleteButton.dataset.delete];
    persistLogs();
    deleteLogFromApi(deleteButton.dataset.delete);
    render();
    setStatus("記録を削除しました");
    return;
  }

  const item = event.target.closest("[data-date]");
  if (!item) {
    return;
  }

  const entry = logs[item.dataset.date];
  refs.date.value = item.dataset.date;
  loadMealInputsForDate(item.dataset.date);
  METRICS.forEach(({ key }) => {
    fieldRefs[key].value = Number.isFinite(entry[key]) ? entry[key] : "";
  });
  setStatus("記録を入力欄に読み込みました");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderCalendar() {
  const year = currentCalendarDate.getFullYear();
  const month = currentCalendarDate.getMonth();
  refs.calendarMonthLabel.textContent = `${year}年${month + 1}月`;

  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startDate = new Date(firstDay);
  startDate.setDate(1 - firstDay.getDay()); // Go back to Sunday

  const metric = getMetric(activeMetric) || METRICS[0];
  const unit = metric.unit;
  let html = "";
  const todayKey = getTodayKey();

  for (let i = 0; i < 42; i++) {
    const d = new Date(startDate);
    d.setDate(startDate.getDate() + i);
    const dateKey = toDateKey(d);
    
    const isOtherMonth = d.getMonth() !== month;
    const isToday = dateKey === todayKey;
    const entry = logs[dateKey];
    const foodEntry = foodLogs[dateKey];
    
    let valueText = "";
    if (entry && Number.isFinite(getMetricValue(entry, metric.key))) {
      valueText = `${round(getMetricValue(entry, metric.key))}${unit}`;
    }
    
    let mealText = "";
    let mealTooltip = "";
    if (foodEntry && hasAnyMeal(foodEntry)) {
      const mealItems = MEAL_FIELDS.map(({ key }) => foodEntry[key]).filter(Boolean).join(", ");
      mealText = `🍛 ${mealItems}`;
      mealTooltip = MEAL_FIELDS
        .map(({ key, label }) => foodEntry[key] ? `[${label}] ${foodEntry[key]}` : "")
        .filter(Boolean)
        .join("\n");
    }
    
    let className = "calendar-day";
    if (isOtherMonth) className += " other-month";
    if (isToday) className += " today";

    html += `
      <div class="${className}" data-cal-date="${dateKey}" title="${mealTooltip}">
        <span class="calendar-day-date">${d.getDate()}</span>
        <span class="calendar-day-value">${valueText}</span>
        <span class="calendar-day-meal">${mealText}</span>
      </div>
    `;

    if (i % 7 === 6) {
      // 土曜日の終わりに、その週（日〜土）のデータを集計して週刊レビューセルを作成
      const weekEntries = [];
      for (let j = 0; j < 7; j++) {
        const wd = new Date(startDate);
        wd.setDate(startDate.getDate() + (i - 6 + j));
        const wkDateKey = toDateKey(wd);
        if (logs[wkDateKey]) {
          weekEntries.push({ dateKey: wkDateKey, entry: logs[wkDateKey] });
        }
      }
      
      let weeklyScoreHtml = "-";
      if (weekEntries.length >= 2) {
        let score = 60 + (weekEntries.length * 2); // 記録日数ボーナス
        const firstEntry = weekEntries[0].entry;
        const lastEntry = weekEntries[weekEntries.length - 1].entry;
        
        const goodLabels = [];
        const badLabels = [];

        WEEKLY_REVIEW_METRIC_KEYS.forEach(metricKey => {
          const firstVal = getMetricValue(firstEntry, metricKey);
          const lastVal = getMetricValue(lastEntry, metricKey);
          if (Number.isFinite(firstVal) && Number.isFinite(lastVal)) {
            const diff = round(lastVal - firstVal);
            if (diff !== 0) {
              const improved = isImprovedMetricDiff(metricKey, diff);
              score += improved ? 6 : -6;
              const mInfo = METRICS.find(m => m.key === metricKey);
              let shortName = mInfo ? mInfo.label : "";
              if (metricKey === "skeletalMuscleMass") shortName = "筋肉";
              else if (metricKey === "basalMetabolism") shortName = "代謝";
              else shortName = shortName.replace("率", "").replace("量", "").replace("レベル", "");
              
              if (improved) goodLabels.push(shortName);
              else badLabels.push(shortName);
            }
          }
        });
        
        score = Math.min(100, Math.max(0, score));
        
        const metricFirst = getMetricValue(firstEntry, metric.key);
        const metricLast = getMetricValue(lastEntry, metric.key);
        let diffHtml = "";
        if (Number.isFinite(metricFirst) && Number.isFinite(metricLast)) {
          const diff = round(metricLast - metricFirst);
          const sign = diff > 0 ? "+" : "";
          diffHtml = `<span class="calendar-weekly-label">${sign}${diff}${unit}</span>`;
        }
        
        let commentHtml = "";
        if (goodLabels.length || badLabels.length) {
          commentHtml += `<div class="calendar-weekly-comments">`;
          if (goodLabels.length) commentHtml += `<div class="weekly-good">👍${goodLabels.join(",")}</div>`;
          if (badLabels.length) commentHtml += `<div class="weekly-bad">👎${badLabels.join(",")}</div>`;
          commentHtml += `</div>`;
        }
        
        weeklyScoreHtml = `
          <div class="calendar-weekly-score">${score}点</div>
          ${diffHtml}
          ${commentHtml}
        `;
      }
      
      html += `
        <div class="calendar-weekly">
          ${weeklyScoreHtml}
        </div>
      `;
    }
  }
  
  refs.calendarGrid.innerHTML = html;
}

function handleCalendarClick(event) {
  const dayDiv = event.target.closest("[data-cal-date]");
  if (!dayDiv) return;
  
  const dateKey = dayDiv.dataset.calDate;
  refs.date.value = dateKey;
  loadMealInputsForDate(dateKey);
  
  const entry = logs[dateKey];
  if (entry) {
    METRICS.forEach(({ key }) => {
      fieldRefs[key].value = Number.isFinite(entry[key]) ? entry[key] : "";
    });
    setStatus(`${formatDate(dateKey)} の記録を読み込みました`);
  } else {
    clearEntryInputs();
    setStatus(`${formatDate(dateKey)} を選択しました`);
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function clearInputs() {
  clearEntryInputs();
  clearMealInputs();

  setStatus("入力を消しました");
}

function clearEntryInputs() {
  refs.rawInput.value = "";
  METRICS.forEach(({ key }) => {
    fieldRefs[key].value = "";
  });
}



function resetAll() {
  if (!confirm("保存済みの体組成データと食事メモをすべて削除しますか？")) {
    return;
  }
  logs = {};
  foodLogs = {};
  persistLogs();
  persistFoodLogs();
  clearLogsFromApi();
  clearFoodLogsFromApi();
  clearMealInputs();
  render();
  setStatus("全記録を削除しました");
}

function exportCsv() {
  const header = ["日付", ...METRICS.map(({ label, unit }) => `${label}${unit ? `(${unit})` : ""}`)];
  const rows = getSortedEntries("asc").map(({ dateKey, entry }) => [
    dateKey,
    ...METRICS.map(({ key }) => Number.isFinite(entry[key]) ? entry[key] : ""),
  ]);
  const csv = [header, ...rows].map((row) => row.map(toCsvCell).join(",")).join("\n");
  const blob = new Blob([`\uFEFF${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `body-composition-${getTodayKey()}.csv`;
  link.click();
  URL.revokeObjectURL(url);
  setStatus("CSVを出力しました");
}


function loadLogs() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    return normalizeLogs(parsed);
  } catch {
    return {};
  }
}

function loadFoodLogs() {
  try {
    return normalizeFoodLogs(JSON.parse(localStorage.getItem(FOOD_STORAGE_KEY) || "{}"));
  } catch {
    return {};
  }
}

function normalizeEntry(entry) {
  const normalized = {};
  METRICS.forEach(({ key }) => {
    normalized[key] = toNumber(entry[key]);
  });

  if (!Number.isFinite(normalized.skeletalMuscleMass) && Number.isFinite(toNumber(entry.muscle))) {
    normalized.skeletalMuscleMass = toNumber(entry.muscle);
  }

  normalized.updatedAt = typeof entry.updatedAt === "string" ? entry.updatedAt : "";
  return normalized;
}

function persistLogs() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(logs));
}

function persistFoodLogs() {
  localStorage.setItem(FOOD_STORAGE_KEY, JSON.stringify(foodLogs));
}

async function syncAllFromApi(options = {}) {
  await syncLogsFromApi(options);
  await syncFoodLogsFromApi(options);
}

async function syncLogsFromApi(options = {}) {
  if (!canUseApi()) {
    if (options.showResult) {
      setStatus("この表示ではクラウド再読み込みを使えません");
    }
    return;
  }

  try {
    if (options.showResult) {
      setStatus("クラウドから再読み込み中...");
    }
    const response = await fetch(apiUrl(`${API_LOGS_PATH}?time=${Date.now()}`), { cache: "no-store" });
    if (!response.ok) {
      if (options.showResult) {
        setStatus("クラウド再読み込みに失敗しました");
      }
      return;
    }

    const remoteLogs = normalizeLogs(await response.json());
    logs = remoteLogs;
    persistLogs();
    render();
    setStatus(`クラウドの記録を同期しました（${Object.keys(logs).length}件）`);
  } catch {
    if (options.showResult) {
      setStatus("クラウド再読み込みに失敗しました。通信状態を確認してください");
    }
  }
}

async function syncFoodLogsFromApi(options = {}) {
  if (!canUseApi()) {
    return;
  }

  try {
    const response = await fetch(apiUrl(`${API_FOOD_LOGS_PATH}?time=${Date.now()}`), { cache: "no-store" });
    if (!response.ok) {
      return;
    }

    foodLogs = normalizeFoodLogs(await response.json());
    persistFoodLogs();
    loadMealInputsForDate(refs.date.value);
    renderFoodList();

    if (options.showResult) {
      setStatus(`クラウドの記録を同期しました（体組成${Object.keys(logs).length}件 / 食事${Object.keys(foodLogs).length}件）`);
    }
  } catch {
    if (options.showResult) {
      setStatus("食事メモのクラウド再読み込みに失敗しました");
    }
  }
}

async function syncSettingsFromApi() {
  if (!canUseApi()) {
    return;
  }

  try {
    const response = await fetch(apiUrl(`${API_SETTINGS_PATH}?time=${Date.now()}`), { cache: "no-store" });
    if (!response.ok) {
      return;
    }

    const settings = await response.json();
    const savedGoal = toNumber(settings.selectedGoalWeight);
    if (Number.isFinite(savedGoal)) {
      selectedGoalWeight = savedGoal;
      localStorage.setItem(SELECTED_GOAL_KEY, String(savedGoal));
      metricTargets.weight = savedGoal;
      persistMetricTargets();
      renderGoals();

      drawChart();
    }
  } catch {
    // Local storage remains the fallback when settings sync is unavailable.
  }
}

async function saveSettingsToApi(settings) {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(API_SETTINGS_PATH), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(settings),
    });
  } catch {
    // Keep local storage as the immediate source of truth if the Worker is unavailable.
  }
}

async function saveLogToApi(dateKey, entry) {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(API_LOGS_PATH), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ dateKey, entry }),
    });
  } catch {
    setStatus("この端末には保存しました。クラウド保存はあとで再同期してください");
  }
}

async function deleteLogFromApi(dateKey) {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(`${API_LOGS_PATH}/${encodeURIComponent(dateKey)}`), { method: "DELETE" });
  } catch {
    setStatus("この端末では削除しました。クラウド削除はあとで確認してください");
  }
}

async function saveFoodLogToApi(dateKey, meal) {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(API_FOOD_LOGS_PATH), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ dateKey, meal }),
    });
  } catch {
    setStatus("この端末には食事を保存しました。クラウド保存はあとで再同期してください");
  }
}

async function deleteFoodLogFromApi(dateKey) {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(`${API_FOOD_LOGS_PATH}/${encodeURIComponent(dateKey)}`), { method: "DELETE" });
  } catch {
    setStatus("この端末では食事を削除しました。クラウド削除はあとで確認してください");
  }
}

async function clearLogsFromApi() {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(API_LOGS_PATH), { method: "DELETE" });
  } catch {
    setStatus("この端末では削除しました。クラウド削除はあとで確認してください");
  }
}

async function clearFoodLogsFromApi() {
  if (!canUseApi()) {
    return;
  }

  try {
    await fetch(apiUrl(API_FOOD_LOGS_PATH), { method: "DELETE" });
  } catch {
    setStatus("この端末では食事を削除しました。クラウド削除はあとで確認してください");
  }
}

function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}

function canUseApi() {
  return window.location.protocol.startsWith("http") || Boolean(API_BASE_URL);
}

function normalizeLogs(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return {};
  }

  return Object.fromEntries(
    Object.entries(value)
      .filter(([dateKey, entry]) => /^\d{4}-\d{2}-\d{2}$/.test(dateKey) && entry && typeof entry === "object")
      .map(([dateKey, entry]) => [dateKey, normalizeEntry(entry)])
  );
}

function normalizeFoodLogs(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return {};
  }

  return Object.fromEntries(
    Object.entries(value)
      .filter(([dateKey, meal]) => /^\d{4}-\d{2}-\d{2}$/.test(dateKey) && meal && typeof meal === "object")
      .map(([dateKey, meal]) => [dateKey, normalizeMeal(meal)])
      .filter(([, meal]) => hasAnyMeal(meal))
  );
}

function normalizeMeal(meal) {
  return {
    ...Object.fromEntries(MEAL_FIELDS.map(({ key }) => [key, typeof meal[key] === "string" ? meal[key] : ""])),
    updatedAt: typeof meal.updatedAt === "string" ? meal.updatedAt : "",
  };
}

function getSortedEntries(direction) {
  return Object.entries(logs)
    .map(([dateKey, entry]) => ({ dateKey, entry }))
    .sort((a, b) => direction === "desc" ? b.dateKey.localeCompare(a.dateKey) : a.dateKey.localeCompare(b.dateKey));
}

function getSortedFoodEntries(direction) {
  return Object.entries(foodLogs)
    .map(([dateKey, meal]) => ({ dateKey, meal }))
    .sort((a, b) => direction === "desc" ? b.dateKey.localeCompare(a.dateKey) : a.dateKey.localeCompare(b.dateKey));
}

function formatEntry(entry) {
  return METRICS
    .map(({ key, label, unit }) => Number.isFinite(entry[key]) ? `${label}: ${round(entry[key])}${unit}` : "")
    .filter(Boolean)
    .join(" / ");
}

function formatMealEntry(meal) {
  if (!meal || !hasAnyMeal(meal)) {
    return "記録なし";
  }

  const mealText = MEAL_FIELDS
    .map(({ key, label }) => meal[key] ? `${label}: ${meal[key]}` : "")
    .filter(Boolean)
    .join(" / ");
  return mealText;
}

function hasAnyMeal(meal) {
  return MEAL_FIELDS.some(({ key }) => typeof meal?.[key] === "string" && meal[key].trim());
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeText(value) {
  return String(value)
    .replace(/[０-９．，]/g, (char) => String.fromCharCode(char.charCodeAt(0) - 0xfee0))
    .replace(/,/g, "")
    .replace(/㎏/g, "kg")
    .replace(/％/g, "%")
    .trim();
}

function extractDate(text) {
  const fullDate = text.match(/(20\d{2})[\/\-.年](\d{1,2})[\/\-.月](\d{1,2})/);
  if (fullDate) {
    const month = normalizeDatePart(fullDate[2], 12);
    const day = normalizeDatePart(fullDate[3], 31);
    return month && day ? `${fullDate[1]}-${month}-${day}` : "";
  }

  const shortDate = text.match(/(?:^|\s|測定日時\s*[:：]?\s*)(\d{1,2})[\/\-.月](\d{1,2})(?:日)?(?:[（\(].*?[）\)]|(?=[^\d]|$))/);
  if (shortDate) {
    const month = normalizeDatePart(shortDate[1], 12);
    const day = normalizeDatePart(shortDate[2], 31);
    return month && day ? `${new Date().getFullYear()}-${month}-${day}` : "";
  }

  return "";
}

function normalizeDatePart(value, max) {
  let number = Number(value);

  if (number > max && value.length === 2 && value[0] === value[1]) {
    number = Number(value[0]);
  }

  if (!Number.isInteger(number) || number < 1 || number > max) {
    return "";
  }

  return String(number).padStart(2, "0");
}

function toNumber(value) {
  if (value == null || value === "") {
    return NaN;
  }
  const number = Number(String(value).replace(/[^\d.-]/g, ""));
  return Number.isFinite(number) ? number : NaN;
}

function round(value) {
  return Math.round(value * 10) / 10;
}

function toCsvCell(value) {
  return `"${String(value).replace(/"/g, '""')}"`;
}

function getTodayKey() {
  return toDateKey(new Date());
}

function toDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatDate(dateKey) {
  const [year, month, day] = dateKey.split("-");
  return `${year}/${Number(month)}/${Number(day)}`;
}

function setStatus(message) {
  refs.statusText.textContent = message;
}

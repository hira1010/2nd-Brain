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


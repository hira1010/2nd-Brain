const METRICS = [
  { key: "weight", column: "weight", patterns: ["体重", "weight"] },
  { key: "bodyFat", column: "body_fat", patterns: ["体脂肪率", "体脂肪", "body fat", "fat"] },
  { key: "bodyFatMass", column: "body_fat_mass", patterns: ["体脂肪量"] },
  { key: "subcutaneousFat", column: "subcutaneous_fat", patterns: ["皮下脂肪率", "皮下脂肪"] },
  { key: "skeletalMuscleRate", column: "skeletal_muscle_rate", patterns: ["骨格筋率", "骨格筋"] },
  { key: "skeletalMuscleMass", column: "skeletal_muscle_mass", patterns: ["骨格筋量", "筋肉量", "muscle"] },
  { key: "bmi", column: "bmi", patterns: ["bmi"] },
  { key: "visceralFat", column: "visceral_fat", patterns: ["内臓脂肪レベル", "内臓脂肪", "内蔵脂肪レベル", "内蔵脂肪", "visceral"] },
  { key: "basalMetabolism", column: "basal_metabolism", patterns: ["基礎代謝", "basal metabolism"] },
  { key: "bodyAge", column: "body_age", patterns: ["体内年齢", "体年齢", "body age"] },
];

const COLUMN_BY_KEY = Object.fromEntries(METRICS.map(({ key, column }) => [key, column]));
const CACHE_CONTROL_NO_STORE = "no-store, no-cache, must-revalidate, max-age=0";
const API_LOGS_PATH = "/api/logs";
const API_FOOD_LOGS_PATH = "/api/food-logs";
const API_SETTINGS_PATH = "/api/settings";
const API_EMAIL_TEST_PATH = "/api/email-test";
const PRIVATE_ASSET_PATHS = new Set(["/worker.js", "/wrangler.toml", "/schema.sql", "/server.js", "/README.md"]);
const NUTRITION_COLUMNS = [
  ["calories", "REAL"],
  ["protein", "REAL"],
  ["fat", "REAL"],
  ["carbs", "REAL"],
  ["sugar", "REAL"],
  ["fiber", "REAL"],
  ["salt", "REAL"],
];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS" && url.pathname.startsWith("/api/")) {
      return new Response(null, { headers: corsHeaders() });
    }

    if (url.pathname === API_LOGS_PATH && request.method === "GET") {
      return json(await listLogs(env));
    }

    if (url.pathname === API_LOGS_PATH && request.method === "POST") {
      const payload = await request.json();
      await upsertLog(env, normalizePayload(payload, "site"));
      return json({ ok: true });
    }

    if (url.pathname.startsWith(`${API_LOGS_PATH}/`) && request.method === "DELETE") {
      const dateKey = decodeURIComponent(url.pathname.slice(`${API_LOGS_PATH}/`.length));
      await env.DB.prepare("DELETE FROM body_composition_logs WHERE date_key = ?").bind(dateKey).run();
      return json({ ok: true });
    }

    if (url.pathname === API_LOGS_PATH && request.method === "DELETE") {
      await env.DB.prepare("DELETE FROM body_composition_logs").run();
      return json({ ok: true });
    }

    if (url.pathname === API_FOOD_LOGS_PATH && request.method === "GET") {
      return json(await listFoodLogs(env));
    }

    if (url.pathname === API_FOOD_LOGS_PATH && request.method === "POST") {
      const payload = await request.json();
      await upsertFoodLog(env, normalizeFoodPayload(payload));
      return json({ ok: true });
    }

    if (url.pathname.startsWith(`${API_FOOD_LOGS_PATH}/`) && request.method === "DELETE") {
      const dateKey = decodeURIComponent(url.pathname.slice(`${API_FOOD_LOGS_PATH}/`.length));
      await ensureFoodLogsTable(env);
      await env.DB.prepare("DELETE FROM food_logs WHERE date_key = ?").bind(dateKey).run();
      return json({ ok: true });
    }

    if (url.pathname === API_FOOD_LOGS_PATH && request.method === "DELETE") {
      await ensureFoodLogsTable(env);
      await env.DB.prepare("DELETE FROM food_logs").run();
      return json({ ok: true });
    }

    if (url.pathname === API_SETTINGS_PATH && request.method === "GET") {
      return json(await getSettings(env));
    }

    if (url.pathname === API_SETTINGS_PATH && request.method === "POST") {
      const payload = await request.json();
      await saveSettings(env, payload);
      return json({ ok: true });
    }

    if (url.pathname === API_EMAIL_TEST_PATH && request.method === "POST") {
      const body = await request.text();
      const parsed = parseText(body);
      await upsertLog(env, normalizePayload({ dateKey: parsed.date, entry: parsed.entry, rawText: body }, "email-test"));
      return json({ ok: true, parsed });
    }

    if (isPrivateAsset(url.pathname)) {
      return new Response("Not found", { status: 404 });
    }

    return withNoStore(await env.ASSETS.fetch(request));
  },

  async email(message, env, ctx) {
    const rawText = await readEmailText(message);
    const text = extractUsefulEmailText(rawText);
    const parsed = parseText(text);

    if (!parsed.date || !hasAnyMetric(parsed.entry)) {
      ctx.waitUntil(Promise.resolve());
      return;
    }

    ctx.waitUntil(upsertLog(env, normalizePayload({ dateKey: parsed.date, entry: parsed.entry, rawText: text }, "email")));
  },
};

function isPrivateAsset(pathname) {
  return PRIVATE_ASSET_PATHS.has(pathname) || pathname.startsWith("/.wrangler/");
}

function withNoStore(response) {
  const headers = new Headers(response.headers);
  headers.set("cache-control", CACHE_CONTROL_NO_STORE);
  headers.set("pragma", "no-cache");
  headers.set("expires", "0");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

async function listLogs(env) {
  const result = await env.DB.prepare("SELECT * FROM body_composition_logs ORDER BY date_key ASC").all();
  const logs = {};

  for (const row of result.results || []) {
    logs[row.date_key] = rowToEntry(row);
  }

  return logs;
}

async function ensureFoodLogsTable(env) {
  await env.DB.prepare(`
    CREATE TABLE IF NOT EXISTS food_logs (
      date_key TEXT PRIMARY KEY,
      breakfast TEXT,
      lunch TEXT,
      dinner TEXT,
      snack TEXT,
      calories REAL,
      protein REAL,
      fat REAL,
      carbs REAL,
      sugar REAL,
      fiber REAL,
      salt REAL,
      updated_at TEXT NOT NULL
    )
  `).run();
  for (const [column, type] of NUTRITION_COLUMNS) {
    await addColumnIfMissing(env, "food_logs", column, type);
  }
}

async function listFoodLogs(env) {
  await ensureFoodLogsTable(env);
  const result = await env.DB.prepare("SELECT * FROM food_logs ORDER BY date_key ASC").all();
  const logs = {};

  for (const row of result.results || []) {
    logs[row.date_key] = rowToFoodLog(row);
  }

  return logs;
}

async function ensureSettingsTable(env) {
  await env.DB.prepare(`
    CREATE TABLE IF NOT EXISTS app_settings (
      setting_key TEXT PRIMARY KEY,
      setting_value TEXT,
      updated_at TEXT NOT NULL
    )
  `).run();
}

async function getSettings(env) {
  await ensureSettingsTable(env);
  const result = await env.DB.prepare("SELECT setting_key, setting_value FROM app_settings").all();
  const settings = {};

  for (const row of result.results || []) {
    settings[row.setting_key] = parseSettingValue(row.setting_value);
  }

  return settings;
}

async function saveSettings(env, payload) {
  await ensureSettingsTable(env);
  const settings = payload && typeof payload === "object" ? payload : {};

  for (const [key, value] of Object.entries(settings)) {
    if (!/^[a-zA-Z0-9_.-]+$/.test(key)) {
      continue;
    }

    if (value == null || value === "") {
      await env.DB.prepare("DELETE FROM app_settings WHERE setting_key = ?").bind(key).run();
      continue;
    }

    await env.DB.prepare(`
      INSERT INTO app_settings (setting_key, setting_value, updated_at)
      VALUES (?, ?, ?)
      ON CONFLICT(setting_key) DO UPDATE SET
        setting_value = excluded.setting_value,
        updated_at = excluded.updated_at
    `).bind(key, JSON.stringify(value), new Date().toISOString()).run();
  }
}

function parseSettingValue(value) {
  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
}

function rowToEntry(row) {
  return {
    weight: row.weight,
    bodyFat: row.body_fat,
    bodyFatMass: row.body_fat_mass,
    subcutaneousFat: row.subcutaneous_fat,
    skeletalMuscleRate: row.skeletal_muscle_rate,
    skeletalMuscleMass: row.skeletal_muscle_mass,
    bmi: row.bmi,
    visceralFat: row.visceral_fat,
    basalMetabolism: row.basal_metabolism,
    bodyAge: row.body_age,
    updatedAt: row.updated_at,
  };
}

function rowToFoodLog(row) {
  return {
    breakfast: row.breakfast || "",
    lunch: row.lunch || "",
    dinner: row.dinner || "",
    snack: row.snack || "",
    nutrition: {
      calories: row.calories,
      protein: row.protein,
      fat: row.fat,
      carbs: row.carbs,
      sugar: row.sugar,
      fiber: row.fiber,
      salt: row.salt,
    },
    updatedAt: row.updated_at,
  };
}

function normalizePayload(payload, source) {
  return {
    dateKey: payload.dateKey || payload.date || "",
    entry: payload.entry || payload,
    rawText: payload.rawText || "",
    source,
  };
}

function normalizeFoodPayload(payload) {
  const meal = payload.meal || payload;
  return {
    dateKey: payload.dateKey || payload.date || "",
    meal: {
      breakfast: stringOrEmpty(meal.breakfast),
      lunch: stringOrEmpty(meal.lunch),
      dinner: stringOrEmpty(meal.dinner),
      snack: stringOrEmpty(meal.snack),
      nutrition: normalizeNutrition(meal.nutrition || meal),
    },
  };
}

async function upsertLog(env, payload) {
  if (!payload.dateKey || !hasAnyMetric(payload.entry)) {
    throw new Error("Missing date or metric values");
  }

  const entry = payload.entry;
  await env.DB.prepare(`
    INSERT INTO body_composition_logs (
      date_key, weight, body_fat, body_fat_mass, subcutaneous_fat,
      skeletal_muscle_rate, skeletal_muscle_mass, bmi, visceral_fat,
      basal_metabolism, body_age, raw_text, source, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date_key) DO UPDATE SET
      weight = excluded.weight,
      body_fat = excluded.body_fat,
      body_fat_mass = excluded.body_fat_mass,
      subcutaneous_fat = excluded.subcutaneous_fat,
      skeletal_muscle_rate = excluded.skeletal_muscle_rate,
      skeletal_muscle_mass = excluded.skeletal_muscle_mass,
      bmi = excluded.bmi,
      visceral_fat = excluded.visceral_fat,
      basal_metabolism = excluded.basal_metabolism,
      body_age = excluded.body_age,
      raw_text = excluded.raw_text,
      source = excluded.source,
      updated_at = excluded.updated_at
  `).bind(
    payload.dateKey,
    valueOrNull(entry.weight),
    valueOrNull(entry.bodyFat),
    valueOrNull(entry.bodyFatMass),
    valueOrNull(entry.subcutaneousFat),
    valueOrNull(entry.skeletalMuscleRate),
    valueOrNull(entry.skeletalMuscleMass),
    valueOrNull(entry.bmi),
    valueOrNull(entry.visceralFat),
    valueOrNull(entry.basalMetabolism),
    valueOrNull(entry.bodyAge),
    payload.rawText,
    payload.source,
    new Date().toISOString()
  ).run();
}

async function upsertFoodLog(env, payload) {
  if (!payload.dateKey || !hasAnyMeal(payload.meal)) {
    throw new Error("Missing date or meal values");
  }

  await ensureFoodLogsTable(env);
  await env.DB.prepare(`
    INSERT INTO food_logs (
      date_key, breakfast, lunch, dinner, snack,
      calories, protein, fat, carbs, sugar, fiber, salt, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date_key) DO UPDATE SET
      breakfast = excluded.breakfast,
      lunch = excluded.lunch,
      dinner = excluded.dinner,
      snack = excluded.snack,
      calories = excluded.calories,
      protein = excluded.protein,
      fat = excluded.fat,
      carbs = excluded.carbs,
      sugar = excluded.sugar,
      fiber = excluded.fiber,
      salt = excluded.salt,
      updated_at = excluded.updated_at
  `).bind(
    payload.dateKey,
    payload.meal.breakfast,
    payload.meal.lunch,
    payload.meal.dinner,
    payload.meal.snack,
    valueOrNull(payload.meal.nutrition.calories),
    valueOrNull(payload.meal.nutrition.protein),
    valueOrNull(payload.meal.nutrition.fat),
    valueOrNull(payload.meal.nutrition.carbs),
    valueOrNull(payload.meal.nutrition.sugar),
    valueOrNull(payload.meal.nutrition.fiber),
    valueOrNull(payload.meal.nutrition.salt),
    new Date().toISOString()
  ).run();
}

function valueOrNull(value) {
  return Number.isFinite(value) ? value : null;
}

function hasAnyMetric(entry) {
  return METRICS.some(({ key }) => Number.isFinite(entry?.[key]));
}

function hasAnyMeal(meal) {
  return ["breakfast", "lunch", "dinner", "snack"].some((key) => meal?.[key]?.trim())
    || Object.values(meal?.nutrition || {}).some((value) => Number.isFinite(value));
}

function stringOrEmpty(value) {
  return typeof value === "string" ? value.trim() : "";
}

function normalizeNutrition(nutrition) {
  return Object.fromEntries(NUTRITION_COLUMNS.map(([key]) => [key, toNumber(nutrition?.[key])]));
}

async function addColumnIfMissing(env, tableName, columnName, type) {
  try {
    await env.DB.prepare(`ALTER TABLE ${tableName} ADD COLUMN ${columnName} ${type}`).run();
  } catch {
    // The column already exists on previously migrated databases.
  }
}

async function readEmailText(message) {
  const arrayBuffer = await new Response(message.raw).arrayBuffer();
  return new TextDecoder("utf-8").decode(arrayBuffer);
}

function extractUsefulEmailText(rawText) {
  return rawText
    .replace(/\r/g, "")
    .split("\n")
    .filter((line) => {
      return !/^(From|To|Subject|Date|MIME-Version|Content-Type|Content-Transfer-Encoding):/i.test(line);
    })
    .join("\n")
    .trim();
}

function parseText(value) {
  const text = normalizeText(value);
  return {
    text,
    date: extractDate(text),
    entry: parseCsvLike(text) || parseKeyValueText(text),
  };
}

function parseCsvLike(text) {
  const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  if (lines.length < 2 || !lines[0].includes(",")) {
    return null;
  }

  const headers = lines[0].split(",").map((cell) => cell.trim().replace(/^"|"$/g, ""));
  const values = lines[1].split(",").map((cell) => cell.trim().replace(/^"|"$/g, ""));
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

  applyBodyCompositionSpecialCases(compact, entry);
  applySectionBodyCompositionCases(text, entry);
  return entry;
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
  if (/^体脂肪(?:率)?$/.test(label)) {
    assignPercentMassPair(entry, valueLine, "bodyFat", "bodyFatMass");
  }
}

function applyMuscleSection(entry, label, nextLine, afterNextLine) {
  if (/^骨格筋(?:率)?$/.test(label)) {
    assignPercentMassPair(entry, /骨格筋率|^全体/.test(nextLine) ? nextLine : afterNextLine, "skeletalMuscleRate", "skeletalMuscleMass");
    assignMatchedNumber(entry, "skeletalMuscleMass", afterNextLine, /(?:骨格筋量|筋肉量)\s*[:：]?\s*(-?\d+(?:\.\d+)?)\s*k?g?/i);
  }
}

function assignPercentMassPair(entry, text, rateKey, massKey) {
  const value = text.match(/(?:全体\s*[:：]?\s*)?(-?\d+(?:\.\d+)?)\s*%?\s*[（(]?\s*(-?\d+(?:\.\d+)?)?\s*k?g?/i);
  if (value) {
    entry[rateKey] = toNumber(value[1]);
    if (value[2] != null) {
      entry[massKey] = toNumber(value[2]);
    }
  }
}

function assignMatchedNumber(entry, key, text, pattern) {
  const match = text.match(pattern);
  if (match) {
    entry[key] = toNumber(match[1]);
  }
}

function findMetricByLabel(label) {
  const normalized = String(label).toLowerCase();
  return METRICS.find((metric) => {
    return metric.key.toLowerCase() === normalized || metric.patterns.some((pattern) => normalized.includes(pattern.toLowerCase()));
  });
}

function flexLabel(label) {
  return label.split("").map((char) => char.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("\\s*");
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
  return Number.isInteger(number) && number >= 1 && number <= max ? String(number).padStart(2, "0") : "";
}

function toNumber(value) {
  if (value == null || value === "") {
    return NaN;
  }
  const number = Number(String(value).replace(/[^\d.-]/g, ""));
  return Number.isFinite(number) ? number : NaN;
}

function json(value, init = {}) {
  return new Response(JSON.stringify(value), {
    ...init,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": CACHE_CONTROL_NO_STORE,
      ...corsHeaders(),
      ...(init.headers || {}),
    },
  });
}

function corsHeaders() {
  return {
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET, POST, DELETE, OPTIONS",
    "access-control-allow-headers": "content-type",
  };
}

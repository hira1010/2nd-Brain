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



const fs = require("fs");
const vm = require("vm");

const elementIds = [
  "entryDate",
  "imageInput",
  "imagePickButton",
  "dropZone",
  "ocrButton",
  "previewImage",
  "imageStatus",
  "rawInput",
  "parseButton",
  "sampleButton",
  "clearButton",
  "mealImageInput",
  "mealImagePickButton",
  "mealOcrButton",
  "mealImageStatus",
  "saveMealButton",
  "clearMealButton",
  "exportButton",
  "resetButton",
  "cloudSyncButton",
  "metricTabs",
  "chartMetricSelect",
  "metricTargetInput",
  "metricTargetButton",
  "metricComment",
  "statsGrid",
  "targetWeight",
  "goalStatus",
  "goalTrack",
  "showAllGoalsButton",
  "weeklyReviewButton",
  "aiPromptButton",
  "weeklyReviewContent",
  "trendChart",
  "chartLatestValue",
  "statusText",
  "foodList",
  "historyList",
  "breakfast",
  "lunch",
  "dinner",
  "snack",
  "calories",
  "protein",
  "fat",
  "carbs",
  "sugar",
  "fiber",
  "salt",
  "weight",
  "bodyFat",
  "bodyFatMass",
  "subcutaneousFat",
  "skeletalMuscleRate",
  "skeletalMuscleMass",
  "bmi",
  "visceralFat",
  "basalMetabolism",
  "bodyAge",
];

const elements = Object.fromEntries(elementIds.map((id) => [id, createElement(id)]));
const localStore = new Map();
const sandbox = {
  Blob: function Blob() {},
  URL: { createObjectURL: () => "", revokeObjectURL() {} },
  confirm: () => true,
  console,
  document: { getElementById: (id) => elements[id] },
  fetch: async () => ({ ok: false }),
  localStorage: {
    getItem: (key) => localStore.get(key) || null,
    removeItem: (key) => localStore.delete(key),
    setItem: (key, value) => localStore.set(key, value),
  },
  location: { hostname: "" },
  window: {
    addEventListener() {},
    bodyCompositionParser: null,
    devicePixelRatio: 1,
    location: { hostname: "", protocol: "file:" },
    scrollTo() {},
  },
};

vm.createContext(sandbox);
vm.runInContext(fs.readFileSync("script.js", "utf8"), sandbox);

verify("June 9 section format", `6/9

体重

93.30 kg（前週平均より 1.88 kg 減少）
体脂肪

29.5 %（27.5 kg）
皮下脂肪率

全体：21.3 %
骨格筋

全体：29.6 %（27.9 kg）
内臓脂肪レベル

16.5 level（高い）
基礎代謝

1,951 kcal
体年齢

58 才
BMI

29.4（やや高い）`, {
  date: "2026-06-09",
  entry: {
    weight: 93.3,
    bodyFat: 29.5,
    bodyFatMass: 27.5,
    subcutaneousFat: 21.3,
    skeletalMuscleRate: 29.6,
    skeletalMuscleMass: 27.9,
    visceralFat: 16.5,
    basalMetabolism: 1951,
    bodyAge: 58,
    bmi: 29.4,
  },
});

verify("June 13 emoji heading format", `測定情報

2026/06/13（土） 5:35
時刻表示：5:52 am

⚖️ 体重

93.50 kg
前週平均より 1.68 kg 減少

🧬 体脂肪

体脂肪率：29.5%
体脂肪量：27.6 kg

🟦 皮下脂肪率

20.8%（高い）

💪 骨格筋

骨格筋率：30.0%
骨格筋量：28.1 kg

🔥 内臓脂肪レベル

15.5（高い）

⚡ 基礎代謝

1,945 kcal

🧓 体年齢

57歳

📏 BMI

28.9（やや高い）`, {
  date: "2026-06-13",
  entry: {
    weight: 93.5,
    bodyFat: 29.5,
    bodyFatMass: 27.6,
    subcutaneousFat: 20.8,
    skeletalMuscleRate: 30,
    skeletalMuscleMass: 28.1,
    visceralFat: 15.5,
    basalMetabolism: 1945,
    bodyAge: 57,
    bmi: 28.9,
  },
});

verify("June 7 mixed screenshot text format", `6/7
時刻：12:22
皮下脂肪率：20.8%
両腕：27.0%
体幹：19.2%
両脚：27.4%
骨格筋：30.1%（28.5 kg）
両腕：34.1%
体幹：21.9%
両脚：47.4%
内臓脂肪レベル：16.5 level
基礎代謝：1,964 kcal
体年齢：58〜59才
BMI：29.6（やや高い）

2枚目画像（体重推移・体脂肪）

記録日：06/07(日) 10:28
体重：94.70 kg
体脂肪率：29.4%（27.8 kg）
皮下脂肪率：20.8%
両腕：27.0%
体幹：19.2%
両脚：27.4%
骨格筋：30.1%（28.5 kg）
両腕：34.1%
体幹：21.9%
両脚：47.4%`, {
  date: "2026-06-07",
  entry: {
    weight: 94.7,
    bodyFat: 29.4,
    bodyFatMass: 27.8,
    subcutaneousFat: 20.8,
    skeletalMuscleRate: 30.1,
    skeletalMuscleMass: 28.5,
    visceralFat: 16.5,
    basalMetabolism: 1964,
    bodyAge: 58,
    bmi: 29.6,
  },
});

verify("June 15 current visceral fat format", `測定情報

2026/06/15（月） 6:12

体重
93.20 kg

体脂肪
体脂肪率：28.1%
体脂肪量：26.2 kg

骨格筋
骨格筋率：30.8%
骨格筋量：28.7 kg

内蔵脂肪
15 level（高い）

基礎代謝
1,951 kcal

体年齢
56歳

BMI
28.8（やや高い）`, {
  date: "2026-06-15",
  entry: {
    weight: 93.2,
    bodyFat: 28.1,
    bodyFatMass: 26.2,
    skeletalMuscleRate: 30.8,
    skeletalMuscleMass: 28.7,
    visceralFat: 15,
    basalMetabolism: 1951,
    bodyAge: 56,
    bmi: 28.8,
  },
});

console.log("Parser verification passed");

function createElement(id) {
  return {
    id,
    dataset: {},
    disabled: false,
    files: [],
    hidden: false,
    innerHTML: "",
    textContent: "",
    value: id === "targetWeight" ? "72.4" : "",
    addEventListener() {},
    classList: { add() {}, remove() {}, toggle() {} },
    closest: () => null,
    contains: () => false,
    getBoundingClientRect: () => ({ bottom: 360, height: 360, left: 0, top: 0, width: 900 }),
    getContext: () => ({
      arc() {},
      beginPath() {},
      clearRect() {},
      fill() {},
      fillRect() {},
      fillText() {},
      lineTo() {},
      moveTo() {},
      restore() {},
      save() {},
      setLineDash() {},
      setTransform() {},
      stroke() {},
      strokeRect() {},
      set fillStyle(value) {},
      set font(value) {},
      set lineWidth(value) {},
      set strokeStyle(value) {},
      set textAlign(value) {},
    }),
    parentElement: { classList: { add() {}, remove() {}, toggle() {} } },
    querySelectorAll: () => [],
    removeAttribute() {},
  };
}

function verify(name, text, expected) {
  const actual = sandbox.window.bodyCompositionParser.parseText(text);
  assertEqual(`${name} date`, actual.date, expected.date);

  Object.entries(expected.entry).forEach(([key, value]) => {
    assertNear(`${name} ${key}`, actual.entry[key], value);
  });
}

function assertEqual(label, actual, expected) {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${expected}, got ${actual}`);
  }
}

function assertNear(label, actual, expected) {
  if (!Number.isFinite(actual) || Math.abs(actual - expected) > 0.001) {
    throw new Error(`${label}: expected ${expected}, got ${actual}`);
  }
}

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


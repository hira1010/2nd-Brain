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


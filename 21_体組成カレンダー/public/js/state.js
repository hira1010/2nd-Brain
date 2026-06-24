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


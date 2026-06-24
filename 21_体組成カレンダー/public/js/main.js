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



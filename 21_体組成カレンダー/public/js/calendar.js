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


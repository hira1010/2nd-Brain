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


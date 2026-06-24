function clearInputs() {
  clearEntryInputs();
  clearMealInputs();

  setStatus("入力を消しました");
}

function clearEntryInputs() {
  refs.rawInput.value = "";
  METRICS.forEach(({ key }) => {
    fieldRefs[key].value = "";
  });
}



function resetAll() {
  if (!confirm("保存済みの体組成データと食事メモをすべて削除しますか？")) {
    return;
  }
  logs = {};
  foodLogs = {};
  persistLogs();
  persistFoodLogs();
  clearLogsFromApi();
  clearFoodLogsFromApi();
  clearMealInputs();
  render();
  setStatus("全記録を削除しました");
}

function exportCsv() {
  const header = ["日付", ...METRICS.map(({ label, unit }) => `${label}${unit ? `(${unit})` : ""}`)];
  const rows = getSortedEntries("asc").map(({ dateKey, entry }) => [
    dateKey,
    ...METRICS.map(({ key }) => Number.isFinite(entry[key]) ? entry[key] : ""),
  ]);
  const csv = [header, ...rows].map((row) => row.map(toCsvCell).join(",")).join("\n");
  const blob = new Blob([`\uFEFF${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `body-composition-${getTodayKey()}.csv`;
  link.click();
  URL.revokeObjectURL(url);
  setStatus("CSVを出力しました");
}



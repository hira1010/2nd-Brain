function handleHistoryClick(event) {
  const deleteButton = event.target.closest("[data-delete]");
  if (deleteButton) {
    delete logs[deleteButton.dataset.delete];
    persistLogs();
    deleteLogFromApi(deleteButton.dataset.delete);
    render();
    setStatus("記録を削除しました");
    return;
  }

  const item = event.target.closest("[data-date]");
  if (!item) {
    return;
  }

  const entry = logs[item.dataset.date];
  refs.date.value = item.dataset.date;
  loadMealInputsForDate(item.dataset.date);
  METRICS.forEach(({ key }) => {
    fieldRefs[key].value = Number.isFinite(entry[key]) ? entry[key] : "";
  });
  setStatus("記録を入力欄に読み込みました");
  window.scrollTo({ top: 0, behavior: "smooth" });
}


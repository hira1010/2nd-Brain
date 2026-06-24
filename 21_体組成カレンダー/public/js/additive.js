const ADDITIVE_WARNINGS = [
  {
    name: "リン酸塩（Na）",
    foods: "ハム、ソーセージ、練り物、スナック菓子など",
    risk: "体内のミネラル（カルシウム、亜鉛など）を奪い、免疫力の低下や代謝の悪化を招きます。"
  },
  {
    name: "亜硝酸ナトリウム",
    foods: "ハム、ソーセージ、ベーコン",
    risk: "肉に含まれる成分と反応して強い発がん性物質を生成する恐れがあります。"
  },
  {
    name: "タール色素（赤色〇号、黄色〇号など）",
    foods: "菓子、漬物、清涼飲料水",
    risk: "子供の多動性やアレルギー、発がん性の疑いが指摘されています。"
  },
  {
    name: "合成甘味料（アスパルテームなど）",
    foods: "ダイエット飲料、ノンシュガー菓子",
    risk: "脳（神経系）への影響や、味覚の麻痺、代謝異常を引き起こす可能性があります。"
  },
  {
    name: "安息香酸ナトリウム",
    foods: "栄養ドリンク、清涼飲料水",
    risk: "ビタミンCと反応するとベンゼン（発がん物質）を生成することがあります。"
  },
  {
    name: "合成保存料・防カビ剤",
    foods: "輸入果実、一部の加工食品",
    risk: "腸内細菌のバランスを崩し、自然治癒力を低下させます。"
  }
];

function showRandomAdditiveWarning() {
  const warningDiv = document.getElementById("additiveWarning");
  if (!warningDiv) return;
  const item = ADDITIVE_WARNINGS[Math.floor(Math.random() * ADDITIVE_WARNINGS.length)];
  
  document.getElementById("additiveName").textContent = item.name;
  document.getElementById("additiveFoods").textContent = "🍞 含まれる食品: " + item.foods;
  document.getElementById("additiveRisk").textContent = item.risk;
  
  // 少し遅れて表示（1秒後）
  setTimeout(() => {
    warningDiv.classList.remove("hidden");
  }, 1000);
  
  // 閉じるボタン
  warningDiv.querySelector(".additive-close").addEventListener("click", () => {
    warningDiv.classList.add("hidden");
  }, { once: true });
}

// 既存のDOMContentLoadedの最後に実行されるように追加
document.addEventListener("DOMContentLoaded", () => {
  showRandomAdditiveWarning();
});

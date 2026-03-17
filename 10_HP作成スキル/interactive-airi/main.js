import './style.css'

const state = {
  currentExpression: 'neutral',
  messageTimeout: null
};

const elements = {
  cursor: document.getElementById('custom-cursor'),
  zones: {
    head: document.getElementById('zone-head'),
    chest: document.getElementById('zone-chest'),
    body: document.getElementById('zone-body')
  },
  images: {
    neutral: document.getElementById('character-neutral'),
    shame: document.getElementById('character-shame'),
    angry: document.getElementById('character-angry')
  },
  dialogue: document.getElementById('message-text')
};

// マウス追従
document.addEventListener('mousemove', (e) => {
  elements.cursor.style.left = `${e.clientX}px`;
  elements.cursor.style.top = `${e.clientY}px`;
});

// 表情とセリフの更新
function updateReaction(expression, message) {
  // 画像の切り替え
  Object.values(elements.images).forEach(img => img.classList.remove('active'));
  elements.images[expression].classList.add('active');

  // セリフの更新（タイピング風演出）
  elements.dialogue.innerText = message;

  // 一定時間で戻る（怒りや羞恥の場合）
  if (state.messageTimeout) clearTimeout(state.messageTimeout);
  
  if (expression !== 'neutral') {
    state.messageTimeout = setTimeout(() => {
      updateReaction('neutral', '...あ、掃除に戻りますね。');
    }, 4000);
  }
}

// インタラクション設定
elements.zones.head.addEventListener('click', () => {
  updateReaction('shame', 'えっ...！？ いきなり頭を撫でるなんて...。そ、その、恥ずかしいです...');
});

elements.zones.chest.addEventListener('click', () => {
  updateReaction('angry', 'な、何を...！？ やめてください！ 警察を呼びますよ...っ！');
});

elements.zones.body.addEventListener('click', () => {
  updateReaction('shame', 'あぅ...。触らないでください...。私、ただの清掃員ですから...');
});

// ホバー時の演出（カーソルが少し動くのはCSSで制御）
Object.entries(elements.zones).forEach(([key, zone]) => {
  zone.addEventListener('mouseenter', () => {
    //elements.cursor.style.filter = 'brightness(1.2)';
  });
  zone.addEventListener('mouseleave', () => {
    //elements.cursor.style.filter = 'none';
  });
});

# Skill Harvesting (Agentic Workflow)

## 概要E(Overview)
**"XP & Skill Tree Updater"**
日誌�E「学習」「経験」セクションから、ユーザーが得た「スキル」や「独自ノウハウ�E�暗黙知�E�」を収穫し、�Eロフィール�E�E4_スキルとノウハウ�E�をアチE�EチE�Eトするワークフローです、E
AIがユーザーの成長をリアルタイムで認識し、封E��の提案に活かせるよぁE��します、E

## Trigger
*   **Routine**: `Weekly Review` ワークフローの **Phase 5** として自動実行、E

## Prerequisite (事前準備)
*   **対象篁E��**: 直迁E日間�E日誌ファイルすべて�E�E05_日誌` 配下）、E
*   ターゲチE��ファイル: `00_シスチE��\00_UserProfile\04_スキルとノウハウ(Skills).md`
*   **参�E允E*: `思老E��感情のログ` 冁E�E「学び」や「改喁E��」、およ�E `抽出された情報` セクション、E

---

## Agent Action Protocol

### Step 1: Analysis (刁E��)
**Null Check (重要E**: まずログ全体をスキャンし、新しい「スキル」や「ノウハウ」�E記述があるか確認してください、E
**惁E��がなぁE��吁E*: 「※関連するスキル惁E��は見つかりませんでした。」と出力し、E*ここで処琁E��終亁E*してください、E

ログ冁E�E `Knowledge Candidates` めE`Improvement` セクションを�E析し、以下�E基準で惁E��を�E類します、E

*   **Skill (能劁E技衁E**: 「できるようになったこと」。客観皁E��証明可能な技術。（例：Viduでの動画生�E、Next.jsでのサイト構築！E
*   **Knowhow (ノウハウ/暗黙知)**: 「やってみて刁E��ったコチE��。独自の工夫めE��学。（例：司会時の間�E取り方、特定�E相手への交渉術！E

### Step 2: Categorization (刁E��E
`04_スキルとノウハウ(Skills).md` の既存カチE��リーと比輁E��、どこに配置すべきか決定します、E
*   既存カチE��リ: `コミュニケーション・表現系`, `クリエイチE��ブ�E企画系`, `ビジネス・マ�EケチE��ング系`
*   該当がなぁE��合�E `New Discoveries / Temporary` として扱ぁE��、新設カチE��リを提案する、E

### Step 3: Integration (統吁E
**重要E 既存�E惁E��を削除・上書きしてはぁE��ません。忁E��「追記」を原則とします、E*

1.  ターゲチE��ファイルを読み込む、E
2.  適刁E��セクションの末尾に、以下�E形式で追記する、E
    ```markdown
    *   **[キーワード]** (YYYY-MM追加):
        *   [詳細な説明、得られた知見�E要約]
    ```
3.  もし冁E��が既存�E頁E��と重褁E�E競合する場合（例：以前�Eノウハウが間違ってぁE��場合）�E、古ぁE��E��の下に `> [!UPDATE] YYYY-MM-DD: 新たな知見により修正...` とぁE��た注釈を加える形で更新する、E

### Step 4: Verification (確誁E
*   更新冁E��をユーザーに提示し、「この刁E��で合ってぁE��すか�E�」と確認を求める場合がある�E�基本は自動化で良ぁE��、Conflictingな時�E聞く�E�、E

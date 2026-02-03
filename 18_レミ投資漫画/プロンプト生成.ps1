# レミ投資漫画 プロンプト自動生成スクリプト
# 使い方: .\プロンプト生成.ps1 -Number 1 -Title "配当貴族" -Description "S&P500指数の中で25年以上連続増配している優良銘柄。信頼の証。"

param(
    [Parameter(Mandatory = $true)]
    [int]$Number,  # TIP番号
    
    [Parameter(Mandatory = $true)]
    [string]$Title,  # タイトル
    
    [Parameter(Mandatory = $true)]
    [string]$Description  # 説明文
)

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# フォルダ名を作成（No01_配当貴族 形式）
$FolderName = "No{0:D2}_{1}" -f $Number, $Title
$FolderPath = Join-Path $ScriptDir $FolderName

Write-Host "=== レミ投資漫画 プロンプト生成 ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 フォルダ: $FolderName" -ForegroundColor Yellow
Write-Host "📝 テーマ: $Title" -ForegroundColor Yellow
Write-Host "💡 説明: $Description" -ForegroundColor Yellow
Write-Host ""

# フォルダを作成
if (-not (Test-Path $FolderPath)) {
    New-Item -ItemType Directory -Path $FolderPath | Out-Null
    Write-Host "✓ フォルダを作成しました" -ForegroundColor Green
}
else {
    Write-Host "⚠ フォルダは既に存在します" -ForegroundColor Yellow
}

# 1ページ目プロンプトのテンプレート
$Prompt1 = @"
【⚠️ CRITICAL LAYOUT INSTRUCTION】
MANGA PAGE 1 - VERTICAL DYNAMIC PANEL LAYOUT
- Panel 1 (TOP 40%): Large horizontal panel
- Panel 2 (MIDDLE 30%): Medium horizontal panel  
- Panel 3 (BOTTOM-LEFT 15%): Small vertical panel
- Panel 4 (BOTTOM-RIGHT 15%): Small vertical panel
ALL PANELS ARRANGED VERTICALLY IN READING ORDER FROM TOP TO BOTTOM.
Image dimensions: 1200px width × 1700px height (12:17 aspect ratio).

【⚠️ TEXT BOX REQUIREMENT】
In Panel 1, BOTTOM-RIGHT corner: Draw a BLACK rectangular box with WHITE border containing WHITE TEXT:
「テーマ：$Title」
Font: Bold, Clear Japanese Gothic font.

【🎨 スタイル仕様】
- Japanese manga style
- 6500K neutral white balance
- Clean bright colors with cel shading
- White panel borders with black outlines
- Pure white speech bubbles
- Professional manga quality

【✨ 演出効果】
- Sparkle effects (キラキラ)
- Light particles (光の粒子)
- Motion lines where appropriate

Title: $Title - [サブタイトル]

【Panel 1】導入 (Large top panel - 40%)
Scene: Modern elegant office room with large windows showing city skyline. Afternoon sunlight streaming in.
Characters: 
- Yuto (優斗): (Traditional Japanese black GAKURAN school uniform:1.5), (High stiff stand-up collar:1.4), (Gold buttons:1.3), short black hair, curious expression, sitting at desk, looking up
- Remi (レミ): *CRITICAL VISUAL ANCHOR*: (Silky long SILVER hair:1.6), (Vibrant sharp RED eyes:1.5), (Sharp almond-shaped eyes:1.3). Wearing (tailored RED blazer:1.4), (RED pleated mini skirt:1.3), (black turtleneck top:1.2), (black tights:1.2), (black boots:1.1), (gold chain belt:1.2). Standing confidently with one hand on hip, arrogant confident expression, full body visible showing outfit. NO red hair, NO brown hair, NO pants.
Composition: Yuto on left sitting at desk, Remi standing on right showing full outfit
Dialogue:
- 優斗: 「[優斗のセリフ - テーマに関する質問]」
TEXT BOX (bottom-right corner): 「テーマ：$Title」 in black box with white border

---

【Panel 2】展開 (Medium panel - 30%)
Scene: Same office, closer upper body shot focusing on Remi
Characters: Remi with confident knowing smile, finger raised in teaching gesture, arrogant elegant expression
Remi appearance: (Silver hair:1.5), (Red eyes:1.4), (Red blazer:1.3), confident posture
Dialogue:
- レミ: 「[レミのセリフ - 説明開始]」

---

【Panel 3】反応 (Small left panel - 15%)
Scene: Close-up of Yuto's surprised face
Characters: Yuto with wide eyes, shocked/interested expression
Effects: ^^^ (surprise lines), sparkle effects
Dialogue:
- 優斗: 「[優斗のセリフ - 驚きや興味]」

---

【Panel 4】予告 (Small right panel - 15%)
Scene: Close-up of Remi's confident smirk
Characters: Remi with superior smile, one finger raised, sharp red eyes glinting
Remi appearance: (Silver hair:1.5), (Red eyes:1.4), arrogant confident expression
Effects: Sparkle background, confident aura
Dialogue:
- レミ: 「[レミのセリフ - 次への引き]」

---

【📝 ストーリー構成メモ】
テーマ: $Title
説明: $Description

1P目の役割：
- 優斗が「$Title」について質問する
- レミが興味を引く形で説明を始める
- 2P目への期待を持たせる

推奨シーン：
- オフィスでの会話シーン（基本）
- リラックスした雰囲気で投資の話題

"@

# 2ページ目プロンプトのテンプレート
$Prompt2 = @"
【⚠️ CRITICAL LAYOUT INSTRUCTION】
MANGA PAGE 2 - DYNAMIC MIXED PANEL LAYOUT
- Panel 1 (TOP 50%): Large wide horizontal cinematic panel
- Panel 2 (MIDDLE-LEFT 25%): Vertical panel on left side
- Panel 3 (MIDDLE-RIGHT 25%): Vertical panel on right side
- Panel 4 (BOTTOM 25%): Wide horizontal conclusion panel
ALL PANELS flow naturally for vertical reading.
Image dimensions: 1200px width × 1700px height (12:17 aspect ratio).

【🎨 スタイル仕様】
- Japanese manga style with dramatic cinematic shots
- 6500K neutral white balance
- Rich colors with dynamic contrast
- White panel borders with black outlines
- Pure white speech bubbles
- [テーマに応じたビジュアルスタイル]

【✨ 演出効果】
- [テーマに応じた効果を選択]
- Light particles
- Sparkle effects
- Dramatic lighting

Title: $Title - [サブタイトル2]

【Panel 1】ビジュアル解説 (Large cinematic top panel - 50%)
Scene: [テーマを視覚化する大きなシーン]
[「$Title」を象徴するビジュアル要素]
Effects: [インパクトのある演出]
Narration box (top-left with white background): 「[ナレーション1]」
[キャラクターの有無を指定]

---

【Panel 2】ポイント① (Left vertical panel - 25%)
Scene: [ポイント1を表現するシーン]
Visual metaphor: [メタファー・図解]
Narration box (white background): 「[ポイント1の説明]」
[構成の補足]

---

【Panel 3】ポイント② (Right vertical panel - 25%)  
Scene: [ポイント2を表現するシーン]
Visual metaphor: [メタファー・図解]
Narration box (white background): 「[ポイント2の説明]」
[構成の補足]

---

【Panel 4】オチ・完結 (Wide bottom panel - 25%)
Scene: Back to modern office. Yuto and Remi concluding the lesson.
Characters:
- Yuto (left): (GAKURAN uniform:1.4), (black hair), excited realization expression, [ポーズ]
- Remi (right): *CRITICAL VISUAL ANCHOR*: (Long silver hair:1.5), (Sharp red eyes:1.4), (Red blazer:1.3), (Red pleated skirt:1.2), (black tights:1.1), satisfied confident smile, arms crossed elegantly, arrogant but pleased expression. Full body or upper body showing her signature outfit.
Composition: Both characters in medium shot, Yuto on left excited, Remi on right proud and confident
Effects: Light sparkles around them, warm afternoon sunlight
Dialogue:
- 優斗: 「[優斗の納得・感動のセリフ]」
- レミ: 「[レミの締めのセリフ]」

---

【📝 ストーリー構成メモ】
テーマ: $Title
説明: $Description

2P目の役割：
- 「$Title」の核心を視覚的に説明
- 具体例や比喩で理解を深める
- 納得感のあるオチで完結

推奨ビジュアル：
- Panel 1: テーマを象徴する大きなビジュアル
- Panel 2-3: 具体例や対比
- Panel 4: 二人の会話で締める

"@

# 1ページ目プロンプトを保存
$Prompt1Path = Join-Path $FolderPath "プロンプト_p1.txt"
$Prompt1 | Out-File -FilePath $Prompt1Path -Encoding UTF8
Write-Host "✓ 1ページ目プロンプトを保存: プロンプト_p1.txt" -ForegroundColor Green

# 2ページ目プロンプトを保存
$Prompt2Path = Join-Path $FolderPath "プロンプト_p2.txt"
$Prompt2 | Out-File -FilePath $Prompt2Path -Encoding UTF8
Write-Host "✓ 2ページ目プロンプトを保存: プロンプト_p2.txt" -ForegroundColor Green

# README.mdを作成
$ReadmeContent = @"
# $Title (No.$Number)

## 📊 テーマ情報
**説明**: $Description

## 📁 ファイル構成
- \`プロンプト_p1.txt\` - 1ページ目用プロンプト
- \`プロンプト_p2.txt\` - 2ページ目用プロンプト
- \`p1.png\` - 1ページ目画像（生成後）
- \`p2.png\` - 2ページ目画像（生成後）
- \`見開き.png\` - 見開き版（生成後）

## 🎨 生成手順

### 1. プロンプトを確認・編集
各プロンプトファイルを開いて、セリフやシーンを具体化します。

### 2. 画像生成
Antigravity の \`generate_image\` ツールで生成：

**1ページ目**:
\`\`\`
generate_image(
    ImageName="remi_no${Number}_p1",
    Prompt="[プロンプト_p1.txtの内容]"
)
\`\`\`

**2ページ目**:
\`\`\`
generate_image(
    ImageName="remi_no${Number}_p2",
    Prompt="[プロンプト_p2.txtの内容]"
)
\`\`\`

### 3. 見開き画像作成
親ディレクトリの \`画像結合スクリプト.ps1\` を使用：

\`\`\`powershell
cd ..
.\画像結合スクリプト.ps1 -Page1 "No${Number}_${Title}\p1.png" -Page2 "No${Number}_${Title}\p2.png" -Output "No${Number}_${Title}\見開き.png"
\`\`\`

## 💡 カスタマイズのヒント

### セリフ例
- **優斗の質問**: 「$Title って何ですか？」「どういう意味ですか？」
- **レミの説明**: 「$Description」の内容を噛み砕いて説明
- **優斗の反応**: 驚き、感心、納得
- **レミの締め**: 投資の教訓や格言

### ビジュアル案
テーマ「$Title」に合わせて：
- 歴史的背景がある場合：過去の時代のシーン
- 概念的な場合：メタファーやグラフ
- 具体的な場合：実例のビジュアル化

---
生成日: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

$ReadmePath = Join-Path $FolderPath "README.md"
$ReadmeContent | Out-File -FilePath $ReadmePath -Encoding UTF8
Write-Host "✓ READMEを保存: README.md" -ForegroundColor Green

Write-Host ""
Write-Host "=== 完了！ ===" -ForegroundColor Cyan
Write-Host "フォルダ: $FolderPath" -ForegroundColor White
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. プロンプトファイルを開いて、セリフやシーンを具体化" -ForegroundColor White
Write-Host "2. generate_image で画像を生成" -ForegroundColor White
Write-Host "3. 画像結合スクリプトで見開き版を作成" -ForegroundColor White

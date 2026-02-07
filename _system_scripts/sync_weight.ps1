# 🏥 体重データ同期＆振り返りスクリプト (PowerShell版)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# パス設定
$scriptDir = $PSScriptRoot
$recordFile = Join-Path $scriptDir "01_ダイエット\記録.md"

if (-not (Test-Path $recordFile)) {
    Write-Host "⚠️ ファイルが見つかりません: $recordFile" -ForegroundColor Red
    exit 1
}

# データ読み込み
$content = Get-Content $recordFile -Encoding UTF8 -Raw
$records = @()

# 正規表現でデータ抽出
# ### 2/5 (木) ── **94.3**kg
$pattern = '###\s+(\d+)/(\d+)\s+\([^)]+\)\s+──\s+\*\*([0-9.]+)\*\*kg'
$matches = [regex]::Matches($content, $pattern)

foreach ($match in $matches) {
    $month = [int]$match.Groups[1].Value
    $day = [int]$match.Groups[2].Value
    $weight = [double]$match.Groups[3].Value
    
    # 日付オブジェクト作成（年は現在年と仮定、ただし月が未来なら去年とする簡易ロジック）
    $now = Get-Date
    $year = $now.Year
    $date = Get-Date -Year $year -Month $month -Day $day -Hour 0 -Minute 0 -Second 0
    if ($date -gt $now) {
        $year -= 1
        $date = Get-Date -Year $year -Month $month -Day $day -Hour 0 -Minute 0 -Second 0
    }
    
    $records += [PSCustomObject]@{
        DateObj = $date
        DateStr = "$month/$day"
        Weight  = $weight
    }
}

# 日付順（新しい順）にソート
$records = $records | Sort-Object DateObj -Descending

if ($records.Count -lt 2) {
    Write-Host "⚠️ データが不足しています（最低2日分の記録が必要です）" -ForegroundColor Yellow
    exit
}

$latest = $records[0]
$previous = $records[1]

Write-Host "✅ 最新データ: $($latest.DateStr) - $($latest.Weight)kg" -ForegroundColor Green

# 分析
$diff = $latest.Weight - $previous.Weight
$startWeight = 94.0
$targetWeight = 76.0
$remaining = $latest.Weight - $targetWeight
$progress = (($startWeight - $latest.Weight) / ($startWeight - $targetWeight)) * 100

# 週間平均（直近7件）
$recent7 = $records | Select-Object -First 7
$avg = ($recent7 | Measure-Object -Property Weight -Average).Average

# トレンド
$trend = "不明"
if ($records.Count -ge 3) {
    $recent3 = $records | Select-Object -First 3
    if ($recent3[0].Weight -lt $recent3[-1].Weight) {
        $trend = "減少傾向"
    }
    else {
        $trend = "横ばいor増加"
    }
}

# アドバイス生成
$advice = @()
$nowStr = (Get-Date).ToString("yyyy年MM月dd日 HH:mm")

$advice += "## 🎯 今日の振り返りとアドバイス`n"
$advice += "**日時**: $nowStr`n"

$advice += "### 📊 体重推移の分析`n"
$advice += "- **最新体重**: $($latest.Weight)kg"

if ($diff -lt 0) {
    $diffAbs = [Math]::Abs($diff)
    $advice += "- **前回比**: -$($diffAbs.ToString("0.0"))kg 減 ✨ 素晴らしい！"
    $advice += "- 💪 **Good Job!** 身体が本来の機能を取り戻しつつあります！"
}
elseif ($diff -gt 0) {
    $advice += "- **前回比**: +$($diff.ToString("0.0"))kg"
    $advice += "- 🌱 **大丈夫!** 体重は波があるもの。長期的なトレンドを見ましょう。"
}
else {
    $advice += "- **前回比**: 変化なし（安定）"
}

$advice += "- **週間平均**: $($avg.ToString("0.0"))kg"
$advice += "- **傾向**: $trend"
$advice += "- **目標まで**: あと$($remaining.ToString("0.0"))kg（達成率 $($progress.ToString("0.0"))%）`n"

$advice += "### 🧘‍♂️ 今日のアクションプラン`n"
$advice += "> 「失われた身体機能を呼び戻す」 - Ninniki-nene Style`n"

if ($diff -ge 0.5) {
    $advice += "**📌 重点アクション**:"
    $advice += "- ✅ 16時間断食を再確認（20時夕食→翌12時昼食）"
    $advice += "- ✅ スワイショウ（腕振り運動）で代謝の地盤を作る"
    $advice += "- ✅ 水分補給を意識（水、お茶、ブラックコーヒー）"
}
elseif ($diff -lt 0) {
    $advice += "**🌟 現在のリズムをキープ！**:"
    $advice += "- ✅ 現在の食事リズムを継続"
    $advice += "- ✅ 座りながらドローイン（お客様との通話中もOK）"
    $advice += "- ✅ 1時間に1回、背骨リセット"
}
else {
    $advice += "**🔄 変化をつけてみましょう**:"
    $advice += "- ✅ 運動のバリエーションを増やす（肩甲骨・股関節を動的に）"
    $advice += "- ✅ 食事内容の見直し（添加物チェック）"
}

$advice += "`n**📝 今日の一言**:"
$advice += '> "10分あれば、座りながらでも機能は回復できる。今日も、本来の自分の身体機能を取り戻しましょう！"'

$adviceText = $advice -join "`n"

Write-Host "`n============================================================"
Write-Host $adviceText
Write-Host "============================================================"

# ファイル書き込み
# 最新の記録行を見つけて、その後に追記する
$latestHeader = "### $($latest.DateStr)"
$lines = $content -split "`r`n|`n"
$insertIndex = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match $latestHeader) {
        # セクションの終わりを探す（次の見出しか、ファイル末尾）
        # ここでは単純にこの行の数行後に追加するのではなく、
        # "日誌・メモ"などの記述があるかもしれないので、次の "---" か "###" の手前まで進める
        
        # 簡易的に、この行の直後ではなく、このセクションの既に書かれている内容の後に入れたい。
        # 単純化: 見出し行が見つかったら、そこから次のセクション開始までスキャンして、
        # "🎯 今日の振り返りとアドバイス" が無ければ挿入する。
        
        # 同じ日付のセクション内で既にアドバイスがあるかチェック
        $alreadyExists = $false
        for ($j = $i; $j -lt $lines.Count; $j++) {
            if ($lines[$j] -match "### \d+/\d+") {
                if ($j -ne $i) { break } # 次の別の日付セクションに来たら終了
            }
            if ($lines[$j] -match "🎯 今日の振り返りとアドバイス") {
                $alreadyExists = $true
                break
            }
        }
        
        if ($alreadyExists) {
            Write-Host "`n✅ 本日のアドバイスは既に記録済みです。" -ForegroundColor Cyan
            exit 0
        }
        
        # 挿入位置を決定（次のセクション開始の前、または --- の前）
        $insertIndex = $i + 1
        for ($j = $i + 1; $j -lt $lines.Count; $j++) {
            if ($lines[$j] -match "^---" -or $lines[$j] -match "^### \d+/\d+") {
                $insertIndex = $j
                break
            }
        }
        if ($insertIndex -eq -1) { $insertIndex = $lines.Count } # 末尾
        break
    }
}

if ($insertIndex -ne -1) {
    Write-Host "`n📝 記録ファイルに追記します..."
    
    # 配列に挿入
    $newLines = $lines[0..($insertIndex - 1)] + "" + $adviceText + "" + $lines[$insertIndex..($lines.Count - 1)]
    $newContent = $newLines -join "`n"
    
    # バックアップ
    # Copy-Item $recordFile "$recordFile.bak"
    
    # 書き込み
    [System.IO.File]::WriteAllText($recordFile, $newContent, [System.Text.Encoding]::UTF8)
    Write-Host "🎉 書き込み完了しました！" -ForegroundColor Green
}
else {
    Write-Host "⚠️ 今日の記録セクションが見つかりませんでした。" -ForegroundColor Yellow
}

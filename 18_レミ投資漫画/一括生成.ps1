# レミ投資漫画 一括プロンプト生成スクリプト
# リストから複数のテーマを一度に生成

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== レミ投資漫画 一括プロンプト生成 ===" -ForegroundColor Cyan
Write-Host ""

# テーマリスト（例）
$Topics = @(
    @{Number = 1; Title = "配当貴族"; Description = "S&P500指数の中で25年以上連続増配している優良銘柄。信頼の証。" },
    @{Number = 2; Title = "複利"; Description = "利益が利益を生む魔法。「人類最大の発見」（アインシュタイン）。雪だるま式に増える。" }
    # ここに追加していく...
)

Write-Host "📋 生成するテーマ数: $($Topics.Count)" -ForegroundColor Yellow
Write-Host ""

foreach ($Topic in $Topics) {
    Write-Host "処理中: No$($Topic.Number) - $($Topic.Title)" -ForegroundColor Cyan
    
    # プロンプト生成スクリプトを呼び出し
    & "$ScriptDir\プロンプト生成.ps1" -Number $Topic.Number -Title $Topic.Title -Description $Topic.Description
    
    Write-Host ""
    Start-Sleep -Milliseconds 500
}

Write-Host "=== すべて完了！ ===" -ForegroundColor Green
Write-Host ""
Write-Host "生成されたフォルダ:" -ForegroundColor Yellow
Get-ChildItem -Path $ScriptDir -Directory | Where-Object { $_.Name -match "^No\d+" } | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

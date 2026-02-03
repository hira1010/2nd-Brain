# 選択した動画をループ再生で開くスクリプト
# 使い方: 動画ファイルを引数として渡す

param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath
)

$htmlPath = Join-Path (Split-Path $VideoPath) "video-loop-player.html"
$videoName = Split-Path $VideoPath -Leaf

# 相対パスに変換
$relativeVideoPath = "./$videoName"

# 一時HTMLを作成
$html = @"
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>$videoName - ループ再生</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #4ec9b0;
            font-size: 18px;
            margin-bottom: 20px;
        }
        video {
            max-width: 95vw;
            max-height: 85vh;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }
        .info {
            color: #d4d4d4;
            margin-top: 15px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>🔄 $videoName （ループ再生中）</h1>
    <video controls loop autoplay>
        <source src="$relativeVideoPath" type="video/mp4">
    </video>
    <div class="info">✅ 自動ループ再生モード</div>
</body>
</html>
"@

$tempHtml = Join-Path $env:TEMP "video-loop-$(Get-Random).html"
$html | Out-File -FilePath $tempHtml -Encoding UTF8

# デフォルトブラウザで開く
Start-Process $tempHtml

Write-Host "✅ $videoName をループ再生で開きました" -ForegroundColor Green

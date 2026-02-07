$ErrorActionPreference = "Stop"

$mySender = "hirakura10@gmail.com"
$myPwd = "Teruki1982@@"
$recipient = "hirakura10@mail.com"
$subject = "【レミ投資漫画】マンガノ長編構成プロンプト 全23ファイル"
$body = "お疲れ様です。全23ファイルのMarkdownプロンプトをZipにまとめてお送りします。"

# ワイルドカードを使用して日本語ディレクトリのエンコーディング問題を回避
$zipFile = Get-Item "*.zip" | Where-Object { $_.Name -like "No102_Manga_Prompts_All.zip" }
$attachmentPath = $zipFile.FullName

$p = ConvertTo-SecureString $myPwd -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($mySender, $p)

Send-MailMessage -From $mySender -To $recipient -Subject $subject -Body $body -SmtpServer "smtp.gmail.com" -Port 587 -UseSsl -Credential $cred -Attachments $attachmentPath

Write-Host "Email sent successfully!"

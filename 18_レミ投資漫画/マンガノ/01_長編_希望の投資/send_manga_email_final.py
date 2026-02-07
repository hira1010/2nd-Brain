import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 設定情報
sender_email = "hirakura10@gmail.com"
password = "Teruki1982@@" # ユーザーから提供されたアプリパスワード
receiver_email = "hirakura10@mail.com"
subject = "【レミ投資漫画】マンガノ長編構成プロンプト 全23ファイル"
body = "お疲れ様です。ご依頼いただいた全23ファイルのMarkdownプロンプトを添付にてお送りします。"

# 送信対象ディレクトリ
target_dir = r"c:\Users\hirak\Desktop\2nd-Brain\18_レミ投資漫画\マンガノ\01_長編_希望の投資"

def send_email():
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # ファイルの添付
    files_to_send = [f for f in os.listdir(target_dir) if f.startswith("No102_") and f.endswith(".md")]
    
    for filename in files_to_send:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

    try:
        # GmailのSMTPサーバーに接続
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_email()

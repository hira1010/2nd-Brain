# -*- coding: utf-8 -*-
import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import manga_config as config

def send_email():
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_SENDER
    msg['To'] = config.EMAIL_RECEIVER
    msg['Subject'] = config.EMAIL_SUBJECT
    msg.attach(MIMEText(config.EMAIL_BODY, 'plain'))

    # 繝輔ぃ繧､繝ｫ縺ｮ豺ｻ莉・
    # Files are in the same directory as this script (or BASE_DIR)
    # The original script used target_dir = r"...\01_髟ｷ邱ｨ_蟶梧悍縺ｮ謚戊ｳ・ which matches config.BASE_DIR
    target_dir = config.BASE_DIR
    
    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        return

    files_to_send = [f for f in os.listdir(target_dir) if f.startswith("No102_") and f.endswith(".md")]
    
    if not files_to_send:
        print("No files found to send.")
        return

    for filename in files_to_send:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

    try:
        # Gmail縺ｮSMTP繧ｵ繝ｼ繝舌・縺ｫ謗･邯・
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_email()

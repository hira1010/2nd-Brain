import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send():
    sender = "hirakura10@gmail.com"
    pwd = "Teruki1982@@"
    to = "hirakura10@mail.com"
    zip_name = "No102_Manga_Prompts_All.zip"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = "Manga Prompts All (Zip)"
    msg.attach(MIMEText("Attached: All 23 files in a zip archive.", 'plain'))

    with open(zip_name, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={zip_name}")
        msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, pwd)
    s.send_message(msg)
    s.quit()
    print("DONE")

if __name__ == "__main__":
    send()

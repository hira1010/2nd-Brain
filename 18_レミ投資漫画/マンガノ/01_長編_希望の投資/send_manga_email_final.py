# -*- coding: utf-8 -*-
import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import manga_config as config


def _build_message() -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_SENDER
    msg["To"] = config.EMAIL_RECEIVER
    msg["Subject"] = config.EMAIL_SUBJECT
    msg.attach(MIMEText(config.EMAIL_BODY, "plain"))
    return msg


def _collect_markdown_files(target_dir: str):
    return [
        f for f in os.listdir(target_dir)
        if f.startswith("No102_") and f.endswith(".md")
    ]


def _attach_file(msg: MIMEMultipart, filepath: str, filename: str) -> None:
    with open(filepath, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)


def send_email() -> None:
    msg = _build_message()

    target_dir = config.BASE_DIR
    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        return

    files_to_send = _collect_markdown_files(target_dir)
    if not files_to_send:
        print("No files found to send.")
        return

    for filename in files_to_send:
        filepath = os.path.join(target_dir, filename)
        _attach_file(msg, filepath, filename)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    send_email()

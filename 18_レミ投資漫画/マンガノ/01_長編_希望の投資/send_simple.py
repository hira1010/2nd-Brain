import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def _build_message(sender: str, receiver: str, subject: str, body: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    return msg


def _attach_file(msg: MIMEMultipart, file_path: str, attachment_name: str) -> None:
    with open(file_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={attachment_name}")
    msg.attach(part)


def send() -> None:
    sender = "hirakura10@gmail.com"
    pwd = "Teruki1982@@"
    receiver = "hirakura10@mail.com"
    zip_name = "No102_Manga_Prompts_All.zip"

    msg = _build_message(
        sender=sender,
        receiver=receiver,
        subject="Manga Prompts All (Zip)",
        body="Attached: All 23 files in a zip archive.",
    )
    _attach_file(msg, zip_name, zip_name)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)

    print("DONE")


if __name__ == "__main__":
    send()

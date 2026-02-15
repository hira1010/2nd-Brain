import datetime
import email
import imaplib
import os
from email.header import decode_header
from pathlib import Path
from typing import Optional

# --- Configuration ---
EMAIL = "hirakura10@gmail.com"
PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

IMAP_SERVER = "imap.gmail.com"
SAVE_DIR = Path(r"C:\Users\hirak\Desktop")
SEARCH_SUBJECT = "繝繧､繧ｨ繝・ヨ"  # Subject to look for


def clean_filename(filename: str) -> str:
    """Clean filename to avoid filesystem issues."""
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_", "-")).strip()


def decode_subject(subject_header: Optional[str]) -> str:
    if not subject_header:
        return "(No Subject)"

    subject = ""
    for part, encoding in decode_header(subject_header):
        if isinstance(part, bytes):
            try:
                subject += part.decode(encoding if encoding else "utf-8")
            except (LookupError, UnicodeDecodeError):
                subject += part.decode("utf-8", errors="ignore")
        else:
            subject += part
    return subject


def fetch_emails() -> None:
    if not PASSWORD:
        print("Error: Set GMAIL_APP_PASSWORD in your environment.")
        return

    mail: Optional[imaplib.IMAP4_SSL] = None

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)

        status, count = mail.select("inbox")
        if status != "OK":
            print(f"Failed to select inbox: {status}")
            return

        print(f"Inbox selected, count: {count}")

        status, messages = mail.uid("search", None, "ALL")
        if status != "OK":
            print("No emails found.")
            return

        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} email(s). checking flags and subjects...")

        for email_id in email_ids:
            status, msg_data = mail.uid("fetch", email_id, "(RFC822 FLAGS)")
            if status != "OK":
                continue

            for response_part in msg_data:
                if not isinstance(response_part, tuple):
                    continue

                try:
                    info = response_part[0].decode()
                    if "\\Seen" in info:
                        continue
                except UnicodeDecodeError:
                    pass

                msg = email.message_from_bytes(response_part[1])
                subject = decode_subject(msg.get("Subject"))

                if SEARCH_SUBJECT.lower() not in subject.lower():
                    continue

                print(f"Processing email: {subject}")

                if not msg.is_multipart():
                    continue

                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    filename = part.get_filename()

                    print(f"  - Part: {content_type}, Disposition: {content_disposition}, Filename: {filename}")

                    if not filename and content_type.startswith("image/"):
                        ext = content_type.split("/")[-1]
                        filename = f"unknown_image.{ext}"

                    if not filename:
                        continue

                    filename = clean_filename(filename)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filepath = SAVE_DIR / f"Email_{timestamp}_{filename}"

                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue

                    filepath.write_bytes(payload)
                    print(f"  -> Saved: {filepath.name}")

        mail.close()
        mail.logout()
        print("Done.")

    except Exception as e:
        print(f"Error: {e}")
        if mail is not None:
            try:
                mail.logout()
            except Exception:
                pass


if __name__ == "__main__":
    fetch_emails()

import argparse
import datetime as dt
import email
import imaplib
import os
import sys
from email.header import decode_header
from email.message import Message
from pathlib import Path
from typing import Iterable, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib import config
from lib.utils import get_safe_filename, setup_logger


IMAP_SERVER = "imap.gmail.com"
DEFAULT_SUBJECT = "ダイエット"

logger = setup_logger("scripts.fetch_gmail_diet")


def decode_subject(subject_header: Optional[str]) -> str:
    if not subject_header:
        return "(No Subject)"

    decoded = []
    for part, encoding in decode_header(subject_header):
        if isinstance(part, bytes):
            codec = encoding or "utf-8"
            try:
                decoded.append(part.decode(codec))
            except (LookupError, UnicodeDecodeError):
                decoded.append(part.decode("utf-8", errors="ignore"))
        else:
            decoded.append(part)
    return "".join(decoded)


def iter_unseen_message_ids(mail: imaplib.IMAP4_SSL) -> Iterable[bytes]:
    status, response = mail.uid("search", None, "UNSEEN")
    if status != "OK" or not response:
        return []
    return response[0].split()


def save_attachments(msg: Message, save_dir: Path, prefix: str) -> int:
    saved_count = 0
    save_dir.mkdir(parents=True, exist_ok=True)

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue

        content_disposition = str(part.get("Content-Disposition", ""))
        filename = part.get_filename()
        content_type = part.get_content_type()

        if "attachment" not in content_disposition.lower() and not content_type.startswith("image/"):
            continue

        if not filename and content_type.startswith("image/"):
            ext = content_type.split("/")[-1]
            filename = f"unknown_image.{ext}"

        if not filename:
            continue

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        safe_name = get_safe_filename(filename)
        output_path = save_dir / f"{prefix}_{safe_name}"
        output_path.write_bytes(payload)
        logger.info("Saved: %s", output_path)
        saved_count += 1

    return saved_count


def fetch_emails(
    gmail_address: str,
    app_password: str,
    save_dir: Path,
    subject_filter: str = DEFAULT_SUBJECT,
) -> int:
    saved_total = 0
    mail: Optional[imaplib.IMAP4_SSL] = None

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(gmail_address, app_password)

        status, _ = mail.select("inbox")
        if status != "OK":
            logger.error("Failed to select inbox")
            return 0

        message_ids = list(iter_unseen_message_ids(mail))
        logger.info("Found %d unseen mail(s)", len(message_ids))

        for message_id in message_ids:
            status, msg_data = mail.uid("fetch", message_id, "(RFC822)")
            if status != "OK" or not msg_data:
                continue

            for response_part in msg_data:
                if not isinstance(response_part, tuple):
                    continue

                msg = email.message_from_bytes(response_part[1])
                subject = decode_subject(msg.get("Subject"))

                if subject_filter.lower() not in subject.lower():
                    continue

                timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                prefix = f"Email_{timestamp}"
                logger.info("Processing: %s", subject)
                saved_total += save_attachments(msg, save_dir=save_dir, prefix=prefix)

    except Exception as exc:
        logger.error("Failed to fetch emails: %s", exc)
    finally:
        if mail is not None:
            try:
                mail.close()
            except Exception:
                pass
            try:
                mail.logout()
            except Exception:
                pass

    logger.info("Done. Saved %d attachment(s).", saved_total)
    return saved_total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch unseen Gmail attachments for diet mails.")
    parser.add_argument("--email", default=os.getenv("GMAIL_ADDRESS", "hirakura10@gmail.com"))
    parser.add_argument("--password", default=os.getenv("GMAIL_APP_PASSWORD"))
    parser.add_argument("--subject", default=DEFAULT_SUBJECT)
    parser.add_argument("--save-dir", type=Path, default=config.DESKTOP_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.password:
        logger.error("Set GMAIL_APP_PASSWORD or use --password.")
        return 1

    fetch_emails(
        gmail_address=args.email,
        app_password=args.password,
        save_dir=args.save_dir,
        subject_filter=args.subject,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import imaplib
import email
from email.header import decode_header
import os
import sys
from pathlib import Path
import datetime

# --- Configuration ---
EMAIL = "hirakura10@gmail.com"
# PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") 
# If you don't use env vars, put the 16-char App Password below:
PASSWORD = "YOUR_APP_PASSWORD_HERE" 

IMAP_SERVER = "imap.gmail.com"
SAVE_DIR = Path(r"C:\Users\hirak\Desktop")
SEARCH_SUBJECT = "Diet" # Subject to look for

def clean_filename(filename):
    """Cleans the filename to avoid filesystem issues."""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).strip()

def fetch_emails():
    if PASSWORD == "YOUR_APP_PASSWORD_HERE":
        print("Error: Please set your Google App Password in the script or environment variable.")
        return

    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # Search for unread emails with specific subject
        # SEARCH criteria: UNREAD SUBJECT "Diet"
        status, messages = mail.search(None, f'(UNREAD SUBJECT "{SEARCH_SUBJECT}")')
        
        if status != "OK":
            print("No new emails found.")
            return

        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} new email(s).")

        for email_id in email_ids:
            # Fetch the email
            res, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    print(f"Processing email: {subject}")

                    # Iterate over email parts to find attachments
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    filename = clean_filename(filename)
                                    # Add timestamp to ensure uniqueness and processed order
                                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                    filepath = SAVE_DIR / f"Email_{timestamp}_{filename}"
                                    
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    print(f"  -> Saved: {filepath.name}")
            
            # Mark as read (already done by fetching usually, but let's be sure)
            # Optionally archive or delete: 
            # mail.store(email_id, '+X-GM-LABELS', '\\Trash') 
    
        mail.close()
        mail.logout()
        print("Done.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_emails()

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
PASSWORD = "evvcupwplppoomqg" 

IMAP_SERVER = "imap.gmail.com"
SAVE_DIR = Path(r"C:\Users\hirak\Desktop")
SEARCH_SUBJECT = "ダイエット" # Subject to look for

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
        # mail.debug = 4 # Enable verbose debug output
        mail.login(EMAIL, PASSWORD)
        stat, count = mail.select("inbox")
        if stat != "OK":
            print(f"Failed to select inbox: {stat}")
            return
            
        print(f"Inbox selected, count: {count}")

        # Search for all emails and filter in Python (since UNREAD command fails)
        status, messages = mail.uid('search', None, "ALL")
        
        if status != "OK":
            print("No emails found.")
            return

        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} email(s). checking flags and subjects...")

        for email_id in email_ids:
            # Fetch the email and flags
            res, msg_data = mail.uid('fetch', email_id, "(RFC822 FLAGS)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Check for \Seen flag (Read emails)
                    # response_part[0] contains headers like: b'1 (UID 1 FLAGS (\\Seen) RFC822 {123}'
                    try:
                        info = response_part[0].decode()
                        if "\\Seen" in info:
                            # print(f"Skipping read email: {email_id.decode()}")
                            continue
                    except:
                        pass

                    msg = email.message_from_bytes(response_part[1])
                    subject_header = msg["Subject"]
                    if subject_header:
                        subject_parts = decode_header(subject_header)
                        subject = ""
                        for part, encoding in subject_parts:
                            if isinstance(part, bytes):
                                try:
                                    subject += part.decode(encoding if encoding else "utf-8")
                                except:
                                    subject += part.decode("utf-8", errors="ignore")
                            else:
                                subject += part
                    else:
                        subject = "(No Subject)"
                    
                    subject_lower = subject.lower() if subject else ""
                    search_lower = SEARCH_SUBJECT.lower()
                    
                    if search_lower not in subject_lower:
                        # print(f"Skipping email (Subject mismatch): {subject}")
                        continue

                    print(f"Processing email: {subject}")

                    # Iterate over email parts to find attachments correctly
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            filename = part.get_filename()
                            
                            print(f"  - Part: {content_type}, Disposition: {content_disposition}, Filename: {filename}")

                            if not filename and content_type.startswith("image/"):
                                # If no filename but content is image, generate one
                                ext = content_type.split("/")[-1]
                                filename = f"unknown_image.{ext}"

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

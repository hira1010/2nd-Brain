# -*- coding: utf-8 -*-
import os
import smtplib
import sys
import logging
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# パス設定
TOOL_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = TOOL_DIR.parent
PROMPT_DIR = PROJECT_ROOT / "02_プロンプト"

# 共通設定のインポート
sys.path.append(str(PROJECT_ROOT.parent))
try:
    import manga_config as config
except ImportError:
    logger.error("manga_config.pyが見つかりません。")
    sys.exit(1)

class MangaEmailSender:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.sender = config.EMAIL_SENDER
        self.password = config.EMAIL_PASSWORD
        self.receiver = config.EMAIL_RECEIVER

    def collect_files(self):
        """送信対象のプロンプトファイルを収集する"""
        files = []
        
        # 1. '02_プロンプト' フォルダから収集
        if PROMPT_DIR.exists():
            files.extend(list(PROMPT_DIR.rglob("No102_*.md")))
        
        # 2. ルートの '作成済み' フォルダから収集
        archive_prompt_dir = PROJECT_ROOT / "作成済み"
        if archive_prompt_dir.exists():
            files.extend(list(archive_prompt_dir.rglob("No102_*.md")))
            
        if not files:
            logger.warning("送信対象のファイルが見つかりませんでした。")
            return []
            
        # 重複排除とソート
        unique_files = sorted(list(set(files)), key=lambda x: x.name)
        return unique_files

    def create_message(self, files):
        """メールメッセージを作成する"""
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.receiver
        msg["Subject"] = config.EMAIL_SUBJECT
        msg.attach(MIMEText(config.EMAIL_BODY, "plain"))

        for filepath in files:
            self._attach_file(msg, filepath)
        
        return msg

    def _attach_file(self, msg, filepath):
        """ファイルを添付する"""
        filename = filepath.name
        with open(filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
        msg.attach(part)

    def run(self):
        """配信処理を実行する"""
        files = self.collect_files()
        if not files:
            logger.warning("送信対象のファイルが見つかりませんでした。")
            return

        logger.info(f"{len(files)} 件のファイルを収集しました。")
        for f in files:
            logger.info(f" - {f.name}")

        if self.dry_run:
            logger.info("ドライラン完了。メール送信はスキップされました。")
            return

        msg = self.create_message(files)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            logger.info("メール送信が成功しました！")
        except Exception as e:
            logger.error(f"メール送信中にエラーが発生しました: {e}")

if __name__ == "__main__":
    # 安全のため、デフォルトではドライラン（リスト表示のみ）を実行
    sender = MangaEmailSender(dry_run=True)
    sender.run()


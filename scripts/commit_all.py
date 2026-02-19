#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Unified Commit Tool (Sync & Refactor & Commit)

1. Google Sheets からのデータ同期 (Asset & Weight)
2. スマート・リファクタリング (Prompt optimization)
3. Git Commit & Push
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from lib import utils, config

logger = utils.initialize_script("commit_all")

def run_script(script_path: Path):
    """外部スクリプトを Python プロセスとして実行する。"""
    logger.info(f"--- Running: {script_path.name} ---")
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return False
    
    try:
        # UTF-8 モードで実行
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(script_path)],
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode != 0:
            logger.warning(f"Script {script_path.name} exited with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error: {result.stderr.strip()}")
            return False
        
        if result.stdout:
            print(result.stdout.strip())
        return True
    except Exception as e:
        logger.error(f"Exception running script {script_path.name}: {e}")
        return False

def main():
    logger.info("=== Antigravity Unified Shortcut [5] Started ===")

    # Step 1: Sync Data
    sync_assets = ROOT_DIR / "18_システム" / "sync_assets.py"
    sync_weight = ROOT_DIR / "18_システム" / "sync_weight.py"
    
    run_script(sync_assets)
    run_script(sync_weight)

    # Step 2: Smart Refactor
    smart_refactor = ROOT_DIR / "18_システム" / "smart_refactor.py"
    # 引数なしで実行（デフォルト設定）
    run_script(smart_refactor)

    # Stage changes
    logger.info("--- Staging changes ---")
    subprocess.run(["git", "add", "-A"], cwd=str(ROOT_DIR))

    # Check for changes
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True
    )
    
    if not status.stdout.strip():
        logger.info("🎉 No changes to commit (Everything is up-to-date).")
        return

    # Step 3: Commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Unified Shortcut 5 - {timestamp}"
    
    logger.info(f"--- Committing: {message} ---")
    subprocess.run(["git", "commit", "-m", message], cwd=str(ROOT_DIR))

    # Push
    logger.info("--- Pushing to remote ---")
    subprocess.run(["git", "push"], cwd=str(ROOT_DIR))

    logger.info("✅ All tasks completed successfully!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Unified Commit Tool (Sync & Refactor & Commit) - Robust Version

1. Google Sheets からのデータ同期 (Asset & Weight)
2. スマート・リファクタリング (Prompt optimization)
3. Git Commit & Push (確実に実行)
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

def run_script(script_args):
    """外部スクリプトを Python プロセスとして実行する。args はリスト形式。"""
    if isinstance(script_args, Path):
        script_args = [str(script_args)]
    
    script_path = Path(script_args[0])
    logger.info(f"--- Running: {script_path.name} ---")
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return False
    
    try:
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        # -X utf8 を付与して文字化けを防止
        result = subprocess.run(
            [sys.executable, "-X", "utf8"] + script_args,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if result.stdout:
            print(result.stdout.strip())
            
        if result.returncode != 0:
            logger.warning(f"Script {script_path.name} exited with code {result.returncode}")
            if result.stderr:
                logger.error(f"Error Output: {result.stderr.strip()}")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Exception running script {script_path.name}: {e}")
        return False

def main():
    logger.info("=== Antigravity Unified Shortcut [5] Started ===")

    # Step -1: Git Pull (もう一台のPCの変更を最初に取り込む)
    logger.info("--- [Step 0/3] Git Pull from GitHub ---")
    pull_result = subprocess.run(
        ["git", "pull", "origin", "main"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True
    )
    if pull_result.returncode == 0:
        logger.info(f"✅ Git pull succeeded: {pull_result.stdout.strip()}")
    else:
        logger.warning(f"⚠️ Git pull failed (continuing anyway): {pull_result.stderr.strip()}")

    # Step 0: Sync Antigravity (Pull from Repo to System)
    # PC間同期のため、最新のリポジトリデータをシステム側に反映する
    sync_antigravity = ROOT_DIR / "18_システム" / "sync_antigravity.py"
    run_script([str(sync_antigravity), "--mode", "pull"])

    # Step 1: Sync Data (失敗しても継続)
    sync_assets = ROOT_DIR / "18_システム" / "sync_assets.py"
    sync_weight = ROOT_DIR / "18_システム" / "sync_weight.py"
    
    run_script(sync_assets)
    run_script(sync_weight)

    # Step 2: Smart Refactor (失敗しても継続)
    smart_refactor = ROOT_DIR / "18_システム" / "smart_refactor.py"
    run_script(smart_refactor)

    # Step 2.5: Auto Format (Markdown Lint Fix)
    fix_lint = ROOT_DIR / "18_システム" / "fix_manga_lint.py"
    run_script(fix_lint)

    # Step 2.9: Sync Antigravity (Push from System to Repo)
    # 現在のコンテキストをリポジトリ用フォルダにコピー
    run_script([str(sync_antigravity), "--mode", "push"])

    # Step 3: Git Commit & Push
    logger.info("--- [Step 3/3] Git Management ---")
    
    # 全変更を自動でステージング
    subprocess.run(["git", "add", "-A"], cwd=str(ROOT_DIR))

    # 変更があるか確認
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True
    )
    
    output = status.stdout.strip()
    if not output:
        logger.info("🎉 No changes to commit (Everything is already up-to-date locally).")
        # 変更がなくても念のため Push を実行して GitHub と同期を確実にしにいく
        logger.info("Enforcing push to ensure GitHub is in sync...")
        subprocess.run(["git", "push", "origin", "main"], cwd=str(ROOT_DIR))
        return

    # コミット実行
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"統合ショートカット 5 - {timestamp}"
    
    logger.info(f"Committing changes: {message}")
    subprocess.run(["git", "commit", "-m", message], cwd=str(ROOT_DIR))

    # 強制的に Push を実行
    logger.info("Pushing to GitHub (origin main)...")
    push_result = subprocess.run(["git", "push", "origin", "main"], cwd=str(ROOT_DIR), capture_output=True, text=True)
    
    if push_result.returncode == 0:
        logger.info("✅ GitHub sync completed successfully!")
    else:
        logger.error(f"❌ Push failed: {push_result.stderr}")

    logger.info("✅ All tasks finished.")

if __name__ == "__main__":
    main()

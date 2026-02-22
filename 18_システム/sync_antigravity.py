#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity Context Synchronization Script
同期対象: brain, conversations, knowledge, global_skills
"""

import os
import shutil
import argparse
from pathlib import Path

# 同期対象のディレクトリ名
SYNC_DIRS = ["brain", "conversations", "knowledge", "global_skills"]

def sync_data(src_base: Path, dst_base: Path, dry_run=False):
    """ディレクトリ群を src から dst へ同期する。"""
    print(f"Syncing: {src_base} -> {dst_base}")
    if not src_base.exists():
        print(f"Source base directory not found: {src_base}")
        return

    for sync_dir in SYNC_DIRS:
        src = src_base / sync_dir
        dst = dst_base / sync_dir

        if not src.exists():
            continue

        print(f"  Processing directory: {sync_dir}")
        
        if dry_run:
            print(f"    [DRY-RUN] Would copy {src} to {dst}")
            continue

        # ターゲットディレクトリの準備
        if dst.exists():
            shutil.rmtree(dst)
        
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("browser_recordings", "*.mp4", "*.webm"))
        print(f"    Successfully synced {sync_dir}")

def main():
    parser = argparse.ArgumentParser(description="Sync Antigravity context data.")
    parser.add_argument("--mode", choices=["push", "pull"], required=True, help="push: System -> Repo, pull: Repo -> System")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actual copying.")
    args = parser.parse_args()

    # パスの設定
    user_profile = Path(os.environ["USERPROFILE"])
    system_base = user_profile / ".gemini" / "antigravity"
    repo_base = Path(__file__).resolve().parent.parent / ".antigravity"

    if args.mode == "push":
        # システムからリポジトリへ
        sync_data(system_base, repo_base, dry_run=args.dry_run)
    else:
        # リポジトリからシステムへ
        if not repo_base.exists() and not args.dry_run:
            print(f"Repository base directory not found: {repo_base}. Skipping pull.")
            return
        sync_data(repo_base, system_base, dry_run=args.dry_run)

    print("\n✅ Sync process completed.")

if __name__ == "__main__":
    main()

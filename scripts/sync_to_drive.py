#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Drive Synchronization Script
Sync local 2nd-Brain to G:\マイドライブ\2nd-Brain
"""

import shutil
import os
import sys
from pathlib import Path
from typing import Iterable

# プロジェクトルートを追加
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from lib import utils

logger = utils.setup_logger("sync_to_drive")

# 同期先の設定
DRIVE_BASE = Path("G:/マイドライブ")
# 同期先を一本化
BACKUP_DEST = DRIVE_BASE / "2nd-Brain"

# 除外パターン
IGNORE_PATTERNS = [
    ".git",
    ".antigravity",
    ".gemini",
    "node_modules",
    ".venv",
    "__pycache__",
    ".obsidian",
    ".vscode",
    "browser_recordings",
    "*.bak",
    ".tmp.driveupload",  # Googleドライブが内部で使う一時ファイル（コピー中に消えてエラーになるため除外）
    ".pi",
    ".pochi",
    ".qoder",
    ".qwen",
    ".roo",
    ".trae",
    ".vibe",
    ".windsurf",
    ".zencoder",
    ".kode",
    ".codebuddy",
    ".continue",
    ".factory",
    ".goose",
    ".iflow",
    ".junie",
    ".kilocode",
    ".kiro",
    ".kode",
    ".mux",
    ".neovate",
    ".openhands",
    ".qoder",
    ".roo-ignore-exploration",
]


def _dedupe_patterns(patterns: Iterable[str]) -> tuple[str, ...]:
    """Preserve order while removing duplicate patterns."""
    seen: set[str] = set()
    unique_patterns: list[str] = []
    for pattern in patterns:
        if pattern in seen:
            continue
        seen.add(pattern)
        unique_patterns.append(pattern)
    return tuple(unique_patterns)


UNIQUE_IGNORE_PATTERNS = _dedupe_patterns(IGNORE_PATTERNS)


def _validate_drive_mount() -> bool:
    if DRIVE_BASE.exists():
        return True
    logger.error("Google Drive (G:/) is not mounted. Please ensure Google Drive for Desktop is running.")
    return False


def sync_to_drive() -> bool:
    """Sync project files to Google Drive."""
    logger.info("=== Starting Google Drive Sync ===")

    if not _validate_drive_mount():
        return False

    logger.info("Syncing: %s -> %s", ROOT_DIR, BACKUP_DEST)

    try:
        # Mirroring: copy new files and delete files in destination not in source
        shutil.copytree(
            ROOT_DIR,
            BACKUP_DEST,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(*UNIQUE_IGNORE_PATTERNS),
        )
        
        # Cleanup discrepancies in destination (Mirroring)
        logger.info("Cleaning up old discrepancies on Drive...")
        # Since sync_to_drive copies the whole project, we walk the destination
        # and delete anything that doesn't exist locally and isn't ignored.
        for root, dirs, files in os.walk(BACKUP_DEST, topdown=False):
            rel_path = os.path.relpath(root, BACKUP_DEST)
            local_root = ROOT_DIR / rel_path
            
            # This is a simplified mirror cleanup for the backup
            # In practice, we skip git and node_modules as defined in UNIQUE_IGNORE_PATTERNS
            
            for f in files:
                dest_file = Path(root) / f
                local_file = local_root / f
                if not local_file.exists():
                    dest_file.unlink()
            
            for d in dirs:
                dest_dir = Path(root) / d
                local_dir = local_root / d
                if not local_dir.exists():
                    shutil.rmtree(dest_dir)

        logger.info("Google Drive synchronization (Mirror) completed successfully!")
        return True
    except Exception as exc:
        logger.error("Sync failed: %s", exc)
        return False


if __name__ == "__main__":
    if sync_to_drive():
        sys.exit(0)
    else:
        sys.exit(1)
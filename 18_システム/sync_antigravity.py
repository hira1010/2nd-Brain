#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity Context Synchronization Script
Sync targets: brain, conversations, knowledge, global_skills
"""

import argparse
import os
import shutil
from pathlib import Path
from typing import Iterable

SYNC_DIRS = ("brain", "conversations", "knowledge", "global_skills")
IGNORE_PATTERNS: tuple[str, ...] = ("browser_recordings", "*.mp4", "*.webm")


def _copy_directory(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(*IGNORE_PATTERNS),
    )


def _iter_existing_sync_dirs(base: Path, sync_dirs: Iterable[str]) -> list[str]:
    return [name for name in sync_dirs if (base / name).exists()]


def sync_data(
    src_base: Path,
    dst_base: Path,
    dry_run: bool = False,
    sync_dirs: Iterable[str] = SYNC_DIRS,
) -> None:
    """Sync selected directories from src to dst."""
    print(f"Syncing: {src_base} -> {dst_base}")
    if not src_base.exists():
        print(f"Source base directory not found: {src_base}")
        return

    targets = _iter_existing_sync_dirs(src_base, sync_dirs)
    for sync_dir in targets:
        src = src_base / sync_dir
        dst = dst_base / sync_dir

        print(f"  Processing directory: {sync_dir}")
        if dry_run:
            print(f"    [DRY-RUN] Would copy {src} to {dst}")
            continue

        _copy_directory(src, dst)
        print(f"    Successfully synced {sync_dir}")


def resolve_sync_bases(user_profile: Path, script_path: Path) -> tuple[Path, Path]:
    """Resolve system and repository antigravity base directories."""
    system_base = user_profile / ".gemini" / "antigravity"
    repo_base = script_path.resolve().parent.parent / ".antigravity"
    return system_base, repo_base


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Antigravity context data.")
    parser.add_argument(
        "--mode",
        choices=["push", "pull"],
        required=True,
        help="push: System -> Repo, pull: Repo -> System",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without actual copying.",
    )
    args = parser.parse_args()

    user_profile = Path(os.environ["USERPROFILE"])
    system_base, repo_base = resolve_sync_bases(user_profile, Path(__file__))

    if args.mode == "push":
        sync_data(system_base, repo_base, dry_run=args.dry_run)
    else:
        if not repo_base.exists() and not args.dry_run:
            print(f"Repository base directory not found: {repo_base}. Skipping pull.")
            return 0
        sync_data(repo_base, system_base, dry_run=args.dry_run)

    print("\nSync process completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

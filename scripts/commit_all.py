#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shortcut 5 runner: keep behavior while refactoring, then commit and push.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Sequence, Union

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from lib import utils

logger = utils.initialize_script("commit_all")
SYSTEM_DIR = ROOT_DIR / "_システム"
SCRIPTS_DIR = ROOT_DIR / "scripts"
REMOTE_NAME = "origin"
BRANCH_NAME = "main"
PULL_STEP_LABEL = "--- [Step 0/3] Git Pull from GitHub ---"
GIT_STEP_LABEL = "--- [Step 3/3] Git Management ---"
DRIVE_STEP_LABEL = "--- [Step 4/4] Google Drive Backup Sync ---"
ScriptArgs = Union[Path, Sequence[str]]


def _normalize_script_args(script_args: ScriptArgs) -> List[str]:
    if isinstance(script_args, Path):
        return [str(script_args)]
    return list(script_args)


def run_script(script_args: ScriptArgs) -> bool:
    """Run a Python script with UTF-8 output and return success state."""
    args = _normalize_script_args(script_args)
    script_path = Path(args[0])

    logger.info("--- Running: %s ---", script_path.name)
    if not script_path.exists():
        logger.error("Script not found: %s", script_path)
        return False

    try:
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        result = subprocess.run(
            [sys.executable, "-X", "utf8", *args],
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if result.stdout:
            print(result.stdout.strip())

        if result.returncode != 0:
            logger.warning(
                "Script %s exited with code %s",
                script_path.name,
                result.returncode,
            )
            if result.stderr:
                logger.error("Error Output: %s", result.stderr.strip())
            return False

        return True
    except Exception as exc:  # pragma: no cover - defensive guard
        logger.error("Exception running script %s: %s", script_path.name, exc)
        return False


def run_git_command(
    args: Sequence[str], capture_output: bool = False
) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(args),
        cwd=str(ROOT_DIR),
        capture_output=capture_output,
        text=True,
    )


def _log_completed_process(result: subprocess.CompletedProcess, success_prefix: str, failure_prefix: str) -> None:
    if result.returncode == 0:
        logger.info("%s: %s", success_prefix, (result.stdout or "").strip())
    else:
        logger.warning("%s: %s", failure_prefix, (result.stderr or "").strip())


def run_refactor_pipeline() -> None:
    """
    Shortcut [5]:
    Execute refactor scripts intended to preserve behavior.
    """
    smart_refactor = SYSTEM_DIR / "smart_refactor.py"
    fix_lint = SYSTEM_DIR / "fix_manga_lint.py"

    run_script([str(smart_refactor), "--all"])
    run_script(fix_lint)


def commit_and_push_if_needed() -> None:
    logger.info(GIT_STEP_LABEL)
    run_git_command(["git", "add", "-A"])

    status = run_git_command(["git", "status", "--porcelain"], capture_output=True)
    output = status.stdout.strip()

    if not output:
        logger.info("No changes to commit (Everything is already up-to-date locally).")
        logger.info("Enforcing push to ensure GitHub is in sync...")
        run_git_command(["git", "push", REMOTE_NAME, BRANCH_NAME])
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"機能そのまま全体リファクタリング (shortcut 5) - {timestamp}"

    logger.info("Committing changes: %s", message)
    run_git_command(["git", "commit", "-m", message])

    logger.info("Pushing to GitHub (%s %s)...", REMOTE_NAME, BRANCH_NAME)
    push_result = run_git_command(
        ["git", "push", REMOTE_NAME, BRANCH_NAME], capture_output=True
    )
    if push_result.returncode == 0:
        logger.info("GitHub sync completed successfully!")
    else:
        logger.error("Push failed: %s", push_result.stderr)


def main() -> int:
    logger.info("=== Shortcut [5]: 機能そのまま全体リファクタリング ===")

    logger.info(PULL_STEP_LABEL)
    pull_result = run_git_command(["git", "pull", REMOTE_NAME, BRANCH_NAME], capture_output=True)
    _log_completed_process(
        pull_result,
        success_prefix="Git pull succeeded",
        failure_prefix="Git pull failed (continuing anyway)",
    )

    run_refactor_pipeline()
    commit_and_push_if_needed()

    # Step [4/4] Google Drive Sync (Added)
    logger.info(DRIVE_STEP_LABEL)
    sync_script = SCRIPTS_DIR / "sync_to_drive.py"
    if run_script([str(sync_script)]):
        logger.info("Google Drive synchronization completed successfully!")
    else:
        logger.warning("Google Drive sync failed. Please check G:/ mount status.")

    logger.info("All tasks finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
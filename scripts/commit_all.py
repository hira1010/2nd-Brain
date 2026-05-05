#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shortcut 5 runner: 全体リファクタリング、検証、コミット、およびプッシュ。
リファクタリングにより可読性と保守性を向上させたバージョン。
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Sequence, Union, Optional

# プロジェクトルートをパスに追加
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from lib import utils
except ImportError:
    # 互換性のためのフォールバック
    import logging
    logging.basicConfig(level=logging.INFO)
    class UtilsFallback:
        @staticmethod
        def initialize_script(name): return logging.getLogger(name)
    utils = UtilsFallback()

class ShortcutRunner:
    """ショートカット5の全行程を管理するクラス。"""

    def __init__(self):
        self.logger = utils.initialize_script("commit_all")
        self.system_dir = ROOT_DIR / "_システム"
        self.scripts_dir = ROOT_DIR / "scripts"
        self.remote_name = "origin"
        self.branch_name = "main"
        self.success_count = 0
        self.total_steps = 7

    def log_step(self, step_num: Union[int, float], title: str):
        """ステップの開始をログ出力します。"""
        self.logger.info(f"\n--- [Step {step_num}/{self.total_steps}] {title} ---")

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, check: bool = False, shell: bool = False) -> subprocess.CompletedProcess:
        """コマンドを実行し、結果を返します。"""
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        
        # Windowsでの実行を考慮
        executable = sys.executable if cmd[0] == "python" else None
        if executable and not shell:
            cmd = [executable, "-X", "utf8"] + cmd[1:]

        try:
            result = subprocess.run(
                cmd,
                cwd=str(cwd) if cwd else str(ROOT_DIR),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=check,
                shell=shell
            )
            if result.stdout:
                print(result.stdout.strip())
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            if e.stdout: print(e.stdout)
            if e.stderr: self.logger.error(e.stderr)
            return subprocess.CompletedProcess(cmd, e.returncode, e.stdout, e.stderr)
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return subprocess.CompletedProcess(cmd, 1, "", str(e))

    def step_0_pull(self):
        self.log_step(0, "Git Pull from GitHub")
        res = self.run_command(["git", "pull", self.remote_name, self.branch_name])
        if res.returncode == 0:
            self.logger.info("Git pull 成功。")
        else:
            self.logger.warning("Git pull 失敗 (作業を継続します)。")

    def step_1_npm(self):
        self.log_step(1, "NPM Updates & Verification")
        remotion_dir = ROOT_DIR / "04_Remotion" / "my-video"
        if remotion_dir.exists():
            self.logger.info(f"Project found: {remotion_dir}")
            # Update
            self.run_command(["npm", "update"], cwd=remotion_dir, shell=True)
            # Verify (ユーザー指定の新規ステップ)
            self.logger.info("Running npm run verify...")
            verify_res = self.run_command(["npm", "run", "verify"], cwd=remotion_dir, shell=True)
            if verify_res.returncode == 0:
                self.logger.info("Verification passed!")
            else:
                self.logger.warning("Verification failed. Please check for errors.")
        else:
            self.logger.info("Remotion project not found, skipping.")

    def step_2_python(self):
        self.log_step(2, "Python Updates (Pyxel etc.)")
        self.run_command([sys.executable, "-m", "pip", "install", "-U", "pyxel"])

    def step_3_renpy(self):
        self.log_step(3, "Ren'Py Status Check")
        renpy_dir = ROOT_DIR / "12_Pyxel_Godot" / "RenPy"
        if renpy_dir.exists():
            self.logger.info("Ren'Py プロジェクトを検出しました。Launcherで更新を確認してください。")
        else:
            self.logger.info("Ren'Py ディレクトリが見つかりません。スキップします。")

    def step_4_refactor(self):
        self.log_step(4, "Refactoring Pipeline")
        smart_refactor = self.system_dir / "smart_refactor.py"
        fix_lint = self.system_dir / "fix_manga_lint.py"
        
        if smart_refactor.exists():
            self.run_command(["python", str(smart_refactor), "--all"])
        if fix_lint.exists():
            self.run_command(["python", str(fix_lint)])

    def step_4_5_check(self) -> bool:
        self.log_step(4.5, "Antigravity Self-Check")
        check_script = self.scripts_dir / "antigravity_check.py"
        res = self.run_command(["python", str(check_script)])
        return res.returncode == 0

    def step_5_git_commit(self):
        self.log_step(5, "Git Commit & Push")
        self.run_command(["git", "add", "-A"])
        
        status = self.run_command(["git", "status", "--porcelain"])
        if not status.stdout.strip():
            self.logger.info("変更はありません。同期のみ行います。")
            self.run_command(["git", "push", self.remote_name, self.branch_name])
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"機能そのまま全体リファクタリング (Shortcut 5) - {timestamp}"
        
        self.run_command(["git", "commit", "-m", message])
        self.logger.info(f"Pushing to {self.remote_name}/{self.branch_name}...")
        res = self.run_command(["git", "push", self.remote_name, self.branch_name])
        
        if res.returncode == 0:
            self.logger.info("GitHub同期完了！")
        else:
            self.logger.error("Pushに失敗しました。")

    def step_6_drive_sync(self):
        self.log_step(6, "Google Drive Backup Sync")
        sync_script = self.scripts_dir / "sync_to_drive.py"
        if sync_script.exists():
            self.run_command(["python", str(sync_script)])
        else:
            self.logger.warning("Sync script not found.")

    def run(self):
        """全ステップを順次実行します。"""
        self.logger.info("=== Shortcut [5]: クラスベース・リファクタリング & 同期システム ===")
        
        self.step_0_pull()
        self.step_1_npm()
        self.step_2_python()
        self.step_3_renpy()
        self.step_4_refactor()
        
        if not self.step_4_5_check():
            self.logger.error("Quality checks failed. Commit aborted.")
            return 1
            
        self.step_5_git_commit()
        self.step_6_drive_sync()
        
        self.logger.info("\n=== Shortcut [5] 全てのタスクが正常に完了しました！ ===")
        return 0

if __name__ == "__main__":
    runner = ShortcutRunner()
    sys.exit(runner.run())
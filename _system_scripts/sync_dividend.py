#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 配当金データ同期スクリプト (Refactored)
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from lib import config, utils, sheets

# 初期化
logger = utils.initialize_script("sync_dividend")

def sync_dividend_data():
    try:
        logger.info("Starting sync process...")
        
        # 1. Google Sheets API連携 (libを使用して認証)
        client = sheets.GSheetClient()
        all_values = client.get_sheet_values(config.ASSETS_SHEET_ID)

        if not all_values:
            logger.error("Failed to retrieve data from sheet.")
            return

        target_year = '2026'
        
        # 3. データの抽出
        header_row_index = -1
        col_index_2026 = -1
        
        # ヘッダー行と対象カラム ('26' または '2026') を探す
        for i, row in enumerate(all_values):
            if '26' in row or '2026' in row:
                try:
                    col_index_2026 = row.index('26')
                    header_row_index = i
                    break
                except ValueError:
                    continue
        
        if col_index_2026 == -1:
             logger.error("Error: Column header '26' not found.")
             return

        updated_values = {} # {month: value}
        for month in range(1, 13):
            row_idx = header_row_index + month
            if row_idx < len(all_values):
                val = all_values[row_idx][col_index_2026]
                if val and val.strip():
                    updated_values[month] = val.strip().replace(',', '')
        
        logger.info("Retrieved values for %s: %s", target_year, updated_values)

        # 4. Markdownファイルの更新
        content = utils.FileIO.read_text(config.DIVIDEND_RECORD_FILE)
        if content is None: return

        lines = content.splitlines()
        new_lines = []
        
        for line in lines:
            if '|' in line and '月' in line:
                month_match = re.search(r'(\d+)月', line)
                if month_match:
                    month = int(month_match.group(1))
                    if month in updated_values:
                        parts = [p.strip() for p in line.split('|')]
                        new_val = "{:,}".format(int(updated_values[month]))
                        
                        last_val_chunk = parts[-2]
                        is_bold = '**' in last_val_chunk
                        formatted_val = f"**{new_val}**" if is_bold else new_val
                        
                        parts[-2] = f" {formatted_val} "
                        new_line = "|".join(parts)
                        new_lines.append(new_line)
                        continue

            new_lines.append(line)

        # ファイル書き込み
        if utils.FileIO.write_text(config.DIVIDEND_RECORD_FILE, "\n".join(new_lines) + "\n"):
            logger.info("Markdown file updated successfully: %s", config.DIVIDEND_RECORD_FILE)

    except Exception as e:
        logger.exception("An error occurred during sync: %s", e)

if __name__ == '__main__':
    sync_dividend_data()

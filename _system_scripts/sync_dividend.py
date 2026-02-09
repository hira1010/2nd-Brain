import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import datetime
import os

# --- 設定 ---
JSON_KEYFILE = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')  # 親ディレクトリのAPI認証キー
SPREADSHEET_KEY = '1lnN_z84DLknNWbQX0YWzHiyn5Ea_Hue9TbxQeHSe3HA' # スプレッドシートID
TARGET_MD_FILE = os.path.join(os.path.dirname(__file__), '..', r'07_株\配当金・資産推移.md') # 親ディレクトリ配下のMarkdown
TARGET_YEAR = '2026'

def sync_dividend_data():
    try:
        print("Starting sync process...")
        
        # 1. Google Sheets API認証
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scope)
        client = gspread.authorize(creds)
        
        # 2. スプレッドシートを開く
        sheet = client.open_by_key(SPREADSHEET_KEY).sheet1
        all_values = sheet.get_all_values()
        
        # 3. 2026年のデータを探す（行単位で検索）
        # 想定データ構造: [..., '2026', '24313', ...]
        target_row = None
        for row in all_values:
            if TARGET_YEAR in row:
                target_row = row
                break
        
        if not target_row:
            print(f"Error: Row for year {TARGET_YEAR} not found in spreadsheet.")
            return

        # データの抽出（カラム位置は変動する可能性があるため、簡単なロジックで推定）
        # '2026' の次のカラムが1月の値、その次が2月の値...と仮定するか、
        # 見出し行 ('17', '18'...) を探してカラムインデックスを特定するのが確実。
        
        # ヘッダー行を探す ('26' または '2026' が含まれる行)
        header_row_index = -1
        col_index_2026 = -1
        
        for i, row in enumerate(all_values):
            if '26' in row or '2026' in row:
                try:
                    # '26' カラムを探す
                    col_index_2026 = row.index('26')
                    header_row_index = i
                    break
                except ValueError:
                    continue
        
        if col_index_2026 == -1:
             print("Error: Column header '26' not found.")
             return

        # 月ごとのデータを取得 (ヘッダー行の次から12行分)
        # 1月=header_row_index+1, 2月=header_row_index+2...
        
        updated_values = {} # {month: value}
        
        for month in range(1, 13):
            row_idx = header_row_index + month
            if row_idx < len(all_values):
                val = all_values[row_idx][col_index_2026]
                if val and val.strip():
                    updated_values[month] = val.strip().replace(',', '')
        
        print(f"Retrieved values for {TARGET_YEAR}: {updated_values}")

        # 4. Markdownファイルの更新
        with open(TARGET_MD_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        is_in_table = False
        
        for line in lines:
            # Markdownテーブルの行を処理
            if '|' in line and '月' in line:
                parts = [p.strip() for p in line.split('|')]
                # parts[0]='', parts[1]='1月', ...
                
                # 月を特定
                month_match = re.search(r'(\d+)月', line)
                if month_match:
                     month = int(month_match.group(1))
                     
                     if month in updated_values:
                         new_val = "{:,}".format(int(updated_values[month]))
                         # 2026年のカラム（最後のカラムと仮定、またはカラム数から計算）
                         # | 年 | 17 | ... | 26 | -> 11番目の要素 (index 10)
                         # | 1月 | 0 | ... | val |
                         
                         # 単純に最後の数値カラムを置換するロジック
                         # **太字** 装飾がある場合は維持する
                         
                         # 行を再構築するのは複雑なので、正規表現で置換
                         # 行の最後のパイプ `|` の直前にある数値を置換
                         
                         # 現在の行: | 1月 | ... | 12,620 | 21,650 | **24,313** |
                         
                         # 最後の `|` の前の要素を取得
                         last_val_chunk = parts[-2] # 最後の要素は空文字列（行末の|の後）
                         
                         # ** ** で囲まれているか確認
                         is_bold = '**' in last_val_chunk
                         
                         formatted_val = f"**{new_val}**" if is_bold else new_val
                         
                         # 置換実行（単純な文字列置換だと誤爆するため、splitして再結合）
                         parts[-2] = f" {formatted_val} "
                         new_line = "|".join(parts) + "\n"
                         new_lines.append(new_line)
                         continue

            new_lines.append(line)

        # ファイル書き込み
        with open(TARGET_MD_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print("Markdown file updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    sync_dividend_data()

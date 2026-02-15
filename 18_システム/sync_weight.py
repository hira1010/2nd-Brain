import re
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
import requests

# Configuration
SPREADSHEET_ID = "1-5kRLKDWkEHd7BKwXqnft0_fISJ4KnDXLf1CAGEKHyc"
GID = "0"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID}"
TARGET_MD = Path(r"c:\Users\hirak\Desktop\2nd-Brain\01_繝繧､繧ｨ繝・ヨ\險倬鹸.md")
WEEKDAYS = ["譛・", "轣ｫ", "豌ｴ", "譛ｨ", "驥・", "蝨・", "譌･"]


def fetch_latest_weight() -> Optional[pd.DataFrame]:
    print("Fetching data from Google Sheets...")
    try:
        response = requests.get(CSV_URL, timeout=30)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        return pd.read_csv(csv_data, header=None)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def normalize_date(date_text: str) -> str:
    return re.sub(r"/0", "/", str(date_text).strip())


def format_header(date_text: str, weight: str) -> str:
    normalized = normalize_date(date_text)
    try:
        dt = datetime.strptime(f"2026/{normalized}", "%Y/%m/%d")
        return f"### {dt.month}/{dt.day} ({WEEKDAYS[dt.weekday()]}) 笏笏 **{weight}**kg"
    except ValueError:
        # Keep original date text if parsing fails.
        return f"### {normalized} 笏笏 **{weight}**kg"


def update_mermaid_chart(content: str, date_str: str, weight_val: str) -> str:
    x_axis_match = re.search(r"x-axis \[(.*?)\]", content)
    date_added = False
    if x_axis_match:
        current_dates = x_axis_match.group(1)
        if date_str not in current_dates:
            new_dates = f"{current_dates}, {date_str}"
            content = content.replace(f"x-axis [{current_dates}]", f"x-axis [{new_dates}]")
            date_added = True

    line_match = re.search(r"line \[(.*?)\]", content)
    if line_match and date_added:
        current_vals = line_match.group(1)
        new_vals = f"{current_vals}, {weight_val}"
        content = content.replace(f"line [{current_vals}]", f"line [{new_vals}]")

    return content


def get_latest_row(df: pd.DataFrame) -> Optional[Tuple[str, str]]:
    valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 1].notna()]
    if valid_data.empty:
        return None

    last_row = valid_data.iloc[-1]
    return str(last_row[0]), str(last_row[1])


def update_markdown_file(date_text: str, weight: str) -> None:
    print(f"Updating Markdown with Date: {date_text}, Weight: {weight}")

    if not TARGET_MD.exists():
        print(f"Target markdown not found: {TARGET_MD}")
        return

    content = TARGET_MD.read_text(encoding="utf-8")

    header_str = format_header(date_text, weight)
    if header_str in content:
        print("Entry already exists. Skipping timeline insert.")
    else:
        insert_marker = "## 統 繧ｿ繧､繝繝ｩ繧､繝ｳ (Daily Log)"
        new_entry = f"""
{header_str}
>
> **投 謨ｰ蛟､隧ｳ邏ｰ**
> (閾ｪ蜍募酔譛・
>
> **笨搾ｸ・譌･險倥・繝｡繝｢**
> 
>
> ---
"""
        if insert_marker in content:
            content = content.replace(insert_marker, f"{insert_marker}\n\n{new_entry}")
            print("Inserted new timeline entry.")

    content = update_mermaid_chart(content, normalize_date(date_text), weight)
    TARGET_MD.write_text(content, encoding="utf-8")
    print("Markdown update complete.")


def main() -> int:
    df = fetch_latest_weight()
    if df is None:
        return 1

    latest = get_latest_row(df)
    if latest is None:
        print("No valid rows found.")
        return 1

    last_date, last_weight = latest
    update_markdown_file(last_date, last_weight)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

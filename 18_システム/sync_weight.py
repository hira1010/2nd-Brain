import requests
import pandas as pd
from io import StringIO
import re
from datetime import datetime
import os

# Configuration
SPREADSHEET_ID = "1-5kRLKDWkEHd7BKwXqnft0_fISJ4KnDXLf1CAGEKHyc"
GID = "0" 
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID}"
TARGET_MD = r"c:\Users\hirak\Desktop\2nd-Brain\01_ダイエット\記録.md"

def fetch_latest_weight():
    print("Fetching data from Google Sheets...")
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, header=None)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_mermaid_chart(content, date_str, weight_val):
    # Update x-axis
    # x-axis [..., 2/5] -> [..., 2/5, 2/6]
    # Regex to find x-axis list
    x_axis_match = re.search(r'x-axis \[(.*?)\]', content)
    if x_axis_match:
        current_dates = x_axis_match.group(1)
        if date_str not in current_dates:
            new_dates = f"{current_dates}, {date_str}"
            content = content.replace(f"x-axis [{current_dates}]", f"x-axis [{new_dates}]")
    
    # Update line data
    # line [..., 94.3] -> [..., 94.3, 93.7]
    line_match = re.search(r'line \[(.*?)\]', content)
    if line_match:
        current_vals = line_match.group(1)
        # Check if we should append (simple check if date was added)
        # Assuming simple sequential add for now
        # If date_str was already in dates, we might need to replace the last val, but let's assume append for "sync new data"
        if f", {date_str}" in content: # we just added it
             new_vals = f"{current_vals}, {weight_val}"
             content = content.replace(f"line [{current_vals}]", f"line [{new_vals}]")
             
    return content

def update_markdown_file(date, weight):
    print(f"Updating Markdown with Date: {date}, Weight: {weight}")
    
    with open(TARGET_MD, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update/Insert Timeline Entry
    # Format: ### 2/6 (金) ── 93.7kg
    # We need to map date to "M/D (Day)" format
    try:
        dt = datetime.strptime(f"2026/{date}", "%Y/%m/%d")
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        day_str = weekdays[dt.weekday()]
        header_date_str = f"{dt.month}/{dt.day}"
        header_str = f"### {header_date_str} ({day_str}) ── **{weight}**kg"
    except:
        # Fallback if date parsing fails locally (though format seems to be M/D)
        pass # use 'date' as is if needed, but the spreadsheet had '2/6' presumably

    if header_str in content:
        print("Entry already exists. Skipping timeline insert.")
    else:
        # Insert after "## 📝 タイムライン (Daily Log)"
        insert_marker = "## 📝 タイムライン (Daily Log)"
        
        # New entry template
        new_entry = f"""
{header_str}
>
> **📊 数値詳細**
> (自動同期)
>
> **✍️ 日記・メモ**
> 
>
> ---
"""
        if insert_marker in content:
            content = content.replace(insert_marker, f"{insert_marker}\n\n{new_entry}")
            print("Inserted new timeline entry.")

    # 2. Update Mermaid Chart
    # Use simple date string matching spreadsheet '2/6'
    content = update_mermaid_chart(content, re.sub(r'/0', '/', date), weight) # remove leading zeros e.g. 02/06 -> 2/6 if needed

    with open(TARGET_MD, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Markdown update complete.")

if __name__ == "__main__":
    df = fetch_latest_weight()
    if df is not None:
         valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 1].notna()]
         if not valid_data.empty:
             last_row = valid_data.iloc[-1]
             last_date = last_row[0] # e.g. "2/6"
             last_weight = last_row[1]
             update_markdown_file(last_date, last_weight)

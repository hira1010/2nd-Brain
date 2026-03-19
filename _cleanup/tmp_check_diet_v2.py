import os
import sys
import pandas as pd

# Add project root to path
LIB_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LIB_PARENT not in sys.path:
    sys.path.append(LIB_PARENT)

from lib import config, sheets

SHEET_ID = config.DIET_SHEET_ID
GID = "0"

def main():
    try:
        df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
        if df is None:
            with open("tmp_debug.txt", "w", encoding="utf-8") as f:
                f.write("Failed to fetch sheet")
            return
        
        valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 3].notna()]
        if not valid_data.empty:
            row = valid_data.iloc[-1]
            date = str(row.iloc[0])
            weight = str(row.iloc[3])
            upper = str(row.iloc[1])
            lower = str(row.iloc[2])
            
            with open("tmp_debug.txt", "w", encoding="utf-8") as f:
                f.write(f"Date: {date}\n")
                f.write(f"Weight: {weight}\n")
                f.write(f"Upper BP: {upper}\n")
                f.write(f"Lower BP: {lower}\n")
        else:
            with open("tmp_debug.txt", "w", encoding="utf-8") as f:
                f.write("No valid data found")
    except Exception as e:
        with open("tmp_debug.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

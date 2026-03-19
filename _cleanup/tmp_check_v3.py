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
            with open("tmp_full_debug.txt", "w", encoding="utf-8") as f:
                f.write("Failed to fetch sheet")
            return
        
        with open("tmp_full_debug.txt", "w", encoding="utf-8") as f:
            f.write("Last 5 rows analysis:\n")
            for i in range(1, 6):
                row = df.iloc[-i]
                f.write(f"\n--- Row {-i} ---\n")
                for idx, val in enumerate(row):
                    f.write(f"Index {idx}: {val}\n")
                    
    except Exception as e:
        with open("tmp_full_debug.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

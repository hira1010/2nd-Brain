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
            print("Failed to fetch sheet")
            return
        
        # Save entire sheet to a CSV-like text file for full inspection
        df.to_csv("tmp_sheet_dump.csv", index=True, encoding="utf-8")
        print(f"Sheet dumped to tmp_sheet_dump.csv with {len(df)} rows.")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

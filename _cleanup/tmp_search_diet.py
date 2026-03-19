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
        
        print(f"Total rows: {len(df)}")
        print("Searching for '3/1' or health values (94, 165, 101)...")
        
        # Searching for rows that contain 94 or 165 or 101 or 3/1
        for i, row in df.iterrows():
            row_str = " ".join(map(str, row.values))
            if "3/1" in row_str or "94" in row_str or "165" in row_str or "101" in row_str or "93.5" in row_str:
                print(f"Row {i}: {row_str}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

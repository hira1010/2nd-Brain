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
        
        row = df.iloc[50]
        print(f"Row 50 Data:")
        for idx, val in enumerate(row):
            print(f"[{idx}] {val}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

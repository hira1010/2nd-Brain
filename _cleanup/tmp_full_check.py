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
        
        # Display all columns to find the correct index
        print("Column Indices and Samples (Last valid row):")
        valid_data = df[df.iloc[:, 0].notna()].tail(1)
        if not valid_data.empty:
            row = valid_data.iloc[0]
            for i, val in enumerate(row):
                print(f"Index {i}: {val}")
        else:
            print("No data found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

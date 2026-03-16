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
    df = sheets.fetch_csv_from_google_sheets(SHEET_ID, GID)
    if df is None:
        print("Failed to fetch sheet")
        return
    
    print("Latest 5 rows:")
    print(df.tail(5))
    
    valid_data = df[df.iloc[:, 0].notna() & df.iloc[:, 3].notna()]
    if not valid_data.empty:
        row = valid_data.iloc[-1]
        print("\nValidated Latest Row:")
        print(row)
        
        upper = str(row.iloc[1]).strip()
        lower = str(row.iloc[2]).strip()
        print(f"\nBlood Pressure: {upper}/{lower}")
    else:
        print("\nNo valid data found")

if __name__ == "__main__":
    main()

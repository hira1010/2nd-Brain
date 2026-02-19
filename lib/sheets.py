from io import StringIO
from typing import Optional

import pandas as pd
import requests

from . import utils


CSV_TIMEOUT_SECONDS = 30
logger = utils.setup_logger("lib.sheets")


def fetch_csv_from_google_sheets(sheet_id: str, gid: str = "0") -> Optional[pd.DataFrame]:
    """Download a Google Sheet tab as CSV and parse it into a DataFrame."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    logger.info("Fetching sheet as CSV: %s (gid=%s)", sheet_id, gid)

    try:
        response = requests.get(url, timeout=CSV_TIMEOUT_SECONDS)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), header=None)
    except Exception as exc:
        logger.error("Failed to fetch sheet CSV: %s", exc)
        return None

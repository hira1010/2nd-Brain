import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import StringIO
from pathlib import Path
from typing import List, Optional, Sequence

import pandas as pd
import requests

from . import utils, config


CSV_TIMEOUT_SECONDS = 30
DEFAULT_SCOPE: Sequence[str] = (
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
)
logger = utils.setup_logger("lib.sheets")


class GSheetClient:
    """Class to handle authenticated access to Google Sheets via gspread."""

    def __init__(self, credentials_file: str = str(config.CREDENTIALS_FILE), scope: Sequence[str] = DEFAULT_SCOPE):
        self.credentials_file = Path(credentials_file)
        self.scope = tuple(scope)
        self.client = None

    def _authorize(self):
        """Authorize and return the gspread client."""
        if self.client is None:
            try:
                creds = ServiceAccountCredentials.from_json_keyfile_name(str(self.credentials_file), list(self.scope))
                self.client = gspread.authorize(creds)
            except Exception as e:
                logger.error("Failed to authorize Google Sheets API: %s", e)
                raise
        return self.client

    def get_sheet_values(self, sheet_id: str, worksheet_index: int = 0) -> List[List[str]]:
        """Fetch all values from a specific worksheet as a list of lists."""
        try:
            client = self._authorize()
            sheet = client.open_by_key(sheet_id).get_worksheet(worksheet_index)
            return sheet.get_all_values()
        except Exception as e:
            logger.error("Failed to fetch values from sheet %s: %s", sheet_id, e)
            return []


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

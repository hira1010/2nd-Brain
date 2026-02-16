import pandas as pd
import requests
from io import StringIO
from typing import Optional
from . import utils

logger = utils.setup_logger("lib.sheets")

def fetch_csv_from_google_sheets(sheet_id: str, gid: str = "0") -> Optional[pd.DataFrame]:
    """
    GoogleスプレッドシートからCSV形式でデータを取得します。
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    logger.info(f"スプレッドシートからデータを取得中: {sheet_id}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), header=None)
    except Exception as e:
        logger.error(f"データの取得に失敗しました: {e}")
        return None

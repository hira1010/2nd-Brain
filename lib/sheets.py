import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import StringIO
from pathlib import Path
from typing import Any, List, Optional, Sequence, cast

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
    """gspread を介した Google Sheets への認証済みアクセスを処理するクラス。"""

    def __init__(self, credentials_file: str = str(config.CREDENTIALS_FILE), scope: Sequence[str] = DEFAULT_SCOPE):
        """
        Args:
            credentials_file: 認証用JSONファイルのパス
            scope: APIアクセススコープ
        """
        self.credentials_file = Path(credentials_file)
        self.scope = tuple(scope)
        self.client: Optional[gspread.Client] = None

    def _authorize(self) -> gspread.Client:
        """gspread クライアントを認証し、返します。
        
        Returns:
            認証済みの gspread.Client オブジェクト
            
        Raises:
            Exception: 認証に失敗した場合
        """
        if self.client is None:
            try:
                self.client = gspread.authorize(self._create_credentials())
            except Exception as exc:
                logger.error("Failed to authorize Google Sheets API: %s", exc)
                raise
        return self.client

    def _create_credentials(self) -> ServiceAccountCredentials:
        """サービスアカウントの認証情報インスタンスを作成します。"""
        return ServiceAccountCredentials.from_json_keyfile_name(
            str(self.credentials_file), list(self.scope)
        )

    def get_sheet_values(self, sheet_id: str, worksheet_index: int = 0) -> List[List[str]]:
        """指定されたシートのワークシートからすべての値を取得します。
        
        Args:
            sheet_id: Google Spreadsheet ID
            worksheet_index: ワークシートのインデックス (デフォルト: 0)
            
        Returns:
            データの二次元リスト。失敗した場合は空リスト。
        """
        try:
            client = self._authorize()
            sheet = client.open_by_key(sheet_id).get_worksheet(worksheet_index)
            if sheet is None:
                logger.warning("Worksheet at index %s not found in sheet %s", worksheet_index, sheet_id)
                return []
            return cast(List[List[str]], sheet.get_all_values())
        except Exception as exc:
            logger.error("Failed to fetch values from sheet %s: %s", sheet_id, exc)
            return []


def fetch_csv_from_google_sheets(sheet_id: str, gid: str = "0") -> Optional[pd.DataFrame]:
    """Google Sheet のタブを CSV としてダウンロードし、DataFrame としてパースします。
    
    Args:
        sheet_id: Google Spreadsheet ID
        gid: シートのGID (デフォルト: "0")
        
    Returns:
        pd.DataFrame オブジェクト。失敗した場合は None。
    """
    url = _build_csv_export_url(sheet_id, gid)
    logger.info("Fetching sheet as CSV: %s (gid=%s)", sheet_id, gid)

    try:
        response = requests.get(url, timeout=CSV_TIMEOUT_SECONDS)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text), header=None)
    except Exception as exc:
        logger.error("Failed to fetch sheet CSV for %s: %s", sheet_id, exc)
        return None


def _build_csv_export_url(sheet_id: str, gid: str) -> str:
    """CSVエクスポート用のURLを作成します。"""
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

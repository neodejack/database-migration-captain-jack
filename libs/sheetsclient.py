from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class SheetsClient:

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE = os.getenv("RANGE")

    def __init__(self) -> None:

        creds = service_account.Credentials.from_service_account_file(
            SheetsClient.SERVICE_ACCOUNT_FILE, scopes=SheetsClient.SCOPES)

        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        self._sheet_arr = sheet.values().get(
            spreadsheetId=SheetsClient.SPREADSHEET_ID, range=SheetsClient.RANGE).execute()["values"]

    @property
    def sheet_arr(self) -> list:
        return self._sheet_arr

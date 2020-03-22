import googleapiclient.discovery
import google.oauth2.service_account
import json
import os.path

from . import scrape_sites
from .data import SiteStatus, SITE_STATUS_FIELDS, site_status_to_fields

SECRET_DIR = os.path.join(os.path.dirname(__file__), "../secret")
SERVICE_ACCOUNT_FILE = os.path.join(SECRET_DIR, "service_account.json")
SPREADSHEET_FILE = os.path.join(SECRET_DIR, "spreadsheet.json")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def update_sheet(site_statuses):
    with open(SPREADSHEET_FILE, "rt") as f:
        spreadsheet_file = json.load(f)
        spreadsheet_id = spreadsheet_file["spreadsheet_id"]
        sheet_id = spreadsheet_file["sheet_id"]

    creds = google.oauth2.service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = googleapiclient.discovery.build("sheets", "v4", credentials=creds)
    spreadsheets = service.spreadsheets()

    sheet_values = spreadsheets.values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_id,
        majorDimension="ROWS",
    ).execute()

    rows = sheet_values["values"]
    col_idx_to_field = [field if field in SITE_STATUS_FIELDS else None
        for field in rows[0]]
    field_to_col_idx = {field: col_idx
        for col_idx, field in enumerate(col_idx_to_field) if field}

    short_id_col_idx = field_to_col_idx["short_id"]
    short_id_to_row_idx = {rows[row_idx][short_id_col_idx]: row_idx
        for row_idx in range(1, len(rows))}

    batch_update_ranges = []
    append_values = []
    for site_status in site_statuses:
        short_id = site_status.short_id
        fields = site_status_to_fields(site_status, "czech")
        row = [fields[field] if field else None for field in col_idx_to_field]
        if short_id in short_id_to_row_idx:
            row_idx = short_id_to_row_idx[short_id]
            batch_update_ranges.append({
                "range": a1_range(sheet_id, 0, row_idx, len(row)-1, row_idx),
                "majorDimension": "ROWS",
                "values": [row],
            })
        else:
            append_values.append(row)

    if batch_update_ranges:
        spreadsheets.values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "RAW",
                "data": batch_update_ranges,
            }
        ).execute()

    if append_values:
        spreadsheets.values().append(
            spreadsheetId=spreadsheet_id,
            valueInputOption="RAW",
            range=sheet_id,
            body={
                "majorDimension": "ROWS",
                "values": append_values,
            }
        ).execute()

def a1_range(sheet, col_first, row_first, col_last, row_last):
    return f"{sheet}!" \
        f"{a1_col(col_first)}{a1_row(row_first)}:" \
        f"{a1_col(col_last)}{a1_row(row_last)}"
def a1_row(col_idx):
    return f"{col_idx+1}"
def a1_col(row_idx):
    assert row_idx < 26
    return chr(ord("A") + row_idx)

if __name__ == "__main__":
    site_statuses = scrape_sites()
    update_sheet(site_statuses)


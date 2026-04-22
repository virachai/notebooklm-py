import gspread
import os
import datetime

def register_service_url(public_url, service_name="NotebookLM-API"):
    """Registers the public tunnel URL to a central Google Sheet for discovery."""
    CREDENTIALS_FILE = os.environ.get("GOOGLE_SHEETS_CREDS", "credentials.json")
    SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME", "NotebookLM Automation")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"⚠️  Discovery: Credentials file not found. Skipping registration.")
        return False

    try:
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        sh = gc.open(SHEET_NAME)
        
        # Look for a sheet named 'Discovery' or create one
        try:
            worksheet = sh.worksheet("Discovery")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sh.add_worksheet(title="Discovery", rows="10", cols="5")
            worksheet.update('A1:C1', [['Service Name', 'Current URL', 'Last Updated']])
        
        # Update Row 2 with our service info
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.update('A2:C2', [[service_name, public_url, now]])
        
        print(f"📡 Discovery: Registered URL to Google Sheet '{SHEET_NAME}' tab 'Discovery'")
        return True
    except Exception as e:
        print(f"❌ Discovery Error: {e}")
        return False

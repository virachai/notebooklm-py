import gspread
import asyncio
import time
import os
import logging
from notebooklm import NotebookLMClient

# Configuration
CREDENTIALS_FILE = os.environ.get("GOOGLE_SHEETS_CREDS", "credentials.json")
SHEET_NAME = os.environ.get("GOOGLE_SHEET_NAME", "NotebookLM Automation")

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sheets-worker")

async def worker_loop():
    if not os.path.exists(CREDENTIALS_FILE):
        logger.error(f"❌ Credentials file '{CREDENTIALS_FILE}' not found!")
        return

    try:
        # Authenticate with Google Sheets
        gc = gspread.service_account(filename=CREDENTIALS_FILE)
        sh = gc.open(SHEET_NAME)
        worksheet = sh.get_worksheet(0)
        logger.info(f"✅ Connected to Google Sheet: {SHEET_NAME}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Sheets: {e}")
        return

    async with await NotebookLMClient.from_storage() as client:
        logger.info("🕵️ Worker is active. Monitoring for new prompts...")
        
        while True:
            try:
                # Fetch all records
                records = worksheet.get_all_records()
                
                for i, row in enumerate(records):
                    # Check for empty status and non-empty prompt
                    # Expected columns: "Prompt", "Status", "Answer", "Notebook ID"
                    status = str(row.get("Status", "")).strip()
                    prompt = str(row.get("Prompt", "")).strip()
                    nb_id = str(row.get("Notebook ID", "")).strip()
                    
                    if not status and prompt:
                        row_idx = i + 2  # 1-indexed + header
                        logger.info(f"⚡ Processing row {row_idx}: {prompt[:50]}...")
                        
                        worksheet.update_cell(row_idx, 2, "Processing...") # Assume column 2 is Status
                        
                        try:
                            # Use provided Notebook ID or default to the first one
                            if not nb_id:
                                notebooks = await client.notebooks.list()
                                if not notebooks:
                                    raise Exception("No notebooks found in account.")
                                nb_id = notebooks[0].notebook_id
                            
                            # Execute Chat
                            result = await client.chat.ask(nb_id, prompt)
                            
                            # Write Answer to Column 3 and Status to Column 2
                            worksheet.update_cell(row_idx, 3, result.answer)
                            worksheet.update_cell(row_idx, 2, "Done ✅")
                            logger.info(f"✅ Row {row_idx} processed successfully.")
                            
                        except Exception as inner_e:
                            worksheet.update_cell(row_idx, 2, f"Error: {str(inner_e)}")
                            logger.error(f"❌ Row {row_idx} failed: {inner_e}")
                
                # Polling interval
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Worker loop encountered an error: {e}")
                await asyncio.sleep(30) # Wait longer on error

if __name__ == "__main__":
    asyncio.run(worker_loop())

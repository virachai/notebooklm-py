# =================================================================
# 🚀 NotebookLM ALL-IN-ONE COLAB BOOTSTRAP (Podcast Factory Master)
# =================================================================
# Copy and Paste this entire code into a single Google Colab Cell.

import os
import subprocess
import time
import re
import threading
import requests

# --- 1. USER CONFIGURATION (BASED ON YOUR DISCOVERY SERVICE) ---
API_KEY = "my-secure-api-key"
SERVICE_NAME = "podcast-factory-master"

# GOOGLE FORM DISCOVERY CONFIG
FORM_ID = "1FAIpQLScJEETFzkyhTxb41257OAFVUXqCLuksfFOxLLnOTJ_CgDVTRA"
ENTRY_URL = "entry.934553227"
ENTRY_SERVICE = "entry.207679271"
# ---------------------------------------------------------------

def setup_environment():
    print("📦 Step 1: Installing dependencies...")
    subprocess.run(["pip", "install", "-q", "fastapi", "uvicorn", "notebooklm-py", "requests"], check=True)

def write_api_server():
    print("📝 Step 2: Creating API Server file...")
    with open("api_server.py", "w") as f:
        f.write(f"""
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from notebooklm import NotebookLMClient
import os
import uvicorn

app = FastAPI(title="NotebookLM Remote - {SERVICE_NAME}")
API_KEY = "{API_KEY}"
api_key_header = APIKeyHeader(name="X-API-KEY")

async def get_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key

_client = None
async def get_client():
    global _client
    if _client is None:
        _client = await NotebookLMClient.from_storage()
    return _client

@app.get("/")
def health(): return {{"status": "alive", "service": "{SERVICE_NAME}"}}

@app.post("/ask")
async def ask(data: dict, k=Depends(get_api_key)):
    try:
        client = await get_client()
        res = await client.chat.ask(data['notebook_id'], data['query'])
        return {{"answer": res.answer}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")

def run_server():
    print("🖥️ Step 3: Starting API Server in background...")
    subprocess.Popen(["python", "api_server.py"])

def submit_to_google_form(public_url):
    """Submits the tunnel URL and Service Name to a Google Form."""
    url = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"
    payload = {
        ENTRY_URL: public_url,
        ENTRY_SERVICE: SERVICE_NAME
    }
    try:
        requests.post(url, data=payload)
        print(f"📡 Discovery: Registered '{SERVICE_NAME}' at {public_url} via Google Form.")
    except Exception as e:
        print(f"❌ Discovery Error: {e}")

def start_tunnel_and_discovery():
    print("☁️ Step 4: Setting up Cloudflare Tunnel...")
    cf_path = "./cloudflared"
    if not os.path.exists(cf_path):
        subprocess.run(["wget", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "-O", cf_path], check=True)
        subprocess.run(["chmod", "+x", cf_path], check=True)

    # Start Tunnel
    proc = subprocess.Popen([cf_path, "tunnel", "--url", "http://localhost:8000"], 
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    print("⏳ Waiting for Public URL...")
    for line in iter(proc.stdout.readline, ""):
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            print("\n" + "="*50)
            print(f"🔥 YOUR REMOTE API IS LIVE!")
            print(f"🔗 SERVICE: {SERVICE_NAME}")
            print(f"🔗 URL: {url}")
            print(f"🔑 API KEY: {API_KEY}")
            print("="*50)
            
            # Submit to Google Form
            submit_to_google_form(url)
            break

# Execute All Steps
if __name__ == "__main__":
    setup_environment()
    write_api_server()
    run_server()
    time.sleep(5) # Give server time to start
    start_tunnel_and_discovery()

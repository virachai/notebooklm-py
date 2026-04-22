import os
import subprocess
import time
import re
from discovery import register_service_url

def start_cloudflare():
    """Setup and start Cloudflare Tunnel on Colab/Linux and Register URL."""
    cf_path = "./cloudflared"
    
    if not os.path.exists(cf_path):
        print("📥 Downloading cloudflared binary...")
        subprocess.run(["wget", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", "-O", cf_path], check=True)
        subprocess.run(["chmod", "+x", cf_path], check=True)

    print("🚀 Launching Cloudflare Tunnel and registering with Discovery Service...")
    
    process = subprocess.Popen(
        [cf_path, "tunnel", "--url", "http://localhost:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    public_url = None
    start_time = time.time()
    while time.time() - start_time < 30:
        line = process.stdout.readline()
        if not line: break
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            print("\n" + "☁️" * 25)
            print(f"✅ Cloudflare Tunnel is LIVE!")
            print(f"🔗 URL: {public_url}")
            print("☁️" * 25 + "\n")
            
            # --- Discovery Registration ---
            register_service_url(public_url)
            # ------------------------------
            break
    
    return process, public_url

if __name__ == "__main__":
    try:
        proc, url = start_cloudflare()
        if url:
            while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping tunnel...")

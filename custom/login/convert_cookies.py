import json
import os
from pathlib import Path

def parse_cookie_string(cookie_str, domain):
    """แปลงสตริง Cookie (name=value; ...) เป็นรายการ dict ของ Playwright"""
    cookies = []
    if not cookie_str.strip():
        return cookies
    
    # แยก cookie แต่ละตัวด้วย ;
    items = cookie_str.strip().split(';')
    for item in items:
        if '=' not in item:
            continue
        
        name, value = item.strip().split('=', 1)
        
        cookies.append({
            "name": name,
            "value": value,
            "domain": domain,
            "path": "/",
            "expires": -1,
            "httpOnly": True, # ตั้งเป็นกลางๆ ไว้
            "secure": True,
            "sameSite": "None"
        })
    return cookies

def main():
    # นิยามไฟล์และโดเมนที่เกี่ยวข้อง
    cookie_files = {
        "cookie.google.com.txt": ".google.com",
        "cookie.notebooklm.google.com.txt": "notebooklm.google.com",
        "cookie.googleusercontent.com.txt": ".googleusercontent.com"
    }
    
    all_cookies = []
    current_dir = Path(__file__).parent
    
    for filename, domain in cookie_files.items():
        file_path = current_dir / filename
        
        if file_path.exists():
            print(f"Reading {filename}...")
            content = file_path.read_text(encoding='utf-8')
            parsed = parse_cookie_string(content, domain)
            all_cookies.extend(parsed)
            print(f"  - Found {len(parsed)} cookies")
        else:
            print(f"Skipping {filename} (File not found)")

    # สร้างโครงสร้าง Storage State
    storage_state = {
        "cookies": all_cookies,
        "origins": []
    }
    
    # บันทึกลง storage_state.json
    output_path = current_dir / "storage_state.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(storage_state, f, indent=2)
        
    print(f"\nSuccessfully created: {output_path}")
    print(f"Total cookies: {len(all_cookies)}")

if __name__ == "__main__":
    main()

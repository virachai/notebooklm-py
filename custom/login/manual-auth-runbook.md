# Manual Authentication Runbook (3-Domain Method)

This guide explains how to manually authenticate `notebooklm-py` by copying cookies from your browser headers into text files and merging them using a Python script. This bypasses the need for `playwright install chromium`.

## 1. Prepare Cookie Files

You will need to create 3 text files in the same directory as your conversion script.

### Step 1: Extract from Browser
1. Go to [notebooklm.google.com](https://notebooklm.google.com) and log in.
2. Open DevTools (F12) and go to the **Network** tab.
3. Refresh the page and find requests going to these 3 domains:
   - `google.com`
   - `notebooklm.google.com`
   - `googleusercontent.com` (Check this after playing audio or video)
4. For each domain, find the **Cookie** header in the **Request Headers** section and copy the entire string.

### Step 2: Save to Text Files
Paste the copied strings into these files respectively:
- `cookie.google.com.txt`
- `cookie.notebooklm.google.com.txt`
- `cookie.googleusercontent.com.txt`

## 2. Convert to storage_state.json

Run the provided Python script to merge these files into the required Playwright format.

### Run Conversion Script:
```bash
python convert_cookies.py
```
This will generate a `storage_state.json` file in the same directory.

## 3. Deployment (Installation)

To make the library recognize your new tokens, follow these steps:

### Step 1: Create Directory Structure
```bash
mkdir -p ~/.notebooklm/profiles/default/
```

### Step 2: Copy the File
```bash
cp ./storage_state.json ~/.notebooklm/profiles/default/storage_state.json
```

## 4. Verification

Verify that your manual tokens are working correctly:

```bash
notebooklm auth check --test
```

### Troubleshooting:
- **"SID cookie: ✗ fail"**: Check if your `cookie.google.com.txt` contains the `SID` token.
- **"Token fetch: ✗ fail"**: Your cookies might have expired. Refresh the NotebookLM page and copy the headers again.
- **Permission Denied**: Ensure you have write access to `~/.notebooklm`.

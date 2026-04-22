# Manual Authentication Runbook

This guide explains how to manually authenticate `notebooklm-py` by copying cookies from your browser, bypassing the need for `playwright install chromium`.

## 1. Extract Cookies from Browser

You need to extract cookies for `google.com` and `notebooklm.google.com`.

### Option A: Using Browser Extension (Recommended)
1. Install an extension like **"EditThisCookie"** or **"Cookie-Editor"**.
2. Go to [notebooklm.google.com](https://notebooklm.google.com) and log in.
3. Export cookies in **JSON** format.

### Option B: Manual extraction (DevTools)
1. Open Chrome DevTools (F12) on the NotebookLM page.
2. Go to the **Application** tab -> **Storage** -> **Cookies**.
3. You specifically need the `SID`, `HSID`, `SSID`, `APISID`, `SAPISID` cookies from `.google.com`.

## 2. Prepare the Storage State JSON

`notebooklm-py` expects the **Playwright Storage State** format. Create a file named `storage_state.json` with this structure:

```json
{
  "cookies": [
    {
      "name": "SID",
      "value": "YOUR_SID_VALUE",
      "domain": ".google.com",
      "path": "/",
      "expires": -1,
      "httpOnly": true,
      "secure": true,
      "sameSite": "None"
    },
    {
      "name": "HSID",
      "value": "YOUR_HSID_VALUE",
      "domain": ".google.com",
      "path": "/",
      "expires": -1,
      "httpOnly": true,
      "secure": true,
      "sameSite": "None"
    }
  ],
  "origins": []
}
```

> [!IMPORTANT]
> At minimum, the `SID` cookie is required. It is highly recommended to include all Google authentication cookies for stability.

## 3. Deployment

Choose one of the following methods to apply the tokens:

### Method 1: File-based (Persistent)
Save the JSON content to:
- **Windows**: `%USERPROFILE%\.notebooklm\storage_state.json`
- **Linux/macOS**: `~/.notebooklm/storage_state.json`

### Method 2: Environment Variable (CI/CD Friendly)
Set the `NOTEBOOKLM_AUTH_JSON` environment variable with the entire JSON string:

**PowerShell:**
```powershell
$env:NOTEBOOKLM_AUTH_JSON = '{"cookies": [...]}'
```

**Bash:**
```bash
export NOTEBOOKLM_AUTH_JSON='{"cookies": [...]}'
```

## 4. Verification

Verify that your manual tokens are working correctly by running:

```bash
notebooklm auth check --test
```

If successful, you will see "Authentication valid" and your account details.

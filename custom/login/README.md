# Manual Auth Maintenance Summary

This folder contains tools and documentation for manually authenticating `notebooklm-py` when standard browser-based login is unavailable.

## 📂 File Overview

| File | Purpose |
| :--- | :--- |
| **`manual-auth-runbook.md`** | Detailed guide on how to perform manual auth. |
| **`convert_cookies.py`** | Python script to merge `.txt` cookies into `storage_state.json`. |
| **`cookie.*.txt`** | Temporary storage for raw Cookie headers copied from DevTools. |
| **`storage_state.json`** | The generated Playwright-compatible session file. |
| **`get-cookie.js`** | (Legacy) CSP-safe script for browser console extraction. |

## 🔄 The Authentication Workflow

Follow these steps whenever your session expires:

1. **Extract**: Copy the `Cookie` header value from the browser's Network tab for the required domains.
2. **Paste**: Update the content of `cookie.google.com.txt` (and others if needed).
3. **Merge**: Run the conversion script:
   ```bash
   python custom/login/convert_cookies.py
   ```
4. **Deploy**: Move the generated JSON to the active profile:
   ```bash
   mkdir -p ~/.notebooklm/profiles/default/
   cp custom/login/storage_state.json ~/.notebooklm/profiles/default/storage_state.json
   ```
5. **Check**: Verify the status:
   ```bash
   notebooklm auth check --test
   ```

---
*Note: Keep your `.txt` and `.json` files secure as they contain active session tokens.*

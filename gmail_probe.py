import requests
import json

def check_gmail(email: str):
    """
    Pure HTTP Gmail existence check using Google's public lookup endpoint.
    No login, no API keys, no browser.
    """

    url = "https://accounts.google.com/_/signin/sl/lookup"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "identifier": email
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=8)
        data = json.loads(r.text.replace(")]}'", ""))  # Google prefixes JSON

        exists = data.get("accountExists", False)

        if exists:
            print(f"[Gmail] [+] {email} appears to exist.")
            return {"exists": True, "note": "Google reports accountExists=True"}

        print(f"[Gmail] [-] {email} does NOT appear to exist.")
        return {"exists": False, "note": "Google reports accountExists=False"}

    except Exception as e:
        print(f"[Gmail] [!] Error: {e}")
        return {"exists": None, "note": f"Error: {e}"}

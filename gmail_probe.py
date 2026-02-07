import requests
import json

def check_gmail(email: str):
    """
    Pure HTTP Gmail existence check using Google's public lookup endpoint.
    """

    url = "https://accounts.google.com/_/signin/sl/lookup"

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "X-Same-Domain": "1"
    }

    payload = {
        "identifier": email
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=8)

        # Google prefixes JSON with )]}'
        clean = r.text.replace(")]}'", "").strip()

        data = json.loads(clean)

        exists = data.get("accountExists", False)

        if exists:
            return {"exists": True, "note": "Google reports accountExists=True"}

        return {"exists": False, "note": "Google reports accountExists=False"}

    except Exception as e:
        return {"exists": None, "note": f"Error: {e}"}

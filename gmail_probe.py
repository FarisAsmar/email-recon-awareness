import requests

def check_gmail_zerobounce(email, api_key):
    url = "https://api.zerobounce.net/v2/validate"
    params = {
        "email": email,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        status = data.get("status", "unknown")
        sub_status = data.get("sub_status", "none")
        free_email = data.get("free_email", False)
        did_you_mean = data.get("did_you_mean")

        print(f"[ZeroBounce] 📬 Status: {status}, Sub-status: {sub_status}, Free: {free_email}")
        if did_you_mean:
            print(f"[ZeroBounce] 🤔 Did you mean: {did_you_mean}?")

        # Return structured data instead of a boolean
        return {
            "status": status,
            "sub_status": sub_status,
            "free_email": free_email,
            "did_you_mean": did_you_mean,
            "is_valid": status == "valid"
        }

    except Exception as e:
        print(f"[ZeroBounce] ❗ Error checking {email}: {e}")
        return {
            "status": "error",
            "sub_status": None,
            "free_email": None,
            "did_you_mean": None,
            "is_valid": False
        }

import requests

def check_gmail_ychecker(email):
    url = "https://ychecker.com/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"email": email}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        status = data.get("status", "unknown")
        deliverable = data.get("deliverable", False)
        reason = data.get("reason", "none")

        print(f"[YChecker] 📬 Status: {status}, Reason: {reason}, Deliverable: {deliverable}")
        return status == "valid" and deliverable

    except requests.exceptions.HTTPError as e:
        print(f"[YChecker] ❌ HTTP error: {e.response.status_code} — {e.response.text}")
        return False
    except Exception as e:
        print(f"[YChecker] ❗ Error checking {email}: {e}")
        return False

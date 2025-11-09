import requests

def check_gmail_ychecker(email):
    url = f"https://ychecker.com/?email={email}"
    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        # ✅ Check if response is JSON
        if "application/json" in response.headers.get("Content-Type", ""):
            data = response.json()
            status = data.get("status", "unknown")
            deliverable = data.get("deliverable", False)
            reason = data.get("reason", "none")

            print(f"[YChecker] 📬 Status: {status}, Reason: {reason}, Deliverable: {deliverable}")
            return status == "valid" and deliverable
        else:
            print(f"[YChecker] ❌ Unexpected content type: {response.headers.get('Content-Type')}")
            print(f"[YChecker] ❌ Raw response: {response.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        print(f"[YChecker] ❌ HTTP error: {e.response.status_code} — {e.response.text}")
        return False
    except Exception as e:
        print(f"[YChecker] ❗ Error checking {email}: {e}")
        return False

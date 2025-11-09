import requests

def check_gmail_ychecker(email):
    url = "https://ychecker.com/api/verify"
    headers = {"Content-Type": "application/json"}
    payload = {"email": email}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        status = data.get("status")
        reason = data.get("reason")
        deliverable = data.get("deliverable")

        if status == "valid" and deliverable:
            print(f"[YChecker] ✅ {email} is valid and deliverable ({reason})")
            return True
        else:
            print(f"[YChecker] ❌ {email} is not deliverable ({reason})")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[YChecker] ❗ Error checking {email}: {e}")
        return False

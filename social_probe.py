import requests

def check_instagram(email: str):
    """
    Pure HTTP Instagram check using the public password reset endpoint.
    No login, no API keys, no browser.
    """

    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-IG-App-ID": "936619743392459",  # public web app ID
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "email_or_username": email,
        "recaptcha_challenge_field": ""
    }

    try:
        r = requests.post(url, headers=headers, data=payload, timeout=8)
        data = r.json()

        if data.get("email_sent"):
            print(f"[Instagram] [+] Account linked to {email}.")
            return {"linked": True, "note": "Instagram says email_sent=True"}

        print(f"[Instagram] [-] No account linked to {email}.")
        return {"linked": False, "note": "Instagram says email_sent=False"}

    except Exception as e:
        print(f"[Instagram] [!] Error: {e}")
        return {"linked": False, "note": f"Error: {e}"}

import requests

def check_instagram(email):
    url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-CSRFToken": "fake-token",  # Instagram may require a real CSRF token
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "email_or_username": email
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if "email_sent" in response.text or "We sent an email" in response.text:
            print(f"[+] Instagram account linked to {email}")
            return ["Instagram"]
        else:
            print(f"[-] No Instagram account found for {email}")
            return []
    except Exception as e:
        print(f"[-] Error checking Instagram: {e}")
        return []

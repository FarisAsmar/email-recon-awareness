from playwright.sync_api import sync_playwright

def check_instagram(email):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Load Instagram recovery page to get real cookies + CSRF token
            page.goto("https://www.instagram.com/accounts/password/reset/")

            # Extract CSRF token from cookies
            cookies = context.cookies()
            csrf = None
            for c in cookies:
                if c["name"] == "csrftoken":
                    csrf = c["value"]

            if not csrf:
                print("[-] Could not extract CSRF token")
                return []

            # Send recovery request
            response = page.request.post(
                "https://www.instagram.com/accounts/account_recovery_send_ajax/",
                headers={
                    "X-CSRFToken": csrf,
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"email_or_username": email}
            )

            text = response.text()

            if "email_sent" in text or "We sent an email" in text:
                print(f"[+] Instagram account linked to {email}")
                return ["Instagram"]
            else:
                print(f"[-] No Instagram account found for {email}")
                return []

    except Exception as e:
        print(f"[-] Error checking Instagram: {e}")
        return []

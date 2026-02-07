from playwright.sync_api import sync_playwright


def check_instagram(email: str):
    """
    Uses Instagram's public password reset flow to infer whether
    an account appears to be linked to the given email.

    No login, no API, just public web behavior.
    Returns a dict:
        {
            "linked": True/False,
            "note": "..."
        }
    """
    name = "Instagram"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Load password reset page
            page.goto("https://www.instagram.com/accounts/password/reset/", wait_until="networkidle")

            # Fill the email/username field
            page.fill("input[name='cppEmailOrUsername']", email)

            # Click the reset button
            page.click("button[type='submit']")

            # Wait a bit for response
            page.wait_for_timeout(3000)

            content = page.content().lower()

            browser.close()

            # Heuristic markers – these may change over time
            if "we sent an email" in content or "email sent" in content:
                print(f"[{name}] [+] Appears to be an account linked to {email}.")
                return {"linked": True, "note": "Instagram indicates a reset email was sent."}

            if "no users found" in content or "can't find that account" in content:
                print(f"[{name}] [-] No obvious account linked to {email}.")
                return {"linked": False, "note": "Instagram indicates no matching account."}

            print(f"[{name}] [?] Could not confidently determine linkage.")
            return {"linked": False, "note": "No clear success/failure markers found."}

    except Exception as e:
        print(f"[{name}] [!] Error during Instagram check: {e}")
        return {"linked": False, "note": f"Error during check: {e}"}

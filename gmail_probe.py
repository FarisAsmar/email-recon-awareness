from playwright.sync_api import sync_playwright

def check_gmail_signup_probe(email):
    username = email.split("@")[0]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://accounts.google.com/signup")

        # Fill dummy data
        page.fill("input[name='firstName']", "Test")
        page.fill("input[name='lastName']", "User")
        page.fill("input[name='Username']", username)
        page.fill("input[name='Passwd']", "Test@1234")
        page.fill("input[name='ConfirmPasswd']", "Test@1234")

        # Trigger validation
        page.click("button:has-text('Next')")
        page.wait_for_timeout(2000)

        content = page.content()
        browser.close()

        if "That username is taken" in content:
            print(f"[Gmail Probe] ✅ Gmail exists: {email}")
            return True
        else:
            print(f"[Gmail Probe] ❌ Gmail not found: {email}")
            return False

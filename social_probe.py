from playwright.sync_api import sync_playwright


def check_instagram(email: str):
    """
    Uses Instagram's public password reset flow to infer whether
    an account appears to be linked to the given email.

    This version includes:
    - Non-headless mode (bypasses automation detection)
    - Realistic user-agent
    - Anti-automation Chromium flags
    - Extra waits for slow VMs
    - More resilient selectors
    """

    name = "Instagram"

    try:
        with sync_playwright() as p:

            # Launch Chromium with anti-detection flags
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-web-security",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                ]
            )

            # Realistic browser fingerprint
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
                locale="en-US",
            )

            page = context.new_page()

            # Load password reset page
            page.goto(
                "https://www.instagram.com/accounts/password/reset/",
                wait_until="networkidle"
            )

            # Give the page time to render dynamic elements
            page.wait_for_timeout(3000)

            # Try multiple selectors (Instagram changes these often)
            possible_fields = [
                "input[name='cppEmailOrUsername']",
                "input[name='email_or_username']",
                "input[aria-label='Email, Phone, or Username']",
                "input[type='text']",
            ]

            field_found = False
            for selector in possible_fields:
                try:
                    page.fill(selector, email)
                    field_found = True
                    break
                except:
                    continue

            if not field_found:
                browser.close()
                print(f"[{name}] [!] Could not find email input field.")
                return {"linked": False, "note": "Instagram field not found (blocked or changed)."}

            # Try multiple submit buttons
            possible_buttons = [
                "button[type='submit']",
                "button._acan._acap._acas._aj1-",
                "button",
            ]

            clicked = False
            for selector in possible_buttons:
                try:
                    page.click(selector)
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                browser.close()
                print(f"[{name}] [!] Could not click submit button.")
                return {"linked": False, "note": "Instagram submit button not found."}

            # Wait for response
            page.wait_for_timeout(4000)

            content = page.content().lower()
            browser.close()

            # Heuristic markers – these may change over time
            success_markers = [
                "we sent an email",
                "email sent",
                "we sent a link",
                "we sent a message",
            ]

            failure_markers = [
                "no users found",
                "can't find that account",
                "no account found",
                "user not found",
            ]

            for marker in success_markers:
                if marker in content:
                    print(f"[{name}] [+] Appears to be an account linked to {email}.")
                    return {
                        "linked": True,
                        "note": f"Instagram indicates a reset email was sent ({marker})."
                    }

            for marker in failure_markers:
                if marker in content:
                    print(f"[{name}] [-] No obvious account linked to {email}.")
                    return {
                        "linked": False,
                        "note": f"Instagram indicates no matching account ({marker})."
                    }

            print(f"[{name}] [?] Could not confidently determine linkage.")
            return {"linked": False, "note": "No clear success/failure markers found."}

    except Exception as e:
        print(f"[{name}] [!] Error during Instagram check: {e}")
        return {"linked": False, "note": f"Error during check: {e}"}

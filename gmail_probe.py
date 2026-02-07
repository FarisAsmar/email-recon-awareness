from playwright.sync_api import sync_playwright


def _check_with_playwright(config, email: str):
    """
    Generic helper to check if an email appears to exist on a provider
    using public web behavior (e.g., forgot password / recovery flows).

    This version includes:
    - Non-headless mode (bypasses automation detection)
    - Realistic user-agent
    - Anti-automation Chromium flags
    - Extra waits for slow VMs
    - Multiple fallback selectors
    """

    name = config["name"]
    url = config["url"]
    field_selector = config["field_selector"]
    submit_selector = config["submit_selector"]
    success_markers = config.get("success_markers", [])
    failure_markers = config.get("failure_markers", [])

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

            # Load provider page
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # Try multiple field selectors (providers change these often)
            possible_fields = [
                field_selector,
                "input[type='email']",
                "input[type='text']",
                "input#username",
                "input[name='login']",
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
                return {"exists": None, "note": "Email field not found (blocked or changed)."}

            # Try multiple submit buttons
            possible_buttons = [
                submit_selector,
                "button[type='submit']",
                "#identifierNext",
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
                return {"exists": None, "note": "Submit button not found."}

            # Wait for response
            page.wait_for_timeout(4000)

            content = page.content().lower()
            browser.close()

            # Check markers
            for marker in success_markers:
                if marker.lower() in content:
                    print(f"[{name}] [+] Email appears to exist based on page response.")
                    return {"exists": True, "note": f"Matched success marker: {marker}"}

            for marker in failure_markers:
                if marker.lower() in content:
                    print(f"[{name}] [-] Email appears NOT to exist based on page response.")
                    return {"exists": False, "note": f"Matched failure marker: {marker}"}

            print(f"[{name}] [?] Could not confidently determine existence.")
            return {"exists": None, "note": "No clear success/failure markers found."}

    except Exception as e:
        print(f"[{name}] [!] Error during check: {e}")
        return {"exists": None, "note": f"Error during check: {e}"}


def check_email_providers(email: str):
    """
    Runs public-web existence checks against multiple providers.
    All behavior is based on visible web flows, no APIs.
    """

    providers = []

    # Gmail
    providers.append(
        {
            "name": "Gmail",
            "url": "https://accounts.google.com/signin/v2/usernamerecovery",
            "field_selector": "input[type='email']",
            "submit_selector": "#identifierNext",
            "success_markers": [
                "check your email",
                "we sent an email",
                "we sent a recovery",
            ],
            "failure_markers": [
                "couldn't find your google account",
                "could not find your google account",
                "enter a valid email",
            ],
        }
    )

    # Yahoo
    providers.append(
        {
            "name": "Yahoo",
            "url": "https://login.yahoo.com/forgot",
            "field_selector": "input#username",
            "submit_selector": "button[type='submit']",
            "success_markers": [
                "we sent a code",
                "check your email",
            ],
            "failure_markers": [
                "sorry, we don't recognize this email",
                "couldn't find your account",
            ],
        }
    )

    # Outlook / Microsoft
    providers.append(
        {
            "name": "Outlook",
            "url": "https://account.live.com/acsr",
            "field_selector": "input[type='email']",
            "submit_selector": "button[type='submit']",
            "success_markers": [
                "we've sent a security code",
                "we sent a code",
            ],
            "failure_markers": [
                "that microsoft account doesn't exist",
                "couldn't find an account",
            ],
        }
    )

    results = {}
    for cfg in providers:
        name = cfg["name"]
        print(f"[+] Checking {name} for {email} via public web flow...")
        results[name] = _check_with_playwright(cfg, email)

    return results

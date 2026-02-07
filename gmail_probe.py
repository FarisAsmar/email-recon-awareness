from playwright.sync_api import sync_playwright


def _check_with_playwright(config, email: str):
    """
    Generic helper to check if an email appears to exist on a provider
    using public web behavior (e.g., forgot password / recovery flows).

    config = {
        "name": "Gmail",
        "url": "...",
        "field_selector": "...",
        "submit_selector": "...",
        "success_markers": ["..."],
        "failure_markers": ["..."],
    }
    """
    name = config["name"]
    url = config["url"]
    field_selector = config["field_selector"]
    submit_selector = config["submit_selector"]
    success_markers = config.get("success_markers", [])
    failure_markers = config.get("failure_markers", [])

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto(url, wait_until="networkidle")

            # Fill email field
            page.fill(field_selector, email)

            # Click submit / next
            page.click(submit_selector)

            # Give the page a moment to respond
            page.wait_for_timeout(3000)

            content = page.content().lower()

            browser.close()

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

    # NOTE: These flows and markers are heuristic and may need tuning over time.
    providers.append(
        {
            "name": "Gmail",
            "url": "https://accounts.google.com/signin/v2/usernamerecovery",
            "field_selector": "input[type='email']",
            "submit_selector": "button[type='submit'], #identifierNext",
            "success_markers": [
                "check your email",
                "we sent an email",
            ],
            "failure_markers": [
                "couldn't find your google account",
                "could not find your google account",
            ],
        }
    )

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

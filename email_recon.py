from gmail_probe import check_gmail
from social_probe import check_instagram
from breach_check import check_breach_stub

def run_recon(email: str):
    print(f"[+] Running recon for: {email}")

    gmail = check_gmail(email)
    insta = check_instagram(email)
    breach = check_breach_stub(email)

    # Critical hijack warning
    hijack = False
    if insta["linked"] and gmail["exists"] is False:
        hijack = True

    print("\n📊 Recon Report:")
    print("----------------")
    print(f"Email: {email}")
    print(f"Gmail exists: {gmail['exists']}")
    print(f"Instagram linked: {insta['linked']}")
    print(f"Breach info: {breach['note']}")
    print(f"Critical hijack risk: {hijack}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    run_recon(args.email)

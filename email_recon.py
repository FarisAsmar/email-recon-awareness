from gmail_probe import check_gmail
from social_probe import check_instagram
from breach_check import check_breach_status

def run_recon(email: str):
    print(f"[+] Running recon for: {email}")

    gmail = check_gmail(email)
    insta = check_instagram(email)
    breach = check_breach_status(email)

    # Simple hijack heuristic:
    hijack = False
    if insta.get("linked") and gmail.get("exists") is False:
        hijack = True

    print("\n📊 Recon Report:")
    print("----------------")
    print(f"Email: {email}")
    print(f"Gmail exists: {gmail.get('exists')} ({gmail.get('note')})")
    print(f"Instagram linked: {insta.get('linked')} ({insta.get('note')})")
    print(f"Breach info: {breach.get('note')}")
    print(f"Critical hijack risk: {hijack}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    run_recon(args.email)

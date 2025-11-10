from social_probe import check_instagram
from gmail_probe import check_gmail_zerobounce

def run_recon(email, api_key):
    print(f"[+] Running recon for: {email}")

    # ✅ Check if email is valid and deliverable via ZeroBounce
    email_valid = check_gmail_zerobounce(email, api_key)

    # ✅ Check linked social accounts
    linked_accounts = check_instagram(email)

    # 🔒 Breach check placeholder
    breach_status = "Unknown"

    # ✅ Gmail availability logic (same as email_valid for now)
    gmail_available = email_valid

    # 🔍 Risk logic
    if gmail_available and linked_accounts:
        risk_level = "High"
    elif not gmail_available and linked_accounts:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # 📊 Final report
    report = {
        "email": email,
        "email_valid": email_valid,
        "linked_accounts": linked_accounts,
        "breach_status": breach_status,
        "gmail_available": gmail_available,
        "risk_level": risk_level
    }

    print("\n📊 Risk Report:")
    for key, value in report.items():
        print(f"{key}: {value}")

    return report

# 🚀 CLI Entry Point
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3 and sys.argv[1] == "--email":
        run_recon(sys.argv[2], api_key=sys.argv[3])
    else:
        print("Usage: python email_recon.py --email example@gmail.com YOUR_API_KEY")

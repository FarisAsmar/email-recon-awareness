from social_probe import check_instagram
from gmail_probe import check_gmail_availability

def run_recon(email):
    print(f"[+] Running recon for: {email}")

    linked_accounts = []
    linked_accounts += check_instagram(email)

    breach_status = "Unknown"  # Skip EmailRep for now

    available = check_gmail_availability(email)

    # Risk logic
    if available and linked_accounts:
        risk_level = "High"
    elif not available and linked_accounts:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Final report
    report = {
        "email": email,
        "linked_accounts": linked_accounts,
        "breach_status": breach_status,
        "gmail_available": available,
        "risk_level": risk_level
    }

    print("\n📊 Risk Report:")
    for key, value in report.items():
        print(f"{key}: {value}")

    return report

# Run it
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--email":
        run_recon(sys.argv[2])
    else:
        print("Usage: python email_recon.py --email example@gmail.com")

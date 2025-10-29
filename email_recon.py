import argparse
from social_probe import check_instagram
from breach_check import check_breach_status

def run_checks(email):
    print(f"\n[+] Running recon for: {email}")
    instagram = check_instagram(email)
    breach = check_breach_status(email)

    report = {
        "email": email,
        "linked_accounts": instagram,
        "breach_status": breach,
        "risk_level": "High" if instagram else "Low"
    }

    print("\n📊 Risk Report:")
    for k, v in report.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Email Recon Awareness Tool")
    parser.add_argument("--email", required=True, help="Target email address")
    args = parser.parse_args()
    run_checks(args.email)

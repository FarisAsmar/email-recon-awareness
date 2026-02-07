import sys
import argparse

from gmail_probe import check_email_providers
from social_probe import check_instagram
from breach_check import check_breach_status


RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def run_recon(email: str):
    print(f"[+] Running recon for: {email}")

    # 1) Check email existence across providers (Gmail/Yahoo/Outlook) via public web flows
    provider_results = check_email_providers(email)

    # 2) Check if Instagram appears to have an account linked to this email
    insta_result = check_instagram(email)
    instagram_linked = insta_result.get("linked", False)

    # 3) Breach status (stubbed – no API mode)
    breach_status = check_breach_status(email)

    # 4) Derive existence flags
    any_provider_exists = any(
        r.get("exists") is True for r in provider_results.values()
    )
    any_provider_negative = any(
        r.get("exists") is False for r in provider_results.values()
    )

    # 5) Critical hijack condition:
    # Instagram says "linked", but no provider reports the email as existing
    critical_hijack_risk = instagram_linked and (not any_provider_exists) and any_provider_negative

    # 6) Risk level
    if critical_hijack_risk:
        risk_level = "Critical"
    elif instagram_linked and any_provider_exists:
        risk_level = "High"
    elif instagram_linked or any_provider_exists:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # 7) Print critical warning if condition is met
    if critical_hijack_risk:
        print()
        print(
            f"{RED}{BOLD}☠️☠️☠️  CRITICAL ACCOUNT TAKEOVER RISK  ☠️☠️☠️{RESET}"
        )
        print(
            f"{RED}Instagram appears to have an account linked to this email,"
            f" but none of the checked providers report this email as registered.{RESET}"
        )
        print(
            f"{RED}This means someone could REGISTER this email and immediately reset"
            f" the Instagram password — instant hijack potential.{RESET}"
        )
        print()

    # 8) Build final report
    report = {
        "email": email,
        "providers": provider_results,
        "instagram": insta_result,
        "breach_status": breach_status,
        "risk_level": risk_level,
        "critical_hijack_risk": critical_hijack_risk,
    }

    print("📊 Recon Report:")
    print("----------------")
    print(f"Email: {email}")
    print(f"Risk level: {risk_level}")
    print(f"Critical hijack risk: {critical_hijack_risk}")
    print("\n[Providers]")
    for name, res in provider_results.items():
        print(f"  {name}: exists={res.get('exists')}, note={res.get('note')}")

    print("\n[Instagram]")
    print(f"  linked={instagram_linked}, note={insta_result.get('note')}")

    print("\n[Breach status]")
    print(f"  {breach_status}")

    return report


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Email Recon Awareness Tool – public web behavior only (no API keys)."
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Target email address (e.g., example@gmail.com)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    run_recon(args.email)

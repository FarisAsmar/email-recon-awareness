def check_instagram(email):
    # Simulated logic for awareness
    if email.endswith("@gmail.com") or email.endswith("@yahoo.com"):
        print(f"[+] Instagram may be linked to {email}")
        return ["Instagram"]
    else:
        print(f"[-] No Instagram account found for {email}")
        return []

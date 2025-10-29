def check_gmail_availability(email):
    username = email.split("@")[0].lower()

    # Simulated logic: treat common usernames as taken
    taken_usernames = ["john", "jane", "admin", "test", "info", "support", "123", "user"]

    if any(x in username for x in taken_usernames):
        print(f"[+] Gmail says {email} is already taken (simulated)")
        return False
    else:
        print(f"[+] Gmail says {email} is available (simulated)")
        return True

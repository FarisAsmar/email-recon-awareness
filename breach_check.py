import requests

def check_breach_status(email, api_key=None):
    try:
        url = f"https://emailrep.io/{email}"
        headers = {"Key": api_key} if api_key else {}

        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            breaches = data.get("details", {}).get("breaches", [])

            if not breaches:
                print("[+] No known breaches found")
                return []

            print(f"[+] Breach status: {breaches}")
            return breaches

        else:
            print(f"[-] EmailRep API unreachable (status {response.status_code})")
            return None

    except Exception as e:
        print(f"[-] Error checking breach status: {e}")
        return None

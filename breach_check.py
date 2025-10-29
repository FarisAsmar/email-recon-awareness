import requests

def check_breach_status(email):
    try:
        response = requests.get(f"https://emailrep.io/{email}")
        if response.status_code == 200:
            data = response.json()
            breaches = data.get("details", {}).get("breaches", "Unknown")
            print(f"[+] Breach status: {breaches}")
            return breaches
        else:
            print("[-] EmailRep API unreachable")
            return "Unknown"
    except Exception as e:
        print(f"[-] Error checking breach status: {e}")
        return "Error"

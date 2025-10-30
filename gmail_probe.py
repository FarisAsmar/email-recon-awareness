import smtplib
import dns.resolver

def check_email_exists(email):
    domain = email.split('@')[-1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)

        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_host)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            print(f"[+] Email appears to be deliverable: {email}")
            return True
        else:
            print(f"[-] Email rejected by server: {email}")
            return False
    except Exception as e:
        print(f"[-] Error checking email: {e}")
        return False

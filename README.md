CREATED BY: FARIS ASMAR | Michigan 

# email-recon-awareness
# 🕵️‍♂️ Email Recon Awareness Tool

This project simulates how unclaimed or reused email addresses can be hijacked across platforms—raising awareness about credential hygiene and digital identity risks. This is one of my first projects, using old memories I had when I was younger to get into accounts for fun, and I realised I could automate this using python.

## 🔍 What It Does

- Checks if an email is available on Gmail, Yahoo, Outlook
- Probes social media platforms (Instagram, TikTok, Twitter) for linked accounts
- Flags breach status using public APIs (EmailRep, HaveIBeenPwned)
- Outputs a risk report showing potential hijack vectors

## ⚠️ Why It Matters

Most people don’t realize:
- Their old or unused emails may still be tied to active accounts
- If those emails are unclaimed, attackers can register them and reset passwords
- This tool demonstrates the risk—ethically and educationally

## 🛠️ How to Run

```bash
cd ~
rm -rf email-recon-awareness  # delete old folder
git clone https://github.com/FarisAsmar/email-recon-awareness.git
cd email-recon-awareness
AFTER DOWNLOAD: 
MAKE A VE: python3 -m venv venv
then run below
source venv/bin/activate
then, python email_recon.py --email targetemail@example.com
MAKE SURE, REQUIREMENTS ARE INSTALLED> (pip install requests)

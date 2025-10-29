from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def check_gmail_availability(email):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://accounts.google.com/signup")
        time.sleep(2)

        # Fill in the email field
        driver.find_element(By.ID, "username").send_keys(email.split("@")[0])
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.NAME, "Passwd").send_keys("FakePassword123!")
        driver.find_element(By.NAME, "ConfirmPasswd").send_keys("FakePassword123!")
        driver.find_element(By.ID, "accountDetailsNext").click()
        time.sleep(3)

        page_source = driver.page_source
        if "That username is taken" in page_source:
            print(f"[+] Gmail says {email} is already taken")
            return False
        else:
            print(f"[+] Gmail says {email} is available")
            return True
    except Exception as e:
        print(f"[-] Error checking Gmail: {e}")
        return None
    finally:
        driver.quit()


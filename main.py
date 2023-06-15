import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os, json, string, random, datetime, names
os.system("cls || clear")
print("Microsoft Account Creator")
try:
    with open("config.json") as f:
        config = json.load(f)
    cfg_signup_link = str(config["signup_link"])
    cfg_webdriver = str(config["webdriver"]).lower()
except Exception as e:
    print(f"Failed to load config: {e}")
class CreatorThread(threading.Thread):
    def __init__(self, position_x):
        super().__init__()
        self.position_x = position_x
    def run(self):
        print("Launching webdriver...")
        if "chrome" in cfg_webdriver:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_window_size(640, 1080)  # Set window size
            driver.set_window_position(self.position_x, 0)  # Set window position
        wait = WebDriverWait(driver, 30)
        driver.get(cfg_signup_link)
        first_name = names.get_first_name()
        surname = names.get_last_name()
        email = f"{first_name.lower()}{surname.lower()}{str(random.randint(1, 99999)).zfill(4)}@outlook.com"
        password = ''.join(random.sample(string.ascii_letters, 8))
        print(f"Started | {email}")
        wait.until(EC.visibility_of_element_located((By.ID, "MemberName"))).send_keys(email)
        wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "PasswordInput"))).send_keys(password)
        wait.until(EC.visibility_of_element_located((By.ID, "iOptinEmail"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "FirstName"))).send_keys(first_name)
        wait.until(EC.visibility_of_element_located((By.ID, "LastName"))).send_keys(surname)
        wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "BirthDateCountryAccrualInputPane")))
        Select(driver.find_element(By.ID, "Country")).select_by_value("US")
        birth_month = str(random.randint(1, 12))
        Select(driver.find_element(By.ID, "BirthMonth")).select_by_value(birth_month)
        birth_day = str(random.randint(1, 28)) 
        Select(driver.find_element(By.ID, "BirthDay")).select_by_value(birth_day)
        current_year = int(datetime.datetime.now().year)
        birth_year = str(random.randint(current_year - 90, current_year - 18))
        driver.find_element(By.ID, "BirthYear").send_keys(birth_year)
        wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()
        print(f"Captcha | {email}")
        WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))
        with open("accounts.txt", "a") as f:
            f.write(f"{email}:{password}\n")
        print(f"Created | {email}")
print("Generating 3 accounts...")
positions = [0, 640, 1280]
for i in range(3):
    CreatorThread(positions[i]).start()
import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import undetected_chromedriver as uc
import string, random, datetime, names, time

SIGNUP_URL = "https://signup.live.com/signup"

class CreatorThread(threading.Thread):
    def __init__(self, position_x, config):
        super().__init__()
        self.position_x = position_x
        self.config = config

    def run(self):
        print("Launching webdriver...")

        if "chrome" in self.config["webdriver"]:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.set_window_size(640, 1080)
            driver.set_window_position(self.position_x, 0)
        elif "uc" in self.config["webdriver"]:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")

            driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.set_window_size(640, 1080)
            driver.set_window_position(self.position_x, 0)
        elif "firefox" in self.config["webdriver"]:
            options = webdriver.FirefoxOptions()
            options.add_argument("--private")

            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            driver.set_window_size(640, 1080)
            driver.set_window_position(self.position_x, 0)
        else:
            print("Invalid webdriver. Please check your config.json file.")
            return

        wait = WebDriverWait(driver, 30)
        email = "Unknown"

        try:
            window_errors_check = True
            driver.get(SIGNUP_URL)
            first_name = names.get_first_name()
            surname = names.get_last_name()
            email = f"{first_name.lower()}{surname.lower()}{str(random.randint(1, 9999))}@outlook.com"
            password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12)).replace(":", "_")

            print(f"Started: {email}")
            wait.until(EC.visibility_of_element_located((By.ID, "MemberName"))).send_keys(email)
            wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "PasswordInput"))).send_keys(password)
            wait.until(EC.visibility_of_element_located((By.ID, "iOptinEmail"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "FirstName"))).send_keys(first_name)
            wait.until(EC.visibility_of_element_located((By.ID, "LastName"))).send_keys(surname)
            wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "BirthDateCountryAccrualInputPane")))
            Select(driver.find_element(By.ID, "Country")).select_by_value(self.config["country_code"])
            birth_month = str(random.randint(1, 12))
            Select(driver.find_element(By.ID, "BirthMonth")).select_by_value(birth_month)
            birth_day = str(random.randint(1, 28))
            Select(driver.find_element(By.ID, "BirthDay")).select_by_value(birth_day)
            current_year = int(datetime.datetime.now().year)
            birth_year = str(random.randint(current_year - 90, current_year - 18))
            driver.find_element(By.ID, "BirthYear").send_keys(birth_year)
            wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()
            wait.until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()

            print(f"Captcha: {email}")    
            self.wait_for_captcha(driver, email)

            # IS THIS REQUIRED?
            #WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

            with open("accounts.txt", "a") as f:
                f.write(f"{email}:{password}\n")
            print(f"Created: {email}")
            driver.quit()
            window_errors_check = False

            while window_errors_check == True:
                if len(driver.window_handles) == 0:
                    print(f"Window closed manually: {email}")
                    break
                time.sleep(1)
        except NoSuchWindowException:
            print(f"Window closed: {email}")
        except WebDriverException:
            print(f"Failed to check if window was closed: {email}")
        except AttributeError:
            print(f"Error: The window is no longer available: {email}")

    def wait_for_captcha(self, driver, email):
        clicked_e1 = False
        clicked_e2 = False
        while not clicked_e1 or not clicked_e2:
            if not clicked_e1:
                try:
                    driver.find_element(By.ID, "idSIButton9").click()
                    clicked_e1 = True
                except:
                    pass

            if not clicked_e2:
                try:
                    driver.find_element(By.ID, "id__0").click()
                    clicked_e2 = True
                except:
                    pass

            try:
                mc_elem = driver.find_element(By.ID, "microsoft_container")
                if mc_elem:
                    print(f"Skipping loop {email}")
                    break
            except:
                pass

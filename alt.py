import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import undetected_chromedriver as uc
import os, json, string, random, datetime, names, time, requests

os.system("cls || clear")

def get_ip_address():
    try:
        response = requests.get('https://ipinfo.io/json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.exceptions.RequestException as e:
        print("Failed to get IP address. Please check your internet connection.")
        return None
       
window_errors_check = True

def choose_webdriver():
    print("Please choose a webdriver:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Undetected Chromedriver (UC)")

    selection = input("Enter the number corresponding to your webdriver choice: ")
    while selection not in ["1", "2", "3"]:
        print("Invalid selection. Please try again.")
        selection = input("Enter the number corresponding to your webdriver choice: ")

    if selection == "1":
        return "chrome"
    elif selection == "2":
        return "firefox"
    elif selection == "3":
        return "uc"

def update_config(webdriver):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            config["webdriver"] = webdriver

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
            print("Config file updated successfully.")

    except Exception as e:
        print(f"Failed to update config file: {e}")

def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config

    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Invalid config file format.")
    
    return None

def logo():
    """logo"""
    print(r"""
      ___           ___           ___           ___     
     /__/\         /  /\         /  /\         /  /\    
    |  |::\       /  /:/_       /  /::\       /  /:/    
    |  |:|:\     /  /:/ /\     /  /:/\:\     /  /:/     
  __|__|:|\:\   /  /:/ /::\   /  /:/~/::\   /  /:/  ___ 
 /__/::::| \:\ /__/:/ /:/\:\ /__/:/ /:/\:\ /__/:/  /  /\
 \  \:\~~\__\/ \  \:\/:/~/:/ \  \:\/:/__\/ \  \:\ /  /:/
  \  \:\        \  \::/ /:/   \  \::/       \  \:\  /:/ 
   \  \:\        \__\/ /:/     \  \:\        \  \:\/:/  
    \  \:\         /__/:/       \  \:\        \  \::/   
     \__\/         \__\/         \__\/         \__\/       """)

logo()

config = load_config()
if config is not None:
    # Check if 'webdriver' field is empty
    if not config.get("webdriver"):
        chosen_webdriver = choose_webdriver()
        update_config(chosen_webdriver)
    else:
        print("Webdriver already specified in the config file.")
else:
    print("Unable to proceed without a valid config file.")

def choose_country():
    print("Please choose a country:")
    print("1. Poland")
    print("2. USA")
    print("3. Other")

    selection = input("Enter the number corresponding to your country choice: ")
    while selection not in ["1", "2", "3"]:
        print("Invalid selection. Please try again.")
        selection = input("Enter the number corresponding to your country choice: ")

    if selection == "1":
        return "PL"
    elif selection == "2":
        return "US"
    elif selection == "3":
        custom_code = input("Enter your custom country code (2 letters): ")
        while not custom_code.isalpha() or len(custom_code) != 2:
            print("Invalid country code. Please enter 2 letters.")
            custom_code = input("Enter your custom country code (2 letters): ")
        return custom_code.upper()

def create_accounts(country_code):
    try:
        with open("config.json") as f:
            config = json.load(f)
        cfg_signup_link = str(config["signup_link"])
        cfg_webdriver = str(config["webdriver"]).lower()

        if cfg_webdriver == "chrome" or cfg_webdriver == "uc":
            ChromeDriverManager().install()
        elif cfg_webdriver == "firefox":
            GeckoDriverManager().install()
        else:
            print("Invalid webdriver. Please check your config.json file.")
            return

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
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                driver.set_window_size(640, 1080)
                driver.set_window_position(self.position_x, 0)
            elif "uc" in cfg_webdriver:
                options = webdriver.ChromeOptions()
                driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                driver.set_window_size(640, 1080)
                driver.set_window_position(self.position_x, 0)
            elif "firefox" in cfg_webdriver:
                options = webdriver.FirefoxOptions()
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
                driver.set_window_size(640, 1080)
                driver.set_window_position(self.position_x, 0)
            else:
                print("Invalid webdriver. Please check your config.json file.")
                return

            wait = WebDriverWait(driver, 30)
            email = "Unknown"

            try:
                driver.get(cfg_signup_link)
                first_name = names.get_first_name()
                surname = names.get_last_name()
                email = f"{first_name.lower()}{surname.lower()}{str(random.randint(1, 9999))}@outlook.com"
                password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12)) 

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

                Select(driver.find_element(By.ID, "Country")).select_by_value(country_code)
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
                
                # messy fix but working one XD
                clicked_e1 = False
                clicked_e2 = False
                while not clicked_e1 or not clicked_e2:
                    if not clicked_e1:
                        try:
                            element1 = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.ID, "idSIButton9")))
                            element1.click()
                            clicked_e1 = True
                        except:
                            pass

                    if not clicked_e2:
                        try:
                            element2 = WebDriverWait(driver, 0.25).until(EC.presence_of_element_located((By.ID, "id__0")))
                            element2.click()
                            clicked_e2 = True
                        except:
                            pass

                WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

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
   

    def create_multiple_accounts(positions):
        threads = []
        for i in range(3):
            thread = CreatorThread(positions[i])
            thread.start()
            threads.append(thread)
            time.sleep(0.33)

        for thread in threads:
            thread.join()

    positions = [0, 640, 1280]
    create_multiple_accounts(positions)

    ip_address = None
    while ip_address is None:
        ip_address = get_ip_address()
        if ip_address is None:
            print("Retrying to get IP address...")
            time.sleep(1)

    print(f"Current IP address: {ip_address}")

    while True:
        time.sleep(1)
        new_ip_address = get_ip_address()
        if new_ip_address != ip_address:
            if new_ip_address != None:
                print("IP address changed. Creating new accounts...")
                create_multiple_accounts(positions)
                ip_address = new_ip_address

country_code = choose_country()
create_accounts(country_code)

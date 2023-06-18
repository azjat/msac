from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.remote.command import Command
import requests, json, os, sys, time

def logo():
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

def get_ip_address():
    try:
        response = requests.get('https://ip.me', timeout=5)
        return response.text
    except:
        print("Failed to get IP address. Please check your internet connection.")
        return None

def wait_until_ip_changes(old_ips):
    while True:
        time.sleep(1)
        new_ip = get_ip_address()

        if new_ip not in old_ips and new_ip != None:
            return new_ip

def update_config(config):
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
            print("Config file updated successfully.")

    except Exception as e:
        print(f"Failed to update config file: {e}")

def load_config():
    if not os.path.isfile("config.json"):
        config = {
            "webdriver": choose_webdriver(),
            "country_code": choose_country()
        }
        update_config(config)
        return config

    # If this point is reached, config.json exists
    with open("config.json", "r") as f:
        config = json.load(f)
        return config

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

def install_webdriver(config):
    if config["webdriver"] == "chrome" or config["webdriver"] == "uc":
        ChromeDriverManager().install()
    elif config["webdriver"] == "firefox":
        GeckoDriverManager().install()
    else:
        print("Invalid webdriver. Please check your config.json file.")
        sys.exit()

def get_status(driver):
    try:
        driver.current_url
        return True
    except:
        return False

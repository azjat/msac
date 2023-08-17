# MSAC

A Microsoft account creator made in Python using Selenium.

## Installation
Install required packages:

`pip install -r requirements.txt`

## Usage
Running the program:
`python3 main.py`

## VPN: 
You should always open the program without your VPN on, this way it detects your own IP and protects you from creating accounts under it.
Accounts are automatically gonna start to get created once your IP adress changes.

## Config
You gonna get an option to choose the webdriver and country code the first time you run the creator. 

If you want to you can set a different webdriver later: 
 - `chrome` - normal chrome webdriver
 - `firefox` - normal gecko webdriver
 - `uc` - undetected chromedriver (requires selenium < 4.10)

To do that - modify `config.json` and set `webdriver` to selected webdriver.

## Known issues
When you've selected `uc` as your webdriver there might be an error with launching it first time - 
just wait for few seconds and restart the python script.

## Disclaimer: Use of MSAC - Microsoft Account Creator
The MSAC - Microsoft Account Creator ("the Program") provided in this repository is intended for legitimate and lawful purposes. The purpose of the Program is to facilitate the automated creation of Microsoft accounts, for purposes such as managing personal accounts or legitimate testing scenarios.

However, the Program could potentially be misused for malicious purposes, such as creating fake accounts, engaging in spam, or violating the terms of service of Microsoft or any other relevant entity. The creators and maintainers of this repository ("the Developers") hereby explicitly and unequivocally disclaim any responsibility for the misuse of the Program by third parties.

By using the Program, you agree that:
- You will only use the Program for lawful and legitimate purposes.
- You will comply with all applicable laws, regulations, and terms of service related to the creation and use of Microsoft accounts.
- You will not use the Program for any malicious, unauthorized, or illegal activities.
- You will take full responsibility for any consequences arising from your use of the Program.

The Developers shall not be held liable for any damages, losses, legal actions, or any other consequences resulting from the use or misuse of the Program. The Developers do not endorse or encourage any form of misuse or illegal activity.

It is strongly advised that you seek legal advice before using the Program and ensure that your usage complies with all relevant laws and regulations. The Developers recommend responsible and ethical use of the Program at all times.

By using the Program, you acknowledge and agree to the terms outlined in this disclaimer.

# MSAC

A Microsoft account creator made in Python using Selenium.

## Installation
Install required packages:

`pip install -r requirements.txt`

## Usage
`python3 main.py`

## Config
If you want you can set different webdriver: 
 - `chrome` - normal chrome webdriver
 - `firefox` - normal gecko webdriver
 - `uc` - undetected chromedriver (requires selenium < 4.10)

To do that - modify `config.json` and set `webdriver` to selected webdriver.

## Known issues
When you've selected `uc` as your webdriver there might be an error with launching it first time - 
just wait for few seconds and restart the python script!

import json
import os
import time
from os.path import join
import calendar

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

# Usernames/passwords:
# { amex: { username: "asdf", password: "aasdf"}, bankwest: { ... } }
PASSWORDS_FILE = join(os.getcwd(), "site-passwords.json")


def click_obscured_link(element):
    for i in range(20):
        try:
            element.click()
            break
        except ElementClickInterceptedException:
            time.sleep(1)
    raise ElementClickInterceptedException("Unable to click on element")


def get_last_date(month, year):
    month = month[:3]
    year = int(year)
    month_map = dict((v, k) for k, v in enumerate(calendar.month_abbr))
    month_number = month_map[month]
    last_date = calendar.monthrange(year, month_number)[1]
    return last_date


def get_selenium_driver(file_type):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2) # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', '/tmp')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', file_type)
    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(20)
    return driver


def get_password(site):
    with open(PASSWORDS_FILE) as f:
        data = json.load(f)
        username = data[site]["username"]
        password = data[site]["password"]
    return [username, password]

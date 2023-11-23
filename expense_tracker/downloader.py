import json
import os
import time
import traceback
from os.path import join
import calendar
import datetime

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException

# Usernames/passwords:
# { amex: { username: "asdf", password: "aasdf"}, bankwest: { ... } }
PASSWORDS_FILE = join(os.getcwd(), "site-passwords.json")


class Downloader(object):
    data = None

    def process_data(self):
        raise NotImplementedError("process_data needs to be implemented by a subclass")

    def _download(self, driver):
        """
        This method should from a logged in account, download the required data locally
        """
        raise NotImplementedError("_download needs to be implemented by a subclass")

    def _login(self, driver):
        """
        This method should complete the login process to the site
        """
        raise NotImplementedError("_login needs to be implemented by a subclass")

    def process_data(self):
        """
        This method processes the downloaded data and places it in to self.data for later access
        Expected output format is a list of lists in the order:
        [date, description, cardholder, amount (without leading minus)]
        """
        raise NotImplementedError("_process_data needs to be implemented by a subclass")

    def _manual_download_required(self):
        return False

    def download(self):
        if not self._manual_download_required():
            while True:
                try:
                    driver = self._get_selenium_driver()
                    self._login(driver)
                    self._download(driver)
                except Exception as ex:
                    traceback.print_exc()
                    response = input("An error has occurred during download. Do you want to try again? (y/n)\n")
                    if response.lower().startswith("y"):
                        print("Retrying...")
                        continue
                    print("Aborting")
                    raise ex
                break

    def click_obscured_link(self, element):
        for i in range(20):
            try:
                element.click()
                break
            except ElementClickInterceptedException:
                time.sleep(1)
        raise ElementClickInterceptedException("Unable to click on element")

    def get_last_date(self, month, year):
        month = month[:3]
        year = int(year)
        month_map = dict((v, k) for k, v in enumerate(calendar.month_abbr))
        month_number = month_map[month]
        last_date = calendar.monthrange(year, month_number)[1]
        return last_date

    def _get_selenium_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)  # custom location
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", "/tmp")
        for file_type in ["application/vnd.ms-excel", "text/csv"]:
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", file_type)
        driver = webdriver.Firefox(profile)
        driver.implicitly_wait(20)
        return driver

    def get_password(self, site):
        with open(PASSWORDS_FILE) as f:
            data = json.load(f)
            username = data[site]["username"]
            password = data[site]["password"]
        return [username, password]

    def _get_dates(self):
        """
        Returns the first and last day of the previous month

        :return e.g. ['01/08/2022', '31/08/2022']
        """
        today = datetime.date.today()
        first = today.replace(day=1)
        end_date = first - datetime.timedelta(days=1)
        end_date_stamp = end_date.strftime("%d/%m/%Y")
        start_date = end_date.replace(day=1)
        start_date_stamp = start_date.strftime("%d/%m/%Y")
        return [start_date_stamp, end_date_stamp]

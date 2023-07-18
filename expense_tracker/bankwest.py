import csv
import time
import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from .downloader import Downloader
import glob
import os


class Bankwest(Downloader):
    def __init__(self):
        self.file_path = "/tmp/bankwest.csv"

    def _download(self):
        print("Starting bankwest download process")
        file_glob_pattern = "/tmp/Transactions_*"
        driver = self.get_selenium_driver()
        self._login(driver)

        try:
            os.remove(self.file_path)
            for file in glob.glob(file_glob_pattern):
                os.remove(file)
        except FileNotFoundError:
            pass

        print("Opening Transaction Search...")
        accounts_button = driver.find_element_by_xpath("//*[contains(text(), 'Accounts')]")
        hover = ActionChains(driver).move_to_element(accounts_button)
        hover.perform()
        driver.find_element_by_xpath("//*[contains(text(), 'Transaction search')]").click()

        print("Searching via custom date range...")
        select = Select(driver.find_element_by_id("_ctl0_ContentMain_ddlRangeOptions"))
        select.select_by_visible_text("Custom date range...")
        start_date, end_date = self._get_dates()

        print(f"Entering start date of {start_date}...")
        driver.find_element_by_id("_ctl0_ContentMain_dpFromDate_txtDate").send_keys(start_date)

        print(f"Entering end date of {end_date}...")
        driver.find_element_by_id("_ctl0_ContentMain_dpToDate_txtDate").send_keys(end_date)
        driver.execute_script("window.scrollBy(0,2000)")

        print("Searching...")
        driver.find_element_by_id("_ctl0_ContentButtonsRight_btnSearch").click()
        driver.execute_script("window.scrollBy(0,2000)")

        print("Exporting...")
        driver.find_element_by_id("_ctl0_ContentButtonsRight_btnExport").click()

        for i in range(30):
            if glob.glob(file_glob_pattern)[0]:
                driver.close()
                break
            time.sleep(1)

        downloaded_file = glob.glob(file_glob_pattern)[0]
        os.rename(downloaded_file, self.file_path)
        print("Successfully retrieved data from Bankwest")

    def _login(self, driver):
        username, password = self.get_password("bankwest")
        print("Loading Bankwest website...")
        driver.get("https://www.bankwest.com.au/personal/login")
        time.sleep(2)

        print("Entering username and password...")
        user_input = driver.find_element_by_id("customerPan")
        user_input.send_keys(username)
        password_input = driver.find_element_by_id("customerPassword")
        password_input.send_keys(password)
        print("Logging in and waiting...")
        password_input.send_keys(Keys.RETURN)

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

    def process_data(self):
        print("Processing data for Bankwest")
        self.data = []
        with open(self.file_path) as f:
            file = csv.reader(f)
            next(file)
            for row in file:
                if row[5] == "":  # nothing in debit column; assuming to be credits
                    continue
                row[5] = row[5][1:]  # strip leading minus that is on all debits
                self.data.append(row[2:6])

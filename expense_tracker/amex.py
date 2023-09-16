import time
import os

import xlrd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from .downloader import Downloader


class Amex(Downloader):
    def __init__(self):
        self.file_path = "/tmp/activity.xlsx"

    def process_data(self):
        print("Processing data for Amex")
        starting_row = 12
        wb = xlrd.open_workbook(self.file_path)
        sheet = wb.sheet_by_index(0)
        self.data = []

        current_row = starting_row
        while True:
            try:
                row = [x.value for x in sheet.row(current_row)]  # Convert from xlrd data types
                output_row = [row[0], row[1], row[2], row[4]]
                self.data.append(output_row)
                current_row += 1
            except IndexError:
                break

    def _download(self, driver):
        print("Starting Amex download process")

        print('Scrolling down to find "Recent Transactions"')
        driver.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)
        print("Waiting 20 seconds. Please close any pop ups that Amex has added this month. Make 'Recent Transactions' visible if it isn't")
        time.sleep(20)
        print("Done waiting")
        driver.find_element_by_link_text("Recent Transactions").click()

        print("Waiting 20 seconds. Please close any pop ups that Amex has added this month. Make sure 'Custom Date Range' on the left is visible")
        time.sleep(20)
        print("Finding and selecting previous month in calendar...")
        driver.find_element_by_link_text("Custom Date Range").click()
        start_date, end_date = self._get_dates()

        start_date_field = driver.find_element_by_id("startDate")
        start_date_field.click()
        start_date_field.send_keys(start_date)

        end_date_field = driver.find_element_by_id("endDate")
        end_date_field.click()
        end_date_field.send_keys(end_date)

        driver.find_element(By.XPATH, "//button[text()='Search']").click()

        # Download
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

        print("Attempting to download in Excel format...")
        time.sleep(3)
        for i in range(20):
            try:
                driver.find_element_by_class_name("dls-icon-download").click()
                break
            except ElementClickInterceptedException:
                time.sleep(1)

        driver.find_element(By.XPATH, "//span[text()='Download']").click()

        for i in range(30):
            if os.path.exists(self.file_path):
                driver.close()
                print("Successfully retrieved data from Amex")
                return self.file_path
            time.sleep(1)
        raise FileNotFoundError(f"Cannot find {self.file_path}; Download probably failed")

    def _login(self, driver):
        username, password = self.get_password("amex")
        print("Loading Amex website...")
        driver.get("https://global.americanexpress.com/dashboard?inav=au_menu_myacct_acctsum")
        time.sleep(2)

        print("Entering username and password...")
        login_input = driver.find_element_by_id("eliloUserID")
        login_input.send_keys(username)
        password_input = driver.find_element_by_id("eliloPassword")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print("Logging in and waiting...")
        time.sleep(10)

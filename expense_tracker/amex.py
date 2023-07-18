import time
import os

import xlrd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

from .downloader import Downloader


class Amex(Downloader):
    def __init__(self):
        self.file_path = "/tmp/Summary.xls"

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
                self.data.append(row[1:5])  # Only keep the relevant columns
                current_row += 1
            except IndexError:
                break

    def _download(self):
        print("Starting Amex download process")
        driver = self.get_selenium_driver()
        self._login(driver)

        print('Scrolling down to find "Recent Transactions"')
        driver.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)
        print("Waiting 20 seconds. Please close any pop ups that Amex has added this month. Maybe keep the cursor over 'Recent Transactions'")
        time.sleep(20)
        print("Done waiting")
        driver.find_element_by_link_text("Recent Transactions").click()

        print("Finding and selecting previous month in calendar...")
        driver.find_element_by_class_name("menu-container").click()
        driver.find_element_by_xpath('//*[@title="Select starting and ending dates"]').click()
        driver.find_element_by_xpath('//*[@title="Previous Month"]').click()

        print("Clicking the first day of the month...")
        items = driver.find_elements_by_xpath("//*[contains(text(), '01')]")
        for item in items:
            if item.text == "01" and item.size["height"] == 17.5:
                item.click()
                break

        print("Clicking the last day of the month...")
        month, year = driver.find_element_by_class_name("months").text.split(" ")
        last_date = self.get_last_date(month, year)
        items = driver.find_elements_by_xpath(f"//*[contains(text(), '{last_date}')]")

        # Get a list of buttons that are the right size for the calendar
        # There might be 2 items; one for the previous month and one for the current.
        # Therefore we always click the last one
        # If Amex resize page elements, this might break :/ uncomment the below to print out the matching elements
        # print("Debug info...")
        # for i in items:
        #     print(f"Dimensions: height: {i.size['height']} width: {i.size['width']}. {i.text}")

        calendar_buttons = [x for x in items if x.size["height"] == 17.5]
        calendar_buttons[-1].click()

        driver.find_element_by_class_name("action_button").click()

        # Download
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

        print("Attempting to download in Excel format...")
        time.sleep(3)
        for i in range(20):
            try:
                driver.find_element_by_xpath('//*[@title="Download"]').click()
                break
            except ElementClickInterceptedException:
                time.sleep(1)

        driver.find_element_by_id("downloadAllExcel").click()
        driver.find_element_by_class_name("get-button").click()

        for i in range(30):
            if os.path.exists(self.file_path):
                driver.close()
                return self.file_path
            time.sleep(1)
        raise FileNotFoundError(f"Cannot find {self.file_path}; Download probably failed")
        print("Successfully retrieved data from Amex")

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

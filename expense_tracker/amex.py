import time
import os

import xlrd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

from . import downloader


class Amex(object):

    def __init__(self):
        self.file_path = "/tmp/Summary.xls"

    def process_data(self):
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

    def download(self):
        driver = downloader.get_selenium_driver("application/vnd.ms-excel")
        self._login(driver)

        driver.find_element_by_css_selector("body").send_keys(Keys.PAGE_DOWN)
        driver.find_element_by_link_text("Recent Transactions").click()
        driver.find_element_by_class_name("menu-container").click()
        driver.find_element_by_xpath('//*[@title="Select starting and ending dates"]').click()
        driver.find_element_by_xpath('//*[@title="Previous Month"]').click()

        # Click first day of the month
        items = driver.find_elements_by_xpath("//*[contains(text(), '01')]")
        for item in items:
            if item.text == "01" and item.size["height"] == 14.5:
                item.click()
                break

        # Click last day of the month
        month, year = driver.find_element_by_class_name("months").text.split(" ")
        last_date = downloader.get_last_date(month, year)
        items = driver.find_elements_by_xpath(f"//*[contains(text(), '{last_date}')]")
        for item in items:
            if item.text == str(last_date) and item.size["height"] == 14.5:
                item.click()
                break

        driver.find_element_by_class_name("action_button").click()

        # Download
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

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

    def _login(self, driver):
        username, password = downloader.get_password("amex")
        driver.get("https://www.americanexpress.com/au/")
        time.sleep(2)

        login_input = driver.find_element_by_id("login-user")
        login_input.send_keys(username)
        password_input = driver.find_element_by_id("login-password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(10)

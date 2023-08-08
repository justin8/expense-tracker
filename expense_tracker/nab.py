import csv
import os
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from .downloader import Downloader


class Nab(Downloader):
    def __init__(self):
        file_path = Path("~/Downloads/Transactions.csv").expanduser().resolve()
        self.file_path = str(file_path)

    def _download(self, driver):
        print("Starting NAB download process")
        print("NAB's anti-bot protections are annoying. Download last month's transactions to ~/Downloads/Transactions.csv")
        input("Press enter to continue once the file is downloaded")

        print("Successfully retrieved data from NAB")

    def _login(self, driver):
        pass

    def process_data(self):
        print("Processing data for NAB")
        self.data = []
        with open(self.file_path) as f:
            file = csv.reader(f)
            next(file)
            for row in file:
                output_row = [row[0], f"{row[5]} - {row[8]}", "", row[1].strip("-")]
                self.data.append(output_row)

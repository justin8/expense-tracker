import csv
from pathlib import Path

from .downloader import Downloader


class Nab(Downloader):
    def __init__(self):
        file_path = Path("~/Downloads/Transactions.csv").expanduser().resolve()
        self.file_path = str(file_path)

    def process_data(self):
        print("Processing data for NAB")
        self.data = []
        with open(self.file_path) as f:
            file = csv.reader(f)
            next(file)
            for row in file:
                output_row = [row[0], f"{row[5]} - {row[8]}", "", row[1].strip("-")]
                self.data.append(output_row)

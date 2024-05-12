import csv
from pathlib import Path

from .downloader import Downloader


class Cba(Downloader):
    def __init__(self):
        file_path = Path("~/Downloads/CSVData.csv").expanduser().resolve()
        self.file_path = str(file_path)

    def process_data(self):
        print("Processing data for CBA")
        self.data = []
        with open(self.file_path) as f:
            file = csv.reader(f)
            for row in file:
                output_row = [row[0], row[2], "", row[1].strip("-")]
                self.data.append(output_row)

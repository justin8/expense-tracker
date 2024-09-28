import csv
from pathlib import Path

from .downloader import Downloader


class StGeorge(Downloader):
    def __init__(self):
        downloads_dir = Path("~/Downloads").expanduser().resolve()
        file_path = [Path(file) for file in downloads_dir.glob("trans*.csv")][0]
        self.file_path = str(file_path)

    def process_data(self):
        print("Processing data for St George")
        self.data = []
        with open(self.file_path) as f:
            file = csv.reader(f)
            next(file)
            for row in file:
                value = row[2] if row[2] else row[3]
                output_row = [row[0], row[1], "", value]
                self.data.append(output_row)

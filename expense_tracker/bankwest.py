import csv


from .downloader import Downloader


class Bankwest(Downloader):
    def __init__(self):
        self.file_path = "~/Downloads/bankwest.csv"

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

import xlrd

from .downloader import Downloader


class Amex(Downloader):
    def __init__(self):
        self.file_path = "~/Downloads/activity.xlsx"

    def process_data(self):
        print("Processing data for Amex")
        starting_row = 12
        wb = xlrd.open_workbook(self.file_path)
        sheet = wb.sheet_by_index(0)
        self.data = []

        current_row = starting_row
        while True:
            try:
                row = [
                    x.value for x in sheet.row(current_row)
                ]  # Convert from xlrd data types
                output_row = [row[0], row[2], row[3], row[5]]
                self.data.append(output_row)
                current_row += 1
            except IndexError:
                break

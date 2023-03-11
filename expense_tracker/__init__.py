import click
import pygsheets
from pygsheets import WorksheetNotFound

from .amex import Amex
from .bankwest import Bankwest
from .parser import autodetect
import datetime

SPREADSHEET_NAME = "Expense Tracking v2"
TEMPLATE_NAME = "Template"


@click.command()
@click.option(
    "--no-download-amex",
    is_flag=True,
    help="Use cached file from previous run instead of re-downloading",
)
@click.option(
    "--no-download-bankwest",
    is_flag=True,
    help="Use cached file from previous run instead of re-downloading",
)
def main(no_download_amex, no_download_bankwest):
    accounts = [Amex(), Bankwest()]

    if not no_download_amex:
        accounts[0].download()
    if not no_download_bankwest:
        accounts[1].download()

    data = []
    for account in accounts:
        account.process_data()
        data += account.data

    print("Filtering data")
    data = filter_data(data)

    print("Connecting to Google sheets")
    sheet = get_sheet_client()
    worksheet = clone_template_to(sheet, get_worksheet_date())
    print("Inserting data to worksheet")
    worksheet.insert_rows(row=1, values=data)
    print("Complete!")


def get_worksheet_date():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    response = last_month.strftime("%Y-%m")
    return response


def filter_data(data):
    # prefix with empty field for filling in purpose
    data = [autodetect(x) for x in data]
    data = [x for x in data if x]
    return data


def clone_template_to(sheet, new_name):
    try:
        worksheet = sheet.worksheet_by_title(new_name)
        print("Attempting to delete existing worksheet...")
        sheet.del_worksheet(worksheet)
        print("Successfully deleted existing worksheet.")
    except WorksheetNotFound:
        print("No existing worksheet found. Continuing without deletion.")
        pass

    print(f"Cloning to new worksheet {new_name}...")
    worksheet = sheet.add_worksheet(new_name, src_worksheet=sheet.worksheet_by_title(TEMPLATE_NAME))
    worksheet.hidden = False
    return worksheet


def get_sheet_client():
    gc = pygsheets.authorize()
    return gc.open(SPREADSHEET_NAME)


if __name__ == "__main__":
    main()

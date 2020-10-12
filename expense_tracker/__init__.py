import click
import re
import pygsheets
from pygsheets import WorksheetNotFound

from .amex import Amex
from .bankwest import Bankwest
import datetime

SPREADSHEET_NAME = "Expense Tracking"
TEMPLATE_NAME = "Template"


@click.command()
@click.option("--no-download", is_flag=True, help="Use cached file from previous run instead of re-downloading")
def main(no_download):
    accounts = [Amex(), Bankwest()]

    if not no_download:
        for account in accounts:
            account.download()

    data = []
    for account in accounts:
        account.process_data()
        data += account.data

    print("Filtering data")
    data = filter_data(data)

    print("Connecting to Google sheets")
    sheet = get_sheet_client()
    print("Cloning template worksheet")
    worksheet = clone_template_to(sheet, get_worksheet_date())
    print("Inserting data to worksheet")
    worksheet.insert_rows(row=1, values=data)


def get_worksheet_date():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    return last_month.strftime("%Y-%m")


def filter_data(data):
    # prefix with empty field for filling in purpose
    data = [autodetect(x) for x in data]
    return data


def autodetect(row):
    description = row[1]
    category = "Unknown"

    if match(
        "GOOD MORNING ASIAN|NIKOS FRUIT|HANARO|DAN MURPHYS|BWS|woolworths|\\bIGA\\b|COLES|ALDI\\b|FOODWORKS|FRESH SENSATIONS|SUMBAL PTY LTD",
            description):
        # SUMBAL is Brumby's in Nundah
        category = "Groceries"
    elif match("UBER|UNIQLO|MIMCO|ITUNES.COM|HUMBLEBUNDL|STEAM GAMES", description):
        category = cardholder(row)
    elif match("TRANSLINK|NUNDAH STATION", description):
        category = "Public Transport"
    elif match("PLUME HOLISTIC SKIN|HAIRZOOM|HMB BARBER|TWO BROTHERS TOOMBUL", description):
        category = "Hair"
    elif match("CALTEX|^BP\\b|^PUMA\\b|7-ELEVEN", description):
        category = "Fuel"
    elif match("REPCO|SUPER CHEAP AUTO", description):
        category = "Vehicle Maintenance"
    elif match("AMSTERDAM|NEDERLAND|CARLSON WAGONLIT", description):
        category = "Work Expense"
    elif match("VETERINARY|PETBARN|Vet", description):
        category = "Pet Expenses"
    elif match("Excella|MARC MILLER|FRIENDLY CARE|GRK PARTNERS|MEDICARE|MCARE BENEFITS|GRAND UNITED CORPORATE|POST OFFICE SQUARE PHAR|GU HEALTH", description):
        category = "Health/Medical"
    elif match("Goodlife", description):
        category = "Fitness"
    elif match("ALDIMOBILE|AMAGICOM|OPTUS|FAMOUS INS|000614696 CLEANING|CRUNCHYROLL|TPG Internet|NETFLIX.COM|AMAZON WEB SERVICES|SPOTIFY|BACKBLAZE|AMZNPRIMEAU MEMBERSHIP", description):
        category = "Untracked"
    elif match("LINKT BRISBANE", description):
        category = "Toll Roads"
    elif match("IKEA|PILLOW TALK", description):
        category = "House Improvements"

    return [category] + row


def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)


def cardholder(row):
    raw_cardholder = row[2]
    if match("justin", raw_cardholder):
        return "Justin"
    if match("celeste", raw_cardholder):
        return "Celeste"


def clone_template_to(sheet, new_name):
    try:
        worksheet = sheet.worksheet_by_title(new_name)
        sheet.del_worksheet(worksheet)
    except WorksheetNotFound:
        pass

    return sheet.add_worksheet(new_name, src_worksheet=sheet.worksheet_by_title(TEMPLATE_NAME))


def get_sheet_client():
    gc = pygsheets.authorize()
    return gc.open(SPREADSHEET_NAME)


if __name__ == '__main__':
    main()

import click
import re
import xlrd
import csv
import pygsheets
import json
from os.path import dirname, realpath, join
from pygsheets import WorksheetNotFound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SPREADSHEET_NAME = "Expense Tracking"
TEMPLATE_NAME = "Template"

# Usernames/passwords:
# { amex: { username: "asdf", password: "aasdf"}, bankwest: { ... } }
PASSWORDS_FILE = join(realpath(dirname(__file__)), ".expense-tracker-passwords.json")


@click.command()
# @click.option("--year", required=True)
# @click.option("--month", required=True)
# def main(year, month):
@click.option("--amex", required=True)
@click.option("--bankwest", required=True)
@click.option("--date", required=True, help="Format is YYYY-MM")
def main(amex, bankwest, date):
    data = read_amex_data(amex)
    data += read_bankwest_data(bankwest)

    # prefix with empty field for filling in purpose
    data = [autodetect(x) for x in data]

    sheet = get_sheet_client()

    worksheet = clone_template_to(sheet, date)

    worksheet.insert_rows(row=1, values=data)


def autodetect(row):
    description = row[1]
    category = "Unknown"

    if match("woolworths|\biga\b|COLES|ALDI\b|FOODWORKS|FRESH SENSATIONS|SUMBAL PTY LTD", description):
        # SUMBAL is Brumby's in Nundah
        category = "Groceries"
    elif match("UBER|UNIQLO|MIMCO|ITUNES.COM|HUMBLEBUNDL|STEAM GAMES", description):
        category = cardholder(row)
    elif match("TRANSLINK|NUNDAH STATION", description):
        category = "Public Transport"
    elif match("HAIRZOOM|HMB BARBER|TWO BROTHERS TOOMBUL", description):
        category = "Hair"
    elif match("CALTEX|^BP\b|^PUMA\b", description):
        category = "Fuel"
    elif match("REPCO", description):
        category = "Vehicle Maintenance"
    elif match("AMSTERDAM|NEDERLAND|CARLSON WAGONLIT", description):
        category = "Work Expense"
    elif match("VETERINARY|PETBARN", description):
        category = "Pet Expenses"
    elif match("Excella|MARC MILLER|FRIENDLY CARE|GRK PARTNERS|MEDICARE|MCARE BENEFITS|GRAND UNITED CORPORATE|POST OFFICE SQUARE PHAR|GU HEALTH", description):
        category = "Health/Medical"
    elif match("Goodlife", description):
        category = "Fitness"
    elif match("ALDIMOBILE|AMAGICOM|OPTUS|FAMOUS INS|000614696 CLEANING|CRUNCHYROLL|TPG Internet|NETFLIX.COM|AMAZON WEB SERVICES|SPOTIFY|BACKBLAZE|AMZNPRIMEAU MEMBERSHIP", description):
        category = "Untracked"
    elif match("LINKT BRISBANE", description):
        category = "Toll Roads"
    elif match("IKEA", description):
        category = "Home Improvements"

    return [category] + row


def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)


def download_amex(year, month):
    driver = webdriver.Firefox()
    driver.get("https://www.americanexpress.com/au/")
    username, password = get_password("amex")

    login_input = driver.find_element_by_id("login-user")
    login_input.send_keys(username)
    password_input = driver.find_element_by_id("login-password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)


def get_password(site):
    with open(PASSWORDS_FILE) as f:
        data = json.load(f)
        username = data[site]["username"]
        password = data[site]["password"]
    return [username, password]


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


def read_amex_data(amex):
    starting_row = 12
    wb = xlrd.open_workbook(amex)
    sheet = wb.sheet_by_index(0)
    data = []

    current_row = starting_row
    while True:
        try:
            row = [x.value for x in sheet.row(current_row)]  # Convert from xlrd data types
            data.append(row[1:5])  # Only keep the relevant columns
            current_row += 1
        except IndexError:
            break
    return data


def read_bankwest_data(bankwest):
    data = []
    with open(bankwest) as f:
        file = csv.reader(f)
        next(file)
        for row in file:
            if row[5] == "":  # nothing in debit column; assuming to be credits
                continue
            row[5] = row[5][1:]  # strip leading minus that is on all debits
            data.append(row[2:6])
    return data


def get_sheet_client():
    gc = pygsheets.authorize()
    return gc.open(SPREADSHEET_NAME)


if __name__ == '__main__':
    main()

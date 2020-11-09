import re


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
    elif match("PLUME HOLISTIC SKIN|HAIRZOOM|HMB BARBER|TWO BROTHERS TOOMBUL|PURELY CURLS", description):
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

def cardholder(row):
    return row[2]

def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)

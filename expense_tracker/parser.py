import re


def autodetect(row):
    description = company_detection(row[1])
    row[1] = description
    category = "Unknown"

    if match(
        "GOOD MORNING ASIAN|NIKOS FRUIT|HANARO|DAN MURPHYS|BWS"
        + "|woolworths|\\bIGA\\b|COLES|ALDI\\b|FOODWORKS|FRESH SENSATIONS"
        + "|FRUITS OF EDEN|HARRIS FARM MARKETS|MARLEYSPOON|BULKNUTRIEN|WW METRO",
        description,
    ):
        category = "Groceries"
    elif match(
        "UBER|UNIQLO|MIMCO|ITUNES.COM|HUMBLEBUNDL|STEAM GAMES|JANG & JANG", description
    ):
        category = cardholder(row)
    elif match("QUEENSLAND URBAN UTI", description):
        category = "Water"
    elif match("TRANSLINK|NUNDAH STATION", description):
        category = "Public Transport"
    elif match("SP 90 Bowen T", description):
        category = "Celeste"
    elif match(
        "PLUME HOLISTIC SKIN|HAIRZOOM|HMB BARBER|TWO BROTHERS TOOMBUL"
        + "|PURELY CURLS|BLACKWOOD BARBERS",
        description,
    ):
        category = "Hair"
    elif match("CALTEX|^BP\\b|^PUMA\\b|AMPOL|CHARGEFOX", description):
        category = "Fuel"
    elif match("REPCO|SUPER CHEAP AUTO", description):
        category = "Vehicle Maintenance"
    elif match(
        "AMSTERDAM|NEDERLAND|CARLSON WAGONLIT|BNE187 S807|O'GABEE COFFEE",
        description,
    ):
        category = "Work Expense"
    elif match("VETERINARY|PETBARN|Vet", description):
        category = "Pet Expenses"
    elif match(
        "Excella|MARC MILLER|FRIENDLY CARE|GRK PARTNERS|MEDICARE|"
        + "MCARE BENEFITS|GRAND UNITED CORPORATE|POST OFFICE SQUARE PHAR"
        + "|GU HEALTH|K C PSYCH|PLINE",
        description,
    ):
        category = "Health/Medical"
    elif match("Goodlife", description):
        category = "Fitness"
    elif match(
        "ALDIMOBILE|AMAGICOM|OPTUS|FAMOUS INS|000614696 CLEANING"
        + "|CRUNCHYROLL|TPG Internet|NETFLIX|AMAZON WEB SERVICES"
        + "|SPOTIFY|BACKBLAZE|AMZNPRIMEAU MEMBERSHIP",
        description,
    ):
        category = "Untracked"
    elif match("MOJO POWER", description):
        category = "Power"
    elif match("LINKT BRISBANE", description):
        category = "Toll Roads"
    elif match("IKEA|PILLOW TALK", description):
        category = "House Improvements"
    elif match("LIQUORLAND|BWS|1ST CHOICE LIQUOR", description):
        category = "Alcohol"
    elif match("apple.com", description):
        value = transaction_value(row)
        if value == 10.99:  # Crunchyroll
            category = "Untracked"
        if value == 11.99:  # Disney+
            category = "Untracked"
    elif match("ADOBESYSTEM", description):
        category = "Education"
    elif match("LIFESTYLEREWARDSAUD", description):
        # Amazon gift card purchase through GU Health
        category = "Untracked"

    return [category] + row


def cardholder(row):
    cardholder_full_name = row[2]
    first_name = cardholder_full_name.split(" ")[0]
    output_name = first_name.capitalize()
    return output_name


def company_detection(description):

    # Add description to Sushi Edo's cryptic name
    if match("JANG & JANG", description):
        description += " (Sushi Edo)"
    elif match("VANINA HOLDINGS", description):
        description += " (Bakers Delight Toombul)"
    elif match("SUMBAL", description):
        description += " (Brumby's Nundah)"
    elif match("JAI SAKHI BABA", description):
        description += " (Noodle Box Nundah)"
    elif match("THE TRUSTEE FOR CHICKE", description):
        description += " (You Came Again)"
    elif match("LIVIN LA VIDA LATROBA", description):
        description += " (King Tea)"
    elif match("BNE187 S807", description):
        description += " (300 George Street parking)"
    elif match("RSQ", description):
        description += " (Charlie's Raw Squeeze)"

    # Unknown so far:
    # PARKJUN

    return description


def transaction_value(row):
    return float(row[3].strip("$"))


def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)

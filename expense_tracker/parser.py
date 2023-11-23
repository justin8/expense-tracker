import re

# Expected spreadsheet format (Downloaders should convert in to this before parsing):
# Date, Description, Card Member, Amount (In positive numbers, with or without a '$' symbol)


def autodetect(row):
    description = company_detection(row)
    row[1] = description
    category = "Unknown"

    if match(
        "GOOD MORNING ASIAN|NIKOS FRUIT|HANARO|DAN MURPHYS|BWS"
        + "|woolworths|\\bIGA\\b|COLES|ALDI\\b|FOODWORKS|FRESH SENSATIONS"
        + "|FRUITS OF EDEN|HARRIS FARM MARKETS|BULKNUTRIEN|WW METRO"
        + "|Wolff Coffee Roasters|CLAYFIELD SEAFOOD MARKE|YUENS MARKET"
        + "|SUNLIT ASIAN SUPERMAR|ZEROCOCOMAU|FRESCO|WOWGIFTCARD|BREWBAKERS"
        + "|SUMBAL|T-Bones|BRUMBYS BAKERY",
        description,
    ):
        category = "Groceries"
    elif match("MARLEYSPOON", description):
        category = "Food"
    elif match("UBER|DIDI MOBILI|ITUNES.COM|HUMBLEBUNDL|STEAM GAMES|JANG & JANG", description):
        category = cardholder(row)
    elif match("QUEENSLAND URBAN UTI", description):
        category = "Water"
    elif match("TRANSLINK|NUNDAH STATION", description):
        category = "Public Transport"
    elif match("THE SMARTY BARBERS|HMB BARBER|BLACKWOOD BARBERS", description):
        category = "Justin"
    elif match("CALTEX|^BP\\b|^PUMA\\b|AMPOL|CHARGEFOX", description):
        category = "Fuel"
    elif match("REPCO|SUPER CHEAP AUTO|TESLA MOTORS AUSTRALIA", description):
        category = "Vehicle Maintenance"
    elif match(
        "CARLSON WAGONLIT|BNE187 S807|O'GABEE COFFEE|Wilson",
        description,
    ):
        category = "Work Expense"
    elif match("VETERINARY|PETBARN|Vet|FOUR PAW", description):
        category = "Pet Expenses"
    elif match(
        "Excella|Dr Mehrzad Entezami|MARC MILLER|FRIENDLY CARE|GRK PARTNERS"
        + "|MEDICARE|MCARE BENEFITS|GRAND UNITED CORPORATE|POST OFFICE SQUARE PHAR"
        + "|GU HEALTH|K C PSYCH|PLINE|THE PEACHAN COLLECTIVE|ReddyMedical",
        description,
    ):
        category = "Health/Medical"
    elif match("Goodlife", description):
        category = "Fitness"
    elif match("LINKT BRISBANE", description):
        category = "Toll Roads"
    elif match("IKEA|PILLOW TALK", description):
        category = "House Improvements"
    elif match("LIQUORLAND|BWS|1ST CHOICE LIQUOR", description):
        category = "Alcohol"
    elif match("Crunchyroll|Disney|AMAZON WEB SERVICES|TESLA INC|AUDIBLE|GOOGLE STORAGE|GEEKHUB|USENETBLOCK|NETFLIX|SPOTIFY|FORWARDEML|BACKBLAZE.COM", description):
        category = "Subscriptions"
    elif match("ADOBESYSTEM", description):
        category = "Education"
    elif match("Amex Travel Redemption|AMEX TRAVEL ONLINE", description):
        category = "Holidays"
    elif match(
        "LIFESTYLEREWARDSAUD|TPG|TELCO PAY|OPTUS BILLING AUTOPAY|VODAFONE|TELCO PAY FORTITUDE VALLE|Insurance|TRANSPORTMAINRDS|RING YEARLY PLAN|AMZNPRIMEAU MEMBERSHIP", description
    ):
        # Amazon gift card purchase through GU Health
        # Internet
        # Optus phone bill
        # Vodafone phone bill
        # Moose Mobile phone bill
        # Insurance
        # Rego
        # Ring
        # Prime membership
        category = "Untracked"
    elif match("HORSEPOWER PT", description):
        category = "Gym"
    elif match("AGLSALESPTY|ALINTA ENERGY", description):
        category = "Power and Gas"
    elif match("MOONPIGCOM", description):
        category = "Presents"
    elif match("GREATNAILS PTY LTD|TIMELYPAY|RAINBOWNAIL|PLUME SKIN|HAIRZOOM|EpicHair|PURELY CURLS", description):
        category = "Celeste"
    elif match("BNE187 S807|WestfieldChermside S805|SP 90 Bowen T", description):
        category = "Parking"
    elif match("BPAY PAYMENT-THANK YOU|INTERNET PAYMENT Linked Acc Trns|\+ANNUAL FEE|CASH/TRANSFER PAYMENT - THANK YOU|DIRECT DEBIT PAYMENT|DIRECT DEBIT RECEIVED", description):
        # Delete these rows
        # Credit card repayment
        return None

    return [category] + row


def cardholder(row):
    cardholder_full_name = row[2]
    first_name = cardholder_full_name.split(" ")[0]
    output_name = first_name.capitalize()
    return output_name


def company_detection(row):
    description = row[1]

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
    elif match("THE PEACHAN COLLECTIVE", description):
        description += " (KCPSYCH)"

    # elif match("apple.com", description):
    #     value = transaction_value(row)
    #     if value == 10.99:
    #         description += " (Crunchyroll)"
    #     if value == 11.99:
    #         description += " (Disney+)"
    # Unknown so far:
    # PARKJUN

    return description


def transaction_value(row):
    return float(row[3].strip("$").replace(",", ""))


def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)

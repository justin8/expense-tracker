import re


def autodetect(row):
    description = company_detection(row)
    row[1] = description
    category = "Unknown"

    if match(
        "GOOD MORNING ASIAN|NIKOS FRUIT|HANARO|DAN MURPHYS|BWS"
        + "|woolworths|\\bIGA\\b|COLES|ALDI\\b|FOODWORKS|FRESH SENSATIONS"
        + "|FRUITS OF EDEN|HARRIS FARM MARKETS|BULKNUTRIEN|WW METRO|"
        + "Wolff Coffee Roasters|CLAYFIELD SEAFOOD MARKE|YUENS MARKET|"
        + "SUNLIT ASIAN SUPERMAR|ZEROCOCOMAU|FRESCO",
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
    elif match(
        "PLUME HOLISTIC SKIN|HAIRZOOM|EpicHair|THE SMARTY BARBERS|HMB BARBER|TWO BROTHERS TOOMBUL|PURELY CURLS|BLACKWOOD BARBERS",
        description,
    ):
        category = "Hair"
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
        "Excella|MARC MILLER|FRIENDLY CARE|GRK PARTNERS|MEDICARE|MCARE BENEFITS|GRAND UNITED CORPORATE|POST OFFICE SQUARE PHAR|GU HEALTH|K C PSYCH|PLINE|THE PEACHAN COLLECTIVE",
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
    elif match("Crunchyroll|Disney|AMAZON WEB SERVICES|TESLA INC|AUDIBLE|GOOGLE GOOGLE|NETFLIX|SPOTIFY|FORWARDEML", description):
        category = "Subscriptions"
    elif match("ADOBESYSTEM", description):
        category = "Education"
    elif match("Amex Travel Redemption|AMEX TRAVEL ONLINE", description):
        category = "Holidays"
    elif match("LIFESTYLEREWARDSAUD|TPG|OPTUS BILLING AUTOPAY|VODAFONE|TELCO PAY FORTITUDE VALLE|Insurance|TRANSPORTMAINRDS", description):
        # Amazon gift card purchase through GU Health
        # Internet
        # Optus phone bill
        # Vodafone phone bill
        # Moose Mobile phone bill
        # Insurance
        # Rego
        category = "Untracked"
    elif match("HORSEPOWER PT", description):
        category = "Gym"
    elif match("AGLSALESPTY", description):
        category = "Power and Gas"
    elif match("MOONPIGCOM", description):
        category = "Presents"
    elif match("GREATNAILS PTY LTD|RAINBOWNAIL|SP 90 Bowen T", description):
        category = "Celeste"
    elif match("BPAY PAYMENT-THANK YOU|INTERNET PAYMENT Linked Acc Trns|\+ANNUAL FEE", description):
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

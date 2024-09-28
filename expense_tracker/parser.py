import re

# Expected spreadsheet format (Downloaders should convert in to this before parsing):
# Date, Description, Card Member, Amount (In positive numbers, with or without a '$' symbol)


def autodetect(row):
    description = company_detection(row)
    row[1] = description
    category = "Unknown"

    mapping = {
        "Groceries": [
            "GOOD MORNING ASIAN",
            "NIKOS FRUIT",
            "HANARO",
            "DAN MURPHYS",
            "BWS",
            "woolworths",
            "\\bIGA\\b",
            "COLES",
            "ALDI\\b",
            "FOODWORKS",
            "FRESH SENSATIONS",
            "FRUITS OF EDEN",
            "HARRIS FARM MARKETS",
            "BULKNUTRIEN",
            "WW METRO",
            "Wolff Coffee Roasters",
            "CLAYFIELD SEAFOOD MARKE",
            "YUENS MARKET",
            "SUNLIT ASIAN SUPERMAR",
            "ZEROCOCOMAU",
            "FRESCO",
            "WOWGIFTCARD",
            "BREWBAKERS",
            "SUMBAL",
            "T-Bones",
            "BRUMBYS BAKERY",
        ],
        "Food": ["MARLEYSPOON"],
        "Cardholder": [
            "UBER",
            "DIDI MOBILI",
            "ITUNES.COM",
            "HUMBLEBUNDL",
            "STEAM GAMES",
            "JANG & JANG",
        ],
        "Water": ["QUEENSLAND URBAN UTI"],
        "Public Transport": ["TRANSLINK", "NUNDAH STATION"],
        "Justin": [
            "THE SMARTY BARBERS",
            "HMB BARBER",
            "BLACKWOOD BARBERS",
            "BABYLON & CO",
        ],
        "Power and Gas": ["AGLSALESPTY", "ALINTA ENERGY", "AMPOL ENERGY"],
        "Fuel": ["CALTEX", "^BP\\b", "^PUMA\\b", "AMPOL", "CHARGEFOX"],
        "Vehicle Maintenance": ["REPCO", "SUPER CHEAP AUTO", "Tesla "],
        "Work Expense": [
            "CARLSON WAGONLIT",
            "BNE187 S807",
            "O'GABEE COFFEE",
            "Wilson",
            "VODAFONE",
        ],
        "Pet Expenses": ["VETERINARY", "PETBARN", "Vet", "FOUR PAW"],
        "Health/Medical": [
            "Excella",
            "Dr Mehrzad Entezami",
            "MARC MILLER",
            "FRIENDLY CARE",
            "GRK PARTNERS",
            "MEDICARE",
            "MCARE BENEFITS",
            "GRAND UNITED CORPORATE",
            "POST OFFICE SQUARE PHAR",
            "GU HEALTH",
            "K C PSYCH",
            "PLINE",
            "THE PEACHAN COLLECTIVE",
            "ReddyMedical",
            "MOHS CLAYFIELD",
            "MHS PSYCHOLOGY",
        ],
        "Fitness": ["Goodlife", "N0BIS TRAINING"],
        "Toll Roads": ["LINKT BRISBANE"],
        "House Improvements": ["IKEA", "PILLOW TALK"],
        "Alcohol": ["LIQUORLAND", "BWS", "1ST CHOICE LIQUOR"],
        "Subscriptions": [
            "Crunchyroll",
            "Disney",
            "AMAZON WEB SERVICES",
            "TESLA",
            "AUDIBLE",
            "GOOGLE STORAGE",
            "GEEKHUB",
            "USENETBLOCK",
            "NETFLIX",
            "SPOTIFY",
            "FORWARDEML",
            "BACKBLAZE",
        ],
        "Education": ["ADOBESYSTEM"],
        "Holidays": ["Amex Travel Redemption", "AMEX TRAVEL ONLINE"],
        "Untracked": [
            "TPG", # Internet
            "TELCO PAY", # Moose Mobile
            "OPTUS BILLING AUTOPAY",
            "Insurance", # Tracked in budget
            "TRANSPORTMAINRDS", # Tracked in budget
            "RING YEARLY PLAN", # Tracked in budget
            "AMZNPRIMEAU MEMBERSHIP", # Tracked in budget
        ],
        "Presents": ["MOONPIGCOM"],
        "Grooming": ["PLUME SKIN"],
        "Celeste": [
            "GREATNAILS PTY LTD",
            "TIMELYPAY",
            "RAINBOWNAIL",
            "HAIRZOOM",
            "EpicHair",
            "PURELY CURLS",
        ],
        "Parking": ["BNE187 S807", "WestfieldChermside S805", "SP 90 Bowen T"],
        "Delete": [
            "BPAY PAYMENT-THANK YOU",
            "INTERNET PAYMENT Linked Acc Trns",
            "ANNUAL FEE",
            "CASH/TRANSFER PAYMENT - THANK YOU",
            "DIRECT DEBIT PAYMENT",
            "DIRECT DEBIT RECEIVED",
            "PAYMENT RECEIVED, THANK YOU",
        ],
    }

    for category, patterns in mapping.items():
        for pattern in patterns:
            if match(pattern, description):
                if category == "Cardholder":
                    return cardholder(row)  # Special case for Cardholder category
                elif category == "Delete":
                    return None  # Delete rows case
                else:
                    return [category] + row
    return ["Unknown"] + row


def cardholder(row):
    cardholder_full_name = row[2]
    first_name = cardholder_full_name.split(" ")[0]
    output_name = first_name.capitalize()
    return output_name


def company_detection(row):
    description = row[1]

    mapping = {
        "Sushi Edo": "JANG & JANG",
        "Bakers Delight Toombul": "VANINA HOLDINGS",
        "Brumby's Nundah": "SUMBAL",
        "Noodle Box Nundah": "JAI SAKHI BABA",
        "You Came Again": "THE TRUSTEE FOR CHICKE",
        "King Tea": "LIVIN LA VIDA LATROBA",
        "300 George Street parking": "BNE187 S807",
        "Charlie's Raw Squeeze": "RSQ",
        "KCPSYCH": "THE PEACHAN COLLECTIVE",
        "Dermatologist": "MOHS CLAYFIELD",
        "Hanok Korean BBQ": "DOUBLE LIFT PTY LTD",
        "Chilink massage": "9STAR",
    }

    for name, pattern in mapping.items():
        if match(pattern, description):
            description += f" ({name})"

    return description


def transaction_value(row):
    return float(row[3].strip("$").replace(",", ""))


def match(pattern, string):
    return re.findall(pattern, string, re.IGNORECASE)

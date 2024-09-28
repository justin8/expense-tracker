import re

# Expected spreadsheet format (Downloaders should convert in to this before parsing):
# Date, Description, Card Member, Amount (In positive numbers, with or without a '$' symbol)


def autodetect(row):
    description = company_detection(row)
    row[1] = description
    category = "Unknown"

    mapping = {
        "Groceries": [
            "good morning asian",
            "nikos fruit",
            "hanaro",
            "dan murphys",
            "bws",
            "woolworths",
            "\\biga\\b",
            "coles",
            "aldi\\b",
            "foodworks",
            "fresh sensations",
            "fruits of eden",
            "harris farm markets",
            "bulknutrien",
            "ww metro",
            "wolff coffee roasters",
            "clayfield seafood marke",
            "yuens market",
            "sunlit asian supermar",
            "zerococomau",
            "fresco",
            "wowgiftcard",
            "brewbakers",
            "sumbal",
            "t-bones",
            "brumbys bakery",
        ],
        "Food": ["marleyspoon"],
        "Cardholder": [
            "uber",
            "didi mobili",
            "itunes.com",
            "humblebundl",
            "steam games",
            "jang & jang",
        ],
        "Water": ["queensland urban uti"],
        "Public Transport": ["translink", "nundah station"],
        "Justin": [
            "the smarty barbers",
            "hmb barber",
            "blackwood barbers",
            "babylon & co",
        ],
        "Power and Gas": ["aglsalespty", "alinta energy", "ampol energy"],
        "Fuel": ["caltex", "^bp\\b", "^puma\\b", "ampol", "chargefox"],
        "Vehicle Maintenance": ["repco", "super cheap auto", "tesla "],
        "Work Expense": [
            "carlson wagonlit",
            "bne187 s807",
            "o'gabee coffee",
            "wilson",
            "vodafone",
        ],
        "Pet Expenses": ["veterinary", "petbarn", "vet", "four paw"],
        "Health/Medical": [
            "excella",
            "dr mehrzad entezami",
            "marc miller",
            "friendly care",
            "grk partners",
            "medicare",
            "mcare benefits",
            "grand united corporate",
            "post office square phar",
            "gu health",
            "k c psych",
            "pline",
            "the peachan collective",
            "reddymedical",
            "mohs clayfield",
            "mhs psychology",
        ],
        "Fitness": ["goodlife", "n0bis training"],
        "Toll Roads": ["linkt brisbane"],
        "House Improvements": ["ikea", "pillow talk"],
        "Alcohol": ["liquorland", "bws", "1st choice liquor"],
        "Subscriptions": [
            "crunchyroll",
            "disney",
            "amazon web services",
            "tesla",
            "audible",
            "google storage",
            "geekhub",
            "usenetblock",
            "netflix",
            "spotify",
            "forwardeml",
            "backblaze",
        ],
        "Education": ["adobesystem"],
        "Holidays": ["amex travel redemption", "amex travel online"],
        "Untracked": [
            "tpg", # Internet
            "telco pay", # Moose Mobile
            "optus billing autopay",
            "insurance", # Tracked in budget
            "transportmainrds", # Tracked in budget
            "ring yearly plan", # Tracked in budget
            "amznprimeau membership", # Tracked in budget
        ],
        "Presents": ["moonpigcom"],
        "Grooming": ["plume skin"],
        "Celeste": [
            "greatnails pty ltd",
            "timelypay",
            "rainbownail",
            "hairzoom",
            "epichair",
            "purely curls",
        ],
        "Parking": ["bne187 s807", "westfieldchermside s805", "sp 90 bowen t"],
        "Delete": [
            "bpay payment-thank you",
            "internet payment linked acc trns",
            "annual fee",
            "cash/transfer payment - thank you",
            "direct debit payment",
            "direct debit received",
            "payment received, thank you",
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

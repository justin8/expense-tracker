import os
from os.path import join


# Usernames/passwords:
# { amex: { username: "asdf", password: "aasdf"}, bankwest: { ... } }
PASSWORDS_FILE = join(os.getcwd(), "site-passwords.json")


class Downloader(object):
    data = None

    def process_data(self):
        """
        This method processes the downloaded data and places it in to self.data for later access
        Expected output format is a list of lists in the order:
        [date, description, cardholder, amount (without leading minus)]
        """
        raise NotImplementedError("_process_data needs to be implemented by a subclass")

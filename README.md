# Expense Tracker

This script logs in to Bankwest and Amex and pulls down last month's transaction logs, merges them in to a common format and pushes it to Google Sheets

## Usage

1. Ensure that `client_secret.json` is created in the root directory per Google docs.

2. Copy `site_passwords.json.example` to `site_passwords.json` and fill in the usernames & passwords

3. Run the script with `poetry run expense_tracker`

## Notes

Bankwest is pretty good in that they never update their website much, so the script rarely has issues.

Amex AU on the other hand likes to add new pop ups, change the names of elements and such most months; good luck!

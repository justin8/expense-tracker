# Expense Tracker

This script logs in to Bankwest and Amex and pulls down last month's transaction logs, merges them in to a common format and pushes it to Google Sheets

## Initial Setup

1. Log on to google cloud console
2. Navigate to APIs -> Credentials
3. Create credentials and choose Desktop app as the application type
4. You can download the file with the download button under OAuth 2.0 client IDs; save it as `client_secret.json`
5. Configure venv and dependencies: `poetry install` (if this fails, run: `rm -rf .venv`)
6. Install `geckodriver`: `brew install geckodriver`

## Usage

1. Ensure that `client_secret.json` is created in the root directory per the initial setup instructions.
2. Copy `site_passwords.json.example` to `site_passwords.json` and fill in the usernames & passwords
4. Run the script with `poetry run expense-tracker`


## Notes

Bankwest is pretty good in that they never update their website much, so the script rarely has issues.

Amex AU on the other hand likes to add new pop ups, change the names of elements and such most months; good luck!

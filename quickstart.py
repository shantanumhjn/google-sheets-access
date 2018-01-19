
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
SHEET_ID = '1-FczP9vFUYz7RVG503cxeuKd9pHKVmPtjQb9IpNnSkc'
SHEET_ID = "1bopO47UZprBcX3YHWOnYXXOGNnR9d6FMtkrUp8Jm9ts" # test sheet

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        # flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service

def get_result(service, rangeName, majorDimension = None):
    result = service.spreadsheets().values().get(
                    spreadsheetId=SHEET_ID,
                    range=rangeName,
                    valueRenderOption="UNFORMATTED_VALUE",
                    majorDimension=majorDimension).execute()
    values = result.get('values', [])
    return values

def get_names():
    service = get_service()
    rangeName = 'badminton!A3:A100'
    values = get_result(service, rangeName)
    for row in values:
        if len(row) > 0: print(row[0])
        else: break

def get_dates():
    service = get_service()
    rangeName = 'badminton!C1:1'
    # SERIAL_NUMBER, FORMATTED_STRING
    # date returned as number of days since dec 30, 1899 (30 is not a typo)
    values = get_result(service, rangeName, "COLUMNS")
    import datetime
    today = datetime.date.today()
    base_date = datetime.date(1899, 12, 30)
    print("base date:", base_date)
    for row in values:
        dt_str = row[0]
        dt = base_date + datetime.timedelta(days = dt_str)
        print(dt_str, '-', dt)

def get_my_balance():
    service = get_service()
    rangeName = 'badminton!A3:B21'
    values = get_result(service, rangeName)
    for row in values:
        if row[0].lower() == 'shantanu':
            print(row[1])
            break

def main():
    service = get_service()

    rangeName = 'badminton!A3:B21'
    values = get_result(service, rangeName)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))


if __name__ == '__main__':
    #main()
    # get_names()
    # get_dates()
    get_my_balance()

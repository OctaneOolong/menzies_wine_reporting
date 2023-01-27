from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

def get_credentials():
    """gets the credientials for the google sheets API
    """
    creds = None

    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    path_to_token = 'credentials_tokens/token_sheets.json'

    path_to_credentials = 'credentials_tokens/credentials_sheets.json'


    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_to_token):
        creds = Credentials.from_authorized_user_file(path_to_token, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_credentials, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_to_token, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def sheets_service_getter(spreadsheet_id):
    
    creds = get_credentials()

    service = build('sheets', 'v4', credentials = creds)

    return service
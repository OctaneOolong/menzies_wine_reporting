from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

import os.path

SCOPES = ['https://www.googleapis.com/auth/documents']

def google_docs_service_getter():
    """contacts the api and returns the document object as a nested dict.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('credentials_tokens/token_docs.json'):
        creds = Credentials.from_authorized_user_file('token_docs.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_tokens/credentials_docs.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials_tokens/token_docs.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

    except HttpError as err:
        print(err)

    return service

def main():
    
    service = google_docs_service_getter()

    print(service)

main()
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
    # created automatically when the authorization flow completes for the first time.

    path_to_token = 'credentials_tokens/token_docs.json'

    path_to_credentials = 'credentials_tokens/credentials_docs.json'

    if os.path.exists(path_to_token):
        creds = Credentials.from_authorized_user_file(path_to_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_to_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_to_token, 'w') as token:
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
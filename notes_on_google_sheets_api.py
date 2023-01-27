from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import pandas as pd
 
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1OMDtvdnsu0kFCXFxQnSRcP49qpIiWrosUSV1si5OKPg'
INPUT_RANGE_NAME = 'restock_status!A1:K150'
OUTPUT_RANGE_NAME = 'restock_status_test!A1'

# Build the service object
service = build('sheets', 'v4', credentials=get_credentials())

# Call the Sheets API

sheets_api = service.spreadsheets()

# there are two main items within the sheets_api, the spreadsheet object and the values object. The spreadsheet object contains high level metadata such as the spreadsheet url, named ranges within the spreadsheet, developer metadata, the names of the sheets within the spreadsheet and etc. The values object contains all of the data within the spreadsheet.

# get the values of the spreadsheet in the form of a dict. The values dict will contain the data itself, the range the data was requested from (inputted by the user on initialisation) and the major dimension of the data (rows or columns).

values_dict = sheets_api.values().get(spreadsheetId=SPREADSHEET_ID, range=INPUT_RANGE_NAME).execute()

# to get each row of data from the values dict, we can access the values key of the dict. This will return a list of lists, where each list is a row of data.

rows_list = values_dict.get('values', "none found")
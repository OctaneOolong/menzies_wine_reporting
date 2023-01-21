from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import pandas
 
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1OMDtvdnsu0kFCXFxQnSRcP49qpIiWrosUSV1si5OKPg'
INPUT_RANGE_NAME = 'restock_status!A1:K150'
OUTPUT_RANGE_NAME = 'restock_status_test!A1'

def get_credentials():
    """gets the credientials for the google sheets API
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def test_function_edit_pj_soh(service, values):

    # Convert the values to a pandas dataframe

    df = pandas.DataFrame(values[1:], columns=values[0])
    
    # edit the dataframe to update values

    df = df.set_index("name")

    df.loc["perrier jouet 'grand brut'", "soh"] = 999

    df = df.reset_index()
    
    # Turn the data back into the API required format (list of lists). Combine the column headers with the data to preserve them.
    
    data = [df.columns.values.tolist()]
    data.extend(df.values.tolist())
        
    # Create the body of the request

    value_range_body = {"values": data}

    # send the request to Google Sheets API

    value_request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=OUTPUT_RANGE_NAME, 
    valueInputOption="USER_ENTERED",includeValuesInResponse=True, body = value_range_body)

    value_request.execute()

    #print(conditionalFormating[0]["ranges"])
    
    # TODO add sheetID to conditional formatting ranges field in order to apply it to restock_status_test. The sheetID should be 2.

    #format_request.execute()

    return value_request

def conditional_format_update(sheets_api):
    ## access the condtionalFormats property of the spreadsheet sheet restock_status, which we will apply to restock_status_test
        
    spreadsheet = sheets_api.get(spreadsheetId=SPREADSHEET_ID).execute()

    conditionalFormating = spreadsheet["sheets"][1]["conditionalFormats"]

    ## acceess the sheetId of target sheet, i.e. restock_status_test

    sheetId = spreadsheet["sheets"][2]["properties"]["sheetId"]

    ## To apply the conditional formatting to the target sheet a sheetId field needs to be added to every conditional format rule range.

    for conditional_format in conditionalFormating:
    
        conditional_format['ranges'][0]['sheetId'] = sheetId

    # The conditional formats must be submitted as a request body in the format below. A loop is used to add each conditional format rule.

    conditional_format_request_body = { "requests" : [] }

    for conditional_format in conditionalFormating:
            
        conditional_format_request_body["requests"].append({"addConditionalFormatRule" : { "rule" : conditional_format } })
    
    # delete existing rules on the sheet

    # conditional_format_request_body["requests"].append({"deleteConditionalFormatRule" : { "index" : 0, "sheetId" : sheetId } })

    # executes the update onto the target sheet using the request body formed above.

    sheets_api.batchUpdate(spreadsheetId=SPREADSHEET_ID, body = conditional_format_request_body).execute()

def main():

    try:
        # Build the service object
        service = build('sheets', 'v4', credentials=get_credentials())

        # Call the Sheets API

        sheets_api = service.spreadsheets()

        # there are two main items within the sheets_api, the spreadsheet object and the values object. The spreadsheet object contains high level metadata such as the spreadsheet url, named ranges within the spreadsheet, developer metadata, the names of the sheets within the spreadsheet and etc. The values object contains all of the data within the spreadsheet.

        # get the values of the spreadsheet in the form of a dict. The values dict will contain the data itself, the range the data was requested from (inputted by the user on initialisation) and the major dimension of the data (rows or columns).

        values_dict = sheets_api.values().get(spreadsheetId=SPREADSHEET_ID, range=INPUT_RANGE_NAME).execute()
        
        # to get each row of data from the values dict, we can access the values key of the dict. This will return a list of lists, where each list is a row of data.

        rows_list = values_dict.get('values', "none found")

        print(len(rows_list))
        #print(json.dumps(values_dict, indent=4))

        if not rows_list:
            print('No data found.')
            return
        
        #test_function_edit_pj_soh(service, values)
        #conditional_format_update(sheets_api)
        '''
        I need to:
        TODO:
        - [ ] form a df from the rows_list.
        - [ ] query the df for rows matching the 'low' criteria defined in the query in the spreadsheet.
        - [ ] output the result into a format that is acceptable to a google docs api request.
        - [ ] send the request to the google docs api and see how it goes.
        '''

        
        
    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()

"""
# 1. get the restock report "restocked" values.

# 2. get the soh counts from "restock_status".

# 3. add the restocked values to the soh count. will need to be done with a inner join (?) to match up the rows.

# 4. update "stock_status" range with the sum values.

# 5. Provide a report of what's been updated.
"""

import google_api_service_getters.sheets_service_getter as sheets_service_getter

import pandas as pd

from restock_report_df_builder import restock_report_df_builder

# I need the service to get the spreadsheet object which contains the values.

def stock_status_df_builder(spreadsheet_id, service, stock_status_range):

    sheets_api = service.spreadsheets()

    stock_status_values_dict = sheets_api.values().get(spreadsheetId = spreadsheet_id, range = stock_status_range).execute()

    sheet_data = stock_status_values_dict.get("values")

    for idx, row in enumerate(sheet_data[1:], 1):

        if len(row) < len(sheet_data[0]):
            sheet_data[idx].append(0)

    stock_status_df = pd.DataFrame(sheet_data[1:], columns = sheet_data[0]).dropna()

    try:
        stock_status_df['wine_index'] = stock_status_df['vintage'] + ' ' + stock_status_df['name']


        stock_status_df = stock_status_df.set_index(['wine_index'])

        stock_status_df['soh'] = pd.to_numeric(stock_status_df['soh'], errors = 'coerce')

        stock_status_df['par'] = pd.to_numeric(stock_status_df['par'], errors = 'coerce')

    except NameError:
        print(NameError)

    return stock_status_df

def soh_from_restocked_updater():

    service = sheets_service_getter.sheets_service_getter(10)

    spreadsheet_id = '1OMDtvdnsu0kFCXFxQnSRcP49qpIiWrosUSV1si5OKPg'

    restocked_values_range = "restock_report!A1:E200"
    
    stock_status_range = "restock_status_test!A1:F200"
    
    restocked_df = restock_report_df_builder(spreadsheet_id, service, restocked_values_range)

    stock_status_df = stock_status_df_builder(spreadsheet_id, service, stock_status_range)

    stock_status_df['soh'] = stock_status_df['soh'].add(restocked_df['restocked'], fill_value = 0)

    print(restocked_df)

    data = [stock_status_df['soh'].values.tolist()]

    body_  = {
        "range" : "restock_status!E2", 
        "majorDimension" : "COLUMNS", 
        "values" : data}
    
    update_soh_request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range="restock_status!E2",valueInputOption="USER_ENTERED",includeValuesInResponse=True, body = body_)
    
    update_soh_request.execute()
    
    print(update_soh_request)
    # update the stock_status soh column with the soh df column values

soh_from_restocked_updater()
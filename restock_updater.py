"""
# 1. get the restock report "restocked" values.

# 2. get the soh counts from "restock_status".

# 3. add the restocked values to the soh count. will need to be done with a inner join (?) to match up the rows.

# 4. update "stock_status" range with the sum values.

# 5. Provide a report of what's been updated.
"""

import google_api_service_getters.sheets_service_getter as sheets_service_getter

from menzies_stock_info import menzies_stock_info

from restock_report_df_builder import restock_report_df_builder

from stock_status_df_builder import stock_status_df_builder

def soh_from_restocked_updater():

    spreadsheet_id, restocked_values_range, stock_status_range = menzies_stock_info()
    
    service = sheets_service_getter.sheets_service_getter(spreadsheet_id)

    restocked_df = restock_report_df_builder(spreadsheet_id, service, restocked_values_range)

    print(restocked_df)
    
    stock_status_df = stock_status_df_builder(spreadsheet_id, service, stock_status_range)

    stock_status_df['soh'] = stock_status_df['soh'].add(restocked_df['restocked'], fill_value = 0)

    data = [stock_status_df['soh'].values.tolist()]

    body_  = {
        "range" : "restock_status!E2", 
        "majorDimension" : "COLUMNS", 
        "values" : data}
    
    update_soh_request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range="restock_status!E2",valueInputOption="USER_ENTERED",includeValuesInResponse=True, body = body_)
    
    # can get the result of the update request by calling the execute() method on the update_soh_request object and setting it to a variable, the output is a dict. 

    result = update_soh_request.execute()

soh_from_restocked_updater()
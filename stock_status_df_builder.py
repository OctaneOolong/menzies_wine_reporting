import pandas as pd

from google_api_service_getters.sheets_service_getter import sheets_service_getter

def stock_status_df_builder(spreadsheet_id, service, stock_status_range):

    service = sheets_service_getter(spreadsheet_id)

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
        print("uh oh, an error: ", NameError)

    return stock_status_df
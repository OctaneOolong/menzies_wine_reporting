import pandas as pd

import google_api_service_getters.sheets_service_getter as sheets_service_getter

from menzies_stock_info import menzies_stock_info

def restock_report_df_builder(spreadsheet_id, service, restocked_values_range):

    sheets_api = service.spreadsheets()

    restocked_values_dict = sheets_api.values().get(spreadsheetId = spreadsheet_id, range = restocked_values_range).execute()

    sheet_data = restocked_values_dict.get("values")

    # to form the df, the inputted rows need to be symmetrical. The restocked column will not necessarily be full of values as it would be fustrating to have to delete every value before input. Thus a quick loop should be written to populate every row.

    for idx, row in enumerate(sheet_data[1:], 1):

        # if idx == len(sheet_data[1:]):
        #     break

        if len(row) < len(sheet_data[0]):
            sheet_data[idx].append(0)

    restocked_values_df = pd.DataFrame(sheet_data[1:], columns = sheet_data[0]).dropna()

    restocked_values_df = restocked_values_df[restocked_values_df['restocked'] != 0]

    restocked_values_df['wine_index'] = restocked_values_df['vintage'] + ' ' + restocked_values_df['name']

    restocked_values_df = restocked_values_df.set_index(['wine_index'])

    restocked_values_df['soh'] = pd.to_numeric(restocked_values_df['soh'], errors = 'coerce')

    restocked_values_df['restock'] = pd.to_numeric(restocked_values_df['restock'], errors = 'coerce')

    restocked_values_df['restocked'] = pd.to_numeric(restocked_values_df['restocked'], errors = 'coerce')

    return restocked_values_df 

def main():

    spreadsheet_id, restocked_values_range, stock_status_range = menzies_stock_info()

    service = sheets_service_getter.sheets_service_getter(spreadsheet_id)

    restock_report_df_builder(spreadsheet_id, service, restocked_values_range)

main()
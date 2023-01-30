import pandas as pd

import hvplot.pandas

from menzies_stock_info import menzies_stock_info

from google_api_service_getters.sheets_service_getter import sheets_service_getter

from stock_status_df_builder import stock_status_df_builder

def dataframe_queries(df):
    
    """
    query the df for btg lows. The algorithm is:
    #"=QUERY(restock_status!A1:I145, "SELECT vintage, name, soh WHERE soh>0 and soh<4 and (1-(par-soh)/par)<(2/3) and format='btg' ORDER BY soh ASC")"
    """

    # convert soh, par, restock to numeric

    # change soh to numeric
    # change par to numeric
    # change restock to numeric

    df["soh"] = pd.to_numeric(df["soh"], errors="coerce")
    df["par"] = pd.to_numeric(df["par"], errors="coerce")
    df["restock"] = pd.to_numeric(df["restock"], errors="coerce")

    # btg lows

    df['soh_ratio'] = round(1-(df["par"]-df['soh'])/df['par'],4)

    low_stock_ratio = 2/3

    # oos btg

    oos_btg_query = 'soh == 0 and format=="btg"'

    oos_btg_df = df.query(oos_btg_query).sort_values(by=['soh'], ascending=True)

    # low btg

    low_btg_query = 'soh > 0 and soh <4 and (1-(par-soh)/par)<({}) and format=="btg"'.format(low_stock_ratio)

    low_btg_df = df.query(low_btg_query).sort_values(by=['soh'], ascending=True)

    # oos btb

    oos_btb_query = 'soh == 0 and format=="btb"'

    oos_btb_df = df.query(oos_btb_query).sort_values(by=['soh'], ascending=True)

    # low btb

    low_btb_query = 'soh > 0 and soh <4 and (1-(par-soh)/par)<({}) and format=="btb"'.format(low_stock_ratio)

    low_btb_df = df.query(low_btb_query).sort_values(by=['soh'], ascending=True)

    return oos_btg_df, low_btg_df, oos_btb_df, low_btb_df
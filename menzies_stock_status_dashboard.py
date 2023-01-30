import panel as pn

import pandas as pd

from stock_status_queries import dataframe_queries

from stock_status_df_builder import test_stock_status_df

import datetime as dt

#pn.extension(template='material', theme='dark')

pn.extension('tabulator', css_files=[pn.io.resources.CSS_URLS['font-awesome']])

oos_btg_df, low_btg_df, oos_btb_df, low_btb_df = dataframe_queries(test_stock_status_df())

margin_ = (0, 0, 0, 0)

columns_to_display = ['soh', 'par']

oos_btg_tbl = pn.widgets.Tabulator(oos_btg_df[columns_to_display], 
                                    #theme = 'materialize'
                                    )

low_btg_tbl = pn.widgets.Tabulator(low_btg_df[columns_to_display],
                                #    theme = 'site'
                                    )

low_btb_tbl = pn.widgets.Tabulator(low_btb_df[columns_to_display], 
                                   #theme = 'modern'
                                   )

oos_btb_tbl = pn.widgets.Tabulator(oos_btb_df[columns_to_display], 
                                    # theme = 'bulma'
                                    )

gspec = pn.GridSpec(sizing_mode = 'stretch_both')


def low_stock_status_mkdwn_genner(df):

    stock_mkdwn = ""

    for index, row in df.iterrows():

        stock_mkdwn +='{} x {}<br>'.format(row['soh'], index)

    return stock_mkdwn

    
def oos_stock_status_mkdwn_genner(df):
    
    stock_mkdwn = ""

    for index, row in df.iterrows():
        
        stock_mkdwn +='{}<br>'.format(index)


    return stock_mkdwn

oos_btg_stock_mkdwn = oos_stock_status_mkdwn_genner(oos_btg_df)
low_btg_stock_mkdown = low_stock_status_mkdwn_genner(low_btg_df)

oos_btb_stock_mkdwn = oos_stock_status_mkdwn_genner(oos_btb_df)
low_btb_stock_mkdwn = low_stock_status_mkdwn_genner(low_btb_df)

oos_btg_tabs = pn.Tabs(('DF format', oos_btg_tbl), ('print format', pn.panel(oos_btg_stock_mkdwn)))
low_btg_tabs = pn.Tabs(('DF format', low_btg_tbl), ('print format', pn.panel(low_btg_stock_mkdown)))
oos_btb_tabs = pn.Tabs(('DF format', oos_btb_tbl), ('print format', pn.panel(oos_btb_stock_mkdwn)))
low_btb_tabs = pn.Tabs(('DF format', low_btb_tbl), ('print format', pn.panel(low_btb_stock_mkdwn)))

oos_btg_col = pn.Column('## oos_btg_tbl', oos_btg_tabs)
low_btg_col = pn.Column('## low_btg_tbl', low_btg_tabs)
oos_btb_col = pn.Column('## oos_btb_tbl', oos_btb_tabs)
low_btb_col = pn.Column('## low_btb_tbl', low_btb_tabs)


gspec[0, 0] = oos_btg_col
gspec[1, 0] = low_btg_col
gspec[0, 1] = oos_btb_col
gspec[1, 1] = low_btb_col

heading_1 = pn.pane.Markdown('# Menzies Wine Stock Status')

column = pn.Column(heading_1, gspec)

column.servable()

#column = pn.Column(heading, gspec).servable()
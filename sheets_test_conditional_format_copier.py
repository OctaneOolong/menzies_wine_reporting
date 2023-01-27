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
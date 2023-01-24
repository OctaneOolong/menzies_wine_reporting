import sheets_data_manip

import docs_manip

def print_to_doc(text, service, doc_id):

    insert_text_request = { 
                "insertText": {
                    "location": {
                        "index": 1
                    },
                    "text": "{}".format(text)
                }
    }

    format_text_request = {
                "updateTextStyle": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": 715,
                    },
                    'textStyle': {
                        "foregroundColor": {
                            "color": {
                                "rgbColor": {
                                    'blue': 0.0,
                                    'green': 0.0,
                                    'red': 1.0
                                }
                            }
                        }
                    },
                
                'fields' : 'foregroundColor'
                }
                
    }

    try: 
        request = [insert_text_request, format_text_request]
        
        result = service.documents().batchUpdate(documentId=doc_id, body={"requests": request}).execute()

    except Exception as e:
        print(e)

    print(result)

    return result


def main():

    # blank test document
    #doc_id = "1hmt8JTuw783RSK7WJ5AmNiOZ7IaZYaPHcZ6XKc8QQxw"

    # menzies_bar_oos_test doc 
    
    doc_id = "1Iyy3ltWTNkEk45fP5rD7efiXG1kJlmTYehauf100DqY"

    # oos_btg_df ,low_btg_df , oos_btb_df ,low_btb_df = sheets_data_manip.stock_queries()

    # print_string = ""

    # for row_id, row in low_btb_df.iterrows():
    #     print_string = print_string + ("{} x {} {}\n\n".format(row["soh"], row["vintage"], row["name"]))

    service = docs_manip.service_getter()

    doc = service.documents().get(documentId=doc_id).execute()

    doc_content = doc["body"]["content"]
    
    start_idx, end_idx = docs_manip.section_idx_getter(doc_content, target_section = "LOW BTB")

    def content_text(content_idx):
        return doc_content[content_idx]["paragraph"]["elements"][0]["textRun"]["content"]

    for i in range(start_idx, end_idx):
        if not content_text(i).isspace():
            print(content_text(i).strip())
    
    #print(print_string)
        
    #print_to_doc(print_string)

    # TODO: figure out how to get the start and stop indexes for the sections. We need them for formatting, not text insertion. Mayhaps a regressive function which gets the endidx of the last wine on the insertion list to feed into the format request.

    # Priority for tomorrows shift is a restock script. for the sheet 'restock report' columns 'name' 'restock' 'restocked', take the values from 'restocked' and add them with the 'soh' values on the base sheet 'restock status'. To do this I will need to get the restock_status dataframe, another dataframe for the restock report, add the values of the two series together, then output back into the sheet, with correct formatting.

main()
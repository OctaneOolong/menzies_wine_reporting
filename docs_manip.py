from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']


def service_getter():
    """contacts the api and returns the document object as a nested dict.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_docs.json'):
        creds = Credentials.from_authorized_user_file('token_docs.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_docs.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_docs.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

    except HttpError as err:
        print(err)

    return service

def section_idx_getter(doc_content, target_section):

    heading_dict = {}

    # and if we copy the above loop, targeting the titles instead:

    for i in range(len(doc_content)):
        if "paragraph" in doc_content[i].keys() and "HEADING" in doc_content[i]["paragraph"]["paragraphStyle"]["namedStyleType"]:
            
            heading = doc_content[i]["paragraph"]["elements"][0]["textRun"]["content"].strip()
            
            heading_dict[heading] = i
            
            print("The following is the idx values of each heading in the document content list, not their start and stop indexes")

            print("{}".format(i) + " " + heading)

    target_section = "LOW BTB"

    start_idx = heading_dict[target_section]

    end_idx = heading_dict[
                        list(heading_dict.keys())
                            [
                                list(heading_dict.keys()).index(target_section)+1]
                                ]-1
    
    return start_idx, end_idx

def main():

    # menzies_bar_oos_test doc 
    
    doc_id = "1Iyy3ltWTNkEk45fP5rD7efiXG1kJlmTYehauf100DqY"
    
    service = service_getter()

    # Retrieve the documents contents from the Docs service.
    doc = service.documents().get(documentId=doc_id).execute()

    # The content list has a length of 98.

    doc_content = doc["body"]["content"]

    section_idx_getter(doc_content, target_section="LOW BTB")

    # for i in range(len(doc["body"]["content"])):
    #     print(i)
    #     print(doc["body"]["content"][i])
    #     ['paragraph']['elements'][0]['textRun']['content'])
    
    #print(doc["body"]["content"][-24]['paragraph']['elements'][0]['textRun']['content'])

    #doc["body"]["content"][-20]['paragraph']['elements'][0]['textRun']['content']="hello world!"

    

    # for i in range(10, len(doc["body"]["content"])):
    #     print(-i)
    #     print(doc["body"]["content"][-i]["paragraph"]['elements'][0]['textRun']['content'])

    # print(doc["body"]["content"][0])

    # Identify which items in the content list do not contain the paragraph field

    # for count, i in enumerate(content):
    #     if "paragraph" not in i.keys():
    #         print(count)
    #         print(i)

    # So items 0 and 9 specifically do not contain the "paragraph" field. Why? What does the 'content' field contain? We can understand this by observing the start and end indexes.

    # for i in range(2):
    #     print(i)
    #     print(json.dumps(content[i], indent=4))

    # The start and end indexes are as though all of the text characters (including whitespace) exist in a 1D array. Adding text to the end will increase the highest value of "endIndex". Inserting text in the middle will increase both the startIndex and endIndex for all items in the content list after the insertion point.

    # to find the section, we need to locate the headers. The headers are identified by the document.body.content.paragraph.paragraphStyle.namedStyleType field. The content of the headers is contained in the document.body.content.paragraph.elements[] list, and the start and end indexes can be found under document.body.content.startIndex and document.body.content.endIndex respectively. To find all the headers we can:

    # for i in range(len(content)):
    #     if "paragraph" in content[i].keys() and "HEADING" in content[i]["paragraph"]["paragraphStyle"]["namedStyleType"]:
    #         print(i)
    #         print(json.dumps(content[i], indent=4))

    # The below block of code constructs a list of the section heading strings, stripping them of whitespace characters. repr() is used to print white space characters.

    heading_dict = {}

    # and if we copy the above loop, targeting the titles instead:

    for i in range(len(doc_content)):
        if "paragraph" in doc_content[i].keys() and "HEADING" in doc_content[i]["paragraph"]["paragraphStyle"]["namedStyleType"]:
            
            heading = doc_content[i]["paragraph"]["elements"][0]["textRun"]["content"].strip()
            
            heading_dict[heading] = i

    #print(heading_dict)
    # To control the text of a section, we need to know where it starts and where it finishes. A section begins at the index of the content list the heading is in, and ends at i-1 of the title following. Assembling a dictionary with "title" "content_idx" could be the way to go:

    #print(section_dict)

    # now we want to use the dict ot get the content idx then iterate through the content list printing the textRun content of each line IF they are not whitespace, until the next heading.

    target_section = "LOW BTB"
    
    start_idx = heading_dict[target_section]

    # Because I cannot easily iterate through the dict by 1 advancement, the complicated expresion below converts the keys() to a list then gets the index of the target section and puts that back into the keys() list to move 1 item forward, then get the content index of that line. Since we actually want the line before, we will subtract 1 from that value.

    end_idx = heading_dict[
                            list(heading_dict.keys())
                                [
                                    list(heading_dict.keys()).index(target_section)+1]
                                    ]-1

    print(end_idx)

    # remembering that the accessor for the text is of the form content[content_idx]["paragraph"]["elements"][0]["textRun"]["content"]. To make it easier, define a short function to iterate through the content_idx position while leaving the rest of the accessors as a template:

    def content_text(content_idx):
        return doc_content[content_idx]["paragraph"]["elements"][0]["textRun"]["content"]

    for i in range(start_idx, end_idx):
        if not content_text(i).isspace():
            print(content_text(i).strip())

if __name__ == '__main__':
    main()
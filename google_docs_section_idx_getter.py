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
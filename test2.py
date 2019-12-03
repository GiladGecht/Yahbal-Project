from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from glob import glob
from helper import convert_date, text2int
import pandas as pd
import docx2txt
import os
import re
import io


def read_pdf(pdf_name):
    fp = open(pdf_name, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    full_text = ''
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                text = lobj.get_text()
                full_text += text

    print("Done parsing file\n")
    text = re.sub(" +", " ", re.sub(r"\n+", " ", full_text))
    return re.sub(r"\(cid:(.*?)\)", "", text)

def parse_pdf(pdf_name):
    text = read_pdf(pdf_name)
    print("Session held on: {}".format(convert_date(text.split(",")[1])))
    print("Session No.: {}".format(text2int(text.split(" session")[0].split(" ")[-1].lower())))
    print("Proceeding: {}".format(pdf_name.replace("_E.pdf", "")))

    session_dict = {"name_bank": [],
                    "name": [],
                    "country": [],
                    "position": [],
                    "speech": [],}




    split_lines = re.split(r"(The Co-Chairperson(\s\((.+?)\))?:|The President|The Acting President)", text)
    for i in range(len(split_lines)):
        try:
            if i != 0:
                if "last speaker" in split_lines[i]:
                    break
                split_by_title = re.split(r"(Judge |Highness |Mr\. |Honourable |Ms\. |Archbishop|Mrs\. |Majesty |Prince |Sir |Shaikh )", split_lines[i])
                if len(split_by_title[1:3]) == 0:
                    next
                else:
                    if set(split_by_title[2].split(",")[0].split(" ")) not in session_dict['name_bank']:
                        if ' '.join(split_by_title[1:3]).split(",")[0] not in session_dict['name']:
                            try:
                                name = ' '.join(split_by_title[1:3]).split(",")[0].replace(re.findall(r'cid:.{2,3}', ' '.join(split_by_title[1:3]).split(",")[0])[0], "").replace("()", "")
                                if set(name.split(" ")) not in session_dict['name_bank']:
                                    session_dict['name_bank'].append(set(name.split(" ")))
                                    session_dict['name'].append(name)
                                    session_dict['country'].append(
                                    split_by_title[2].split(",")[1].split(".")[0].split("of")[-1])
                                    session_dict['position'].append(split_by_title[2].split(",")[1].split(".")[0])
                                    print("Speaker: {}, Position: {}, Country: {}".format(name.split(" (")[0],
                                                                                          split_by_title[2].split(",")[1].split(".")[0],
                                                                                          split_by_title[2].split(",")[1].split(".")[0].split("of")[-1]))
                                else:
                                    next
                            except:
                                try:
                                    session_dict['name_bank'].append(set(split_by_title[2].split(",")[0].split(" ")))
                                except:
                                    session_dict['name_bank'].append(None)
                                try:
                                    session_dict['name'].append(' '.join(split_by_title[1:3]).split(",")[0])
                                except:
                                    session_dict['name'].append(None)
                                try:
                                    session_dict['country'].append(split_by_title[2].split(",")[1].split(".")[0].split("of")[-1])
                                except:
                                    session_dict['country'].append(None)
                                try:
                                    session_dict['position'].append(split_by_title[2].split(",")[1].split(".")[0])
                                except:
                                    session_dict['position'].append(None)
                                print("Speaker: {}, Position: {}, Country: {}".format(' '.join(split_by_title[1:3]).split(",")[0].split(" (")[0],
                                                                                      split_by_title[2].split(",")[1].split(".")[0],
                                                                                      split_by_title[2].split(",")[1].split(".")[0].split("of")[-1]))
                        else:
                            next
                    else:
                        next
        except:
            next


    print("\n")
    for i in range(len(session_dict['name'])):
        try:
            # check last name
            session_dict['speech'].append(re.split(r"{}(\s\((.+?)\))?:(.+?)(The Co-Chairperson(\s\((.+?)\))?:|The President|The Acting President)?:".format(session_dict['name'][i].split(" ")[-1][0].upper() + session_dict['name'][i].split(" ")[-1][1:]), text)[3])
        except:
            try:
                # check first name
                session_dict['speech'].append(re.split(r"{}(\s\((.+?)\))?:(.+?)(The Co-Chairperson(\s\((.+?)\))?:|The President|The Acting President)?:".format(session_dict['name'][i].split(" ")[2][0].upper() + session_dict['name'][i].split(" ")[2][1:]), text)[3])
            except:
                try:
                    # check multiple last names
                    session_dict['speech'].append(re.split(
                        r"{}(\s\((.+?)\))?:(.+?)(The Co-Chairperson(\s\((.+?)\))?:|The President|The Acting President)?:".format(
                            session_dict['name'][i].split(" ")[-2] + " "  +session_dict['name'][i].split(" ")[-1]), text)[3])
                except:
                    session_dict['speech'].append(None)


    session_dict = pd.DataFrame(session_dict)
    session_dict['proceeding'] = pdf_name.replace("_E.pdf", "")
    session_dict['date'] = convert_date(text.split(",")[1])
    session_dict['session'] = text2int(text.split(" session")[0].split(" ")[-1].lower())
    if len(session_dict['name_bank']) < 10:
        return session_dict, (text2int(text.split(" ")[4].lower()), len(session_dict['name_bank'])), True
    return session_dict, (text2int(text.split(" ")[4].lower()), len(session_dict['name_bank'])), False


if __name__ == "__main__":
    os.chdir(os.getcwd() + "\Data")
    pdf_files = glob('A_73*.pdf')
    pdf_files = ['A_73_PV.25_E.pdf']
    fault_files = []
    results = []
    temp_df = pd.DataFrame(columns=['name_bank', 'name', 'country', 'position', 'speech'])
    for i, file in enumerate(pdf_files):
        # if i == 4:
        #     break
        print("\nProcessing Session: {}".format(file))
        session_df, result, num_speakers = parse_pdf(file)
        temp_df = pd.concat((temp_df, session_df), axis=0, sort=False)
        if num_speakers:
            fault_files.append(file)
        results.append(result)


    os.chdir("..")
    temp_df.to_csv("sample2.csv", index=False)

print("Done")
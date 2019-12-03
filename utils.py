from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage

from fill_position import find_speaker_position
from fill_speech import find_speaker_speech
import pandas as pd
import os
import re


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
                text =  lobj.get_text()
                full_text += text

    print("Done parsing file\n")
    return re.sub(" +", " ", re.sub(r"\n+", " ", full_text.lower())), re.sub(" +", " ", re.sub(r"\n+", " ", full_text))



def parse_pdf(pdf_name, names, proceeding, speakers_df):
    text, upper_case_text = read_pdf(pdf_name)
    names = [name.lower() for name in names]


    for name in names:
        name_order = {"speech": []}
        original_name = name
        # try:
        if '-' in name:
            name = name.split("-")[1]
        elif ' ' in name:
            name = name.split(" ")[1]
        else:
            pass
        country = speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'country'].values[0]
        speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = find_speaker_position(name, text, speakers_df, proceeding, original_name, upper_case_text)


        print("Name: {}".format(name))
        find_speaker_speech(name, text, name_order, country, proceeding)
        # try:
        #     if name not in text:
        #         try:
        #             speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(name[:3]), text)[6]
        #             name_order['speech'].append(speech)
        #             speech = pd.DataFrame(name_order)
        #             speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #             next
        #         except:
        #             name_order['speech'].append(None)
        #             speech = pd.DataFrame(name_order)
        #             speech.to_json(os.getcwd() + '\\speeches\\' + 'bug_{}_{}_{}.json'.format(country, name, proceeding))
        #     else:
        #         speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(name), text)[5]
        #         name_order['speech'].append(speech)
        #         speech = pd.DataFrame(name_order)
        #         speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #         next
        # except:
        #     try:
        #         if name not in text:
        #             try:
        #                 speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)'.format(name[:3]), text)[6]
        #                 name_order['speech'].append(speech)
        #                 speech = pd.DataFrame(name_order)
        #                 speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                 next
        #             except:
        #                 pass
        #         else:
        #             speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)'.format(name), text)[6]
        #             name_order['speech'].append(speech)
        #             speech = pd.DataFrame(name_order)
        #             speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #             next
        #     except:
        #         try:
        #             if name not in text:
        #                 try:
        #                     speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)+'.format(name[:3]), text)[6]
        #                     name_order['speech'].append(speech)
        #                     speech = pd.DataFrame(name_order)
        #                     speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                     next
        #                 except:
        #                     pass
        #             else:
        #                 speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)+'.format(name), text)[6]
        #                 name_order['speech'].append(speech)
        #                 speech = pd.DataFrame(name_order)
        #                 speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                 next
        #         except:
        #
        #             try:
        #                 if name not in text:
        #                     try:
        #                         speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(name[:3]), text)[6]
        #                         name_order['speech'].append(speech)
        #                         speech = pd.DataFrame(name_order)
        #                         speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                         next
        #                     except:
        #                         pass
        #                 else:
        #                     speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(name), text)[5]
        #                     name_order['speech'].append(speech)
        #                     speech = pd.DataFrame(name_order)
        #                     speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                     next
        #             except:
        #                 try:
        #                     if name not in text:
        #                         try:
        #                             # if there are more names after the known name
        #                             speech = re.split(
        #                                 r'{}(.{{1,10}})((\s(.+?)){1,3})?(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?: | the acting president(\s\((.+?)\))?:)'.format(name), text)[6]
        #                             name_order['speech'].append(speech)
        #                             speech = pd.DataFrame(name_order)
        #                             speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                         except:
        #                             pass
        #                     else:
        #                         # if there are more names after the known name
        #                         speech = re.split(r'{}((\s(.+?)){1,3})?(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?: | the acting president(\s\((.+?)\))?:)'.format(name), text)[5]
        #                         name_order['speech'].append(speech)
        #                         speech = pd.DataFrame(name_order)
        #                         speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
        #                 except:
        #                     print("Failed - Name:{}".format(name))
        #                     name_order['speech'].append(None)
        #                     speech = pd.DataFrame(name_order)
        #                     speech.to_json(os.getcwd() + '\\speeches\\' + 'bug_{}_{}_{}.json'.format(country, name, proceeding))


# speakers_df.loc[speakers_df['proceeding'] == proceeding + '_E', ['position', 'surname']]
    return pd.DataFrame(name_order), speakers_df.loc[speakers_df['proceeding'] == proceeding + '_E']
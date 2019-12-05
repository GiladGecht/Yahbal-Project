from pathlib import Path
from fill_position import find_speaker_position
from fill_speech import find_speaker_speech
import pandas as pd
import unicodedata
import os
import re


def read_pdf(pdf_name):
    with open(pdf_name, "rb") as pdf:
        text = pdf.read().decode('utf-8')

    processed_text = ""
    for word in text.split():
        word = ''.join(char for char in
                       unicodedata.normalize('NFKD', word)
                       if unicodedata.category(char) != 'Mn')

        processed_text += ' ' + word
    upper_case_text = re.sub(" +", " ", re.sub(r"\n+", " ", processed_text))
    text = re.sub(" +", " ", re.sub(r"\n+", " ", processed_text.lower()))
    text = text.replace(r"\r\n", "").replace("’", "")

    return text, re.sub(" +", " ", upper_case_text)




def parse_pdf(pdf_name, names, proceeding, speakers_df, year):
    text, upper_case_text = read_pdf(pdf_name)
    names = [name.lower() for name in names]
    try:
        os.mkdir(Path("Data/speeches/" + year))
    except:
        pass

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

        if '\'' in name:
            name = name.replace("\'", "")
        name = ''.join(char for char in unicodedata.normalize('NFKD', name) if unicodedata.category(char) != 'Mn')

        country = speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'country'].values[0]
        speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = find_speaker_position(name, text, speakers_df, proceeding, original_name, upper_case_text)

        print("Name: {}".format(name))
        find_speaker_speech(name, text, name_order, country, proceeding, year)

    return pd.DataFrame(name_order), speakers_df.loc[speakers_df['proceeding'] == proceeding + '_E']


def load_data():
    try:
        print("Loading Data...")
        speakers_df = pd.read_csv(Path('Data/speakers.csv'))
        speakers_df['position'] = None
        print("Finished Loading Data...")

        return speakers_df
    except:
        print("Folder not found\nCreating one...")
        os.mkdir(Path("Data"))
        os.mkdir(Path("Data/speeches"))


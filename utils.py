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

    processed_text = []
    for word in text.split():
        word = ''.join(char for char in
                       unicodedata.normalize('NFKD', word)
                       if unicodedata.category(char) != 'Mn')

        processed_text.append(word)
    processed_text = ' '.join(processed_text)
    upper_case_text = re.sub(" +", " ", re.sub(r"\n+", " ", processed_text))
    text = re.sub(" +", " ", re.sub(r"\n+", " ", processed_text))
    text = text.replace(r"\r\n", "").replace("’", "")
    text = re.sub(r"\w\/\d{2}\/PV\.\d{2}", "", text)
    text = re.sub(r"([0-9]{0,2}|[\w])\/[0-9]{0,4}(\/[0-9]{0,4}|PV\.[0-9]})?", "", text)
    text = re.sub(r"\(E\)\*\d{7}\*", "", text)
    text = re.sub(r"\d{1,2}-\d{5}", "", text)
    text = re.sub(r"PV.\d{1,2}", "", text)
    text = re.sub(" +", " ", re.sub(r"\n+", " ", text))

    return text, re.sub(" +", " ", upper_case_text)


def parse_pdf(pdf_name, names, proceeding, speakers_df, year, partial_df):
    text, upper_case_text = read_pdf(pdf_name)
    try:
        os.mkdir(Path("Data/speeches/" + year))
    except:
        pass

    for name in names:
        full_name = partial_df.loc[partial_df['speaker_surname'] == name, 'speaker_name'].values[0]
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
            name    = name.replace("\'", "")
            name    = list(name)
            name[1] = name[1].lower()
            name    = ''.join(name)

        full_name = ''.join(char for char in unicodedata.normalize('NFKD', full_name) if unicodedata.category(char) != 'Mn')
        name = ''.join(char for char in unicodedata.normalize('NFKD', name) if unicodedata.category(char) != 'Mn')

        country = speakers_df.loc[(speakers_df['speaker_surname']== original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'country_code'].values[0]
        speakers_df.loc[(speakers_df['speaker_surname']== original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = find_speaker_position(name, text, speakers_df, proceeding, original_name, full_name)

        print("Name: {}".format(name))
        find_speaker_speech(name, text, name_order, country, proceeding, year, full_name)

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


import re
import logging
import pandas as pd

import numpy as np
from glob import glob
from tqdm import tqdm
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

logging.basicConfig(filename='compare.log', level=logging.DEBUG)
HARVARD                 = Path('Data/Converted sessions/')
GILAD                   = Path('Data/speeches/')
df                      = pd.read_csv(Path('Data/speakers_1992_2017.csv'))
df                      = df[~(df['position'] == "MISSING")].reset_index(drop=True)
df['similarity_score']  = 0
df['word_count_diff']   = 0


def is_in_speeches(speeches, name):
    return name in speeches


for YEAR in range(1992, 2018):
    harvard_speeches = pd.Series(glob(str(HARVARD) + '\Session {} - {}'.format(YEAR - 1945, YEAR) + '\*.txt'))
    gilad_speeches = pd.Series(glob(str(GILAD) + '\{}'.format(YEAR) + '\*.json'))

    for speech in tqdm(harvard_speeches):
        FLAG = False
        try:
            country = speech.split('\\')[-1].split("_")[0]
            name = df[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR)))]['speaker_surname'].values[
                0]
            iso_speeches = np.array([speech.split("\\")[-1].split("_")[0] for speech in gilad_speeches])

            if "bug" in gilad_speeches[gilad_speeches.str.contains(country) == True].values[0]:
                df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'similarity_score'] = "BUG"
                df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'word_count_diff'] = "BUG"
                continue
            try:
                country_index = np.where(iso_speeches == country)[0][0]
            except:
                df.loc[
                    (df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'similarity_score'] = None
                df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'word_count_diff'] = None
                continue

            json_speech = gilad_speeches[country_index]

            if len(json_speech) == 0:
                df.loc[
                    (df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'similarity_score'] = None
                df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'word_count_diff'] = None
                continue
            else:
                FLAG = True
                try:
                    with open(json_speech, 'r', encoding='utf-8') as f:
                        data = f.read()
                    with open(speech, 'r', encoding='utf-8') as f:
                        harvard_data = f.read()

                    harvard_data      = re.sub(" +", " ", re.sub(r"\n+", " ", harvard_data))
                    documents         = [harvard_data, eval(data)['speech']['0']]
                    vectorizer        = CountVectorizer()
                    matrix            = vectorizer.fit_transform(documents).toarray()
                    tfidf_vectorizer  = TfidfTransformer()
                    tf_matrix         = tfidf_vectorizer.fit_transform(matrix)
                    sim_score         = (tf_matrix * tf_matrix.T).toarray()[0, 1]
                    num_gilad_words   = len(eval(data)['speech']['0'].split())
                    num_harvard_words = len(harvard_data.split())
                    proceeding        = '_'.join(json_speech[0].split('\\')[-1].split('_')[2:]).split('.json')[0] + '_E'

                    df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'similarity_score'] = sim_score
                    df.loc[(df['country_code'] == country) & (df['date'].str.contains(str(YEAR))), 'word_count_diff'] = num_gilad_words - num_harvard_words
                except Exception as e:
                    logging.debug(f"Country: {country}, Speech: {speech}")
                if not FLAG:
                    print("################## FAILED ##################")
                    print(name, json_speech[0])
                    print("------------------------------------------------------------------")

        except Exception as e:
            logging.debug(f"Country: {country}, Speech: {speech}")

df.to_csv(Path('Data/validated_speakers_1992_2017.csv'), index=False)

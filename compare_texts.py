import os
import re
from glob import glob
from pathlib import Path

import pandas as pd
import pycountry
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

HARVARD = Path('Data/Converted sessions/')
GILAD = Path('Data/speeches/')
df = pd.read_csv(Path('Data/speakers_working.csv'))
df['similarity_score'] = 0
df['word_count_diff'] = 0

for YEAR in range(2010, 2018):
    harvard_speeches = glob(str(HARVARD) + '\Session {} - {}'.format(YEAR-1945, YEAR) +'\*.txt')
    gilad_speeches   = glob(str(GILAD) + '\{}'.format(YEAR) +'\*.json')

    for speech in harvard_speeches:
        FLAG = False
        try:
            country = speech.split('\\')[-1].split("_")[0]
            # country_name = pycountry.countries.get(alpha_3=country).name.split(',')[0]
            for json_speech in gilad_speeches:
                good_speeches = []
                if country in json_speech:
                    good_speeches.append(json_speech)



            FLAG = True
            try:
                # if country_name == 'Sudan':
                #     print(country)
                with open(json_speech, 'r', encoding='utf-8') as f:
                    data = f.read()
                with open (speech, 'r', encoding='utf-8') as f:
                    harvard_data = f.read()

                harvard_data     = re.sub(" +", " ", re.sub(r"\n+", " ", harvard_data))
                documents        = [harvard_data, eval(data)['speech']['0']]
                vectorizer       = CountVectorizer()
                matrix           = vectorizer.fit_transform(documents).toarray()
                tfidf_vectorizer = TfidfTransformer()
                tf_matrix        = tfidf_vectorizer.fit_transform(matrix)

                sim_score = (tf_matrix*tf_matrix.T).toarray()[0, 1]

                num_gilad_words = len(eval(data)['speech']['0'].split())
                num_harvard_words = len(harvard_data.split())
                proceeding = '_'.join(json_speech.split('\\')[-1].split('_')[2:]).split('.json')[0] + '_E'
                name = json_speech.split('\\')[-1].split('_')[1]
                df.loc[(df['speaker_surname'] == name) & (df['proceeding'] == proceeding), 'similarity_score'] = sim_score
                df.loc[(df['speaker_surname'] == name) & (df['proceeding'] == proceeding), 'word_count_diff'] = num_gilad_words - num_harvard_words
                # print(sim_score)
                # print("------------------------------------------------------------------")
            except Exception as e:
                print(e)
                break
            if not FLAG:
                print("################## FAILED ##################")
                print(name, json_speech)
                print("------------------------------------------------------------------")

        except Exception as e:
            print(e, speech)

df.to_csv(Path('Data/validated_speakers1.csv'), index=False)
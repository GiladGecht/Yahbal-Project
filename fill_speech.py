import re
from pathlib import Path
import pandas as pd


def find_speaker_speech(name, text, name_order, country, proceeding, year):
    try:
        if name not in text:
            try:
                # if the name has non-english letters check only part of the name
                speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\)){{0,3}}\s?:(.+?)(The President(\s\((.+?)\)){{0,3}}\s?:|The Acting President(\s\((.+?)\)){{0,3}}\s?:|\.\s?The meeting rose)'.format(name[:3]), text)[4]
                # speech = ' '.join([x.encode('utf-8').decode() for x in speech.split()])
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                    speech.to_json(file, force_ascii=False)
                # speech.to_json(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)))
            except:
                name_order['speech'].append(None)
                speech = pd.DataFrame(name_order)
                with open(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                    speech.to_json(file, force_ascii=False)
                next
        else:
            speech = re.split(r'{}(\s\w+\s?){{0,2}}(\s\((.+?)\)){{0,3}}\s?:(.+?)(The President(\s\((.+?)\))?\s?:|The Acting President(\s\((.+?)\))?\s?:|\.\s?The meeting rose)'.format(name), text)[4]
            # speech = ' '.join([x.encode('utf-8').decode() for x in speech.split()])
            name_order['speech'].append(speech)
            speech = pd.DataFrame(name_order)
            with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                speech.to_json(file, force_ascii=False)
    except:
        name_order['speech'].append(None)
        speech = pd.DataFrame(name_order)
        with open(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
            speech.to_json(file, force_ascii=False)
        # speech.to_json(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)))
        next

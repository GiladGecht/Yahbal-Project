import re
from pathlib import Path
import pandas as pd

def find_speaker_speech(name, text, name_order, country, proceeding, year):
    try:
        if name not in text:
            try:
                # if the name has non-english letters check only part of the name
                speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\)){{0,3}}\s?:(.+?)(the president(\s\((.+?)\)){{0,3}}\s?:|the acting president(\s\((.+?)\)){{0,3}}\s?:|\.\s?the meeting rose)'.format(name[:3]), text)[4]
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                speech.to_json(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)))
            except:
                name_order['speech'].append(None)
                speech = pd.DataFrame(name_order)
                speech.to_json(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)))
                next
        else:
            speech = re.split(r'{}(\s\w+\s?){{0,2}}(\s\((.+?)\)){{0,3}}\s?:(.+?)(the president(\s\((.+?)\))?\s?:|the acting president(\s\((.+?)\))?\s?:|\.\s?the meeting rose)'.format(name), text)[4]
            name_order['speech'].append(speech)
            speech = pd.DataFrame(name_order)
            speech.to_json(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)))
    except:
        name_order['speech'].append(None)
        speech = pd.DataFrame(name_order)
        speech.to_json(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)))
        next

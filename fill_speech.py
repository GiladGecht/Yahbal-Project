import re
from pathlib import Path
import pandas as pd


def find_speaker_speech(name, text, name_order, country, proceeding, year, full_name):
    try:
        if name not in text:
            try:
                # if the name has non-english letters check only part of the name
                speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\)){{0,7}}\s?:(.+?)(The President(\s\((.+?)\)){{0,7}}\s?:|The Acting President(\s\((.+?)\)){{0,7}}\s?:|\.\s?The meeting rose)'.format(name[:3]), text)[4]
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                    speech.to_json(file, force_ascii=False)
            except:
                for partial_name in range(len(full_name.split())):
                    try:
                        speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\)){{0,7}}\s?:(.+?)(The President(\s\((.+?)\)){{0,7}}\s?:|The Acting President(\s\((.+?)\)){{0,7}}\s?:|\.\s?The meeting rose)'.format(full_name.split()[partial_name][:4]), text)[4]
                        name_order['speech'].append(speech)
                        speech = pd.DataFrame(name_order)
                        with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                            speech.to_json(file, force_ascii=False)
                        break
                    except:
                        if partial_name == len(full_name.split()) - 1:
                            name_order['speech'].append(None)
                            speech = pd.DataFrame(name_order)
                            with open(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                                speech.to_json(file, force_ascii=False)
                        next

        else:
            speech = re.split(r'{}(\s\w+\s?){{0,7}}(\s\((.+?)\)){{0,7}}\s?:(.+?)(The President(\s\((.+?)\))?\s?:|The Acting President(\s\((.+?)\))?\s?:|\.\s?The meeting rose)'.format(name), text)[4]
            name_order['speech'].append(speech)
            speech = pd.DataFrame(name_order)
            with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                speech.to_json(file, force_ascii=False)

    except:
        for partial_name in range(len(full_name.split())):
            try:
                speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\)){{0,7}}\s?:(.+?)(The President(\s\((.+?)\)){{0,7}}\s?:|The Acting President(\s\((.+?)\)){{0,7}}\s?:|\.\s?The meeting rose)'.format(full_name.split()[partial_name][:4]), text)[4]
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                with open(Path("Data/speeches/" + year + "/{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                    speech.to_json(file, force_ascii=False)
                break
            except:
                if partial_name == len(full_name.split()) - 1:
                    name_order['speech'].append(None)
                    speech = pd.DataFrame(name_order)
                    with open(Path("Data/speeches/" + year + "/bug_{}_{}_{}.json".format(country, name, proceeding)), 'w', encoding='utf-8') as file:
                        speech.to_json(file, force_ascii=False)
                else:
                    next


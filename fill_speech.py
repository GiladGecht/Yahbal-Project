import os
import re
import pandas as pd


def find_speaker_speech(name, text, name_order, country, proceeding):
    try:
        if name not in text:
            try:
                speech = re.split(
                    r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(
                        name[:3]), text)[6]
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                next
            except:
                name_order['speech'].append(None)
                speech = pd.DataFrame(name_order)
                speech.to_json(os.getcwd() + '\\speeches\\' + 'bug_{}_{}_{}.json'.format(country, name, proceeding))
        else:
            speech = re.split(
                r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(
                    name), text)[5]
            name_order['speech'].append(speech)
            speech = pd.DataFrame(name_order)
            speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
            next
    except:
        try:
            if name not in text:
                try:
                    speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)'.format(name[:3]), text)[6]
                    name_order['speech'].append(speech)
                    speech = pd.DataFrame(name_order)
                    speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                    next
                except:
                    pass
            else:
                speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)'.format(name), text)[6]
                name_order['speech'].append(speech)
                speech = pd.DataFrame(name_order)
                speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                next
        except:
            try:
                if name not in text:
                    try:
                        speech = re.split(r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)+'.format(name[:3]), text)[6]
                        name_order['speech'].append(speech)
                        speech = pd.DataFrame(name_order)
                        speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                        next
                    except:
                        pass
                else:
                    speech = re.split(r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)+'.format(name), text)[6]
                    name_order['speech'].append(speech)
                    speech = pd.DataFrame(name_order)
                    speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                    next
            except:

                try:
                    if name not in text:
                        try:
                            speech = re.split(
                                r'{}(.{{1,10}})(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(
                                    name[:3]), text)[6]
                            name_order['speech'].append(speech)
                            speech = pd.DataFrame(name_order)
                            speech.to_json(
                                os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                            next
                        except:
                            pass
                    else:
                        speech = re.split(
                            r'{}(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?:|the acting president(\s\((.+?)\))?:)'.format(
                                name), text)[5]
                        name_order['speech'].append(speech)
                        speech = pd.DataFrame(name_order)
                        speech.to_json(os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                        next
                except:
                    try:
                        if name not in text:
                            try:
                                # if there are more names after the known name
                                speech = re.split(
                                    r'{}(.{{1,10}})((\s(.+?)){1,3})?(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?: | the acting president(\s\((.+?)\))?:)'.format(
                                        name), text)[6]
                                name_order['speech'].append(speech)
                                speech = pd.DataFrame(name_order)
                                speech.to_json(
                                    os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                            except:
                                pass
                        else:
                            # if there are more names after the known name
                            speech = re.split(
                                r'{}((\s(.+?)){1,3})?(\s\((.+?)\))?(\s\((.+?)\))?:(.+?)(the president(\s\((.+?)\))?: | the acting president(\s\((.+?)\))?:)'.format(
                                    name), text)[5]
                            name_order['speech'].append(speech)
                            speech = pd.DataFrame(name_order)
                            speech.to_json(
                                os.getcwd() + '\\speeches\\' + '{}_{}_{}.json'.format(country, name, proceeding))
                    except:
                        print("Failed - Name:{}".format(name))
                        name_order['speech'].append(None)
                        speech = pd.DataFrame(name_order)
                        speech.to_json(
                            os.getcwd() + '\\speeches\\' + 'bug_{}_{}_{}.json'.format(country, name, proceeding))
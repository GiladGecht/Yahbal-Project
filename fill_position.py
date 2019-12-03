import re


def find_speaker_position(name, text, speakers_df, proceeding, original_name, upper_case_text):
    try:
        if name not in text:
            try:
                speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(The Acting President|The President|\.)', upper_case_text.split('{}'.format(name[0].upper() + name[1:4]))[1])[0]
            except:
                pass
        else:
            speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(The Acting President|The President|\.)', upper_case_text.split('{}'.format(name[0].upper() + name[1:]))[1])[0]
            # print("Made in 1: {}".format(name))
    except:
        # currently for names cant be found like vucic or kabore
        print("Could not find position - {}".format(name))

        try:
            if name not in text:
                try:
                    speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(The Acting President|The President|\.)', upper_case_text.split('{},'.format(name[0].upper() + name[1:4]))[1])[0].split(",")[0]
                except:
                    pass
            else:
                speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(The Acting President|The President|\.)', upper_case_text.split('{},'.format(name[0].upper() + name[1:]))[1])[0].split(",")[0]
                # print("Made in 2: {}".format(name))
        except:
            print("Could not find position - {}".format(name))

            try:
                if name not in text:
                    try:
                        speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(the acting president|the president|\.)', text.split('{}'.format(name[:4]))[1])[0]
                    except:
                        pass
                else:
                    speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = re.split(r'(the acting president|the president|\.)', text.split('{}'.format(name))[1])[0]
                    # print("Made in 3: {}".format(name))
            except:
                print("Could not find position - {}".format(name))
                pass

    return speakers_df.loc[(speakers_df['surname'].str.lower() == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']
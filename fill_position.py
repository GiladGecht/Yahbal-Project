import re

# re.split(r'(The Acting President|The President|\.)', text.split('{}'.format(name[0].upper() + name[1:4]))[1])[0].split(", ")[1]

# first = re.search(r"{}(\s?\w+-?\s?){{0,9}},(\s?\w+){{0,9}},".format(name), text).regs[0][0]
# second = re.search(r"{}(\s?\w+-?\s?){{0,9}},(\s?\w+){{0,9}},".format(name), text).regs[0][1]
# text[first:second].split(",")[1][1:]




def find_speaker_position(name, text, speakers_df, proceeding, original_name, full_name):
    try:
        if name not in text:
            try:
                pos = re.search(r"{}(\s?\w+-?\s?){{0,5}}(?=,)(.+?)(?=(The President|The Acting President|,)))".format(name[:3]), text)
                if pos == None:
                    pos = re.search(r"{}(\s?\w+-?\s?){{0,5}},(\s?\w+){{0,9}}(\.?\s?),".format(name[:3]), text).group().split(", ")[1].split(",")[0]
                else:
                    pos = pos.group().split(", ")[1].split("The")[0]

                # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = pos
                return pos #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

            except:
                for partial_name in range(len(full_name.split())):
                    try:
                        pos = re.search(r"{}(\s?\w+-?\s?){{0,5}}(?=,)(.+?)(?=(The President|The Acting President|,))".format(full_name.split()[partial_name][:4]), text)
                        if pos == None:
                            pos = re.search(r"{}(\s?\w+-?\s?){{0,5}},(\s?\w+){{0,9}}(\.?\s?),".format(full_name.split()[partial_name][:4]), text).group().split(", ")[1].split(",")[0]
                        else:
                            pos = pos.group().split(", ")[1].split("The")[0]

                        # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = pos
                        return pos #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

                    except:
                        # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = None
                        return None #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

        else:
            try:
                pos = re.search(r"{}(\s?\w+-?\s?){{0,5}}(?=,)(.+?)(?=(The President|The Acting President|,))".format(name), text)
                if pos == None:
                    pos = re.search(r"{}(\s?\w+-?\s?){{0,5}},(\s?\w+){{0,9}}(\.?\s?),".format(name), text).group().split(", ")[1].split(",")[0]
                else:
                    pos = pos.group().split(", ")[1].split("The")[0]

                # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = pos
                return pos #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

            except:
                for partial_name in range(len(full_name.split())):
                    try:
                        pos = re.search(r"{}(\s?\w+-?\s?){{0,5}}(?=,)(.+?)(?=(The President|The Acting President|,))".format(full_name.split()[partial_name][:4]), text)
                        if pos == None:
                            pos = re.search(r"{}(\s?\w+-?\s?){{0,5}},(\s?\w+){{0,9}}(\.?\s?),".format(full_name.split()[partial_name][:4]), text).group().split(", ")[1].split(",")[0]
                        else:
                            pos = pos.group().split(", ")[1].split("The")[0]
                        # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = pos
                        return pos # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

                    except:
                        # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = None
                        return None #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']

    except:
        # speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position'] = None
        return None #speakers_df.loc[(speakers_df['surname'] == original_name) & (speakers_df['proceeding'] == proceeding + '_E'), 'position']


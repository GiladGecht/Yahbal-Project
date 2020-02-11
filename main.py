"""

#### YAHBAL PROJECT ####

__Author__: Gilad Gecht


"""
from utils import parse_pdf, load_data
from pathlib import Path
import pandas as pd
import warnings
import argparse
import json
warnings.simplefilter("ignore")

# parser = argparse.ArgumentParser()
# parser.add_argument("year", help="The year you wish to extract speeches from")
# parser.add_argument("lower_bound", help="the proceeding's number to start from", nargs="?", const=1, type=int, default=0)
# parser.add_argument("upper_bound", help="the final proceeding's number", nargs="?", const=1, type=int, default=100)
#
# args        = parser.parse_args()
# YEAR        = args.year
# UPPER_BOUND = args.upper_bound
# LOWER_BOUND = args.lower_bound


# For debugging use
# YEAR        = "2015"
# LOWER_BOUND = 13
# UPPER_BOUND = 28

if __name__ == "__main__":

    entire_df = pd.DataFrame()
    with open('config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for YEAR in data:
        if int(YEAR) >= 0 and int(YEAR) <= 3000:
            print("# ============== CURRENTLY HANDLING YEAR: {} ============== #".format(YEAR))
            LOWER_BOUND = data[YEAR][0]
            UPPER_BOUND = data[YEAR][1]
            yearly_df   = pd.DataFrame()
            speakers_df = load_data()
            data_folder = Path('Data/new_texts')
            pdf_files   = data_folder.glob("*.txt")
            for file in pdf_files:
                try:
                    proceeding = str(file).split("E")[0].split("\\")[-1][:-1]
                    proceeding_number = proceeding.split("_")[1]
                    if proceeding_number == str(int(YEAR) - 1945):
                        if (int(proceeding.split(".")[-1]) >= LOWER_BOUND) and (int(proceeding.split(".")[-1]) <= UPPER_BOUND):
                            print("\nProcessing Session: {}".format(file))
                            names = speakers_df[speakers_df['proceeding'] == proceeding + "_E"]['speaker_surname'].value_counts().index
                            full_names = speakers_df[speakers_df['proceeding'] == proceeding + "_E"]['speaker_name'].value_counts().index
                            partial_df = speakers_df[speakers_df['proceeding'] == proceeding + "_E"]
                            session_df, updated_position_df = parse_pdf(file, names, proceeding, speakers_df, YEAR, partial_df)
                            yearly_df = pd.concat((yearly_df, updated_position_df), axis=0)
                            # yearly_df.to_csv(Path("Data/speeches/" + YEAR + '/{}.csv'.format(YEAR), index=False))


                except Exception as e:
                    print(e)
                    print("Could not find: {}".format(file))
            # entire_df.to_csv(Path('Data/speakers_1992_2017.csv'.format()), index=False)
            entire_df = pd.concat((entire_df, yearly_df), axis=0)
            yearly_df.to_csv(Path("Data/speeches/" + YEAR + '/{}.csv'.format(YEAR), index=False))

    entire_df.to_csv(Path('Data/speakers_1992_2017.csv'.format()), index=False)

    print("Done")


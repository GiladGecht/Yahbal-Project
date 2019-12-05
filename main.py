"""

#### YAHBAL PROJECT ####

__Author__: Gilad Gecht


"""
from utils import parse_pdf, load_data
from pathlib import Path
import pandas as pd
import warnings
import argparse

warnings.simplefilter("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("year", help="The year you wish to extract speeches from")
parser.add_argument("lower_bound", help="the proceeding's number to start from", nargs="?", const=1, type=int, default=0)
parser.add_argument("upper_bound", help="the final proceeding's number", nargs="?", const=1, type=int, default=100)

args        = parser.parse_args()
YEAR        = args.year
UPPER_BOUND = args.upper_bound
LOWER_BOUND = args.lower_bound


# For debugging use
# YEAR = "2017"
# UPPER_BOUND = 100
# LOWER_BOUND = 0

if __name__ == "__main__":

    yearly_df   = pd.DataFrame()
    speakers_df = load_data()
    data_folder = Path('Data/texts')
    pdf_files   = data_folder.glob("*.json")

    for file in pdf_files:
        try:
            proceeding = str(file).split("E")[0].split("\\")[-1][:-1]
            proceeding_number = proceeding.split("_")[1]
            if proceeding_number == str(int(YEAR) - 1945):
                if (int(proceeding.split(".")[-1]) >= LOWER_BOUND) and (int(proceeding.split(".")[-1]) <= UPPER_BOUND):
                    print("\nProcessing Session: {}".format(file))
                    names = speakers_df[speakers_df['proceeding'] == proceeding + "_E"]['surname'].value_counts().index
                    partial_df = speakers_df[speakers_df['proceeding'] == proceeding + "_E"]
                    session_df, updated_position_df = parse_pdf(file, names, proceeding, speakers_df, YEAR)
                    yearly_df = pd.concat((yearly_df, updated_position_df), axis=0)

        except Exception as e:
            print(e)
            print("Could not find: {}".format(file))
    yearly_df.to_csv(Path("Data/speeches/" + YEAR + '/{}.csv'.format(YEAR), index=False))
    print("Done")


"""

#### YAHBAL PROJECT ####

__Author__: Gilad Gecht


"""
from utils import parse_pdf
from glob import glob
import pandas as pd
import os

if __name__ == "__main__":
    num_names = 0
    yearly_df = pd.DataFrame()
    speakers_df = pd.read_csv('speakers.csv')
    speakers_df['position'] = None
    os.chdir(os.getcwd() + "\Data")
    pdf_files = glob("*.pdf")
    fault_files = []
    results = []
    for file in pdf_files:
        try:
            proceeding = file.split("E")[0][:-1]
            proceeding_number = proceeding.split("_")[1]
            if proceeding_number == '72':
                print("\nProcessing Session: {}".format(file))
                names = speakers_df[speakers_df['proceeding'] == file.replace(".pdf", "")]['surname'].value_counts().index
                num_names += len(names)
                partial_df = speakers_df[speakers_df['proceeding'] == file.replace(".pdf", "")]
                session_df, updated_position_df = parse_pdf(file, names, proceeding, speakers_df)
                yearly_df = pd.concat((yearly_df, updated_position_df), axis=0)

        except Exception as e:
            print(e)
            print("Could not find: {}".format(file))
    # yearly_df.to_csv('2017.csv', index=False)
    print("Total Amount of speakers: {}".format(num_names))
    print("Done")
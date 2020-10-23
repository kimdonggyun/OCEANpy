# handle CTD data

import pandas as pd
from tkinter.filedialog import askdirectory
from tkinter import Tk
import glob, os


def find_start_row (file_path, string):
    with open(file_path, 'r') as df:
        index = 0
        for line in df:
            if string in line:
                return index
            index += 1


def raw_ctd_to_df (file_path):
    start_index = find_start_row(file_path, 'NOBS [#]')
    df = pd.read_csv(file_path, sep='\t', skiprows=start_index)
    return df


if __name__ == "__main__":

    Tk().withdraw()
    print('choose project directory')
    path_to_data = askdirectory()

    for file_path in glob.glob(path_to_data+os.sep+'CTD*.tsv'):
        raw_ctd_to_df(file_path)

    
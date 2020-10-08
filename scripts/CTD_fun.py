# handle CTD data

import pandas as pd
from tkinter.filedialog import askdirectory
from tkinter import Tk
import glob, os


def raw_ctd_to_df (file_path):
    pass

if __name__ == "__main__":

    Tk().withdraw()
    print('choose project directory')
    path_to_data = askdirectory()

    for file_path in glob.glob(path_to_data+os.sep+'CTD*.tsv'):
        print(file_path)

    
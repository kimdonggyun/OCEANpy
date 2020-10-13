# this file was created to handle processed ISC data

import os, glob
import pandas as pd
import numpy as np
from pandas import read_excel
from pathlib import Path
from matplotlib import pyplot as plt

def vertical_plot (df, title):
    print(title)
    depth = tuple(df['Depths (m)'])
    temp = tuple(df['Temperature (dC)'])
    sal = tuple(df['Salinity (PSU)'])
    turb = tuple(df['Turbidity (NTU)'])
    fluo = tuple(df['Fluorescence (mg/m3)'])
    aggr_vol = tuple(df['Total Aggregate Volume (ppm)'])
    aggr_abund = tuple(df['Aggregate abundance (#/l)'])
    median_esd = tuple(df['Median ESD (µm)'])
    average_esd = tuple(df['Average ESD (µm)'])

    fig, axs = plt.subplots(2,2, figsize = (10, 10))
    axs = axs.ravel()

    unit_dict = {'depth': 'Depths (m)', 'temp': 'Temperature (dC)', 'sal': 'Salinity (PSU)', 'turb': 'Turbidity (NTU)',
                    'fluo': 'Fluorescence (mg/m3)', 'aggr_vol': 'Total Aggregate Volume (ppm)', 'aggr_abund': 'Aggregate abundance (#/l)',
                    'median_esd': 'Median ESD (µm)', 'average_esd':'Average ESD (µm)'}

    # 1st plot for temperature and salanity
    axs[0].plot(temp, depth, color='red', linewidth= 1, alpha=0.7)
    axs[0].set_ylabel(unit_dict['depth'], color ='black')
    axs[0].set_xlabel(unit_dict['sal'], color = 'red')
    axs[0].invert_yaxis()

    sec_axs = axs[0].twiny()
    sec_axs.plot(sal, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel(unit_dict['temp'], color = 'blue')

    # 2nd plot for turbidity and Fluorescence
    axs[1].plot(turb, depth, color='red', linewidth= 1, alpha=0.7)
    axs[1].set_ylabel(unit_dict['depth'], color ='black')
    axs[1].set_xlabel(unit_dict['turb'], color = 'red')
    axs[1].invert_yaxis()

    sec_axs = axs[1].twiny()
    sec_axs.plot(fluo, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel(unit_dict['fluo'], color = 'blue')

    # 3rd plot for Total Aggregate Volume and Aggregate abundance
    axs[2].plot(aggr_vol, depth, color='red', linewidth= 1, alpha=0.7)
    axs[2].set_ylabel(unit_dict['depth'], color ='black')
    axs[2].set_xlabel(unit_dict['aggr_vol'], color = 'red')
    axs[2].invert_yaxis()

    sec_axs = axs[2].twiny()
    sec_axs.plot(aggr_abund, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel(unit_dict['aggr_abund'], color = 'blue')

    # 4th plot for Median ESD and Average ESD
    mid_min, mid_max = np.nanmin(median_esd), np.nanmax(median_esd) # find min and max values considering from both median and average ESD
    avg_min, avg_max = np.nanmin(average_esd), np.nanmax(average_esd)
    x_min, x_max = min(mid_min, avg_min), max(mid_max, avg_max)
    axs[3].scatter(median_esd, depth, color='red', s= 2, alpha=0.7)
    axs[3].set_ylabel(unit_dict['depth'], color ='black')
    axs[3].set_xlabel(unit_dict['median_esd'], color = 'red')
    axs[3].invert_yaxis()
    axs[3].set_xlim(x_min, x_max)

    sec_axs = axs[3].twiny()
    sec_axs.scatter(average_esd, depth, color ='blue', s=2, alpha=0.7)
    sec_axs.set_xlabel(unit_dict['average_esd'], color = 'blue')
    sec_axs.set_xlim(x_min, x_max)

    fig.tight_layout(pad=3) # adjust layout of subplots
    plt.suptitle(title, y = 0.99) # main title

    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/ISCpy/plots')
    fig_name = str('CTD10_'+title+'.pdf')
    plt.savefig(fig_name)
    plt.close()


def sum_up (df, list_size_spectra, min_size, max_size):
    '''
    This function handle 'Binned_All_Images' sheet to define the number of images per each depth bin (default 10 images)
    And return number of images per bin
    '''
    target_size_spectra = [x for x in list_size_spectra if x > min_size and x < max_size] # select target size spectra
    target_df = df.loc[:, target_size_spectra] # create target size spectra image
    target_df = target_df.loc[: , ~(target_df == 0).all()] # drop size spectra having all Zero value
    
    loc_number = 10 # start loc image number with 10 (loc means number of images)
    more_than_three = False
    while more_than_three == False: 
        for i in range(0, len(target_df.index), loc_number):
            loc_target_df = target_df.loc[i: i+loc_number].sum(skipna=True, axis=0)
            if any(x < 2 for x in loc_target_df):
                loc_number += 1
                break
            else:
                if len(target_df.index) <= loc_number + i:
                    more_than_three = True
                else:
                    pass
            continue

    return loc_number


def bin_interval (df, bin_size, max_depth):
    # reforming dataframe with certain depth interval
    df.dropna(axis=1, how='all', inplace=True) # drop columns having all nan
    depth_range = range(0, int(max_depth+bin_size), bin_size) # set depth bin range
    bin_df = pd.DataFrame() # create empty dataframe
    for b in range(0, len(depth_range)-1):
        each_df = df.loc[(depth_range[b] <= df['Depths (m)']) & (df['Depths (m)'] < depth_range[b+1])]
        index_each_df = tuple(each_df.index)
        index_up, index_down = index_each_df[0], index_each_df[-1]
        bin_df[depth_range[b+1]] = df.loc[(depth_range[b] <= df['Depths (m)']) & (df['Depths (m)'] < depth_range[b+1])].sum(axis=0)/(index_down-index_up+1)

    bin_df = bin_df.T
    bin_df['Depths (m)'] = bin_df.index
    bin_df.reset_index(drop=True, inplace=True) 
    print(bin_df)

def isc_xlsx (file_name, bin_size):
    '''
    this function read in processed ISC data and,
    return as organised data
    '''
    # 1. import xlsx file and seperate each sheets to seperate dataframe
    xl_file = pd.ExcelFile(file_name)

    ctd_df = pd.read_excel(xl_file, sheet_name='CTD-Data', header=2)
    vol_spec_df = pd.read_excel(xl_file, sheet_name='VolumeSpectraData', header=2)
    aggr_con_df = pd.read_excel(xl_file, sheet_name='AggregateConcentration', header=2)
    size_spec_df = pd.read_excel(xl_file, sheet_name='SizeSpectraData', header=2)

    # 2. reformaing dataframe with given bin_size interval
    max_depth = ctd_df['Depths (m)'].max()
    bin_interval (vol_spec_df, 10, max_depth)
    return ctd_df

if __name__ == "__main__":
    file_path = '/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/OCEANpy'
    for excel_file in glob.glob(file_path+os.sep+'data'+os.sep+'isc'+os.sep+'IR*.xlsx'):
        ctd_df = isc_xlsx(excel_file, 10)
        quit()
        #vertical_plot(ctd_df, excel_file.split(os.sep)[-1].replace('.xlsx', ''))
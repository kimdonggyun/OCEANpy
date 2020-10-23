# this file was created to handle processed ISC data

import os, glob
import pandas as pd
import numpy as np
from pandas import read_excel
from pathlib import Path
from matplotlib import pyplot as plt

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


def vertical_plot (ctd_df, vol_spec_df, aggr_con_df, title, particle_range):
    # plot for ISC and CTD

    # data preparation
    # CTD
    depth = tuple(ctd_df['Depths (m)'])
    temp = tuple(ctd_df['Temperature (dC)'])
    sal = tuple(ctd_df['Salinity (PSU)'])
    turb = tuple(ctd_df['Turbidity (NTU)'])
    fluo = tuple(ctd_df['Fluorescence (mg/m3)'])

    ctd_dict = {'depth': 'Depths (m)', 'temp': 'Temperature (dC)', 'sal': 'Salinity (PSU)', 'turb': 'Turbidity (NTU)',
                    'fluo': 'Fluorescence (mg/m3)'}

    # particle volume data
    vol_sml = tuple(vol_spec_df[str(particle_range[0])+'-'+str(particle_range[1])])
    vol_med = tuple(vol_spec_df[str(particle_range[1])+'-'+str(particle_range[2])])
    vol_lrg = tuple(vol_spec_df[str(particle_range[2])+'-'+str(particle_range[3])])
    vol_tol = tuple(np.array(vol_sml) + np.array(vol_med) + np.array(vol_lrg))

    # particle abundance data
    abd_sml = tuple(aggr_con_df[str(particle_range[0])+'-'+str(particle_range[1])])
    abd_med = tuple(aggr_con_df[str(particle_range[1])+'-'+str(particle_range[2])])
    abd_lrg = tuple(aggr_con_df[str(particle_range[2])+'-'+str(particle_range[3])])
    abd_tol = tuple(np.array(abd_sml) + np.array(abd_med) + np.array(abd_lrg))

    ##########
    # plotting 
    fig, axs = plt.subplots(2,3, figsize = (8, 10))
    axs = axs.ravel()

    # 1st plot for temperature and salanity / data from ISC CTD
    axs[0].plot(temp, depth, color='red', linewidth= 1, alpha=0.7)
    axs[0].set_ylabel(ctd_dict['depth'], color ='black')
    axs[0].set_xlabel(ctd_dict['temp'], color = 'red')
    axs[0].set_xlim(-3, 9)
    axs[0].set_ylim(0,1000)
    axs[0].invert_yaxis()


    sec_axs = axs[0].twiny()
    sec_axs.plot(sal, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel(ctd_dict['sal'], color = 'blue')
    sec_axs.set_xlim(30, 36)

    # 2nd plot for turbidity and Fluorescence / data from ISC CTD
    axs[3].plot(turb, depth, color='red', linewidth= 1, alpha=0.7)
    axs[3].set_ylabel(ctd_dict['depth'], color ='black')
    axs[3].set_xlabel(ctd_dict['turb'], color = 'red')
    axs[3].set_xlim(-0.5, 6)
    axs[3].set_ylim(0,1000)
    axs[3].invert_yaxis()


    sec_axs = axs[3].twiny()
    sec_axs.plot(fluo, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel(ctd_dict['fluo'], color = 'blue')
    sec_axs.set_xlim(-0.5, 6)

    # 3rd plot for Total Aggregate Volume and Aggregate abundance
    axs[1].plot(vol_sml, depth, color='red', linewidth= 1, alpha=0.7)
    axs[1].set_xlabel('vol 0.15-0.5 [mm]', color = 'red')
    axs[1].set_ylim(0,1000)
    axs[1].invert_yaxis()

    sec_axs = axs[1].twiny()
    sec_axs.plot(vol_med, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel('vol 0.5-1 [mm]', color = 'blue')

    # 4th plot for vol_median ESD and Average ESD
    axs[4].plot(vol_lrg, depth, color='red', linewidth= 1, alpha=0.7)
    axs[4].set_xlabel('vol 1 [mm] > ', color = 'red')
    axs[4].set_ylim(0,1000)
    axs[4].invert_yaxis()

    sec_axs = axs[4].twiny()
    sec_axs.plot(vol_tol, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel('vol total (0.15 [mm] > )', color = 'blue')

    # 5th plot for Total Aggregate Volume and Aggregate abundance
    axs[2].plot(abd_sml, depth, color='red', linewidth= 1, alpha=0.7)
    axs[2].set_xlabel('abd 0.15-0.5 [mm]', color = 'red')
    axs[2].set_ylim(0,1000)
    axs[2].invert_yaxis()

    sec_axs = axs[2].twiny()
    sec_axs.plot(abd_med, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel('abd 0.5-1 [mm]', color = 'blue')

    # 6th plot for vol_median ESD and Average ESD
    axs[5].plot(abd_lrg, depth, color='red', linewidth= 1, alpha=0.7)
    axs[5].set_xlabel('abd 1 [mm] > ', color = 'red')
    axs[5].set_ylim(0,1000)
    axs[5].invert_yaxis()

    sec_axs = axs[5].twiny()
    sec_axs.plot(abd_tol, depth, color ='blue', linewidth= 1, alpha=0.7)
    sec_axs.set_xlabel('abd total (0.15 [mm] > )', color = 'blue')


    # addtional plot modification
    fig.tight_layout(pad=3, h_pad=1, w_pad=1) # adjust layout of subplots
    plt.suptitle(title, y = 0.99) # main title

    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/OCEANpy/plots')
    fig_name = str('abd_vol_'+title+'.png')
    plt.savefig(fig_name)
    plt.close()

def depth_bin_interval (df, depth_bin_size, max_depth):
    # reforming dataframe with certain depth interval

    # 1. drop unnecessary columns and modify error values (e.g. - value to 0)
    df.dropna(axis=1, how='all', inplace=True) # drop columns having all nan
    for c in df.columns:
        if df[c].dtype == 'object':
            df.drop([c], axis=1, inplace=True)

    # 2. reforming data frame with certain depth interval
    depth_range = range(0, int(max_depth+depth_bin_size), depth_bin_size) # set depth bin range
    bin_df = pd.DataFrame() # create empty dataframe
    for b in range(0, len(depth_range)-1):
        each_df = df.loc[(depth_range[b] <= df['Depths (m)']) & (df['Depths (m)'] < depth_range[b+1])]
        index_each_df = tuple(each_df.index)
        index_up, index_down = index_each_df[0], index_each_df[-1]
        bin_df[depth_range[b+1]] = df.loc[(depth_range[b] <= df['Depths (m)']) & (df['Depths (m)'] < depth_range[b+1])].sum(axis=0)/(index_down-index_up+1)

    bin_df = bin_df.T
    bin_df['Depths (m)'] = bin_df.index
    bin_df.reset_index(drop=True, inplace=True) 
    
    return bin_df


def particle_bin_interval (df, particle_range):
    # reformatig particel size range 
    # df is dataframe from ISC excel file, particle range is the range of particle in list 

    # 1. drop unnecessary columns
    df.dropna(axis=1, how='all', inplace=True) # drop columns having all nan
    for c in df.columns:
        if df[c].dtype == 'object':
            df.drop([c], axis=1, inplace=True)

    # 2. collapse columns (raw particel size) to certain particle size range
    bin_df = pd.DataFrame() # create empty frame
    bin_df['Depths (m)'] = df['Depths (m)'] # add depth data

    for b in range(0, len(particle_range)-1) :
        cols = list(df.columns) # list the columns
        cols.remove('Depths (m)') # remove the 'Depths (m)'
        col_list = [x for x in cols if (float(x) < particle_range[b+1]) & (float(x) >= particle_range[b])]
        each_df = df.loc[:, col_list] # this datafram contains within the particle size b to b+1
        bin_df[str(particle_range[b])+'-'+str(particle_range[b+1]) ] = each_df.sum(axis=1)

    return bin_df


def isc_xlsx (file_name, depth_bin_size, particle_range):
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

    # 2. reformaing dataframe with given depth_bin_size interval
    max_depth = ctd_df['Depths (m)'].max()

    ctd_df.loc[ctd_df['Fluorescence (mg/m3)'] < 0, 'Fluorescence (mg/m3)'] = 0
    ctd_df = depth_bin_interval (ctd_df, depth_bin_size, max_depth)
    vol_spec_df = depth_bin_interval (vol_spec_df, depth_bin_size, max_depth)
    aggr_con_df = depth_bin_interval (aggr_con_df, depth_bin_size, max_depth)
    size_spec_df = depth_bin_interval (size_spec_df, depth_bin_size, max_depth)

    # 3. reforming dataframe with given paritcle size range
    vol_spec_df = particle_bin_interval (vol_spec_df, particle_range)
    aggr_con_df = particle_bin_interval (aggr_con_df, particle_range)

    return ctd_df, vol_spec_df, aggr_con_df, size_spec_df



if __name__ == "__main__":
    file_path = '/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/OCEANpy'
    for excel_file in glob.glob(file_path+os.sep+'data'+os.sep+'isc'+os.sep+'IR*.xlsx'):
        particle_range = [150, 500, 1000, 100000]
        ctd_df, vol_spec_df, aggr_con_df, size_spec_df = isc_xlsx(excel_file, 10, particle_range)
        vertical_plot(ctd_df, vol_spec_df, aggr_con_df, excel_file.split(os.sep)[-1].replace('.xlsx', ''), particle_range)
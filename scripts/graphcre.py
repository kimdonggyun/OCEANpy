# any functions for plots

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import dates as mdates
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
from pathlib import Path
import glob, os
import datetime

def deployment_constancy (df, title):
    '''
    create a plot to check weather LOKI was deployed constantly with depth
    '''
    depth = df['Depth (m)'].tolist()
    time = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in df['Time_Loki (UTC)'].tolist()]

    fig, [ax1, ax2] = plt.subplots(2,1)

    # plot depth vs time
    ax1.scatter(time, depth, color='black', s=3)
    #ax1.set_xlabel('time (UTC)')
    ax1.set_ylabel('depth (m)')
    ax1.invert_yaxis()
    ax1.set_title(str(title+' (depth vs time)'), fontsize =10)
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=5)) # modify the date time x ticker frequency with interval(min) =5min
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # modify the datetime dicker format
    
    # plot velocity vs time
    velocity = []
    vel_time = []
    for i in range(0, len(time)-1):
        if time[i] != time[i+1]:
            each_vel = abs((depth[i]-depth[i+1])/((time[i]-time[i+1])/datetime.timedelta(seconds=1)))
            velocity.append(each_vel)
            vel_time.append(time[i])
        else:
            pass

    ax2.scatter(vel_time, velocity, color='black', s=3)
    ax2.set_xlabel('time (UTC)')
    ax2.set_ylabel('velocity (m/s)')
    ax2.set_title(str(title+' (velocity vs time)'), fontsize =10)
    ax2.xaxis.set_major_locator(mdates.MinuteLocator(interval=5)) # modify the date time x ticker frequency with interval(min) =5min
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # modify the datetime dicker format

    fig.tight_layout() #adjust subplots space
    
    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/LOKIpy/plots')
    fig_name = str('dist_vel_'+title+'.pdf')
    plt.savefig(fig_name)
    plt.close()

def vertical_distribution_old (count_dict, title, min_depth, max_depth, depth_interval, water_vol):
    '''
    bins describes the depth interval
    density describes ratio, default: False
    align describes the location of histogram, default: right
    '''
    for org, count in count_dict.items():
        bins=np.arange(min_depth,max_depth, depth_interval)
        count_vol = [x/((max_depth/depth_interval)*depth_interval) for x in count]
        plt.barh(bins[:len(count_vol)], count_vol, align='edge', color='black', height = 10) # horizontal bar plot
        plt.xlabel('concentration (n/m3)')
        plt.ylabel('depth (m)')
        plt.gca().invert_yaxis()
        plt.title(org)
        
        os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/LOKIpy/plots')
        fig_name = str('concent_'+org+'_'+title+'.pdf')
        plt.savefig(fig_name)
        plt.close()


def vertical_each_org_distribution (each_df, count_dict, title, min_depth, max_depth, depth_interval, water_vol):
    '''
    bins describes the depth interval
    density describes ratio, default: False
    align describes the location of histogram, default: right
    work with dictionary
    this function works for station level
    '''
    # organize environmental data e.g. depth, temperature, salinity, oxygen
    depth = each_df['Depth (m)'].tolist()
    temperature = each_df['Temperature (°C)'].tolist()
    salinity = each_df['Salinity (psu)'].tolist()
    oxygen = each_df['Oxygen concentration (µM)'].tolist()

    fig, axs = plt.subplots(2,3, figsize = (15, 10))
    axs = axs.ravel()

    i = 0
    for org, count in count_dict.items():
        # add target data
        bins=np.arange(min_depth,max_depth, depth_interval)
        count_vol = [x/((max_depth/depth_interval)*depth_interval) for x in count]

        axs[i].barh(bins[:len(count_vol)], count_vol, align='edge', color='black', height = 10) # horizontal bar plot
        axs[i].set_xlabel('concentration (n/m3)')
        axs[i].set_ylabel('depth (m)')
        axs[i].invert_yaxis()
        axs[i].set_title(org, y =1.0) # subplot title
        axs[i].xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # add environmental data
        temp_ax = axs[i].twiny()
        temp_ax.plot(temperature, depth, color='red')
        temp_ax.set_xlabel('temperature', color='red')
        
        sal_ax = axs[i].twiny()
        sal_ax.plot(salinity, depth, color='green')
        sal_ax.xaxis.set_ticks_position('bottom')
        sal_ax.xaxis.set_label_position('bottom')
        sal_ax.spines['bottom'].set_position(('outward', 40))
        sal_ax.set_xlabel('salinity (PSU)', color = 'green')
        
        # change tick and colors
        axs[i].xaxis.set_ticks_position('top') # change the position of each spines of axis
        axs[i].xaxis.set_label_position('top')
        temp_ax.xaxis.set_ticks_position('bottom')
        temp_ax.xaxis.set_label_position('bottom')

        temp_ax.spines['bottom'].set_color('red') # change the location color of spines and ticks
        temp_ax.tick_params(axis='x', color='red')
        sal_ax.spines['bottom'].set_color('green')
        sal_ax.tick_params(axis='x', color='green')

        axs[i].set_xticks(np.arange(0, max(count_vol) + 0.05, 0.05))

        i += 1
    
    fig.tight_layout(pad=3) # adjust layout of subplots
    plt.suptitle(title, y = 0.99) # main title
    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/LOKIpy/plots')
    fig_name = str('concent_'+title+'.pdf')
    plt.savefig(fig_name)
    plt.close()


def stacked_vertical_distribution (mask_dict, title, min_depth, max_depth, depth_interval, water_vol):
        i = False
        bins=np.arange(min_depth,max_depth, depth_interval)

        org_list = []

        fig, ax = plt.subplots()
        for org, count in mask_dict.items():
            org_list.append(org)
            # sum each element in count to botton in bar
            count_vol = [x/((max_depth/depth_interval)*depth_interval) for x in count]

            if i == False:
                bar_bottom = [0]*len(count)
                i = True
            
            ax.barh(bins[:len(count_vol)], count_vol, height = 10, align='edge', left=np.array(bar_bottom)) # horizontal bar plot
            bar_bottom = [a+b for a, b in zip(bar_bottom, count_vol)]

        ax.invert_yaxis()
        ax.set_title(title)
        ax.set_xlabel('concentration (n/m3)')
        ax.set_ylabel('depth (m)')
        ax.legend(org_list, loc ='upper right')
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/LOKIpy/plots')
        fig_name = str('stacked_'+title+'.pdf')
        plt.savefig(fig_name)
        plt.close()


def comp_vertical_distribution (ecotaxa_df, min_depth, max_depth, depth_interval):
    '''
    create a plot with two vertical profile to compare between them
    '''
    left_depth = np.asarray(ecotaxa_df['Depth (m)'])
    right_depth = np.asarray(ecotaxa_df['Depth (m)'])

    fig, [ax1, ax2] = plt.subplots(1,2)
    ax1.hist(left_depth, bins=np.arange(min_depth,max_depth, depth_interval), orientation='horizontal', color='black')
    ax1.invert_yaxis() # invert axis subplot level
    ax1.invert_xaxis()
    ax1.set_xlabel('counts') # add label on subplot level
    ax1.set_ylabel('depth [m]')

    ax2.hist(left_depth, bins=np.arange(min_depth,max_depth, depth_interval), orientation='horizontal', color='black')
    ax2.invert_yaxis()
    ax2.set_xlabel('counts')
    #ax2.set_ylabel('depth [m]')

    plt.show()
    plt.close()

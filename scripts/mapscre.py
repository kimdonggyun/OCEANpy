# create maps
from sqlays import export_sql, import_sql
from iscays import isc_xlsx
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import maskoceans
# brew install geos
# pip3 install https://github.com/matplotlib/basemap/archive/master.zip
# for DIVA tools
# https://github.com/gher-ulg/DivaPythonTools
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import sys, os, glob, re
from scipy.interpolate import griddata
import scipy.ndimage
import matplotlib.tri as tri
import math
from timeinfo import day_night
from datetime import datetime

def station_map (dict_cruise_pos, topo_ary, lat_min, lat_max, lon_min, lon_max, label_color):
    '''
    create maps showing the location of stations
    the form of dictionary should be like below:
    dict = {'cruise1': ((lat),(lon)), 'cruise2': ((lat),(lon))}
    '''
    #################################################################################
    # 1. create map
    fig, ax = plt.subplots(figsize=(10,10))
    m = Basemap(projection='merc', lat_0 = (lat_min+lat_max)/2, lon_0 = (lon_min+lon_max)/2, resolution = 'h',
            llcrnrlon = lon_min, llcrnrlat = lat_min, urcrnrlon = lon_max, urcrnrlat = lat_max, ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.etopo()
    m.shadedrelief()
    m.drawmapboundary()
    m.fillcontinents(color='grey')

    #################################################################################
    # 2. draw lat/lon grid lines every 5 degrees. labels = [left, right, top, bottom]
    m.drawmeridians(np.arange(lon_min, lon_max, math.ceil(abs((lon_max-lon_min)/3))), labels=[0,1,0,1], fontsize=10) # line for longitude
    m.drawparallels(np.arange(lat_min, lat_max, math.ceil(abs((lat_max-lat_min)/3))), labels=[1,0,1,0], fontsize=10) # line for latitude

    #################################################################################
    # 3. draw the contour of bathymetry
    x = topo_ary[:,0] # lat
    y = topo_ary[:,1] # lon
    z = topo_ary[:,2] # topo

    lon, lat = np.meshgrid(np.linspace(np.min(y), np.max(y), 100), np.linspace(np.min(x), np.max(x),100)) 
    topo = griddata((y, x), z, (lon, lat), method='cubic') 
    lon_m, lat_m = m(lon, lat)

    mask_ocean = topo >= 0 # mask inland
    topo_ocean = np.ma.masked_array(topo, mask=mask_ocean)

    #topo_ocean = maskoceans(lon_m, lat_m, topo, inlands=False, grid=10)
    m.contourf(lon_m, lat_m, topo_ocean, cmap = 'Blues_r') 
    m.contour(lon_m, lat_m, topo_ocean, colors = 'black', linewidths = 0.3) 


    #################################################################################
    # 4. locate the station on the map
    # get the data frame from SQL server and drop the duplication filtered by station name
    color_list = label_color; c = 0
    for cruise, pos in dict_cruise_pos.items():
        lat_list = pos[0]
        lon_list = pos[1]
        lons_m, lats_m = m(lon_list,lat_list)
        m.scatter(lons_m,lats_m, marker='o', s=15, label=cruise, color=color_list[c], edgecolors='black')
        c += 1
    ax.legend(loc='upper right')

    ################################################################################
    return ax, m

def bathy_data (minlat, maxlat, minlon, maxlon):
    '''
    return an array : [[lat, lon, topo], [lat, lon, topo], ...]
    data from : https://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.html
    '''
    import io, csv, json
    import urllib.request as urllib2
    url = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/srtm30plus_LonPM180.json?z[(%s):100:(%s)][(%s):100:(%s)]'%(minlat, maxlat, minlon, maxlon)
    response = urllib2.urlopen(url) 
    data = response.read()
    data_dic = json.loads(data.decode('utf-8'))
    topo = np.asarray(data_dic['table']['rows'])
    return topo

def contour_ver (topo_ary, lat_or_lon, value_of_transec, range_transec, value_ary, z_label):
    '''
    create contour plot with bathymetry data
    should type the paramter like this; contour_ver(topo, 'lat', 79, (-10, 10))
    value array should be like: np.array = [[lat, lon, z value, depth]]
    '''
    if lat_or_lon == 'lat':
        x = topo_ary[:,0] # lat
        y = topo_ary[:,1] # lon
        z = topo_ary[:,2] # topo

        lon, lat = np.meshgrid(np.linspace(np.min(y), np.max(y), 100), np.linspace(np.min(x), np.max(x),100)) 
        topo = griddata((y, x), z, (lon, lat), method='linear') 
        mask_ary = (lat >= value_of_transec+1) | (lat <= value_of_transec-1) # mask array give the value of transec
        topo_mask = np.ma.masked_array(topo, mask=mask_ary)

        lon_transec = lon[1,] # raw longitude
        topo_transec = np.ma.mean(topo_mask, axis=0) # raw topology of given transec

        geo_range = lon_transec[(lon_transec >= range_transec[0]-0.5) & (lon_transec <= range_transec[1]+0.5)] # set precise lon range
        topo_range = topo_transec[(lon_transec >= range_transec[0]-0.5) & (lon_transec <= range_transec[1]+0.5)] # set precise topo range

        # for contour
        fig, ax = plt.subplots(figsize=(11,5))
        cntr = ax.tricontourf(value_ary[:,1], value_ary[:,3], value_ary[:,2], 30, cmap='jet')

    elif lat_or_lon == 'lon':
        x = topo_ary[:,0] # lat
        y = topo_ary[:,1] # lon
        z = topo_ary[:,2] # topo

        lon, lat = np.meshgrid(np.linspace(np.min(y), np.max(y), 100), np.linspace(np.min(x), np.max(x),100)) 
        topo = griddata((y, x), z, (lon, lat), method='linear') 
        mask_ary = (lon >= value_of_transec+1) | (lon <= value_of_transec-1) # mask array give the value of transec
        topo_mask = np.ma.masked_array(topo, mask=mask_ary)

        lat_transec = lat[1,] # raw longitude
        topo_transec = np.ma.mean(topo_mask, axis=0) # raw topology of given transec

        geo_range = lat_transec[(lat_transec >= range_transec[0]-0.5) & (lat_transec <= range_transec[1]+0.5)] # set precise lon range
        topo_range = topo_transec[(lat_transec >= range_transec[0]-0.5) & (lat_transec <= range_transec[1]+0.5)] # set precise topo range

        # for contour
        fig, ax = plt.subplots(figsize=(18,8))
        cntr = ax.tricontourf(value_ary[:,0], value_ary[:,3], value_ary[:,2], 30, cmap='jet')

    # create plot and add data
    ax.fill_between(geo_range, topo_range, np.min(topo_range)-100, color='black') # fill topology
    
    # addtional for plot
    ax.set_xlim(*range_transec)
    ax.set_ylim(np.min(value_ary[:,3]), 0)
    ax.set_xlabel('degree $^\circ$')
    ax.set_ylabel('depth [m]')
    cbar = fig.colorbar(cntr, ticks = range( math.floor(np.nanmin(value_ary[:,2])), math.ceil(np.nanmax(value_ary[:,2])),
                                            math.ceil(abs(math.floor(np.nanmin(value_ary[:,2]))-math.ceil(np.nanmax(value_ary[:,2])))/10)) )

    cbar.ax.set_ylabel(z_label, rotation=90, labelpad=10)  # Fluorescence [mg m$^{-3}$] / Temp [dC] / Salinity [PSU] / Press [dbar]
    
    return ax


def TS_diagram (TSD_dict):
    # plot Temp and Salinity diagram to see the water mass characters
    plt.figure(figsize=(5, 5))
    sc = plt.scatter(TSD_dict['sal'], TSD_dict['temp'], c=TSD_dict['depth'], cmap = 'jet_r', s=1)
    
    # additional plot detail
    plt.xlim(30, 37)
    plt.ylim(-2, 8)
    plt.title('TS diagram')
    plt.xlabel('Salinity [PSU]')
    plt.ylabel('Temperature [dC]')

    cbar = plt.colorbar(sc)
    cbar.ax.set_ylabel('Depth [m]', rotation=270, labelpad=10)

    return plt

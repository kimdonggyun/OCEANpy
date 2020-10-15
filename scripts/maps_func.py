# create maps
from sql_func import export_sql, import_sql
from ISC import isc_xlsx
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
from time_info import day_night
from datetime import datetime

def station_map (dict_cruise_pos, topo_ary):
    '''
    create maps showing the location of stations
    the form of dictionary should be like below:
    dict = {'cruise1': ((lat),(lon)), 'cruise2': ((lat),(lon))}
    '''
    #################################################################################
    # 1. create map
    m = Basemap(projection='merc', lat_0 = 79, lon_0 = 0, resolution = 'h',
            llcrnrlon = -30, llcrnrlat = 75, urcrnrlon = 20, urcrnrlat = 83)
    m.drawcoastlines()
    m.drawcountries()
    m.etopo()
    m.shadedrelief()
    m.drawmapboundary()
    m.fillcontinents(color='grey')

    #################################################################################
    # 2. draw lat/lon grid lines every 5 degrees. labels = [left, right, top, bottom]
    m.drawmeridians(np.arange(-30, 30, 10.), labels=[0,1,0,1], fontsize=10) # line for longitude
    m.drawparallels(np.arange(75, 90, 2.), labels=[1,0,1,0], fontsize=10) # line for latitude

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
    color_list = ['yellow', 'red', 'green']; c = 0
    for cruise, pos in dict_cruise_pos.items():
        lat_list = pos[0]
        lon_list = pos[1]
        lons_m, lats_m = m(lon_list,lat_list)
        m.scatter(lons_m,lats_m, marker='o', s=15, label=cruise, color=color_list[c], edgecolors='black')
        c += 1
    plt.legend(loc='upper right')

    ################################################################################
    # 5. Add figure detail
    plt.title('ISC stations')


    # save the plot
    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/OCEANpy/plots')
    fig_name = "ISC_station_map.pdf"
    plt.savefig(fig_name)
    plt.close()

def bathy_data (minlat, maxlat, minlon, maxlon):
    '''
    return an array : [[lat, lon, topo], [lat, lon, topo], ...]
    data from : https://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.html
    '''
    import io, csv, json
    import urllib.request as urllib2
    response = urllib2.urlopen('http://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeSrtm30v6.json?topo[(' \
                            +str(maxlat)+'):100:('+str(minlat)+')][('+str(minlon)+'):100:('+str(maxlon)+')]')
    data = response.read()
    data_dic = json.loads(data.decode('utf-8'))
    topo = np.asarray(data_dic['table']['rows'])
    return topo

def contour_ver (topo_ary, lat_or_lon, value_of_transec, range_transec, value_ary):
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
        # plt.tricontourf(value_ary[:,3], value_ary[:,1], value_ary[:,2], 2000, cmap='jet')
 
        geo_mesh, depth_mesh = np.meshgrid( np.linspace(np.min(geo_range), np.max(geo_range), int((np.max(geo_range)- np.min(geo_range))*10) ),
                                            np.linspace(np.min(topo_range), 0, int(np.abs(np.min(topo_range))) ) ) # creat mesh grid of x(position) and y(depth)

        z_value = griddata((value_ary[:,1], value_ary[:,3]), value_ary[:,2] , (geo_mesh, depth_mesh), method='linear')

        removenan = np.isnan(z_value) # remove nan vlaue in z value and apply this to x and y parameter
        geo_mesh = np.ma.masked_array(geo_mesh, removenan)
        depth_mesh = np.ma.masked_array(depth_mesh, removenan)
        z_value = np.ma.masked_array(z_value, removenan)
        

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
        geo_mesh, depth_mesh = np.meshgrid( np.linspace(np.min(geo_range), np.max(geo_range), int((np.max(geo_range)- np.min(geo_range))*10) ),
                                            np.linspace(np.min(topo_range), 0, int(np.abs(np.min(topo_range))) ) ) # creat mesh grid of x(position) and y(depth)

        z_value = griddata((value_ary[:,1], value_ary[:,3]), value_ary[:,2] , (geo_mesh, depth_mesh), method='linear')


    # create plot and add data
    plt.figure(figsize=(8, 4))
    #cntr = plt.imshow(z_value, aspect='auto', origin='lower', cmap ='jet', extent=[np.min(geo_range), np.max(geo_range), np.min(topo_range), 0 ]) # same but other method to contour
    cntr = plt.contourf(geo_mesh,depth_mesh, z_value, levels=1000, cmap = 'jet')

    #plt.scatter(list(value_ary[:,1]), list(value_ary[:,3]), s=0.5, c='black')
    plt.fill_between(geo_range, topo_range, np.min(topo_range)-100, color='black') # fill topology
    
    # addtional for plot
    plt.xlim(*range_transec)
    plt.ylim(np.min(depth_mesh), 0)
    plt.xlabel('degree $^\circ$')
    plt.ylabel('depth [m]')
    cbar = plt.colorbar(cntr, ticks = range(math.floor(np.nanmin(z_value)), math.ceil(np.nanmax(z_value)), 1)) # draw colorbar
    cbar.ax.set_ylabel('Press [dbar]', rotation=270, labelpad=10)  # Fluorescence [mg m$^{-3}$] / Temp [dC] / Salinity [PSU]
    plt.title('PS107')

    # save plot
    path_to_save = '/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/OCEANpy/plots'
    file_name = 'press_'+lat_or_lon+'_contour_ver_'+ str(value_of_transec) +str(range_transec)+'.png'

    plt.savefig(os.path.join(path_to_save, file_name))    


def TS_diagram (TSD_dict):
    # plot Temp and Salinity diagram to see the water mass characters
    plt.figure(figsize=(8, 4))
    plt.scatter(TSD_dict['sal'], TSD_dict['temp'], c=TSD_dict['depth'], cmap = 'jet')
    plt.xlim(25, 37)
    plt.ylim(-3, 9)
    plt.show()
    plt.close()
    pass


if __name__ == "__main__":
        # create TS diagram
        ctd_df = export_sql('ctd', 'ctd_meta')
        station_list = ['PS107_18']
        ctd_df = ctd_df.loc[ctd_df['Event'].str.contains('|'.join(station_list))]
        depth = tuple(pd.to_numeric(ctd_df['Depth water [m]']))
        sal = tuple(pd.to_numeric(ctd_df['Sal']))
        temp = tuple(pd.to_numeric(ctd_df['Temp [°C]']))
        TSD_dict = {'temp': temp, 'sal': sal, 'depth':depth}
        TS_diagram(TSD_dict)

        quit()

        # create contour map
        ctd_df = export_sql('ctd', 'ctd_meta'); print(list(ctd_df))
        station_list = ['PS107_10', 'PS107_12', 'PS107_14', 'PS107_16', 'PS107_18']
        cols_to_use = ['Latitude', 'Longitude', 'Depth water [m]', 'Press [dbar]']
        ctd_df_filter = ctd_df.loc[ctd_df['Event'].str.contains('|'.join(station_list))] # select by station
        #ctd_df_filter = ctd_df_filter[cols_to_use] # select only necessary columns
        ctd_df_filter = ctd_df.loc[(pd.to_numeric(ctd_df['Latitude']) >=78.9) & (pd.to_numeric(ctd_df['Latitude']) <=79.1)] # select by lat and lon
        ctd_df_filter = ctd_df_filter.loc[(pd.to_numeric(ctd_df_filter['Depth water [m]']) <=1000)]
        ctd_df_filter = ctd_df_filter.dropna() # drop rows having empty value (empty values will affect contouring method)

        ctd_df_filter['d_n'] = ctd_df_filter.apply(lambda row: day_night(float(row['Latitude']), float(row['Longitude']), datetime.strptime(row['Date/Time'], '%Y-%m-%dT%H:%M')), axis=1 )
        ctd_df_filter = ctd_df_filter.loc[ctd_df_filter['d_n'] == 'day']

        depth = [i*(-1) for i in list(pd.to_numeric(ctd_df_filter['Depth water [m]']).values)]
        lat = list(pd.to_numeric(ctd_df_filter['Latitude']).values)
        lon = list(pd.to_numeric(ctd_df_filter['Longitude']).values)
        z = list(pd.to_numeric(ctd_df_filter['Press [dbar]']).values)

        ctd_array = np.array((lat, lon, z, depth)).transpose() # create array

        topo = bathy_data (75, 83, -30, 20)
        contour_ver(topo, 'lat', 79, (-5, 10), ctd_array)
        #contour_ver(topo, 'lon', 79, (-5, 10), ctd_array)
        quit()

        # create station maps
        isc_df = export_sql('isc', 'isc_meta')
        cruise_list = ('PS107', 'PS114', 'PS121')
        cruise_dict = {}
        for cruise in cruise_list:
            cruise_df = isc_df[isc_df['cruise_station_haul'].str.contains(cruise)]
            cruise_dict[cruise] = (tuple(pd.to_numeric(cruise_df['lat'])) , tuple(pd.to_numeric(cruise_df['lon'])))

        topo = bathy_data (75, 83, -30, 20) # -30, 30, 75, 85
        station_map(cruise_dict, topo)
        
        quit()


        # create contour plot of cross section
        station_dict = {}
        '''
        station_dict = {'cruise_station_haul': (lat, lon, profile_number)}
        '''
        for index, row in cruise_df.iterrows():
            if row['cruise_station_haul'] not in station_dict:
                station_dict[row['cruise_station_haul']] = (row['lat'], row['lon'], row['profile_number'])
            else:
                pass
        
        contour_dict = {}
        '''
        contour_dict = {(lat, lon): (depth, parameter)}
        '''
        file_path = '/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/ISCpy'
        for excel_file in glob.glob(file_path+os.sep+'data'+os.sep+'IR*.xlsx'):
            print(excel_file)
            profile_num = re.findall('[0-9]+', Path(excel_file).name)[0]
            c_df = isc_xlsx(excel_file)
            for station, item in station_dict.items():
                if True in np.isnan(item): # ignore if nan value in item(lat, lon, profile number)
                    continue
                elif (int(item[2]) == int(profile_num)):
                    contour_dict[(item[0], item[1])] = tuple(c_df['Depths (m)']), tuple(c_df['Temperature (dC)']) 
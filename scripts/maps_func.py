# create maps
from sql_func import export_sql, import_sql
from isc_prcs_func import isc_prcs
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import maskoceans
# brew install geos
# pip3 install https://github.com/matplotlib/basemap/archive/master.zip
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np
import sys, os, glob, re
from scipy.interpolate import griddata

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
    os.chdir('/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/github/ISCpy/plots')
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



if __name__ == "__main__":
        isc_df = export_sql('isc', 'isc_meta')
        cruise_list = ('PS107', 'PS114', 'PS121')
        cruise_dict = {}
        for cruise in cruise_list:
            cruise_df = isc_df[isc_df['cruise_station_haul'].str.contains(cruise)]
            cruise_dict[cruise] = (tuple(pd.to_numeric(cruise_df['lat'])) , tuple(pd.to_numeric(cruise_df['lon'])))

        topo = bathy_data (75, 85, -30, 30) # -30, 30, 75, 85
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
            c_df = isc_prcs(excel_file)
            for station, item in station_dict.items():
                if True in np.isnan(item): # ignore if nan vlaue in item(lat, lon, profile number)
                    continue
                elif (int(item[2]) == int(profile_num)):
                    contour_dict[(item[0], item[1])] = tuple(c_df['Depths (m)']), tuple(c_df['Temperature (dC)']) 
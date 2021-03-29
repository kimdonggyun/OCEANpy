'''
This function includes three separate definitions
1. Export and adjust data from LOKI_browser to Zoomie
2. Export and adjust data from Zoomie to EcoTaxa
3. Export and adjust data from EcoTaxa to Data storage

Created by : Dong-gyun KIM
Contact : kdk921219@gmail.com
Creation date : 02.07.2020
'''
from tkinter.filedialog import askdirectory, askopenfilename
from pathlib import Path
import pandas as pd
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import re
import glob
import psycopg2 as pgsql
import pandas.io.sql as sql
from sqlalchemy import create_engine
from tkinter import Tk
import sqlalchemy

def Browser_to_Zoomie():
    ###### fix data type!! #####



    '''
    This function is created to modify the metadata from LOKI_browser for the later use of Zoomie
    As a return, a CSV file will be generated on the working dir
    '''
    # set the working directory
    #path_to_data = input('type path of the data: ')
    Tk().withdraw()
    print('choose project directory')
    path_to_data = askdirectory()
    work_dir = Path(path_to_data).expanduser()
    os.chdir(work_dir)
    
    # conmbine all *_Export.txt files in one dataframe and sort it by 'img_file_name'
    export_df = []
    for export_filename in work_dir.glob('*_Export.txt'):
        if '._' not in str(export_filename):
            print(export_filename)
            datdf = pd.read_csv(export_filename, sep='\t', engine='python', decimal=',')
            datdf = datdf.loc[datdf['Index'] != 'Evaluation']
            export_df.append(datdf)
    export_df = pd.concat(export_df)
    export_df.columns = ['object_index','object_cruise',
              'object_vessel_name','object_station','object_haul',
              'object_date','object_time','object_lat','object_lon','object_bottom_depth',
              'object_depth_min','object_pressure','object_temperature','object_salinity',
              'object_conductivity','object_oxygen_concentration','object_temperature_oxsens',
              'object_oxygen_saturation','object_chlorophyll_a','object_light','object_speed',
              'object_Dr._Haardt_fluorescence_channel_A','object_Dr._Haardt_fluorescence_channel_B',
              'object_Dr._Haardt_fluorescence_channel_C','object_Dr._Haardt_fluorescence_channel_D',
              'object_speed_over_ground','object_speed_in_water','object_frames',
              'object_automatic_classification','object_manual_classification','object_area_px',
              'object_form','object_area','object_lenght','object_width','object_convexity',
              'object_structure','object_graymean','object_kurtosis','object_skewness',
              'object_Hu_moment_1','object_Hu_moment_2','object_Hu_moment_3','object_Hu_moment_4',
              'object_Hu_moment_5','object_Hu_moment_6','object_Hu_moment_7',
              'object_fourier_descriptor_01','object_fourier_descriptor_02',
              'object_fourier_descriptor_03','object_fourier_descriptor_04',
              'object_fourier_descriptor_05','object_fourier_descriptor_06',
              'object_fourier_descriptor_07','object_fourier_descriptor_08',
              'object_fourier_descriptor_09','object_fourier_descriptor_10',
              'img_file_name']

    export_df.sort_values(by=['img_file_name'])
    export_df.reset_index(drop=True, inplace=True)


    # create same table as export_df but with columns for zoomie (old:new)
    zoomie_cols_name_dict = {'object_lenght':'Length', 'object_width':'Width', 'object_area_px':'Areapix', 'object_form':'Form','object_area':'Area', 'object_convexity':'Convex', 'object_structure':'Structure', 'object_graymean':'Gray', 'object_kurtosis':'Kurtosis', 'object_skewness':'Skew',
                            'object_Hu_moment_1':'Hu1', 'object_Hu_moment_2':'Hu2', 'object_Hu_moment_3':'Hu3', 'object_Hu_moment_4':'Hu4', 'object_Hu_moment_5':'Hu5', 'object_Hu_moment_6':'Hu6', 'object_Hu_moment_7':'Hu7', 
                            'object_fourier_descriptor_01':'Fodec01', 'object_fourier_descriptor_02':'Fodec02', 'object_fourier_descriptor_03':'Fodec03', 'object_fourier_descriptor_04':'Fodec04', 'object_fourier_descriptor_05':'Fodec05', 'object_fourier_descriptor_06':'Fodec06', 'object_fourier_descriptor_07':'Fodec07', 'object_fourier_descriptor_08':'Fodec08', 'object_fourier_descriptor_09':'Fodec09', 'object_fourier_descriptor_10':'Fodec10',
                            'img_file_name':'  Image                       ', 'object_index':'ObjNoBrowser', 'object_cruise':'Cruise', 'object_station':'Station', 'object_haul':'Haul', 'object_date':'Date','object_time':'Time', 'object_pressure':'  Pressure      ', 'object_depth_min':'Depth', 'object_salinity':'  Salinity', 'object_conductivity':'  Conductivity            ', 'object_oxygen_concentration':'  Oxygenconc', 'object_temperature_oxsens':'  Tempoxy', 'object_oxygen_saturation':'  Oxysat            ', 'object_Dr._Haardt_fluorescence_channel_A':'FLuoa  ', 'object_manual_classification':'Manuclass              '}
           
    zoomie_df = export_df.rename(columns=zoomie_cols_name_dict)
    zoomie_df = zoomie_df.assign(manualLength2=np.nan, manualWidth2=np.nan, posx=np.nan, posy=np.nan, milliseconds=np.nan, timestamp=np.nan, state=np.nan, id=np.nan, processed=np.nan, group_id=np.nan, deleted=np.nan)
    # modify the file format from .bmp to .png on '  Image                       ' and datatype of certain columns
    zoomie_df['  Image                       '] = zoomie_df['  Image                       '].apply(lambda x: x.replace('.bmp', '.png')) 

    # remain only necessary columns
    zoomie_df = zoomie_df[['Length','Width','Areapix','Form','Area','Convex','Structure','Gray','Kurtosis','Skew','Hu1','Hu2','Hu3','Hu4','Hu5','Hu6','Hu7',
                                'Fodec01','Fodec02','Fodec03','Fodec04','Fodec05','Fodec06','Fodec07','Fodec08','Fodec09','Fodec10','  Image                       ',
                                'ObjNoBrowser','Cruise','Station','Haul','Date','Time','  Pressure      ','Depth','  Salinity','  Conductivity            ','  Oxygenconc','  Tempoxy','  Oxysat            ',
                                'FLuoa  ','Manuclass              ','manualLength2','manualWidth2','posx','posy','milliseconds','timestamp','state','id','processed','group_id','deleted']]

    # save the file as CSV
    zoomie_df['Station'] = input('type Cruise-station-haul (e.g PS107-22-5):')

    meta_file_name = str(zoomie_df.loc[1, 'Station'])+'_Zoomie.csv'
    zoomie_df.to_csv(meta_file_name, sep=',', index=False)
    print('Zoomie.csv created')




def Zoomie_to_Ecotaxa():
    '''
    This function is created to modify the results from Zoomie for the later use of Ecotaxa
    As a return, a txt file will be generated on the working dir
    '''
    # set the working directory
    # path_to_data = input('type path of the data: ')
    Tk().withdraw()
    print('choose project directory')
    path_to_data = askdirectory()
    work_dir = Path(path_to_data).expanduser()
    os.chdir(work_dir)

    zoomie_cols = ['object_length','object_width','object_area_px','object_form','object_area','object_convexity',
              'object_structure','object_graymean','object_kurtosis','object_skewness','object_Hu_moment_1',
              'object_Hu_moment_2','object_Hu_moment_3','object_Hu_moment_4','object_Hu_moment_5','object_Hu_moment_6',
              'object_Hu_moment_7','object_fourier_descriptor_01','object_fourier_descriptor_02',
              'object_fourier_descriptor_03','object_fourier_descriptor_04','object_fourier_descriptor_05',
              'object_fourier_descriptor_06','object_fourier_descriptor_07','object_fourier_descriptor_08',
              'object_fourier_descriptor_09','object_fourier_descriptor_10','img_file_name','object_index',
              'object_cruise','object_station','object_haul','object_date','object_time','object_pressure',
              'object_depth_min','object_salinity','object_conductivity','object_oxygen_concentration',
              'object_temperature_oxsens','object_oxygen_saturation','object_Dr._Haardt_fluorescence_channel_A',
              'object_manual_classification','object_manual_length','object_manual_width','object_posx','object_posy','object_milliseconds',
              'object_timestamp','object_zoomie_state','object_zoomie_deleted','object_zoomie_id','object_zoomie_proc','object_zoomie_group_id']
    
    for zoomie_export in work_dir.glob('*Zoomie_Export.csv'):
        zoomiedf = pd.read_csv(zoomie_export, names=zoomie_cols ,sep=';', header=None, engine='python')

        # modifing object_Hu_moment_* columns
        object_Hu_moment_col_list = [col for col in zoomiedf.columns if 'object_Hu_moment' in col]
        for object_Hu_moment_col in object_Hu_moment_col_list:
            zoomiedf[object_Hu_moment_col] = zoomiedf['object_Hu_moment_1']

        # remove duplicated images and empty images estimated by zoomie
        zoomiedf = zoomiedf[~zoomiedf['object_zoomie_state'].str.contains('double')]
        zoomiedf = zoomiedf[zoomiedf['object_zoomie_deleted'] != 1]

        # Replace extension (.bmp to .png)
        zoomiedf['img_file_name'] = zoomiedf['img_file_name'].apply(lambda x:x.replace('bmp', 'png'))

        # Adding new columns and correcting haul information
        vessel, gear, lat, lon, haul = 'Polarstern', 'LOKI', '89.15383', '-116.0145', '00'
        zoomiedf['object_vessel_name'], zoomiedf['acq_instrument'], zoomiedf['object_lat'], zoomiedf['object_lon'], zoomiedf['object_haul'] = vessel, gear, lat, lon, haul
        zoomiedf['object_id'] = zoomiedf['img_file_name'].apply(lambda x:str(x)[0:37])

        # Add Date and Time information from file name
        zoomiedf['object_date'] = zoomiedf['img_file_name'].apply(lambda x: datetime.strptime(x.split(' ')[0], '%Y%m%d'))
        zoomiedf['object_time'] = zoomiedf['img_file_name'].apply(lambda x: datetime.strptime(x.split(' ')[1], '%H%M%S'))

        # sort dataframe by img_file_name
        zoomiedf.sort_values(by = ['img_file_name'], inplace=True)

        # insert data type info at the first row
        zoomiedf_col_list = list(zoomiedf)
        dtype = ['[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]',
                    '[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]',
                    '[f]','[f]','[f]','[f]','[f]','[f]','[f]','[t]','[f]','[t]',
                    '[t]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]','[f]',
                    '[f]','[f]','[t]','[f]','[f]','[f]','[f]','[f]','[f]','[t]',
                    '[f]','[t]','[f]','[f]','[t]','[t]','[t]','[f]','[f]']
        zoomiedf = pd.DataFrame(np.insert(zoomiedf.values, 0, values=dtype, axis =0), columns = zoomiedf_col_list)

        # remain necessary columns
        zoomiedf = zoomiedf[['object_length','object_width','object_area_px','object_form','object_area','object_convexity','object_structure','object_graymean','object_kurtosis','object_skewness',
        	                'object_Hu_moment_1','object_Hu_moment_2','object_Hu_moment_3','object_Hu_moment_4','object_Hu_moment_5','object_Hu_moment_6','object_Hu_moment_7','object_fourier_descriptor_01',
                            'object_fourier_descriptor_02','object_fourier_descriptor_03','object_fourier_descriptor_04','object_fourier_descriptor_05','object_fourier_descriptor_06','object_fourier_descriptor_07',
                            'object_fourier_descriptor_08','object_fourier_descriptor_09','object_fourier_descriptor_10','img_file_name','object_index','object_cruise','object_station','object_haul','object_date',
                            'object_time','object_pressure','object_depth_min','object_salinity','object_conductivity','object_oxygen_concentration','object_temperature_oxsens','object_oxygen_saturation',
                            'object_Dr._Haardt_fluorescence_channel_A','object_manual_classification','object_posx','object_posy','object_milliseconds','object_timestamp','object_zoomie_state','object_id','object_vessel_name',
                            'acq_instrument','object_lat','object_lon']]
        # save as table
        meta_file_name = 'ecotaxa.'+str(zoomiedf.loc[2, 'object_station'])+'.txt'
        zoomiedf.to_csv(meta_file_name, sep='\t', index=False, decimal='.')
        print('ecotaxa.txt created')


def Ecotaxa_to_Storage():
    '''
    This function is created to modify the results from Ecotaxa for the later use of Data storage
    As a return, a txt file will be generated on the working dir
    '''

    # set the working directory
    path_to_data = input('type path of the data: ')
    work_dir = Path(path_to_data).expanduser()
    os.chdir(work_dir)

    # Add missing data
    haul, region, detail_location, bottom_depth = 'Type Haul', 'Type Region', 'Type location detail', 'Type bottom depth'


    # Reading in Ecotada file
    for ecotaxa_export in work_dir.glob('*Ecotaxa_Export.tsv'):
        ecotaxadf = pd.read_csv(ecotaxa_export, sep='\t', encoding= 'unicode_escape', dtype={'complement_info':'string'})

        # create new df for data storage with new column names (old:new)
        datastorage_cols_name_dict = {'object_vessel_name':'Vessel', 'object_cruise':'Cruise', 'object_station':'Station', 'object_date':'Date (UTC)', 'object_time':'Time LOKI (UTC)', 'object_lat':'Latitude', 'object_lon':'Longitude',
                                        'object_depth_min':'Depth (m)', 'object_temperature_oxsens':'Temperature (°C)', 'object_salinity':'Salinity (psu)', 'object_conductivity':'Conductivity (mS cm-1)', 'object_oxygen_concentration':'Oxygen concentration (µM)',
                                        'object_oxygen_saturation':'Oxygen saturation (%)', 'object_dr._haardt_fluorescence_channel_a':'Fluorescence', 'object_annotation_category':'Classif', 'object_area_px':'Area (pixels)', 'object_area':'Area (mm2)', 'object_length':'Length (mm)', 'object_width':'Width (mm)',
                                        'object_id':'Image file name', 'object_annotation_person_name':'Scientist'}                    
        datastorage_df = ecotaxadf.rename(columns=datastorage_cols_name_dict)
        datastorage_df['Haul'] = haul
        datastorage_df['Region'] = region
        datastorage_df['Detail_Location'] = detail_location
        datastorage_df['Bottom depth (m)'] = bottom_depth

        # add and modify the columns (consider 'assign' function here later)
        datastorage_df['Manual classification'], datastorage_df['Developmental stage'] = '', ''
        datastorage_df['Image file name'] = datastorage_df['Image file name'].apply(lambda x: str(x)+'.png')

        # date and time format modification
        datastorage_df['Time LOKI (UTC)'] = datastorage_df['Image file name'].apply(lambda x: pd.to_datetime(x.split(' ')[1], format='%H%M%S').strftime('%H:%M:%S'))
        datastorage_df['Date (UTC)'] = datastorage_df['Image file name'].apply(lambda x: pd.to_datetime(x.split(' ')[0], format='%Y%m%d').strftime('%d.%m.%Y'))

        # classification
        # correct 'like' for normal description
        datastorage_df['Classif'] = datastorage_df['Classif'].apply(lambda x: str(x.replace('like<','')+' like') if 'like' in x else x)
        # Manual and parent columns modification (separate Classsif to parent category and manual classification)
        exception_list = ['Ctenophora<Metazoa','egg<other'] # if the lower cat should go to manual classification, add the variable of corresponding Classif here
        for df_index, df_line in datastorage_df.iterrows():
            if '<' not in df_line['Classif']:
                datastorage_df.loc[df_index, 'Manual classification'] = df_line['Classif']
            else:
                lower_cat = df_line['Classif'].split('<')[0]
                higher_cat = df_line['Classif'].split('<')[1]
                if any(x in df_line['Classif'] for x in exception_list):
                    datastorage_df.loc[df_index, 'Manual classification'] = lower_cat
                elif 'artefact' in df_line['Classif']:
                    datastorage_df.drop(df_index, axis=1)
                else:
                    datastorage_df.loc[df_index, 'Manual classification'] = higher_cat
                    datastorage_df.loc[df_index, 'Developmental stage'] = lower_cat

        datastorage_df.reset_index(drop=True, inplace=True)

        #datastorage_df['Manual classification'] = datastorage_df['Classif'].apply(lambda x:x.split('<')[0] if '<' in x else x)
        #datastorage_df['Developmental stage'] = datastorage_df['Classif'].apply(lambda x:x.split('<')[1] if '<' in x else '')
        # Extract developmental stages and correct the manual classification (needed to further modify column :targetParCat)
        mask_dict = {'female':'female', 'male':'male', 'female+male':'female+male', 'CIstage':'CI', 'CIIstage':'CII', 'CIIIstage':'CIII',
                        'CIVstage':'CIV','CVstage':'CV', 'head':'head', 'middle':'middle','tail':'tail', 'nauplii':'NI-NVI', 'larvae':'larvae',
                        'calyptopsis':'calyptopis', 'female/eggs':'female with eggs', 'female with ectoparasites':'female with ectoparasites',
                        'calyptopis':'calyptopis', 'CVstage with ectoparasites':'CV with ectoparasites', 'antenna':'antenna', 'transparent':'Exuvia'}
        for old_anot, new_anot in mask_dict.items():
            if old_anot == 'transparent':
                datastorage_df.loc[datastorage_df['Manual classification'] == old_anot, 'Manual classification'] = new_anot
            else:
                datastorage_df.loc[datastorage_df['Developmental stage'] == old_anot, 'Developmental stage'] = new_anot

        # remain necessary columns
        datastorage_df = datastorage_df[['Vessel','Cruise','Station','Haul','Region','Detail_Location','Date (UTC)','Time LOKI (UTC)','Latitude','Longitude',
                                    	'Bottom depth (m)',	'Depth (m)','Temperature (°C)','Salinity (psu)','Conductivity (mS cm-1)','Oxygen concentration (µM)',
                                        'Oxygen saturation (%)','Fluorescence','Manual classification','Developmental stage','Area (pixels)','Area (mm2)','Length (mm)',
                                        'Width (mm)','Image file name','Scientist']]

        # save file to xlsx format
        meta_file_name = str('LOKI_'+datastorage_df['Station'].iloc[2]+'_'+datastorage_df['Haul'].iloc[2]+'.xlsx').replace('-', '_')
        datastorage_df.to_excel(meta_file_name, index=False)

        

def Merge_Telemetry():
    # merge telemetry data on telemetrie file as one .txt file
    #path_to_data = input('Type full path to telemetrie:')
    path_to_data = '/Users/dong/Library/Mobile Documents/com~apple~CloudDocs/Work/LOKI/Cruises/0022_PS107-22'
    work_dir = Path(path_to_data).expanduser()
    
    # loop through all Haul in one project
    for telemetrie in os.walk(work_dir):
        if 'Telemetrie' in telemetrie[1]:
            telemetrie_path = Path(os.path.join(telemetrie[0], 'Telemetrie'))
            os.chdir(telemetrie_path)

            # combine all .tmd files to one data frame
            Telemetry_df = pd.DataFrame()
            for tmd in glob.glob(str(Path(telemetrie_path)/'*.tmd')):
                tmddf = pd.read_csv(tmd, sep=';', header=None, decimal='.').iloc[:,1] # only use second column
                tmddf.loc[-1] = str(tmd).split(os.sep)[-1].split('.')[0] # add filename (= datetime) on the last row
                tmddf.sort_index(inplace=True)
                Telemetry_df = pd.concat([Telemetry_df, tmddf], axis=1)

            # Transposing row <> column and reset index
            Telemetry_df = Telemetry_df.T
            Telemetry_df = Telemetry_df.reset_index(drop=True)

            # Set column names and sort by file value (datetime)
            Telemetry_df.columns = ['file', 'DEVICE', 'GPS_LONG', 'GPS_LAT', 'PRESS', 'TEMP', 'OXY_CON', 'OXY_SAT',
                    'OXY_TEMP','COND_COND', 'COND_TEMP', 'COND_SALY', 'COND_DENS', 
                    'COND_SSPEED', 'FLOUR_1', 'LOKI_REC', 'LOKI_PIC', 
                    'LOKI_FRAME', 'CAM_STAT', 'HOUSE_STAT', 'HOUSE_T1', 'HOUSE_T2', 'HOUSE_VOLT']
            Telemetry_df = Telemetry_df.sort_values('file')

            # replace comma to point
            Telemetry_df = Telemetry_df.apply(lambda x:x.str.replace(',', '.'))

            # add Nan to empty columns
            empty_cols = [col for col in Telemetry_df.columns if Telemetry_df[col].isnull().all()]
            for col in empty_cols:
                Telemetry_df[col] = np.nan

            # save file with cruise and haul info
            cruise_name, haul_number = str(telemetrie_path).split(os.sep)[-4], re.findall('\d+', str(telemetrie_path).split(os.sep)[-3])[0]
            Telemetry_df.to_csv('%s-%s_telemetry.tsv'%(cruise_name, haul_number,), sep='\t', index=False)

            # show to result as plot
            #time = dates.date2num(Telemetry_df['Date/Time'].tolist())

            #plt.plot('PRESS', data=Telemetry_df)
            #plt.ylabel('pressure')
            #plt.xlabel('time')
            #plt.show()
            #plt.close()

if __name__ == "__main__":
    pass
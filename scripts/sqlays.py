## sql definition to import and export data

import psycopg2 as pgsql
import pandas as pd
import sqlalchemy, os
from ctdays import raw_ctd_to_df

def export_sql(database_name, edit, location):
    # export table from sql
    # cruise name (in list, case insensitive) for AWI server, 
    # table name for local
    if location == 'local':
        mydb = pgsql.connect(dbname='%s'%(database_name,), host='localhost', user='dong', password='Lava10203!')
        cur = mydb.cursor()
        df = pd.read_sql('''SELECT * FROM %s'''%(edit), mydb)
    elif location == 'awi_server':
        mydb = pgsql.connect(dbname='%s'%(database_name,), host='postgres5.awi.de', user='loki', password='DwnmdN!')
        cur = mydb.cursor()
        
        df = pd.read_sql('''SELECT v.name as vessel, c.name as cruise, 
                        s.name as station, s.region as region, s.latitude as latitude, s.longitude as longitude, s.bottom_depth as bottom_depth,
                        l.datetime as date_time,
                        l.loki_depth as loki_depth, l.temperature as temperatue, l.salinity as salinity, l.oxygen_conc as oxygen, l.fluorescence as fluorescence,
                        l.manual_classification as manual_classification, l.developmental_stage as developmental_stage, l.area_pixel as area_pixel,
                        l.area_sqrmm as area_sqrmm, l.spec_length as spec_length, l.spec_width as spec_width, l.image_filename as image_filename,
                        t.animal as animal, t.copepod as copepod, t.phylum as phylum, t.class as class, t.spec_order as spec_order,
                        t.family as family, t.genus as genus, t.species as species
                        FROM vessel v, cruise c, station s, loki_data l, taxa_group t 
                        WHERE c.id_vessel = v.id_vessel AND c.id_cruise = s.id_cruise 
                        AND s.id_station = l.id_station AND l.id_taxa_group = t.id_taxa_group
                        AND c.name ILIKE ANY ( ARRAY %s ) '''%(edit,), mydb)
    return df

def import_sql (database_name,table_name, df, replace_or_append):
    # create new table or insert on database and import the data
    engine = sqlalchemy.create_engine('postgresql+psycopg2://dong:Lava10203!@localhost/%s' %(database_name,), paramstyle='format')
    df.to_sql('%s' % (table_name,), engine, if_exists=replace_or_append, index=False, 
            dtype={col_name: sqlalchemy.types.String() for col_name in df})
    

'''

'''
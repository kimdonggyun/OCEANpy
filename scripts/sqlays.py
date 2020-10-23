## sql definition to import and export data

import psycopg2 as pgsql
import pandas as pd
import sqlalchemy, os
from ctdays import raw_ctd_to_df

def export_sql(database_name, edit, location):
    # export table from sql
    if location == 'local':
        mydb = pgsql.connect(dbname='%s'%(database_name,), host='localhost', user='dong', password='Lava10203!')
        cur = mydb.cursor()
        df = pd.read_sql('''SELECT * FROM %s'''%(edit), mydb)
    elif location == 'awi_server':
        mydb = pgsql.connect(dbname='%s'%(database_name,), host='postgres5.awi.de', user='loki', password='DwnmdN!')
        cur = mydb.cursor()
        df = pd.read_sql('''SELECT * 
                        FROM vessel v, cruise c, station s, loki_data l, taxa_group t 
                        WHERE c.id_vessel = v.id_vessel AND c.id_cruise = s.id_cruise AND s.id_station = l.id_station AND l.id_taxa_group = t.id_taxa_group
                        AND c.name ILIKE ANY ( ARRAY %s ) '''%(edit,), mydb)
    return df

def import_sql (database_name,table_name, df, replace_or_append):
    # create new table or insert on database and import the data
    engine = sqlalchemy.create_engine('postgresql+psycopg2://dong:Lava10203!@localhost/%s' %(database_name,), paramstyle='format')
    df.to_sql('%s' % (table_name,), engine, if_exists=replace_or_append, index=False, 
            dtype={col_name: sqlalchemy.types.String() for col_name in df})
    


if __name__ == "__main__":
    action = 'export'
    if action == 'export':
        edit = ['ps107'] # cruise name (in list, case insensitive) for AWI server and table name for local
        df = export_sql('loki', edit, 'awi_server')
        print(df)
      
    elif action == 'import':
        filepath = os.path.expanduser('~/Git/OCEANpy/data/loki/LOKI_station.xlsx')
        df = pd.read_excel(filepath)
        # df = raw_ctd_to_df(filepath) # processing for raw ctd file
        import_sql('loki', 'loki_meta', df, 'replace')
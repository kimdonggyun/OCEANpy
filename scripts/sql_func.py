## sql definition to import and export data

import psycopg2 as pgsql
import pandas.io.sql as sql
import sqlalchemy, os, glob
from tkinter.filedialog import askdirectory
from tkinter import Tk
from CTD_func import raw_ctd_to_df

def export_sql(database_name, table_name):
    # export table from sql
    mydb = pgsql.connect(dbname='%s'%(database_name,), host='localhost', user='dong', password='Lava10203!')
    cur = mydb.cursor()
    df = sql.read_sql('''SELECT * FROM %s'''%(table_name), mydb)
    return df

def import_sql (database_name,table_name, df, replace_or_append):
    # create new table or insert on database and import the data
    engine = sqlalchemy.create_engine('postgresql+psycopg2://dong:Lava10203!@localhost/%s' %(database_name,), paramstyle='format')
    df.to_sql('%s' % (table_name,), engine, if_exists=replace_or_append, index=False, 
                dtype={col_name: sqlalchemy.types.String() for col_name in df})


if __name__ == "__main__":


    # CTD to sql
    Tk().withdraw()
    print('choose project directory')
    path_to_data = askdirectory()

    for file_path in glob.glob(path_to_data+os.sep+'CTD*.tsv'):
        df = raw_ctd_to_df(file_path)
        import_sql('ctd', 'ctd_meta', df, 'replace')
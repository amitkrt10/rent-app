import io
import requests
import streamlit as st
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import warnings
warnings.filterwarnings("ignore")

def insert_values(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    st,write(f"{len(df)} records inserted")
    cursor.close()

HOST="ec2-34-235-31-124.compute-1.amazonaws.com"
DATABASE="d62t8amconeiot"
USER="whifrizefokwhe"
PORT="5432"
PASSWORD="784e968ef8840b240d1060a33d7740c26e729e2d7fded8eadcf5bf476b76090a"
conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

dbDf = pd.read_sql('''SELECT * FROM public.bank_statement ORDER BY transaction_date''', con=conn)
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1srCRDJ53Zf-TxQGW3jWuyG2PgM3Le46L2Jr-iCyLPWg/export?format=csv&gid=1759634673"
s = requests.get(GOOGLE_SHEET_URL).content
gsheetDf = pd.read_csv(io.StringIO(s.decode('utf-8')))

common = gsheetDf.merge(dbDf,on=['narration'])
subDf = gsheetDf[(~gsheetDf.narration.isin(common.narration))]

insert_values(conn, subDf, 'public.bank_statement')
conn.close()

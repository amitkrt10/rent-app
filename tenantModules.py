import pandas as pd
import psycopg2
import streamlit as st
import streamlit_authenticator as stauth
import warnings
warnings.filterwarnings("ignore")

@st.experimental_memo
def get_tenantInfo(flatNo):
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute(f"""select * from public.active_tenants where flat_no  = '{flatNo}'""")
    result = cursor.fetchall()
    conn.close()
    return list(result[0])

@st.experimental_memo
def get_tenantBillDf(flatNo):
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    tenantBillDf = pd.read_sql(f"""select * from public.bills where flat_no  = '{flatNo}' order by bill_month desc""", con=conn)
    tenantBillDf.set_index('bill_month',inplace=True)
    conn.close()
    return tenantBillDf

@st.experimental_memo
def get_tenantStatementDf(flatNo):
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = f'''select t_date, bill, payment,
        SUM(tempdiff) OVER (partition by flat_no ORDER BY t_date) AS dues
        from (
        select flat_no, t_date, bill, payment, bill- payment as tempdiff
        from(select flat_no, '2022-04-01' as t_date, previous_due as bill, 0 as payment from public.active_tenants where previous_due != 0 and flat_no = '{flatNo}'
        union
        select flat_no, bill_date as t_date, total as bill, 0 as payment from public.bills where flat_no = '{flatNo}'
        union
        select flat_no, payment_date as t_date, 0 as bill, amount as payment from public.payments where flat_no = '{flatNo}'
        order by 1,2) st) raw'''
    tenantStatementDf = pd.read_sql(sql, con=conn)
    conn.close()
    return tenantStatementDf

@st.experimental_memo
def get_tenantCurrentDue(flatNo):
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    sql = f"""select t.previous_due+coalesce(b.total_bill,0)-coalesce(p.total_payment,0) as dues
        from public.active_tenants t
        left join (select flat_no, sum(total) as total_bill from public.bills group by 1) b
        on t.flat_no = b.flat_no
        left join (select flat_no, sum(amount) as total_payment from public.payments group by 1) p
        on t.flat_no = p.flat_no
        where t.flat_no = '{flatNo}'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result[0][0]

@st.experimental_memo
def get_loginCredential():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute('''SELECT flat_no, username, password FROM public.active_tenants''')
    result = cursor.fetchall()
    conn.close()
    credentialList = list(map(list, zip(*result)))
    hashed_passwords = stauth.Hasher(credentialList[2]).generate()
    usernames = {}
    for i in range(len(credentialList[0])):
        usernames[credentialList[1][i]] = {"name":credentialList[0][i],"password":hashed_passwords[i]}
    credentialDict = {"usernames":usernames}
    return credentialDict
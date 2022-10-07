from unittest import result
import pandas as pd
import psycopg2
import streamlit as st
from babel.numbers import format_number
from twilio.rest import Client
import warnings
warnings.filterwarnings("ignore")

def list_diff(list1,list2):
    diff_list = []
    for x in list1:
        if x not in list2:
            diff_list.append(x)
    return diff_list

def runSql(sql):
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    conn.autocommit = True
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #Creating a database
    cursor.execute(sql)
    conn.commit()
    #Closing the connection
    conn.close()

@st.experimental_memo
def get_tenantDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    tenantDf = pd.read_sql('''SELECT * FROM public.active_tenants ORDER BY flat_no''', con=conn)
    tenantDf.set_index('flat_no',inplace=True)
    cursor = conn.cursor()
    cursor.execute('''SELECT flat_no, previous_due FROM public.active_tenants ORDER BY flat_no''')
    result = cursor.fetchall()
    initiaDueDict = {}
    for x in result:
        initiaDueDict.update({x[0]:x[1]})
    activeFlatList = list(initiaDueDict.keys())
    cursor.execute('''select flat_no from public.active_tenants where (CURRENT_DATE -  date_of_ocupancy) < 28 order by flat_no''')
    newTenant = cursor.fetchall()
    newTenant = list(map(list, zip(*newTenant)))
    conn.close()
    return tenantDf, activeFlatList, initiaDueDict, newTenant[0]

@st.experimental_memo
def get_exitTenantDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    exitTenantDf = pd.read_sql('''SELECT * FROM public.inactive_tenant order by out_date desc''', con=conn)
    exitTenantDf.set_index('flat_tenant',inplace=True)
    exitStatementDf = pd.read_sql('''select * from public.exit_statement order by flat_tenant, transaction_date''', con=conn)
    exitStatementDf.set_index('flat_tenant',inplace=True)
    conn.close()
    return exitTenantDf, exitStatementDf

@st.experimental_memo
def get_billDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    billDf = pd.read_sql('''SELECT * FROM public.bills''', con=conn)
    billDf.set_index('flat_no',inplace=True)
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT(bill_month) FROM public.bills ORDER BY 1 DESC''')
    result = cursor.fetchall()
    billMonthList = list(map(list, zip(*result)))
    conn.close()
    return billDf, billMonthList[0]

@st.experimental_memo
def get_meterDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = '''select
        flat_no,
        reading_month,
        readings
        from meter_reading
        union
        select
        flat_no,
        '00/0000' as reading_month,
        initial_meter_reading as readings
        from active_tenants
        order by 1,2'''
    meterDf = pd.read_sql(sql, con=conn)
    meterDf.set_index('flat_no',inplace=True)
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT(reading_month) FROM public.meter_reading ORDER BY 1 DESC''')
    result = cursor.fetchall()
    readingMonthList = list(map(list, zip(*result)))
    conn.close()
    return meterDf, readingMonthList[0]

@st.experimental_memo
def get_paymentDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    paymentDf = pd.read_sql('''SELECT * FROM public.payments''', con=conn)
    paymentDf.set_index('flat_no',inplace=True)
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT(payment_month) FROM public.payments ORDER BY 1 DESC''')
    result = cursor.fetchall()
    paymentMonthList = list(map(list, zip(*result)))
    conn.close()
    return paymentDf, paymentMonthList[0]

@st.experimental_memo
def get_flatDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    flatDf = pd.read_sql('''SELECT * FROM public.flats ORDER BY flat_no''', con=conn)
    flatDf.set_index('flat_no',inplace=True)
    cursor = conn.cursor()
    cursor.execute('''SELECT flat_no FROM public.flats where flat_no not in (SELECT flat_no FROM public.active_tenants) ORDER BY 1''')
    result = cursor.fetchall()
    vacantFlatList = list(map(list, zip(*result)))
    if len(vacantFlatList)==0:
        vacantFlatList = [["No Flat is Vacant!"]]
    conn.close()
    return flatDf, vacantFlatList[0]

@st.experimental_memo
def get_collectionDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = '''select
        p.payment_month,
        sum(case when p.payment_mode = 'Cash' then p.amount else 0 end) as cash,
        sum(case when p.payment_mode = 'Online Transfer' then p.amount else 0 end) as online,
        sum(case when p.payment_mode = 'Adjustment' then p.amount else 0 end) as adjustment,
        sum(p.amount) as total_payment,
        b.bill_total
        from payments p
        left join (select bill_month, sum(fulltotal) as bill_total from public.bills group by 1) b
        on p.payment_month = b.bill_month
        group by 1,6
        order by 1 desc'''
    collectionDf = pd.read_sql(sql, con=conn)
    collectionDf["ratio"] = (collectionDf["total_payment"]/collectionDf["bill_total"])*100
    collectionDf["ratio"] = collectionDf["ratio"].astype(int)
    collectionDf["ratio"] = collectionDf['ratio'].apply(lambda x: f"{x} %")
    collectionDf["cash"] = collectionDf['cash'].apply(lambda x: format_number(x, locale='en_IN'))
    collectionDf["online"] = collectionDf['online'].apply(lambda x:format_number(x, locale='en_IN'))
    collectionDf["adjustment"] = collectionDf['adjustment'].apply(lambda x: format_number(x, locale='en_IN'))
    collectionDf["total_payment"] = collectionDf['total_payment'].apply(lambda x: format_number(x, locale='en_IN'))
    collectionDf["bill_total"] = collectionDf['bill_total'].apply(lambda x: format_number(x, locale='en_IN'))
    conn.close()
    return collectionDf

@st.experimental_memo
def get_statementDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = '''select flat_no, t_date, bill, payment,
        SUM(tempdiff) OVER (partition by flat_no ORDER BY t_date) AS dues
        from (
        select flat_no, t_date, bill, payment, bill- payment as tempdiff
        from(select flat_no, '2022-04-01' as t_date, previous_due as bill, 0 as payment from public.active_tenants where previous_due != 0
        union
        select flat_no, bill_date as t_date, total as bill, 0 as payment from public.bills
        union
        select flat_no, payment_date as t_date, 0 as bill, amount as payment from public.payments
        order by 1,2) st) raw'''
    statementDf = pd.read_sql(sql, con=conn)
    statementDf.set_index('flat_no',inplace=True)
    conn.close()
    return statementDf

@st.experimental_memo
def get_currentDueDf():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = '''select t.flat_no, t.tenant_name, t.previous_due+coalesce(b.total_bill,0)-coalesce(p.total_payment,0) as dues
        from public.active_tenants t
        left join (select flat_no, sum(total) as total_bill from public.bills group by 1) b
        on t.flat_no = b.flat_no
        left join (select flat_no, sum(amount) as total_payment from public.payments group by 1) p
        on t.flat_no = p.flat_no
        order by dues desc'''
    currentDueDf = pd.read_sql(sql, con=conn)
    currentDueDf.set_index('flat_no',inplace=True)
    totalCurrentDue=currentDueDf[currentDueDf["dues"]>0]["dues"].sum()
    conn.close()
    return currentDueDf, totalCurrentDue

@st.experimental_memo
def get_exitDueDict():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    sql = '''select es.flat_tenant, es.due as mtd, it.mobile from public.exit_statement es
        left join public.inactive_tenant it on es.flat_tenant = it.flat_tenant
        where concat(es.flat_tenant,es.transaction_date) in 
        (select concat(flat_tenant,mtd) from (select flat_tenant, max(transaction_date) as mtd from public.exit_statement group by 1)mxd)
        order by 2'''
    cursor.execute(sql)
    result = cursor.fetchall()
    #Closing the connection
    conn.close()
    exitDueDict = {}
    for x in result:
        exitDueDict.update({x[0]:x[1]})
    exitDueList = []
    for x in result:
        if x[1] > 0:
            exitDueList.append([x[0].split(" | ")[0],x[0].split(" | ")[1],x[1]])
    exitTenantList = []
    for x in result:
        exitTenantList.append([x[0].split(" | ")[0],x[0].split(" | ")[1],x[2]])
    return exitDueDict, exitDueList, exitTenantList, sum(exitDueDict.values())

@st.experimental_memo
def get_consumption():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute('''select flat_no, readings from public.meter_reading order by 1, 2 desc''')
    z = cursor.fetchall()
    conn.close()
    keyList = []
    valueList = []
    tempList = []
    for i in range(len(z)):
        if i==0:
            keyList.append(z[i][0])
            tempList.append(z[i][1])
        elif z[i][0] in keyList:
            tempList.append(z[i][1])
        else:
            valueList.append(tempList)
            tempList = []
            keyList.append(z[i][0])
            tempList.append(z[i][1])
    valueList.append(tempList)
    consumptionDict = {}
    for i in range(len(keyList)):
        if len(valueList[i]) > 1:
            consumptionDict.update({keyList[i]:valueList[i][0] - valueList[i][1]})
    return dict(sorted(consumptionDict.items(), key=lambda item: item[1]))

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
    credential = list(map(list, zip(*result)))
    #Closing the connection
    conn.close()
    return credential

@st.experimental_memo
def get_bankStatement():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    sql = '''with summary as (
        select transaction_date, deposit, withdrawal, deposit - withdrawal as temp_diff, remark
        from public.bank_statement
        where account = 'PKD'
        order by transaction_date)
        select
        transaction_date, deposit, withdrawal,
        sum(temp_diff) over (order by transaction_date asc rows between unbounded preceding and current row) as balance,
        remark
        from summary'''
    bankDf = pd.read_sql(sql, con=conn)
    bankDf['deposit'] = bankDf['deposit'].apply(lambda x: format_number(int(x), locale='en_IN'))
    bankDf['withdrawal'] = bankDf['withdrawal'].apply(lambda x: format_number(int(x), locale='en_IN'))
    bankDf['balance'] = bankDf['balance'].apply(lambda x: format_number(int(x), locale='en_IN'))
    cursor = conn.cursor()
    cursor.execute("""select sum(deposit), sum(withdrawal) from public.bank_statement where account = 'PKD'""")
    depWit = cursor.fetchall()
    cursor.execute("""select sum(deposit) from public.bank_statement where account = 'PKD' and remark like '%Rent%'""")
    rentCol = cursor.fetchall()
    cursor.execute("""select sum(withdrawal) from public.bank_statement where account = 'PKD' and remark like '%Electricity%'""")
    elec = cursor.fetchall()
    cursor.execute("""select sum(withdrawal) from public.bank_statement where account = 'PKD' and remark like '%Wifi%'""")
    wifi = cursor.fetchall()
    cursor.execute("""select sum(withdrawal) from public.bank_statement where account = 'PKD' and remark like '%Ticket%'""")
    ticket = cursor.fetchall()
    cursor.execute("""select account, cast(sum(deposit)-sum(withdrawal) as int) as balance from public.bank_statement where account != 'Anita' group by account order by balance desc""")
    bankAccountDf = cursor.fetchall()
    # bankAccountDf = list(map(list, zip(*bankAccount)))
    conn.close()
    return bankDf, int(depWit[0][0]), int(depWit[0][1]), int(rentCol[0][0]), int(elec[0][0]), int(wifi[0][0]), int(ticket[0][0]), bankAccountDf

@st.experimental_memo
def get_tenantInfo():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    cursor.execute("""select flat_no, tenant_name, mobile, security_deposite, rent_amount, water_charge, garbage_charge, date_of_ocupancy from public.active_tenants""")
    result = cursor.fetchall()
    conn.close()
    tenantInfoDict = {}
    for x in result:
        tenantInfoDict[x[0]]=x[1:]
    return tenantInfoDict

@st.experimental_memo
def get_whatsappData():
    # read the connection parameters
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    # connect to the PostgreSQL server
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cursor = conn.cursor()
    sql = """select t.flat_no, t.tenant_name, t.mobile, t.previous_due+coalesce(b.total_bill,0)-coalesce(p.total_payment,0) as dues
        from public.active_tenants t
        left join (select flat_no, sum(total) as total_bill from public.bills group by 1) b
        on t.flat_no = b.flat_no
        left join (select flat_no, sum(amount) as total_payment from public.payments group by 1) p
        on t.flat_no = p.flat_no
        order by t.flat_no"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    whatsappData = {}
    for x in result:
        whatsappData[x[0]]=x[1:]
    return whatsappData

# def send_whatsapp_msg(body,mobile):
#     mobile=8918104083
#     TWILIO_SSID=st.secrets["TWILIO_SSID"]
#     TWILIO_API_KEY=st.secrets["TWILIO_API_KEY"]
#     client = Client(TWILIO_SSID,TWILIO_API_KEY)
#     client.messages.create(body=body,from_='whatsapp:+14155238886',to=f'whatsapp:+91{mobile}')
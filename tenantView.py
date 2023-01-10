import streamlit as st
import tenantModules as tm
import appPlots as ap
import pandas as pd
import streamlit_authenticator as stauth
from babel.numbers import format_number
import warnings
warnings.filterwarnings("ignore")

# Configure app display
st.set_page_config(
    page_title="Kartikey Bhawan",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state='collapsed'
)
def add_stream_url(phone_num):
	return [f'tel:+91{n}' for n in phone_num]

def make_clickable(url):
    text = url[-10:]
    return f'<a target="_blank" href="{url}">{text}</a>'

st.markdown("<h1 style='text-align: center;text-shadow: 3px 2px RED;font-style: oblique;'>KARTIKEY BHAWAN</h1>", unsafe_allow_html=True)

credentialDict = tm.get_loginCredential()

authenticator = stauth.Authenticate(credentialDict,"tenant_signature_name","tenant_cookie_key",365,"amitkrt10@gmail.com")
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    flatNo = st.session_state["name"]
    with st.spinner(text='Reading Data... Please Wait...!'):
        tenantInfo = tm.get_tenantInfo(flatNo)
        tenantBillDf = tm.get_tenantBillDf(flatNo)
        tenantStatementDf = tm.get_tenantStatementDf(flatNo)
        tenantCurrentDue = tm.get_tenantCurrentDue(flatNo)
        st.balloons()

    st.write(f"Wecome **{tenantInfo[1]}**")

    #Current Due
    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px red;font-style: oblique;color:yellow;'>Current Due = ₹ {format_number(tenantCurrentDue, locale='en_IN')}</h3>", unsafe_allow_html=True)

    try:
        #Bills
        st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>View Bills</h3>", unsafe_allow_html=True)
        billMonth = st.selectbox("Select Rent Month", list(tenantBillDf.index))
        tempBillList = list(tenantBillDf[tenantBillDf.index==billMonth].values[0])
        cellText = []
        cellText.append(["Rent",tempBillList[2]])
        cellText.append(["Electricity",tempBillList[5]])
        if tempBillList[3] != 0:
            cellText.append(["Water Charge",tempBillList[3]])
        cellText.append(["Garbage",tempBillList[4]])
        if tempBillList[6] != 0:
            cellText.append(["Previous Due",tempBillList[6]])
        cellText.append(["Total",tempBillList[8]])
        column_headers = [flatNo,billMonth]
        colWidths = [1,1]
        scaleY = 5
        headerFontSize = 30
        cellFontSize = 30
        alignList = ['left','right']
        ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
    except:
        pass

    #Statement
    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Statement</h3>", unsafe_allow_html=True)
    tempStatementList = ['Total',tenantStatementDf["bill"].sum(),tenantStatementDf["payment"].sum(),tenantStatementDf["bill"].sum()-tenantStatementDf["payment"].sum()]
    tenantStatementDf.loc[len(tenantStatementDf.index)] = tempStatementList
    column_headers = ['Date','Bills','Payments','Dues']
    cellText = tenantStatementDf.values
    colWidths = [1,1,1,1]
    scaleY = 9
    headerFontSize = 40
    cellFontSize = 40
    alignList = ['center','right','right','right']
    ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Tenant Info
    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Your Information</h3>", unsafe_allow_html=True)
    column_headers = ['Name', tenantInfo[1]]
    cellText = []
    cellText.append(['Flat No.', flatNo])
    cellText.append(['Mobile', tenantInfo[2]])
    cellText.append(['Security Deposite', f'₹ {tenantInfo[3]}'])
    cellText.append(['Rent', f'₹ {tenantInfo[4]}'])
    cellText.append(['Water Charge', f'₹ {tenantInfo[5]}'])
    cellText.append(['Garbage Charge', f'₹ {tenantInfo[6]}'])
    cellText.append(['Electricity Charge', '₹ 10 / unit'])
    cellText.append(['Date of Occupancy', tenantInfo[9]])
    colWidths = [1,1]
    scaleY = 6
    headerFontSize = 30
    cellFontSize = 30
    alignList = ['left','right']
    ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    pd.set_option('display.max_colwidth', -1)

    #Service Providers
    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Service Providers</h3>", unsafe_allow_html=True)
    data = {'Name':['Bijay','Bapan','Ashok Kaku','Meghnath'],
            'Number':[7501077783,9641223532,9933761483,9832696055]}
    df = pd.DataFrame(data, index=['Electrician','Plumber','Painter','Carpenter'])
    df['Phone'] = add_stream_url(df['Number'])
    df['Phone'] = df['Phone'].apply(make_clickable)
    st.write(df[['Name','Phone']].to_html(escape = False), unsafe_allow_html = True)
    st.error("Please inform the owner before making any changes or repair to the property")

    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Owner Details</h3>", unsafe_allow_html=True)
    data = {'Name':['RN Thakur','Amit','Santosh'],
            'Number':[7005143261,8918104083,9036023003]}
    df1 = pd.DataFrame(data, index=[1,2,3])
    df1['Phone'] = add_stream_url(df1['Number'])
    df1['Phone'] = df1['Phone'].apply(make_clickable)
    st.write(df1[['Name','Phone']].to_html(escape = False), unsafe_allow_html = True)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

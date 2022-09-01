import streamlit as st
import tenantModules as tm
import appPlots as ap
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

st.markdown("<h1 style='text-align: center;text-shadow: 3px 2px RED;font-style: oblique;'>KARTIKEY BHAWAN</h1>", unsafe_allow_html=True)

credentialDict = tm.get_loginCredential()

authenticator = stauth.Authenticate(credentialDict,"tenant_signature_name","tenant_cookie_key",0,"immy.brat@gmail.com")
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    flatNo = st.session_state["name"]
    st.write(flatNo)
    with st.spinner(text='Reading Data... Please Wait...!'):
        st.session_state["tenantInfo"] = tm.get_tenantInfo(flatNo)
        st.session_state["tenantBillDf"] = tm.get_tenantBillDf(flatNo)
        st.session_state["tenantStatementDf"] = tm.get_tenantStatementDf(flatNo)
        st.session_state["tenantCurrentDue"] = tm.get_tenantCurrentDue(flatNo)
        tenantInfo = st.session_state["tenantInfo"]
        tenantBillDf = st.session_state["tenantBillDf"]
        tenantStatementDf = st.session_state["tenantStatementDf"]
        tenantCurrentDue = st.session_state["tenantCurrentDue"]
        st.balloons()

    st.write(f"Wecome **{tenantInfo[1]}**")

    #Current Due
    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px red;font-style: oblique;color:yellow;'>Current Due = ₹ {format_number(tenantCurrentDue, locale='en_IN')}</h3>", unsafe_allow_html=True)

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
    colWidths = [1,1,1,1]
    scaleY = 6
    headerFontSize = 30
    cellFontSize = 30
    alignList = ['left','right']
    ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
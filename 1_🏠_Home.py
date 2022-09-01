import streamlit as st
import adminModules as am
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

hashed_passwords = stauth.Hasher([st.secrets["LPASSWORD"]]).generate()
credentials = {"usernames":{st.secrets["USERNAME"]:{"name":st.secrets["NAME"],"password":hashed_passwords[0]}}}
authenticator = stauth.Authenticate(credentials,"some_signature_key","some_cookie_name",30,"amitkrt10@gmail.com")
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    if "login" not in st.session_state:
        st.session_state["login"] = True
    with st.spinner(text='Reading Data... Please Wait...!'):
        st.session_state["bankDf"], st.session_state["totalDeposite"], st.session_state["totalWithdraw"], st.session_state["rentCollection"], st.session_state["electricityExpense"], st.session_state["wifiExpense"], st.session_state["travelDeposite"] = am.get_bankStatement()
        st.session_state["tenantDf"], st.session_state["activeFlatList"], st.session_state["initiaDueDict"] = am.get_tenantDf()
        st.session_state["billDf"], st.session_state["billMonthList"] = am.get_billDf()
        st.session_state["paymentDf"], st.session_state["paymentMonthList"] = am.get_paymentDf()
        st.session_state["meterDf"], st.session_state["readingMonthList"] = am.get_meterDf()
        st.session_state["statementDf"] = am.get_statementDf()
        st.session_state["exitDueDict"], st.session_state["exitDueList"], st.session_state["exitTenantList"], st.session_state["exitDueTotal"] = am.get_exitDueDict()
        st.session_state["exitTenantDf"], st.session_state["exitStatementDf"] = am.get_exitTenantDf()
        st.session_state["collectionDf"] = am.get_collectionDf()
        st.session_state["currentDueDf"], st.session_state["totalCurrentDue"] = am.get_currentDueDf()
        st.session_state["consumptionDict"] = am.get_consumption()
        st.session_state["flatDf"], st.session_state["vacantFlatList"] = am.get_flatDf()
        st.session_state["bankDf"], st.session_state["totalDeposite"], st.session_state["totalWithdraw"], st.session_state["rentCollection"], st.session_state["electricityExpense"], st.session_state["wifiExpense"], st.session_state["travelDeposite"] = am.get_bankStatement()
        collectionDf = st.session_state["collectionDf"]
        currentDueDf, totalCurrentDue = st.session_state["currentDueDf"], st.session_state["totalCurrentDue"]
        exitDueDict, exitDueList, exitTenantList, exitDueTotal = st.session_state["exitDueDict"], st.session_state["exitDueList"], st.session_state["exitTenantList"], st.session_state["exitDueTotal"]
        st.balloons()

    # Current Dues
    currentDueDf.loc[len(currentDueDf.index)] = ["Total",totalCurrentDue]
    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Current Dues = ₹ {format_number(totalCurrentDue, locale='en_IN')}</h3>", unsafe_allow_html=True)
    #Show Table
    column_headers = ['Flat','Tenant Name','Dues']
    cellText = currentDueDf[currentDueDf["dues"]>0].to_records()
    colWidths = [1,3,2]
    scaleY = 15
    headerFontSize = 80
    cellFontSize = 70
    alignList = ['center','left','right']
    ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Monthly Collection
    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Monthly Collection</h3>", unsafe_allow_html=True)
    #show Table
    column_headers = ['Month','Cash','Online','Adjust','Payment','Billed','Collection']
    cellText = collectionDf.values
    colWidths = [1,1,1,1,1,1,1]
    scaleY = 15
    headerFontSize = 60
    cellFontSize = 70
    alignList = ['center','right','right','right','right','right','right']
    ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Exit Dues
    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Exit Tenants Dues = ₹ {format_number(exitDueTotal, locale='en_IN')}</h3>", unsafe_allow_html=True)
    column_headers = ['Flat','Tenant Name','Dues']
    cellText = exitDueList+ [['Total',"",exitDueTotal]]
    colWidths = [1,3,2]
    scaleY = 15
    headerFontSize = 80
    cellFontSize = 70
    alignList = ['center','left','right']
    ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
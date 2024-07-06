import streamlit as st
from datetime import date
import dateutil.relativedelta
import adminModules as am
import time
import warnings
warnings.filterwarnings("ignore")

# Configure app display
st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed'
)
st.markdown("<h1 style='text-align: center;text-shadow: 3px 2px RED;font-style: oblique;'>KARTIKEY BHAWAN</h1>", unsafe_allow_html=True)

if "login" in st.session_state.keys():
    with st.spinner(text='Reading Data... Please Wait...!'):
        tenantDf, activeFlatList = st.session_state["tenantDf"], st.session_state["activeFlatList"]
        currentDueDf = st.session_state["currentDueDf"]

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Payments</h2>", unsafe_allow_html=True)
    am.get_header('Payments')

    #Payments
    with st.expander("Recieved Payments"):
        flatNo = st.selectbox("Flat No.",activeFlatList)
        st.write(f"{tenantDf[tenantDf.index==flatNo]['tenant_name'].values[0]} | ₹ {currentDueDf[currentDueDf.index==flatNo]['dues'].values[0]}")
        with st.form("Recieved Payments",clear_on_submit=True):
            paymentDate = st.date_input("Payment Date")
            amount = st.text_input("Payment Amount")
            mode = st.radio("Payment Mode",["Cash","Online Transfer","Adjustment"],horizontal=True)
            submitted = st.form_submit_button("Submit")
            if submitted:
                paymentMonth = (paymentDate- dateutil.relativedelta.relativedelta(months=1)).strftime("%Y/%m")
                am.runSql(f"""INSERT INTO public.payments(flat_no, payment_date, payment_month, amount, payment_mode) VALUES ('{flatNo}','{paymentDate}','{paymentMonth}','{amount}','{mode}')""")
                st.write(f"₹ {amount} recieved from {tenantDf[tenantDf.index==flatNo]['tenant_name'].values[0]} by {mode}")
                time.sleep(3)
                am.get_paymentDf.clear()
                am.get_collectionDf.clear()
                am.get_statementDf.clear()
                am.get_currentDueDf.clear()
                am.get_whatsappData.clear()
                am.get_otherCharges.clear()
                st.session_state["paymentDf"], st.session_state["paymentMonthList"] = am.get_paymentDf()
                st.session_state["collectionDf"] = am.get_collectionDf()
                st.session_state["statementDf"] = am.get_statementDf()
                st.session_state["currentDueDf"], st.session_state["totalCurrentDue"] = am.get_currentDueDf()
                st.session_state["whatsappData"] = am.get_whatsappData()
                st.session_state["otherChargesDf"] = am.get_otherCharges()
                st.experimental_rerun()

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

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
        st.balloons()

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Payments</h2>", unsafe_allow_html=True)

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
                paymentMonth = (paymentDate- dateutil.relativedelta.relativedelta(months=1)).strftime("%m/%Y")
                am.runSql(f"""INSERT INTO public.payments(flat_no, payment_date, payment_month, amount, payment_mode) VALUES ('{flatNo}','{paymentDate}','{paymentMonth}','{amount}','{mode}')""")
                st.write(f"₹ {amount} recieved from {tenantDf[tenantDf.index==flatNo]['tenant_name'].values[0]} by {mode}")
                time.sleep(3)
                st.experimental_memo.clear()
                st.experimental_rerun()

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://amitkrt10-rent-app-1--home-8wtbg6.streamlitapp.com/)")

import streamlit as st
from datetime import date
import dateutil.relativedelta
import adminModules as am
import time
from babel.numbers import format_number
from urllib.parse import quote
import appPlots as ap
# import pywhatkit
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
        otherChargesDf = st.session_state["otherChargesDf"]
        st.balloons()

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Other Charges</h2>", unsafe_allow_html=True)

    # other charges
    with st.expander("Enter Other Chages"):
        selectedFlatOC = st.selectbox("Select Flat No.",activeFlatList+["Select"],index=len(activeFlatList+["Select"])-1,key="OtherChages")
        if selectedFlatOC == "Select":
            st.write("Select a flat!")
        else:
            with st.form("Other Chages",clear_on_submit=True):
                chargeDate = st.date_input("Charge Date")
                amount = st.text_input("Amount")
                remark = st.text_input("Remark")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    chargeMonth = (chargeDate.strftime("%Y/%m"))
                    am.runSql(f"""INSERT INTO public.other_charges(flat_no,charge_date,charge_month,amount,remark) VALUES ('{selectedFlatOC}','{chargeDate}','{chargeMonth}','{amount}','{remark}')""")
                    st.write(f'₹ {amount} added to {selectedFlatOC} for {remark}')
                    time.sleep(3)
                    am.get_otherCharges.clear()
                    st.session_state["otherChargesDf"] = am.get_otherCharges()
                    st.experimental_rerun()

    with st.expander("Other Chages Statement"):
        column_headers = ['Flat No.','Date','Amount','Remark']
        cellText = otherChargesDf.values
        colWidths = [1,2,1,3]
        scaleY = 15
        headerFontSize = 60
        cellFontSize = 70
        alignList = ['center','center','right','left']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
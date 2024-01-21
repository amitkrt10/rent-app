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

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Notes</h2>", unsafe_allow_html=True)

    st.markdown("_<h4> Flat No: 003 AIHM </h4>_", unsafe_allow_html=True)
    columns_003 = ['From', 'To', 'Rent Amount']
    data_003 = [
        ['2023-08-15', '2024-06-30', 17000],
        ['2024-07-01', '2025-05-31', 18500],
        ['2025-06-01', '2028-02-29', 20000],
        ['2028-03-01', 'Every 11 Month', '+5%']
    ]
    column_headers = columns_003
    cellText = data_003
    colWidths = [1,1,1]
    scaleY = 10
    headerFontSize = 35
    cellFontSize = 35
    alignList = ['center','center','center']
    ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
    
    st.markdown("_<h4> Flat No: 201 ABN Network </h4>_", unsafe_allow_html=True)
    columns_201 = ['From', 'To', 'Rent Amount']
    data_201 = [
        ['2023-06-01', '2024-04-30', 20000],
        ['2024-05-01', '2025-03-31', 25000],
        ['2025-04-01', 'Onwards', 30000]
    ]
    column_headers = columns_201
    cellText = data_201
    colWidths = [1,1,1]
    scaleY = 10
    headerFontSize = 35
    cellFontSize = 35
    alignList = ['center','center','center']
    ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    st.write("Rs 35000 due for the furnitures.")
    


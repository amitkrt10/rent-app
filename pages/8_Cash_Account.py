import streamlit as st
from babel.numbers import format_number
import plotly.graph_objects as go
import appPlots as ap
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
        cashCredit, cashDebit = st.session_state["cashCredit"],st.session_state["cashDebit"]
        st.balloons()
    
    credit = cashCredit["Amount"].sum()
    debit = cashDebit["Amount"].sum()
    cashInHand = credit - debit
    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Cash in Hand = ₹ {format_number(cashInHand, locale='en_IN')}</h3>", unsafe_allow_html=True)
    st.write(f"Cash Credit = ₹ {credit}")
    st.write(f"Cash Debit = ₹ {debit}")
    
    with st.expander("Cash Credit"):
        column_headers = ["Date","Credit","Remarks"]
        cellText = cashCredit.values
        colWidths = [1,1,3]
        scaleY = 10
        headerFontSize = 70
        cellFontSize = 50
        alignList = ['left','right','left']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    with st.expander("Cash Debit"):
        column_headers = ["Date","Debit","Remarks"]
        cellText = cashDebit.values
        colWidths = [1,1,3]
        scaleY = 10
        headerFontSize = 70
        cellFontSize = 50
        alignList = ['left','right','left']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
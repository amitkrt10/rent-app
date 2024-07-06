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
am.get_header1()

if "login" in st.session_state.keys():
    with st.spinner(text='Reading Data... Please Wait...!'):
        cashCredit, cashDebit = st.session_state["cashCredit"],st.session_state["cashDebit"]
    
    credit = cashCredit["Amount"].sum()
    debit = cashDebit["Amount"].sum()
    cashInHand = credit - debit
    # st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Cash in Hand = ₹ {format_number(cashInHand, locale="en_IN")}</h3>", unsafe_allow_html=True)
    am.get_header(f'Cash in Hand = ₹ {format_number(cashInHand, locale="en_IN")}')
    # st.write(f"Cash Credit = ₹ {credit}")
    # st.write(f"Cash Debit = ₹ {debit}")
    #Show Table
    column_headers = ['Credit','Debit']
    cellText = [[f"₹ {format_number(credit, locale="en_IN")}",f"₹ {format_number(debit, locale="en_IN")}"]]
    colWidths = [1,1]
    scaleY = 8
    headerFontSize = 50
    cellFontSize = 30
    alignList = ['center','center']
    ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
    
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
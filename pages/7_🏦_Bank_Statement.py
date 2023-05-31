import streamlit as st
from babel.numbers import format_number
import plotly.graph_objects as go
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
        bankDf, totalDeposite, totalWithdraw, rentCollection, electricityExpense, wifiExpense, travelDeposite = st.session_state["bankDf"], st.session_state["totalDeposite"], st.session_state["totalWithdraw"], st.session_state["rentCollection"], st.session_state["electricityExpense"], st.session_state["wifiExpense"], st.session_state["travelDeposite"]
        bankDf_j, totalDeposite_j, totalWithdraw_j, rentCollection_j, electricityExpense_j, wifiExpense_j, travelDeposite_j = st.session_state["bankDf_j"], st.session_state["totalDeposite_j"], st.session_state["totalWithdraw_j"], st.session_state["rentCollection_j"], st.session_state["electricityExpense_j"], st.session_state["wifiExpense_j"], st.session_state["travelDeposite_j"]
        st.balloons()

    st.markdown(f"<h3 style='text-align: center;text-shadow: 3px 2px red;font-style: oblique;color:yellow;'>Bank Balance = ₹ {format_number(((totalDeposite+totalDeposite_j) - (totalWithdraw+totalWithdraw_j)), locale='en_IN')}</h3>", unsafe_allow_html=True)
    # with st.expander("View Break-Ups"):
    #     st.metric("Deposits",f"₹ {format_number((totalDeposite+totalDeposite_j), locale='en_IN')}")
    #     st.metric("Withdrawals",f"₹ {format_number((totalWithdraw+totalWithdraw_j), locale='en_IN')}")
    #     st.metric("Rent Collection",f"₹ {format_number((rentCollection+rentCollection_j), locale='en_IN')}")
    #     st.metric("Electricity Expense",f"₹ {format_number((electricityExpense+electricityExpense_j), locale='en_IN')}")
    #     st.metric("Wifi Expense",f"₹ {format_number((wifiExpense+electricityExpense_j), locale='en_IN')}")
    #     st.metric("Travel Expense",f"₹ {format_number((travelDeposite+travelDeposite_j), locale='en_IN')}")

    st.markdown("<h3 style='text-align: center;text-shadow: 3px 2px gray;font-style: oblique;'>Bank Statement</h3>", unsafe_allow_html=True)
    with st.expander(f"HDFC Bank Statement : {format_number((totalDeposite - totalWithdraw), locale='en_IN')}"):
        #Show Table
        lendf = len(bankDf)
        fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4,5],
        columnwidth = [30,25,25,25,80],
        header = dict(
            values = [['<b>Date</b>'],
                        ['<b>Credit</b>'],
                        ['<b>Debit</b>'],
                        ['<b>Balance</b>'],
                        ['<b>Remark</b>']],
            line_color='darkslategray',
            fill_color='royalblue',
            align='center',
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=bankDf.tail(15).T.values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white', 'white', '#8AD88D', '#EAECEE']),
            align=['right', 'right', 'right', 'right', 'left'],
            font=dict(color='black', size=10),
            height=30)
            )
        ]
        #layout=go.Layout(title=go.layout.Title(text=f"<b>{tenantName}</b> | Flat No. : <b>{flatNo}</b>"))
        )
        fig.update_layout(width=370, height=(100+((15+2)*30)), margin=dict(l=0, r=0, t=50, b=0))
        st.write(fig)

        csv = bankDf.to_csv(index=False).encode('utf-8')
        fileName = "hdfc_bank_statement.csv"
        st.download_button("Download Statement", csv, fileName, "text/csv", key="download")

    with st.expander(f"JANA Bank Statement : {format_number((totalDeposite_j - totalWithdraw_j), locale='en_IN')}"):
        #Show Table
        lendf = len(bankDf_j)
        fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4,5],
        columnwidth = [30,25,25,25,80],
        header = dict(
            values = [['<b>Date</b>'],
                        ['<b>Credit</b>'],
                        ['<b>Debit</b>'],
                        ['<b>Balance</b>'],
                        ['<b>Remark</b>']],
            line_color='darkslategray',
            fill_color='royalblue',
            align='center',
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=bankDf_j.tail(15).T.values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white', 'white', '#8AD88D', '#EAECEE']),
            align=['right', 'right', 'right', 'right', 'left'],
            font=dict(color='black', size=10),
            height=30)
            )
        ]
        #layout=go.Layout(title=go.layout.Title(text=f"<b>{tenantName}</b> | Flat No. : <b>{flatNo}</b>"))
        )
        fig.update_layout(width=370, height=(100+((15+2)*30)), margin=dict(l=0, r=0, t=50, b=0))
        st.write(fig)

        csv = bankDf.to_csv(index=False).encode('utf-8')
        fileName = "jana_bank_statement.csv"
        st.download_button("Download Statement", csv, fileName, "text/csv", key="download_j")

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

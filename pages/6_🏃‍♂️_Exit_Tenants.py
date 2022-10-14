import streamlit as st
import adminModules as am
import appPlots as ap
from babel.numbers import format_number
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
        exitDueDict, exitTenantList = st.session_state["exitDueDict"], st.session_state["exitTenantList"]
        exitTenantDf, exitStatementDf = st.session_state["exitTenantDf"], st.session_state["exitStatementDf"]
        st.balloons()

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Exit Tenants</h2>", unsafe_allow_html=True)

    with st.expander("Inactive Tenants"):
        column_headers = ["Flat","Tenant Name","Contact"]
        cellText = exitTenantList
        colWidths = [1,3,2]
        scaleY = 15
        headerFontSize = 100
        cellFontSize = 80
        alignList = ['center','left','center']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    # Exit Tenants Payments
    with st.expander("Recieved Payments of Exit Tenants"):
        with st.form("Recieved Payments of Exit Tenants",clear_on_submit=True):
            flatTenant = st.selectbox("Flat No.",exitDueDict.keys())
            paymentDate = st.date_input("Payment Date")
            amount = st.text_input("Payment Amount")
            submitted = st.form_submit_button("Submit")
            if submitted:
                finalDue = exitDueDict[flatTenant]-int(amount)
                am.runSql(f"""INSERT INTO public.exit_statement (flat_tenant, transaction_date, bill, payment, due) VALUES ('{flatTenant}','{paymentDate}','0','{amount}','{finalDue}')""")
                st.write(f"{amount} recieved from {flatTenant}")
                time.sleep(3)
                st.experimental_memo.clear()
                st.experimental_rerun()

    #View Final Exit Bills
    with st.expander("View Final Exit Bills"):
        selectFlatTenant = st.selectbox("Select Flat No.",exitDueDict.keys(),key="viewexitbill")
        tempExitViewList = list(exitTenantDf[exitTenantDf.index==selectFlatTenant].values[0])

        cellText = []
        cellText.append(["Rent",tempExitViewList[4]])
        cellText.append(["Electricity",tempExitViewList[5]])
        if tempExitViewList[6] != 0:
            cellText.append(["Water",tempExitViewList[6]])
        cellText.append(["Garbage",tempExitViewList[7]])
        if tempExitViewList[8] != 0:
            cellText.append([tempExitViewList[11],tempExitViewList[8]])
        if tempExitViewList[12] != 0:
            cellText.append(["Previous Due",tempExitViewList[12]])
        cellText.append(["Security Deposite (-)",tempExitViewList[9]])
        cellText.append(["Total",tempExitViewList[10]])


        column_headers = [selectFlatTenant.split(" | ")[1],selectFlatTenant.split(" | ")[0]]
        colWidths = [2,1]
        scaleY = 6
        headerFontSize = 40
        cellFontSize = 40
        alignList = ['left','right']
        ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    # Exit Tenants Payments
    with st.expander("Exit Tenants Statement"):
        selectFlatTenant = st.selectbox("Select Flat No.",list(exitDueDict.keys())+["Select"],index=len(exitDueDict.keys())-1,key="viewexitStatement")
        if selectFlatTenant == "Select":
            st.write("Select a flat!")
        else:
            tempExitStatementDf = exitStatementDf[exitStatementDf.index==selectFlatTenant]
            tempBill = tempExitStatementDf["bill"].sum()
            tempPay = tempExitStatementDf["payment"].sum()
            tempExitStatementDf.loc[len(tempExitStatementDf.index)] = ["Total",tempBill,tempPay,tempBill-tempPay]
            tempExitStatementDf["bill"] = tempExitStatementDf['bill'].apply(lambda x: format_number(x, locale='en_IN'))
            tempExitStatementDf["payment"] = tempExitStatementDf['payment'].apply(lambda x: format_number(x, locale='en_IN'))
            tempExitStatementDf["due"] = tempExitStatementDf['due'].apply(lambda x: format_number(x, locale='en_IN'))
            column_headers = ['Date','Bills','Payments','Dues']
            cellText = tempExitStatementDf.values
            colWidths = [1,1,1,1]
            scaleY = 6
            headerFontSize = 40
            cellFontSize = 40
            alignList = ['center','right','right','right']
            ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

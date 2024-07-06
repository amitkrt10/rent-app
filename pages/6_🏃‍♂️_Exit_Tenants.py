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
am.get_header1()

if "login" in st.session_state.keys():
    with st.spinner(text='Reading Data... Please Wait...!'):
        exitDueDict, exitTenantList = st.session_state["exitDueDict"], st.session_state["exitTenantList"]
        exitTenantDf, exitStatementDf = st.session_state["exitTenantDf"], st.session_state["exitStatementDf"]
        tenantDf, activeFlatList = st.session_state["tenantDf"], st.session_state["activeFlatList"]
        currentDueDf = st.session_state["currentDueDf"]
        meterDf = st.session_state["meterDf"]

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Exit Tenants</h2>", unsafe_allow_html=True)
    am.get_header('Exit Tenants')

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
                am.get_exitTenantDf.clear()
                am.get_exitDueDict.clear()
                st.session_state["exitTenantDf"], st.session_state["exitStatementDf"] = am.get_exitTenantDf()
                st.session_state["exitDueDict"], st.session_state["exitDueList"], st.session_state["exitTenantList"], st.session_state["exitDueTotal"] = am.get_exitDueDict()
                st.experimental_rerun()

    #View Final Exit Bills
    with st.expander("View Final Exit Bills"):
        sortedExitTenants = list(exitDueDict.keys())
        sortedExitTenants.sort()
        selectFlatTenant = st.selectbox("Select Flat No.",sortedExitTenants,key="viewexitbill")
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

    # Exit Tenants Statement
    with st.expander("Exit Tenants Statement"):
        sortedExitTenants = list(exitDueDict.keys())
        sortedExitTenants.sort()
        selectFlatTenant = st.selectbox("Select Flat No.",sortedExitTenants+["Select"],index=len(exitDueDict.keys()),key="viewexitStatement")
        if selectFlatTenant == "Select":
            st.write("Select a flat!")
        else:
            tempExitStatementDf = exitStatementDf[exitStatementDf.index==selectFlatTenant]
            tempBill = tempExitStatementDf["bill"].sum()
            tempPay = tempExitStatementDf["payment"].sum()
            tempExitStatementDf.loc[len(tempExitStatementDf.index)] = ["Total",tempBill,tempPay,tempBill-tempPay]
            tempExitStatementDf["bill"] = tempExitStatementDf['bill'].apply(lambda x: format_number(x, locale="en_IN"))
            tempExitStatementDf["payment"] = tempExitStatementDf['payment'].apply(lambda x: format_number(x, locale="en_IN"))
            tempExitStatementDf["due"] = tempExitStatementDf['due'].apply(lambda x: format_number(x, locale="en_IN"))
            column_headers = ['Date','Bills','Payments','Dues']
            cellText = tempExitStatementDf.values
            colWidths = [1,1,1,1]
            scaleY = 6
            headerFontSize = 40
            cellFontSize = 40
            alignList = ['center','right','right','right']
            ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Remove Tenant Calculation
    with st.expander("Exit Calculation"):
        selectedFlat = st.selectbox("Select Flat No.",activeFlatList,key="removetenant_calc")
        tenantName = currentDueDf[currentDueDf.index==selectedFlat]['tenant_name'].values[0]
        currentDue = currentDueDf[currentDueDf.index==selectedFlat]['dues'].values[0]
        tenantSecurity = tenantDf[tenantDf.index==selectedFlat]['security_deposite'].values[0]
        st.write(f"{tenantName} | Previous Due = ₹ {currentDue} | Secirity Deposite = ₹ {tenantSecurity}")
        with st.form("Final Settlement",clear_on_submit=True):
            rentAmt = st.text_input("Rent Amount",tenantDf[tenantDf.index==selectedFlat]["rent_amount"].values[0])
            finalMeterReading = st.text_input("Final Meter Reading")
            waterCharge = st.text_input("Water Charge",tenantDf[tenantDf.index==selectedFlat]["water_charge"].values[0])
            garbageCharge = st.text_input("Garbage Charge",20)
            otherCharges = st.text_input("Other Charge")
            remark = st.text_input("Remark")
            exitDate = st.date_input("Exit Date")
            submitted = st.form_submit_button("Submit")
            if submitted:
                meterCharge = (int(finalMeterReading) - meterDf[meterDf.index==selectedFlat]["readings"].max()) * 10
                finalDue = int(rentAmt) + int(meterCharge) + int(waterCharge) + int(garbageCharge) + int(otherCharges) + currentDue - tenantSecurity

                cellText = []
                cellText.append(["Rent",rentAmt])
                cellText.append(["Electricity",meterCharge])
                if waterCharge != 0:
                    cellText.append(["Water",waterCharge])
                if garbageCharge != 0:
                    cellText.append(["Garbage",garbageCharge])
                if otherCharges != 0:
                    cellText.append([remark,otherCharges])
                if currentDue != 0:
                    cellText.append(["Previous Due",currentDue])
                cellText.append(["Security Deposite (-)",tenantSecurity])
                cellText.append(["Total",finalDue])

                column_headers = [tenantName,selectedFlat]
                colWidths = [2,1]
                scaleY = 6
                headerFontSize = 40
                cellFontSize = 40
                alignList = ['left','right']
                ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

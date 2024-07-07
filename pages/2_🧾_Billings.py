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
am.get_header1()

if "login" in st.session_state.keys():
    with st.spinner(text='Reading Data... Please Wait...!'):
        tenantDf, activeFlatList = st.session_state["tenantDf"], st.session_state["activeFlatList"]
        billDf, billMonthList = st.session_state["billDf"], st.session_state["billMonthList"]
        paymentDf = st.session_state["paymentDf"]
        meterDf, readingMonthList = st.session_state["meterDf"], st.session_state["readingMonthList"]
        statementDf = st.session_state["statementDf"]
        newTenantFlats = st.session_state["newTenantFlats"]
        whatsappData = st.session_state["whatsappData"]

    upBillingDate = date.today() - dateutil.relativedelta.relativedelta(months=1)
    upBillingMonth = upBillingDate.strftime("%Y/%m")

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Billings</h2>", unsafe_allow_html=True)
    am.get_header('Billings')

    #Create Bills
    with st.expander(f"Create Bills for {upBillingMonth}"):
        if upBillingMonth in billMonthList:
            st.write(f"Bills already created for {upBillingMonth}")
        else:
            if upBillingMonth not in readingMonthList:
                st.write(f"Take meter reading for {upBillingMonth} first")
            else:
                if len(newTenantFlats)>0:
                    st.write("Bill days for new tenant")
                    for x in newTenantFlats:
                        st.text_input(f"No. of days for {x}",key=f"{x}factor")
                if st.button(f"Create for {upBillingMonth}"):
                    for x in activeFlatList:
                        try:
                            rentAmt = tenantDf[tenantDf.index==x]["rent_amount"].values[0] * (int(st.session_state[f"{x}factor"])/30)
                        except:
                            rentAmt = tenantDf[tenantDf.index==x]["rent_amount"].values[0]
                        try:
                            waterCharge = tenantDf[tenantDf.index==x]["water_charge"].values[0] * (int(st.session_state[f"{x}factor"])/30)
                        except:
                            waterCharge = tenantDf[tenantDf.index==x]["water_charge"].values[0]
                        garbageCharge = tenantDf[tenantDf.index==x]["garbage_charge"].values[0]
                        readingList = list(meterDf[meterDf.index==x]["readings"].values)
                        meterCost = (readingList[-1]-readingList[-2])*10
                        previousDue = billDf[billDf.index==x]["total"].sum() - paymentDf[paymentDf.index==x]["amount"].sum() + tenantDf[tenantDf.index==x]["previous_due"].values[0]
                        total = rentAmt + waterCharge + garbageCharge + meterCost
                        fulltotal = total + previousDue
                        am.runSql(f"""INSERT INTO public.bills(flat_no, bill_date, bill_month, rent_amount, water_charge, garbage_charge, meter_cost, previous_due, total, fulltotal) VALUES ('{x}','{date.today()}','{upBillingMonth}','{int(rentAmt)}','{int(waterCharge)}','{garbageCharge}','{meterCost}','{previousDue}','{int(total)}','{int(fulltotal)}')""")
                        st.write(f"Bill created for {x}")
                    st.write('Done!')
                    time.sleep(3)
                    am.get_billDf.clear()
                    am.get_collectionDf.clear()
                    am.get_statementDf.clear()
                    am.get_currentDueDf.clear()
                    am.get_whatsappData.clear()
                    st.session_state["billDf"], st.session_state["billMonthList"] = am.get_billDf()
                    st.session_state["collectionDf"] = am.get_collectionDf()
                    st.session_state["statementDf"] = am.get_statementDf()
                    st.session_state["currentDueDf"], st.session_state["totalCurrentDue"] = am.get_currentDueDf()
                    st.session_state["whatsappData"] = am.get_whatsappData()
                    st.rerun()

    # View Bills
    with st.expander("View Bills"):
        selectMonth = st.selectbox("Select Billing Month", billMonthList)
        selectedFlat = st.selectbox("Select Flat No.",activeFlatList+["Select"],index=len(activeFlatList+["Select"])-1,key="viewbill")
        if selectedFlat == "Select":
            st.write("Select a flat!")
        else:
            try:
                viewDf = billDf.loc[(billDf.index==selectedFlat) & (billDf["bill_month"]==selectMonth)]
                viewList = (viewDf.values.tolist())[0]
                tenantName = tenantDf[tenantDf.index==selectedFlat]["tenant_name"].values[0]
                userId = tenantDf[tenantDf.index==selectedFlat]["username"].values[0]
                pw = tenantDf[tenantDf.index==selectedFlat]["password"].values[0]
                cellText = []
                cellText.append(["Rent",viewList[2]])
                cellText.append(["Electricity",viewList[5]])
                if viewList[3] != 0:
                    cellText.append(["Water",viewList[3]])
                if viewList[4] != 0:
                    cellText.append(["Garbage",viewList[4]])
                if viewList[6] != 0:
                    cellText.append(["Previous Due",viewList[6]])
                cellText.append(["Total",viewList[8]])

                title_text = f'{tenantName}'
                subtitle_text = f'** Pay Before 06/{viewList[0].strftime("%m/%Y")}'
                column_headers = [selectedFlat,selectMonth]
                colWidths = [1,1]
                scaleY = 5
                headerFontSize = 30
                cellFontSize = 30
                alignList = ['left','right']
                ap.plot_table_with_title_total(title_text,subtitle_text,column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)
                st.code(f"Your total rent due for the month of {selectMonth} is ₹ {viewList[8]}.\nPlease pay the rent before 06/{viewList[0].strftime('%m/%Y')}.\nYou can now view your bills and statements at https://kb-tenant.streamlitapp.com .\nYour username is {userId} and password is {pw}")
            except:
                st.write("Bill Not Available")

    # View Statments
    with st.expander("View Statments"):
        selectedFlat = st.selectbox("Select Flat No.",activeFlatList+["Select"],index=len(activeFlatList+["Select"])-1,key="viewStatement")
        if selectedFlat == "Select":
            st.write("Select a flat!")
        else:
            tenantName = tenantDf[tenantDf.index==selectedFlat]["tenant_name"].values[0]
            tempStatementDf = statementDf[statementDf.index==selectedFlat]
            tempStatementList = ['Total',tempStatementDf["bill"].sum(),tempStatementDf["payment"].sum(),tempStatementDf["bill"].sum()-tempStatementDf["payment"].sum()]
            tempStatementDf.loc[len(tempStatementDf.index)] = tempStatementList
            tempStatementDf["bill"] = tempStatementDf['bill'].apply(lambda x: format_number(x, locale="en_IN") if x != 0 else "-")
            tempStatementDf["payment"] = tempStatementDf['payment'].apply(lambda x: format_number(x, locale="en_IN") if x != 0 else "-")
            tempStatementDf["dues"] = tempStatementDf['dues'].apply(lambda x: format_number(x, locale="en_IN") if x != 0 else "-")
            st.write(f'{tenantName} | {selectedFlat}')
            column_headers = ['Date','Bills','Payments','Dues']
            cellText = tempStatementDf.values
            colWidths = [1,1,1,1]
            scaleY = 9
            headerFontSize = 40
            cellFontSize = 40
            alignList = ['center','right','right','right']
            ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    # View Statments
    with st.expander("Send Reminder"):
        waFlatList = list(whatsappData.keys())
        selectedFlatWa = st.selectbox("Select Flat No.",waFlatList+["Select"],index=len(waFlatList+["Select"])-1,key="waflats")
        if selectedFlatWa == "Select":
            st.write("Select a flat!")
        else:
            detailList = whatsappData[selectedFlatWa]
            st.write(f"{detailList[0]} | Current Due = ₹ {detailList[2]}")
            messages = f"*REMINDER!!!*\n\nYour Current Rent Due = ₹ {detailList[2]}\nPlease pay at the earliest\n\nThanks"
            st.write(f"[Send Reminder](https://wa.me/phone=+91{detailList[1]}?text={quote(messages)})")
            # if st.button("Send Reminder"):
                # messages = f"REMINDER!!!\n\nHi, {detailList[0]}\nYour Current Rent Due = ₹ {detailList[2]}\nPlease pay at the earliest\n\nThanks\nKartikey Bhawan"
                # st.write(f"Reminder sent to {selectedFlatWa}")


else:
    st.error("Session Expired! Go to homepage...!")
    st.markdown("[Homepage](https://kb-owner-v1.streamlitapp.com/)")

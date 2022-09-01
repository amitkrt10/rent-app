import streamlit as st
from datetime import date
import dateutil.relativedelta
import adminModules as am
import time
from babel.numbers import format_number
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
        tenantDf, activeFlatList, initiaDueDict = st.session_state["tenantDf"], st.session_state["activeFlatList"], st.session_state["initiaDueDict"]
        billDf, billMonthList = st.session_state["billDf"], st.session_state["billMonthList"]
        paymentDf, paymentMonthList = st.session_state["paymentDf"], st.session_state["paymentMonthList"]
        meterDf, readingMonthList = st.session_state["meterDf"], st.session_state["readingMonthList"]
        statementDf = st.session_state["statementDf"]
        st.balloons()

    upBillingDate = date.today() - dateutil.relativedelta.relativedelta(months=1)
    upBillingMonth = upBillingDate.strftime("%m/%Y")

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Billings</h2>", unsafe_allow_html=True)

    #Create Bills
    with st.expander(f"Create Bills for {upBillingMonth}"):
        if upBillingMonth in billMonthList:
            st.write(f"Bills already created for {upBillingMonth}")
        else:
            if upBillingMonth not in readingMonthList:
                st.write(f"Take meter reading for {upBillingMonth} first")
            else:
                if st.button(f"Create for {upBillingMonth}"):
                    for x in activeFlatList:
                        rentAmt = tenantDf[tenantDf.index==x]["rent_amount"].values[0]
                        waterCharge = tenantDf[tenantDf.index==x]["water_charge"].values[0]
                        garbageCharge = tenantDf[tenantDf.index==x]["garbage_charge"].values[0]
                        readingList = list(meterDf[meterDf.index==x]["readings"].values)
                        meterCost = (readingList[-1]-readingList[-2])*10
                        previousDue = billDf[billDf.index==x]["total"].sum() - paymentDf[paymentDf.index==x]["amount"].sum() + tenantDf[tenantDf.index==x]["previous_due"].values[0]
                        total = rentAmt + waterCharge + garbageCharge + meterCost
                        fulltotal = total + previousDue
                        am.runSql(f"""INSERT INTO public.bills(flat_no, bill_date, bill_month, rent_amount, water_charge, garbage_charge, meter_cost, previous_due, total, fulltotal) VALUES ('{x}','{today}','{upBillingMonth}','{rentAmt}','{waterCharge}','{garbageCharge}','{meterCost}','{previousDue}','{total}','{fulltotal}')""")
                        st.write(f"Bill created for {x}")
                    st.write('Done!')
                    time.sleep(3)
                    with st.spinner(text='Updating Data... Please Wait...!'):
                        am.get_billDf.clear()
                        am.get_collectionDf.clear()
                        am.get_statementDf.clear()
                        am.get_currentDueDf.clear()
                    st.experimental_rerun()

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
                st.write(f"Your total rent due for the month of {selectMonth} is ₹ {viewList[8]}. Please pay the rent before 06/{viewList[0].strftime('%m/%Y')}. You can now view your bills and statements at https://tinyurl.com/kb-tenant-app . Your username is {userId} and password is {pw}")
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
            tempStatementDf["bill"] = tempStatementDf['bill'].apply(lambda x: format_number(x, locale='en_IN'))
            tempStatementDf["payment"] = tempStatementDf['payment'].apply(lambda x: format_number(x, locale='en_IN'))
            tempStatementDf["dues"] = tempStatementDf['dues'].apply(lambda x: format_number(x, locale='en_IN'))
            st.write(f'{tenantName} | {selectedFlat}')
            column_headers = ['Date','Bills','Payments','Dues']
            cellText = tempStatementDf.values
            colWidths = [1,1,1,1]
            scaleY = 9
            headerFontSize = 40
            cellFontSize = 40
            alignList = ['center','right','right','right']
            ap.plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://amitkrt10-rent-app-1--home-8wtbg6.streamlitapp.com/)")

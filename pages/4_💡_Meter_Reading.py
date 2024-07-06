import streamlit as st
from datetime import date
import dateutil.relativedelta
import adminModules as am
import appPlots as ap
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
        activeFlatList = st.session_state["activeFlatList"]
        meterDf, readingMonthList = st.session_state["meterDf"], st.session_state["readingMonthList"]
        consumptionDict = st.session_state["consumptionDict"]

    upBillingDate = date.today() - dateutil.relativedelta.relativedelta(months=1)
    upBillingMonth = upBillingDate.strftime("%Y/%m")

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Electricity</h2>", unsafe_allow_html=True)
    am.get_header('Electricity')

    # Meter Reading Form
    with st.expander(f"Take Meter Reading for {upBillingMonth}"):
        if upBillingMonth in readingMonthList:
            st.write(f"Meter reading sucessfully taken for {upBillingMonth}")
            st.write("You will be able to take the next reading from 1st of the next month")
        else:
            with st.form("Electric Meter Reading",clear_on_submit=True):
                readingDict = {}
                readingDate = st.date_input("Reading Date")
                for x in activeFlatList:
                    tempReading = st.text_input(x)
                    readingDict.update({x:tempReading})
                submitted = st.form_submit_button("Submit")
                if submitted:
                    for x in readingDict.keys():
                        am.runSql(f"""INSERT INTO public.meter_reading(flat_no, reading_date, reading_month, readings) VALUES ('{x}','{readingDate}','{upBillingMonth}','{readingDict[x]}')""")
                    st.write(f"Reading successfully taken for {upBillingMonth}")
                    time.sleep(3)
                    am.get_meterDf.clear()
                    am.get_consumption.clear()
                    st.session_state["meterDf"], st.session_state["readingMonthList"] = am.get_meterDf()
                    st.session_state["consumptionDict"] = am.get_consumption()
                    st.experimental_rerun()

    # Show Meter Readings by Month
    with st.expander("Electricity Consumptions by Month"):
        selectedFlat = st.selectbox("Select Flat No.",activeFlatList+["Select"],index=len(activeFlatList+["Select"])-1)
        if selectedFlat == "Select":
            st.write("Select a flat!")
        else:
            tempConsumptionDf=meterDf[meterDf.index==selectedFlat]
            tempConsumptionDf['consumption'] = tempConsumptionDf['readings'].diff(1)
            tempConsumptionDf['consumption'].fillna(0,inplace=True)
            tempConsumptionDf['consumption'] = tempConsumptionDf['consumption'].astype(int)
            tempConsumptionDf.reset_index(inplace = True, drop = True)

            column_headers = ['Month','Reading','Consumption']
            cellText = tempConsumptionDf[['reading_month','readings','consumption']].values
            colWidths = [1,1,1]
            scaleY = 9
            headerFontSize = 40
            cellFontSize = 40
            alignList = ['center','center','center']
            ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

            title = f'Electricity Consumption for {upBillingMonth}'
            x_data = tempConsumptionDf[tempConsumptionDf.index>0]['reading_month']
            y_data = tempConsumptionDf[tempConsumptionDf.index>0]['consumption']
            bar_width = 0.4
            x_rotate = 45
            fontsize = 15
            ap.plot_bar(title,x_data,y_data,bar_width,x_rotate,fontsize)

    #Electricity Consumptions by Flat
    with st.expander("Electricity Consumptions by Flat"):
        title = f'Electricity Consumption - {upBillingMonth}'
        x_data = consumptionDict.keys()
        y_data = consumptionDict.values()
        bar_width = 0.6
        x_rotate = 90
        fontsize = 10
        ap.plot_bar(title,x_data,y_data,bar_width,x_rotate,fontsize)    

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

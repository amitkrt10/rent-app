import streamlit as st
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
        tenantDf, activeFlatList = st.session_state["tenantDf"], st.session_state["activeFlatList"]
        meterDf = st.session_state["meterDf"]
        vacantFlatList = st.session_state["vacantFlatList"]
        currentDueDf = st.session_state["currentDueDf"]
        tenantInfoDict = st.session_state["tenantInfoDict"]
        st.balloons()

    st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Tenants</h2>", unsafe_allow_html=True)

    #Active Tenants
    with st.expander("Active Tenants"):
        column_headers = ["Flat","Tenant Name","Contact"]
        cellText = tenantDf[['tenant_name','mobile']].to_records()
        colWidths = [1,3,2]
        scaleY = 15
        headerFontSize = 100
        cellFontSize = 80
        alignList = ['center','left','center']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Tenants Info
    with st.expander("Tenants Info"):
        selectedInfoFlat = st.selectbox("Flat No.",activeFlatList,key='tenantInfo')
        infoList = tenantInfoDict[selectedInfoFlat]
        column_headers = [selectedInfoFlat, infoList[0]]
        cellText = []
        cellText.append(['Mobile', infoList[1]])
        cellText.append(['Security Deposite', f'₹ {infoList[2]}'])
        cellText.append(['Rent', f'₹ {infoList[3]}'])
        cellText.append(['Water Charge', f'₹ {infoList[4]}'])
        cellText.append(['Garbage Charge', f'₹ {infoList[5]}'])
        cellText.append(['Electricity Charge', '₹ 10 / unit'])
        cellText.append(['Date of Occupancy', infoList[6]])
        colWidths = [1,1]
        scaleY = 6
        headerFontSize = 30
        cellFontSize = 30
        alignList = ['left','right']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Add New Tenant Form
    with st.expander("Add New Tenant"):
        with st.form("New Tenant Details",clear_on_submit=True):
            flatNo = st.selectbox("Flat No.",vacantFlatList)
            tenantName = st.text_input("Full Name")
            tenantMobile = st.text_input("Mobile Number")
            securityDeposite = st.text_input("Secutity Deposite Amount")
            rentAmt = st.text_input("Rent Amount")
            waterCharge = st.text_input("Water Charge")
            garbageCharge = st.text_input("Garbage Charge",20)
            previousDue = st.text_input("Previous Due, if any",0)
            initialMeterReading = st.text_input("Initial Electric Meter Reading")
            dateOfOccupancy = st.date_input("Date of Occupancy")
            submitted = st.form_submit_button("Submit")
            if submitted:
                password = f"{tenantName[0:4]}{dateOfOccupancy.strftime('%d%m')}"
                am.runSql(f"""INSERT INTO public.active_tenants(flat_no, tenant_name, mobile, security_deposite, rent_amount, water_charge, garbage_charge, previous_due, initial_meter_reading, date_of_ocupancy, password, username) VALUES ('{flatNo}','{tenantName}','{tenantMobile}','{securityDeposite}','{rentAmt}','{waterCharge}','{garbageCharge}','{previousDue}','{initialMeterReading}','{dateOfOccupancy}','{password}','{str(tenantMobile)}')""")
                st.write(f"Details of {tenantName} successfully added to Flat No. {flatNo}")
                time.sleep(3)
                st.experimental_memo.clear()
                st.experimental_rerun()

    #Remove Tenant Form
    with st.expander("Remove Tenant"):
        selectedFlat = st.selectbox("Select Flat No.",activeFlatList,key="removetenant")
        tenantName = currentDueDf[currentDueDf.index==selectedFlat]['tenant_name'].values[0]
        currentDue = currentDueDf[currentDueDf.index==selectedFlat]['dues'].values[0]
        st.write(f"{tenantName} | Previous Due = ₹ {currentDue}")
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
                flatTenant = f"{selectedFlat} | {tenantName}"
                tenantMobile = tenantDf[tenantDf.index==selectedFlat]['mobile'].values[0]
                dateOfOccupancy = tenantDf[tenantDf.index==selectedFlat]['date_of_ocupancy'].values[0]
                meterCharge = (int(finalMeterReading) - meterDf[meterDf.index==selectedFlat]["readings"].max()) * 10
                tenantSecurity = tenantDf[tenantDf.index==selectedFlat]['security_deposite'].values[0]
                finalDue = int(rentAmt) + int(meterCharge) + int(waterCharge) + int(otherCharges) + currentDue - tenantSecurity
                am.runSql(f"""INSERT INTO public.inactive_tenant (flat_tenant, mobile, in_date, out_date, final_reading, final_rent, final_meter, final_water, final_garbage, final_other, security_deposite, final_due, remark, previous_due) VALUES ('{flatTenant}', '{tenantMobile}', '{dateOfOccupancy}', '{exitDate}', '{finalMeterReading}', '{rentAmt}', '{meterCharge}', '{waterCharge}', '{garbageCharge}', '{otherCharges}', '{tenantSecurity}', '{finalDue}', '{remark}','{currentDue}')""")
                st.write("Exit Tenant Table - Updated!")
                sql = f"""insert into public.exit_statement
                    select concat(raw.flat_no,' | ',t.tenant_name), raw.t_date, raw.bill, raw.payment,
                    SUM(raw.tempdiff) OVER (partition by raw.flat_no ORDER BY raw.t_date) AS dues
                    from (
                    select flat_no, t_date, bill, payment, bill- payment as tempdiff
                    from(select flat_no, '2022-04-01' as t_date, previous_due as bill, 0 as payment from public.active_tenants where previous_due != 0
                    union
                    select flat_no, bill_date as t_date, total as bill, 0 as payment from public.bills
                    union
                    select flat_no, payment_date as t_date, 0 as bill, amount as payment from public.payments
                    order by 1,2) st) raw
                    left join public.active_tenants t on raw.flat_no = t.flat_no
                    where raw.flat_no = '{selectedFlat}'"""
                am.runSql(sql)
                am.runSql(f"""INSERT INTO public.exit_statement (flat_tenant, transaction_date, bill, payment, due) VALUES ('{flatTenant}','{exitDate}','{finalDue-currentDue}','0','{finalDue}')""")
                st.write("Exit Statement Table - Updated!")
                am.runSql(f"""DELETE FROM public.active_tenants WHERE flat_no = '{selectedFlat}'""")
                st.write("Active Tenant Table - Updated!")
                am.runSql(f"""DELETE FROM public.bills WHERE flat_no = '{selectedFlat}'""")
                st.write("Bills - Removed!")
                am.runSql(f"""DELETE FROM public.payments WHERE flat_no = '{selectedFlat}'""")
                st.write("Payments - Removed!")
                am.runSql(f"""DELETE FROM public.meter_reading WHERE flat_no = '{selectedFlat}'""")
                st.write("Meter Readings - Removed!")
                st.experimental_memo.clear()
                st.experimental_rerun()

else:
    st.error("Please Login First...!")
    st.markdown("[Login](https://kb-owner.streamlitapp.com/)")

import streamlit as st
import adminModules as am
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
        activeFlatList = st.session_state["activeFlatList"]
        flatDf, vacantFlatList = st.session_state["flatDf"], st.session_state["vacantFlatList"]

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Property</h2>", unsafe_allow_html=True)
    am.get_header('Property')

    #Property Details
    with st.expander("Property Details"):
        column_headers = ["Flat","Type","Facilities"]
        cellText = flatDf.to_records()
        colWidths = [1,1,2]
        scaleY = 9
        headerFontSize = 60
        cellFontSize = 50
        alignList = ['center','center','center']
        ap.plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList)

    #Add new Flat
    with st.expander("Add New Property"):
        with st.form("Add New Flat",clear_on_submit=True):
            flatNo = st.text_input("Flat No.","KB-",key="newFlat")
            flatType = st.selectbox("Flat Type",["2BHK","1BHK","OFFICE","3BHK","1RK"])
            facilities = st.text_input("Facilities.","NA")
            submitted = st.form_submit_button("Submit")
            if submitted:
                am.runSql(f"""INSERT INTO public.flats(flat_no, flat_type, facilities) VALUES ('{flatNo}','{flatType}','{facilities}')""")
                st.write(f"New flat - {flatNo} successfully added.")
                am.get_flatDf.clear()
                st.session_state["flatDf"], st.session_state["vacantFlatList"] = am.get_flatDf()
                st.rerun()

    #Modify Facilities
    with st.expander("Update Facilities"):
        with st.form("Modify Facilities",clear_on_submit=True):
            selectedFlat = st.selectbox("Select Flat No.",activeFlatList+vacantFlatList)
            facilities = st.text_input("Update Facilities.","NA")
            submitted = st.form_submit_button("Submit")
            if submitted:
                am.runSql(f"""UPDATE public.flats SET facilities = '{facilities}' WHERE flat_no = '{selectedFlat}'""")
                st.write(f"Flat - {selectedFlat} successfully updated.")
                am.get_flatDf.clear()
                st.session_state["flatDf"], st.session_state["vacantFlatList"] = am.get_flatDf()
                st.rerun()

    #Revomve flat
    with st.expander("Remove Property"):
        with st.form("Remove Property",clear_on_submit=True):
            flatNoR = st.selectbox("Select Flat No.",vacantFlatList, key="removeFlat")
            submitted = st.form_submit_button("Submit")
            if submitted:
                am.runSql(f"""DELETE FROM public.flats WHERE flat_no = '{flatNoR}'""")
                st.write(f"Flat - {flatNoR} successfully removed.")
                am.get_flatDf.clear()
                st.session_state["flatDf"], st.session_state["vacantFlatList"] = am.get_flatDf()
                st.rerun()

else:
    st.error("Session Expired! Go to homepage...!")
    st.markdown("[Homepage](https://kb-owner-v1.streamlitapp.com/)")

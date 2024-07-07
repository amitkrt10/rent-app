import streamlit as st
import pickle
import os
import os.path
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import adminModules as am
import time
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed'
)
am.get_header1()

if "login" in st.session_state.keys():
    with st.spinner(text='Reading Data... Please Wait...!'):
        tenantDf, activeFlatList = st.session_state["tenantDf"], st.session_state["activeFlatList"]
        currentDueDf = st.session_state["currentDueDf"]

    # st.markdown("<h2 style='text-align: center;text-shadow: 3px 2px blue;font-style: oblique;'>Backup Data</h2>", unsafe_allow_html=True)
    am.get_header('Backup Data')

    # Read txt
    f = open("backup_files/temp.txt", "r")
    txt = f.read()
    st.write(txt.rsplit(' ', 1)[0])
    st.markdown(f"[View Backup Files](https://drive.google.com/drive/folders/{txt.rsplit(' ', 1)[1]})")
    f.close()

    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]

    BACKUP_CRED= st.secrets["BACKUP_CRED"]

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive.file']

    def get_gdrive_service():
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)

    def createFolder(folderName):
        """
        Creates a folder
        """
        # authenticate account
        service = get_gdrive_service()
        # folder details we want to make
        folder_metadata = {
            "name": folderName,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": ["1suj_ezYvvfeFOUZKa9EqyO2w5EJMrJG6"]
        }
        # create the folder
        file = service.files().create(body=folder_metadata, fields="id").execute()
        # get the folder id
        folder_id = file.get("id")
        return(folder_id)

    def upload_files(curr_time,table,folder_id):
        """
        Upload a file to folder
        """
        # authenticate account
        service = get_gdrive_service()
        # upload a file text file
        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": f"{curr_time}_{table}.csv",
            "parents": [folder_id]
        }
        # upload
        media = MediaFileUpload(f"backup_files/{curr_time}_{table}.csv", resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        st.write(f"File Uploaded : {table}")

    def db_connection():
        # DB Credentials
        HOST="aws-0-ap-south-1.pooler.supabase.com"
        DATABASE="postgres"
        USER="postgres.kgmhukjqliwvlbieoayv"
        PORT="5432"
        PASSWORD="nQagzat3Cakqkhit"
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        return conn

    if st.button("Backup Data",key="backupData"):
        with open('credentials.json', 'w') as fp:
            json.dump(BACKUP_CRED, fp)
        curr_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
        print_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        folder_id = createFolder(f"{curr_time}_Backup")
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';''')
        result = cursor.fetchall()
        table_list = list(map(list, zip(*result)))[0]
        for table in table_list:
            df = pd.read_sql(f'''SELECT * FROM public.{table};''', con=conn)
            df.to_csv(f'backup_files/{curr_time}_{table}.csv', index=False)
            upload_files(curr_time,table,folder_id)
            if os.path.exists(f'backup_files/{curr_time}_{table}.csv'):
                os.remove(f'backup_files/{curr_time}_{table}.csv')

        if os.path.exists("credentials.json"):
            os.remove("credentials.json")

        st.write("Backup Completed!")

        txtFile = open("backup_files/temp.txt", "w")
        txtFile.write(f"Last backup done at {print_time} {folder_id}")
        txtFile.close()

else:
    st.error("Session Expired! Go to homepage...!")
    st.markdown("[Homepage](https://kb-owner-v1.streamlitapp.com/)")

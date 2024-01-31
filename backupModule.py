from unittest import result
import io
import streamlit as st
import pickle
import os
import os.path
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import time
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from tabulate import tabulate
import warnings
warnings.filterwarnings("ignore")

json_cred = st.secrets["BACKUP_CRED"]

with open('credentials.json', 'w') as fp:
    json.dump(json_cred, fp)

# If modifying these scopes, delete the file token.pickle.
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
    HOST= st.secrets["HOST"]
    DATABASE= st.secrets["DATABASE"]
    USER= st.secrets["USER"]
    PORT= st.secrets["PORT"]
    PASSWORD= st.secrets["PASSWORD"]
    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return conn

def backup_tables():
    curr_time = time.strftime("%Y_%m_%d_%H_%M", time.localtime())
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
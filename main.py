import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
from csv import reader
import pandas as pd
import gcsfs

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.cache
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "wmca-streamlit-app"
file_path = "sample_outputs.csv"

content = read_file(bucket_name, file_path)

df=pd.DataFrame( list(reader(content)))

st.write("File read successfully  from Bucket  {}.".format(bucket_name))
st.write(df.head())

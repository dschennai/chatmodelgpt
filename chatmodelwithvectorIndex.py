import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTSimpleVectorIndex, download_loader
from google.oauth2.credentials import Credentials
import streamlit as st
import openai

st.set_page_config(
    page_title="Chat Using GPT Index",
    layout="wide"
)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents.readonly']


def authorize_gdocs():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def load_data():
    # function to authorize or download latest credentials
    authorize_gdocs()

    # initialize LlamaIndex google doc reader
    GoogleDocsReader = download_loader('GoogleDocsReader')

    # list of google docs we want to index
    gdoc_ids = ['1A-jqshmmeVY37jvZimKtjLBTyvctwta9Ydg_sed5zVI']

    loader = GoogleDocsReader()

    # load gdocs and index them
    documents = loader.load_data(document_ids=gdoc_ids)
    index = GPTSimpleVectorIndex(documents)

    # Save your index to a index.json file
    index.save_to_disk('index.json')
    # Load the index from your saved index.json file
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    return index


#st.subheader("# Enter your Source Document")
#documentId = st.text_input("GDoc","",label_visibility="collapsed")

st.subheader("# Lets Start")
cols = st.columns((3.5, 0.5))
chatQuestion = cols[0].text_input("Input Question","",label_visibility="collapsed")
check = cols[1].button("Ok")
#
if check:
    #write response
    # Querying the index
    index = load_data()
    while True:
        #prompt = input("Type prompt...")
        print("chatQuestion")
        print(chatQuestion)
        response = index.query(chatQuestion)
        print(response)
        st.text_area(label ="Response",value=response, height =500)

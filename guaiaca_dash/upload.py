import streamlit as st
import pandas as pd

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0

def upload_files():
    # File uploader with a unique key
    uploaded_files = st.sidebar.file_uploader(
        "Choose files", 
        accept_multiple_files=True, 
        key=f"uploader_{st.session_state['uploader_key']}"
    )
    if uploaded_files:
        st.session_state['uploaded_files'] = uploaded_files
        

def reset_uploader():
    if st.session_state['uploaded_files']:
        print("Tem coisa no upload_files")
        for uploaded_file in st.session_state['uploaded_files']:
                print("iterei sobre os arquivos no upload_files")
                # Process each uploaded file (e.g., read the file into a DataFrame)
                df = pd.read_csv(uploaded_file)
                st.write(f"File {uploaded_file.name} uploaded successfully!")
                st.write(df)
                st.write(f"Uploaded file: {uploaded_file.name}")
    print("iniciando processo de reset")
    aux = st.session_state['uploader_key']
    print(aux)            
    st.session_state['uploaded_files'] = []
    st.session_state['uploader_key'] += 1  # Change key to reset the uploader
    st.rerun()
    print("reset efetuado por isso que mais nada ta aparecendo")

# File upload section
upload_files()

# Display a button to clear the file uploader
if st.sidebar.button("Clear file uploader"):
    reset_uploader()

# Display the uploaded files if any
#if st.session_state['uploaded_files']:
#    for uploaded_file in st.session_state['uploaded_files']:
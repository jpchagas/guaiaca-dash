import streamlit as st
from logger import ColoredLogger
from uploader import Uploader

# Create a centralized colored logger
logger = ColoredLogger(__name__)

uploader = Uploader()

def upload_files():
     if st.session_state['uploaded_files']:
        for uploaded_file in st.session_state['uploaded_files']:
                # Process each uploaded file (e.g., read the file into a DataFrame)
                file_name = uploaded_file.name.split(".")
                name = file_name[0]
                extension = uploaded_file.name.split(".")[1]
                banco,tipo,mes = name.split("_")
                uploader.upload(uploaded_file, extension,banco,tipo,mes,"jpchagas")
        

def reset_uploader():
    upload_files()
    logger.debug("Limpando uploader_widget")
    st.session_state['uploaded_files'] = []
    st.session_state['uploader_key'] += 1  # Change key to reset the uploader
    st.rerun()

def generate_upload_button_widget():
    if st.sidebar.button("Enviar arquivos"):
        reset_uploader()
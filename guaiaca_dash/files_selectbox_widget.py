import streamlit as st
from logger import ColoredLogger
import os

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_files_selectbox_widget():
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        files = [x.replace(".csv","") for x in os.listdir(current_output_path)] 
    except:
        files = []
    st.session_state['selected_date'] = st.sidebar.selectbox('Período', files)
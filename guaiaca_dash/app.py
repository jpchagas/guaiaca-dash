import streamlit as st
from logger import ColoredLogger
from upload_widget import generate_upload_widget
from upload_button_widget import generate_upload_button_widget
from files_selectbox_widget import generate_files_selectbox_widget
from auth_widget import generate_auth_widget
from data_widget import generate_data_widget

# Create a centralized colored logger
logger = ColoredLogger(__name__)


# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0
if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = []

def main():
    st.title('Guaiaca Raiz')

    if generate_auth_widget():

        st.sidebar.header('Menu')
        generate_files_selectbox_widget()
        # File upload section
        generate_upload_widget()

        # Display a button to clear the file uploader
        generate_upload_button_widget()

        generate_data_widget()

        # Display the uploaded files if any
        #if st.session_state['uploaded_files']:
        #    for uploaded_file in st.session_state['uploaded_files']:


if __name__ == '__main__':
    main()
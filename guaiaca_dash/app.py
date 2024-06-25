import streamlit as st
from logger import ColoredLogger
from upload_widget import generate_upload_widget
from upload_button_widget import generate_upload_button_widget
from files_selectbox_widget import generate_files_selectbox_widget
from auth_widget import generate_auth_widget
from data_widget import generate_data_widget
from expense_widget import generate_expense_widget
from balance_chart_widget import generate_balance_chart_widget
from amount_by_category_chart_widget import generate_amoutbycategory_chart_widget
from amout_by_origin_chart_widget import generate_amoutbyorigin_chart_widget
from amount_by_bank_chart_widget import generate_amoutbybank_chart_widget
from amout_by_method_chart_widget import generate_amoutbymethod_chart_widget


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
        metrics, charts, data = st.tabs(["Métricas", "Gráficos", "Dados"])
        with metrics:
            generate_expense_widget()

        with charts:
            generate_balance_chart_widget()
            generate_amoutbycategory_chart_widget()
            generate_amoutbyorigin_chart_widget()
            generate_amoutbybank_chart_widget()
            generate_amoutbymethod_chart_widget()

        with data:
            generate_data_widget()

        divisao = st.sidebar.radio('Formato Divisão:', ['Igualmente','Proporcional'])


        

        

        
        #generate_rebenue_widget
        #generate_balance_widget

        # Display the uploaded files if any
        #if st.session_state['uploaded_files']:
        #    for uploaded_file in st.session_state['uploaded_files']:


if __name__ == '__main__':
    main()
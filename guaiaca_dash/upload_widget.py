import streamlit as st
from logger import ColoredLogger

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_upload_widget():
    st.sidebar.header('Upload dados')
    # File uploader with a unique key
    uploaded_files = st.sidebar.file_uploader(
        "Escolha os arquivos",
        type=['csv', 'pdf'],
        help="O nome do arquivo deve seguir o seguinte padrão:<banco_(fatura/extrato)_mês(nome)>, por exemplo, caixa_fatura_marco.csv", 
        accept_multiple_files=True, 
        key=f"uploader_{st.session_state['uploader_key']}"
    )
    if uploaded_files and uploaded_files not in st.session_state['uploaded_files']:
        st.session_state['uploaded_files'] = uploaded_files
        logger.debug("Salvando arquivos no session_state")
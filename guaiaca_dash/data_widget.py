import streamlit as st
from logger import ColoredLogger
import pandas as pd
import os
import time

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_data_widget():
    pd.options.display.float_format = '{:,.2f}'.format
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        original_df = pd.read_csv(current_output_path+st.session_state['selected_date']+".csv")  
        edited_df = st.data_editor(original_df, use_container_width=True)
        if not original_df.equals(edited_df):
            with st.spinner('Atualizando dados...'):
                edited_df = edited_df.drop_duplicates()
                edited_df.to_csv(current_output_path+st.session_state['selected_date']+".csv",index=False)
                time.sleep(5)
            st.success('Atualizado!')
            #st.rerun()

    except:
        st.warning('Não foi feito upload de nenhum dado para o período escolhido')
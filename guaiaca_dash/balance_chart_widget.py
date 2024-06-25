import streamlit as st
from logger import ColoredLogger
import pandas as pd
import os
import time

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_balance_chart_widget():
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        original_df = pd.read_csv(current_output_path+st.session_state['selected_date']+".csv")  
        original_df['valor'] = pd.to_numeric(original_df['valor'], errors='coerce')
        grouped_sum = original_df.groupby('transacao')['valor'].sum().reset_index()

        data = {
            'transacao': grouped_sum['transacao'].to_list(),
            'valor': grouped_sum['valor'].to_list()
        }
        df = pd.DataFrame(data)

        # Set the index to 'transacao' for better visualization with st.bar_chart
        df.set_index('transacao', inplace=True)

        # Display bar chart in Streamlit
        st.bar_chart(df)

    except:
        st.warning('Não foi feito upload de nenhum dado para o período escolhido')
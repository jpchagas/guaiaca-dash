import streamlit as st
from logger import ColoredLogger
import pandas as pd
import os
import time
import plotly.express as px

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_amoutbymethod_chart_widget():
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        original_df = pd.read_csv(current_output_path+st.session_state['selected_date']+".csv")  
        original_df['valor'] = pd.to_numeric(original_df['valor'], errors='coerce')
        filtered_df = original_df[original_df['transacao'] == 'despesa']
        grouped_sum = filtered_df.groupby('metodo')['valor'].sum().reset_index()

        data = {
            'metodo': grouped_sum['metodo'].to_list(),
            'valor': grouped_sum['valor'].to_list()
        }
        df = pd.DataFrame(data)

        # Set the index to 'transacao' for better visualization with st.bar_chart
        #df.set_index('transacao', inplace=True)
        fig = px.pie(df, values='valor', names='metodo')
        st.plotly_chart(fig, use_container_width=True)

    except:
        st.warning('Não foi feito upload de nenhum dado para o período escolhido')
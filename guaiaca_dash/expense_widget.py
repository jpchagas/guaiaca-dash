import streamlit as st
from logger import ColoredLogger
import pandas as pd
import os
import time

# Create a centralized colored logger
logger = ColoredLogger(__name__)

def generate_expense_widget():
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        original_df = pd.read_csv(current_output_path+st.session_state['selected_date']+".csv")  
        original_df['valor'] = pd.to_numeric(original_df['valor'], errors='coerce')
        grouped_sum = original_df.groupby('transacao')['valor'].sum().reset_index()


        # Extract the values
        despesa_valor = round(grouped_sum.loc[grouped_sum['transacao'] == 'despesa', 'valor'].values[0],2)
        receita_valor = round(grouped_sum.loc[grouped_sum['transacao'] == 'receita', 'valor'].values[0],2)
        balanco = round(receita_valor-despesa_valor,2)
        col1, col2,col3 = st.columns(3)
        col1.metric(label=":green[Total Receita]", value=receita_valor)
        col2.metric(label=":orange[Total Despesa]", value=despesa_valor)
        col3.metric(label="Balanço", value=balanco, delta=balanco)
    except:
        st.warning('Não foi feito upload de nenhum dado para o período escolhido')
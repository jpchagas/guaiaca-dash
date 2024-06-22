import streamlit as st
import pandas as pd
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from uploader import Uploader

uploader = Uploader()

st.title('Guaiaca Raiz')

with open(os.getcwd() + "/guaiaca_dash/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Olá *{st.session_state["name"]}*')
    current_output_path = f'{os.getcwd()}/guaiaca_dash/data/output/{st.session_state["username"]}/'
    try:
        files = [x.replace(".csv","") for x in os.listdir(current_output_path)] 
    except:
        files = []


    metrics, charts, info = st.tabs(["Métricas", "Gráficos", "Dados"])
    st.sidebar.header('Menu')
    selected_date = st.sidebar.selectbox('Período', files)
    st.sidebar.header('Upload dados')

    
    uploaded_files = st.sidebar.file_uploader(
        'Fazer upload',
        type=['csv', 'pdf'],
        help="O nome do arquivo deve seguir o seguinte padrão:<banco_(fatura/extrato)_mês(nome)>, por exemplo, caixa_fatura_marco.csv", 
        accept_multiple_files=True)
    print(uploaded_files)
    for uploaded_file in  uploaded_files:
        file_name = uploaded_file.name.split(".")
        name = file_name[0]
        extension = uploaded_file.name.split(".")[1]
        banco,tipo,mes = name.split("_")
        uploader.upload(uploaded_file, extension,banco,tipo,mes,st.session_state["username"])
    
        
    divisao = st.sidebar.radio('Formato Divisão:', ['Igualmente','Proporcional'])

    try:
        current_df = pd.read_csv(current_output_path+selected_date+".csv")  
        st.data_editor(current_df, use_container_width=True)
        current_df['valor'] = pd.to_numeric(current_df['valor'], errors='coerce')
        grouped_sum = current_df.groupby('transacao')['valor'].sum().reset_index()

        st.metric(label="Balanço", value="273 K", delta="1.2 K")

        st.table(grouped_sum)

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

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')



with open('../config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)




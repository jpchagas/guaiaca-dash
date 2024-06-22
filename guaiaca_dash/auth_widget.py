import streamlit as st
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from logger import ColoredLogger

logger = ColoredLogger(__name__)

def generate_auth_widget():
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
        return True
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
        return False
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        return False
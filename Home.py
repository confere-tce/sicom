import streamlit as st
from funcoes import *
from streamlit_extras.app_logo import add_logo

init(st)

st.subheader("Home", divider='rainbow')

st.session_state.usuario = st.sidebar.text_input('Usuário', 'USER')
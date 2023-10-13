import streamlit as st
from funcoes import *

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

esconde_objetos_streamlit(st)

if 'cod_municipio_AM' not in st.session_state:
    st.session_state.cod_municipio_AM = None
    st.session_state.cod_orgao = None
    st.session_state.mes = None
    st.session_state.ano = None

if st.session_state.cod_municipio_AM:
    st.sidebar.subheader(":red[Dados de Importação:]")
    st.sidebar.write(f"Código Município: {st.session_state.cod_municipio_AM}")
    st.sidebar.write(f"Código Orgão: {st.session_state.cod_orgao}")
    st.sidebar.write(f"Mês: {st.session_state.mes}")
    st.sidebar.write(f"Ano: {st.session_state.ano}")



st.subheader("Home", divider='rainbow')
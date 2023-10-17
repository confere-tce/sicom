import streamlit as st
from funcoes import *
from streamlit_extras.app_logo import add_logo

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

init(st)

if 'cod_municipio_AM' not in st.session_state:
    st.session_state.cod_municipio_AM = None
    st.session_state.cod_orgao = None
    st.session_state.mes = None
    st.session_state.ano = None
    st.session_state.usuario = None

if st.session_state.cod_municipio_AM:
    texto = f"""
        :red[Dados de Importação:] \n
        Código Município: {st.session_state.cod_municipio_AM} \n
        Código Orgão: {st.session_state.cod_orgao} \n
        Mês: {st.session_state.mes} \n
        Ano: {st.session_state.ano} \n
        Usuário: {st.session_state.usuario}
    """
    st.sidebar.info(texto)



st.subheader("Home", divider='rainbow')
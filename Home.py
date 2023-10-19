import streamlit as st
from funcoes import init
from ConsultasSQL import *
import pandas as pd
import altair as alt

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

init(st)

st.subheader("Home", divider='rainbow')

st.experimental_user = st.sidebar.text_input('Usuário', 'USER')
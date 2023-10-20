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

with open('senha.txt') as f:
    senha = f.read()

st.experimental_user = senha
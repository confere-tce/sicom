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


if st.session_state.cod_municipio_AM:
    ##### EMPENHOS #####
    with st.container():

        dados = graficoEmpenhoReceita(st.experimental_user, st.session_state.ano)
        valores = [float(dados[0][0]), float(dados[0][1])]

        col1, col2, col3 = st.columns(3)
        with col1:
            source = pd.DataFrame({
                'Tipo': ['Empenho', 'Receita'],
                'Valores em R$': valores
            })

            bar_chart = alt.Chart(source).mark_bar().encode(
                x='Tipo',
                y='Valores em R$:Q',
                color=alt.Color('Tipo', scale=alt.Scale( domain=['Empenho', 'Receita'], range=['red', 'green']))
            ).properties(
                title='Empenho x Receitas',
                width=300, 
                height=300
            )

            st.altair_chart(bar_chart, use_container_width=True)

        with col2:
            # st.markdown("<p style='color: red; font-weight: bold'>Empenho x Receita</p>", unsafe_allow_html=True) -> de exemplo

            source = pd.DataFrame({
                'Tipo': ['Empenho', 'Receita'],
                'Valores em R$': valores
            })

            bar_chart = alt.Chart(source).mark_arc().encode(
                theta="Valores em R$",
                color="Tipo"
            ).properties(
                title='Empenho x Receitas',
                width=300,
                height=300
            )

            st.altair_chart(bar_chart, use_container_width=True)
        with col3:
            source = pd.DataFrame({
                'Tipo': ['Empenho', 'Receita'],
                'Valores em R$': valores
            })

            bar_chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
                # theta="Valores em R$",
                # color="Tipo:N",
                theta=alt.Theta(
                    field="Valores em R$", 
                    type="quantitative", 
                    stack=True, 
                    scale=alt.Scale(type="linear", rangeMax=1.5708, rangeMin=-1.5708)),
                color=alt.Color('Tipo', scale=alt.Scale(
                    domain=['Empenho', 'Receita'], range=['red', 'green']))
            ).properties(
                title='Empenho x Receitas',
                width=300,
                height=300
            )

            st.altair_chart(bar_chart, use_container_width=True)

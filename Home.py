import streamlit as st
from funcoes import init
from ConsultasSQL import *
import pandas as pd
import plotly.express as px

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
        col1, col2, col3 = st.columns(3)
        with col1:
            dados = graficoEmpenhoReceita(st.experimental_user, st.session_state.ano)
            
            valores = [dados[0][0], dados[0][1]]

            data = {
                'Tipo ': ['Empenho', 'Receita'],
                'Valores em R$ ': valores
            }
            fig = px.pie(data, names='Tipo ', values='Valores em R$ ', title='Empenhos x Receita', color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(autosize=True)
            st.write(fig)
        
        with col2:
            df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
            df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
            fig = px.pie(df, values='pop', names='country', title='Population of European continent')
            st.write(fig)
        with col3:
            df = px.data.tips()
            fig = px.pie(df, values='tip', names='day')
            fig.update_layout(autosize=True)
            st.write(fig)

        dados = graficoEmpenhoReceita(st.experimental_user, st.session_state.ano)
        if dados:
            valores = [dados[0][0], dados[0][1]]
            # st.line_chart(pd.DataFrame(data=dados, columns=["Emp", "Rec"]))

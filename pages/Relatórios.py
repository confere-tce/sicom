import streamlit as st



st.subheader("Relatórios", divider='rainbow')

opcoes = ['Analítico de Despesa', 'Analítico de Despesa por Fonte de Recurso','Analítico de Receita', 'Analítico de Receita Por Fonte Recurso']

relatorios = st.radio("", opcoes, index=0)

st.divider()

if st.button("Imprimir"):
    if relatorios == 'Analítico de Despesa':
        st.caption(relatorios)
    elif relatorios == 'Analítico de Despesa por Fonte de Recurso':
        st.write(relatorios)
    elif relatorios == 'Analítico de Receita':
        st.write(relatorios)
    elif relatorios == 'Analítico de Receita Por Fonte Recurso':
        st.write(relatorios)
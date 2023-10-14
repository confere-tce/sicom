import streamlit as st
import pandas as pd
from ConsultasSQL import *
from funcoes import *


st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

init(st)

if 'cod_municipio_AM' not in st.session_state:
    st.session_state.cod_municipio_AM = None
    st.session_state.cod_orgao = None
    st.session_state.mes = None
    st.session_state.ano = None
    st.session_state.usuario = None

if st.session_state.cod_municipio_AM:
    st.sidebar.subheader(":red[Dados de Importação:]")
    st.sidebar.write(f"Código Município: {st.session_state.cod_municipio_AM}")
    st.sidebar.write(f"Código Orgão: {st.session_state.cod_orgao}")
    st.sidebar.write(f"Mês: {st.session_state.mes}")
    st.sidebar.write(f"Ano: {st.session_state.ano}")
    st.sidebar.write(f"Usuário: {st.session_state.usuario}")

st.subheader("Relatórios", divider='rainbow')

opcoes = ['Analítico de Despesa', 'Movimentos Por Fonte']

relatorios = st.radio("", opcoes, index=0)

st.divider()

if st.button("Imprimir"):
    if relatorios == 'Analítico de Despesa':
        dados = relatorioAnaliticoEmpenho(st.session_state.usuario, st.session_state.ano)

        # Exibe os dados em uma tabela
        if dados:
            df = pd.DataFrame(dados, columns=['Empenho', 'Fonte\nRecurso', 'Cod.\nOper.', 'Empenhado', 'Anulado\nEmpenhado', 'Liquidado', 'Anulado\nLiquidado', 'Pago', 'Anulado\nPago'])

            # Exibindo a tabela estilizada
            st.write('Dados do relatório:')
            st.dataframe(df, width=1800, height=1000)  # Ajuste o tamanho conforme necessário

            pdf_filename = "Analítico de Despesa.pdf"

            exportar_pdf(df, pdf_filename, formato="A4", orientacao="portrait", percentual_tabela=10, tamanho_letra=7)
            exportar_excel(df, "Analítico de Despesa.xlsx")

        else:
            st.write('Nenhum dado encontrado para os parâmetros inseridos.')

    elif relatorios == 'Movimentos Por Fonte':
        dados = totalizaMovimentosPorFonte(st.session_state.usuario, st.session_state.ano)

        # Exibe os dados em uma tabela
        if dados:
            df = pd.DataFrame(dados, columns=['Fonte\nRecurso', 'Receita', 'Anulação\nReceita', 'Entrada\nBanco', 'Saida\nBanco', 'Entrada\nCaixa', 'Saida\nCaixa', 'Entrada\nCUTE', 'Saida\nCUTE', 'Empenho', 'Reforço\nEmpenho', 'Aulação\nEmpenho', 'Liquidação', 'Retenção', 'Anulação\nliquidação', 'Anulação\nRetenção', 'Pagamento\nExtra', 'Anulação\nPagto Extra', 'Pagamento', 'Aulação\nPagamento', 'Outras\nBaixas', 'Anul.Outras\nBaixas', 'Inscrição\nRestos' ])
            st.write('Dados do relatório:')
            st.dataframe(df, width=1800, height=1000)  # Ajuste o tamanho conforme necessário

            pdf_filename = "Movimentos Por Fonte.pdf"
            exportar_pdf(df, pdf_filename, formato="A4", orientacao="landscape", percentual_tabela=6, tamanho_letra=5)
            exportar_excel(df, "Movimentos Por Fonte.xlsx")

        else:
            st.write('Nenhum dado encontrado para os parâmetros inseridos.')
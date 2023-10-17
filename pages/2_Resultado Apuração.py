import streamlit as st
import locale
from funcoes import *
from streamlit_extras.app_logo import add_logo
from ConsultasSQL import *
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from st_aggrid import AgGrid

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

def custom_css(column_name):
    return {
        "selector": f".ag-cell-{column_name}",
        "rule": "text-align: right;",
    }

st.subheader("Resultado da Apuração", divider='rainbow')

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if st.session_state.cod_municipio_AM:
    ######## DADOS BANCÁRIOS ############
    st.subheader(":red[Contas Bancárias:]")

    ano_arquivo = st.session_state.ano

    bancos = confereSaldoFinalBancos(st.session_state.usuario, ano_arquivo)
    if bancos:
        saldo_AM = locale.currency(bancos[0][0], grouping=True, symbol=False)
        saldo_BAL = locale.currency(bancos[0][1], grouping=True, symbol=False)
        diferenca = bancos[0][0] - bancos[0][1]

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Saldo Final no CTB", value=saldo_AM)
        col2.metric(label="Saldos Contabilizados no Balancete", value=saldo_BAL)
        col3.metric(label="Diferença encontrada", value=locale.currency(bancos[0][0] - bancos[0][1], grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")

        if bancos[0][0] == bancos[0][1]:
            st.success("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são diferentes: ⚠️")

            ficha = []
            fonterecurso = []
            saldo_Final_CTB = []
            saldo_Final_BAL = []
            diferenca = []

            diferenca_bancos = buscaDiferencaSaldoFinalBancos(st.session_state.usuario, ano_arquivo)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in diferenca_bancos:
                    # st.write(f"""Ficha: {linha[0]} 
                    #         - Fonte de Recurso: {linha[1]} 
                    #         - Saldo Final no CTB: {locale.currency(linha[2], grouping=True, symbol=False)} 
                    #         - Saldo Final no Balancete: {locale.currency(linha[3], grouping=True, symbol=False)}
                    #         - Diferença: {locale.currency(linha[2] - linha[3], grouping=True, symbol=False)}""")
                    
                    ficha.append(int(linha[0]))
                    fonterecurso.append(linha[1])
                    saldo_Final_CTB.append(locale.currency(linha[2], grouping=True, symbol=False))
                    saldo_Final_BAL.append(locale.currency(linha[3], grouping=True, symbol=False))
                    # diferenca.append(float(linha[2] - linha[3]))
                    # diferenca.append(locale.currency(linha[2] - linha[3], grouping=True, symbol=False))
                    numero_formatado = "{:,.2f}".format(linha[2] - linha[3]).replace(',', ' ').replace('.', ',').replace(' ', '.')
                    diferenca.append(numero_formatado)

                df=pd.DataFrame({
                    "Ficha":ficha,
                    "Fonte Recurso":fonterecurso,
                    "Saldo Final no CTB":saldo_Final_CTB,
                    "Saldo Final no Balancete":saldo_Final_BAL,
                    "Diferença":diferenca,
                    })
                
                # st.dataframe(df, use_container_width=True)

                AgGrid(df)
                
            # Exibe Conciliacao Bancaria
            concilicacao_bancos = buscaValoresConciliacaoBancaria(st.session_state.usuario, ano_arquivo)
            if concilicacao_bancos:
                with st.expander("Informações de Conciliação Bancária"):
                    for linha in concilicacao_bancos:
                        if linha[1] == '1':
                            st.write(f"Ficha: {linha[0]} Entradas contabilizadas e não consideradas no extrato bancário: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '2':
                            st.write(f"Ficha: {linha[0]} Saídas contabilizadas e não consideradas no extrato bancário: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '3':
                            st.write(f"Ficha: {linha[0]} Entradas não consideradas pela contabilidade: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        elif linha[1] == '4':
                            st.write(f"Ficha: {linha[0]} Saídas não consideradas pela contabilidade: {locale.currency(linha[2], grouping=True, symbol=False)}")
                        else:
                            st.write("Valor desconhecido")
            else:
                st.warning("Foi encontrado diferença entre o CTB e Balancete e não possui informação de Conciliação Bancária: ⚠️")
    else:
        st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")


    ######## DADOS EMPENHOS ############
    st.divider()

    st.subheader(":red[Valores Empenhados:]")

    empenhos = confereValoresEmpenhados(st.session_state.usuario, ano_arquivo)
    if empenhos:
        saldo_AM = locale.currency(empenhos[0][0], grouping=True, symbol=False)
        saldo_BAL = locale.currency(empenhos[0][1], grouping=True, symbol=False)
        diferenca = empenhos[0][0] - empenhos[0][1]
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Valores Empenhados", value=saldo_AM)
        col2.metric(label="Valores Contabilizados no Balancete", value=saldo_BAL)
        col3.metric(label="Diferença encontrada", value=locale.currency(empenhos[0][0] - empenhos[0][1], grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")
        
        if empenhos[0][0] == empenhos[0][1]:
            st.success("Os valores dos arquivos EMP e Contabilizados no Balancete são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos EMP e Contabilizados no Balancete são diferentes: ⚠️")
            diferenca = buscaDiferencaValoresEmpenhados(st.session_state.usuario, ano_arquivo)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in diferenca:
                    st.write(f"""Funcional: {linha[0]} {linha[1]} {linha[2]} {linha[3]} {linha[4]} {linha[5]} {linha[6]} {linha[7]} {linha[8]} 
                             - EMP: {locale.currency(linha[9], grouping=True, symbol=False)} 
                             - Balancete: {locale.currency(linha[10], grouping=True, symbol=False)} 
                             - Diferença: {locale.currency(linha[9] - linha[10], grouping=True, symbol=False)}""")
    else:
        st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

    ######## DADOS RECEITAS ############
    st.divider()

    st.subheader(":red[Valores de Receitas:]")

    receitas = confereValoresReceitas(st.session_state.usuario, ano_arquivo)
    if receitas:
        saldo_AM = locale.currency(receitas[0][0], grouping=True, symbol=False)
        saldo_BAL = locale.currency(receitas[0][1], grouping=True, symbol=False)
        diferenca = receitas[0][0] - receitas[0][1]

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Valores Receita", value=saldo_AM)
        col2.metric(label="Valores Contabilizados no Balancete", value=saldo_BAL)
        col3.metric(label="Diferença encontrada", value=locale.currency(diferenca, grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")

        if receitas[0][0] == receitas[0][1]:
            st.success("Os valores dos arquivos REC e Contabilizados no Balancete são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos REC e Contabilizados no Balancete são diferentes: ⚠️")
            diferenca = buscaDiferencaValoresReceitas(st.session_state.usuario, ano_arquivo)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in diferenca:
                    st.write(f"""Receita: {linha[0]} 
                             - Fonte de Recurso: {linha[1]} 
                             - REC: {locale.currency(linha[2], grouping=True, symbol=False)} 
                             - Balancete: {locale.currency(linha[3], grouping=True, symbol=False)}
                             - Diferença: {locale.currency(linha[2] - linha[3], grouping=True, symbol=False)}""")
    else:
        st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

    st.divider()
else:
    st.error("Sem Informações a serem processadas e visualizadas")    
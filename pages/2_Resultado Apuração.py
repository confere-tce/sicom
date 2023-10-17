import streamlit as st
import locale
from funcoes import *
from ConsultasSQL import *
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from st_aggrid import AgGrid

init(st)

st.subheader("Resultado da Apuração", divider='rainbow')

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

if st.session_state.cod_municipio_AM:
    ######## DADOS BANCÁRIOS ############
    st.subheader(":red[Contas Bancárias:]")

    bancos = confereSaldoFinalBancos(st.experimental_user, st.session_state.ano)
    if bancos:
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Saldo Final no CTB", value=locale.currency(bancos[0][0], grouping=True, symbol=False))
        col2.metric(label="Saldos Contabilizados no Balancete", value=locale.currency(bancos[0][1], grouping=True, symbol=False))
        col3.metric(label="Diferença encontrada", value=locale.currency(bancos[0][0] - bancos[0][1], grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")

        if bancos[0][0] == bancos[0][1]:
            st.success("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são diferentes: ⚠️")

            ficha = []
            fonteRecurso = []
            saldo_Final_CTB = []
            saldo_Final_BAL = []
            diferenca = []

            valores = buscaDiferencaSaldoFinalBancos(st.experimental_user, st.session_state.ano)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in valores:
                    ficha.append(linha[0])
                    fonteRecurso.append(linha[1])
                    saldo_Final_CTB.append(locale.currency(linha[2], grouping=True, symbol=False))
                    saldo_Final_BAL.append(locale.currency(linha[3], grouping=True, symbol=False))
                    # diferenca.append(float(linha[2] - linha[3]))
                    diferenca.append(locale.currency(linha[2] - linha[3], grouping=True, symbol=False))

                df=pd.DataFrame({
                    "Ficha":ficha,
                    "Fonte Recurso":fonteRecurso,
                    "Saldo Final no CTB":saldo_Final_CTB,
                    "Saldo Final no Balancete":saldo_Final_BAL,
                    "Diferença":diferenca,
                    })
                
               
                # st.dataframe(df, use_container_width=True)

                AgGrid(df)
                
            # Exibe Conciliacao Bancaria
            concilicacao_bancos = buscaValoresConciliacaoBancaria(st.experimental_user, st.session_state.ano)
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

    empenhos = confereValoresEmpenhados(st.experimental_user, st.session_state.ano)
    if empenhos:
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Valores Empenhados", value=locale.currency(empenhos[0][0], grouping=True, symbol=False))
        col2.metric(label="Valores Contabilizados no Balancete", value=locale.currency(empenhos[0][1], grouping=True, symbol=False))
        col3.metric(label="Diferença encontrada", value=locale.currency(empenhos[0][0] - empenhos[0][1], grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")
        
        if empenhos[0][0] == empenhos[0][1]:
            st.success("Os valores dos arquivos EMP e Contabilizados no Balancete são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos EMP e Contabilizados no Balancete são diferentes: ⚠️")

            funcional = []
            fonteRecurso = []
            saldo_EMP_AM = []
            saldo_Final_BAL = []
            diferenca = []

            valores = buscaDiferencaValoresEmpenhados(st.experimental_user, st.session_state.ano)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in valores:
                    funcional.append(f"{linha[0]}.{linha[1]}.{linha[2]}.{linha[3]}.{linha[4]}.{linha[5]}.{linha[6]}.{linha[7]}")
                    fonteRecurso.append(linha[8])
                    saldo_EMP_AM.append(locale.currency(linha[9], grouping=True, symbol=False))
                    saldo_Final_BAL.append(locale.currency(linha[10], grouping=True, symbol=False))
                    diferenca.append(locale.currency(linha[9] - linha[10], grouping=True, symbol=False))
                
                df=pd.DataFrame({
                    "Funcional":funcional,
                    "Fonte Recurso":fonteRecurso,
                    "Total Empenhado":saldo_EMP_AM,
                    "Saldo Final no Balancete":saldo_Final_BAL,
                    "Diferença":diferenca,
                    })
                
                # st.dataframe(df, use_container_width=True)                

                AgGrid(df)
    else:
        st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

    ######## DADOS RECEITAS ############
    st.divider()

    st.subheader(":red[Valores de Receitas:]")

    receitas = confereValoresReceitas(st.experimental_user, st.session_state.ano)
    if receitas:
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Valores Receita", value=locale.currency(receitas[0][0], grouping=True, symbol=False))
        col2.metric(label="Valores Contabilizados no Balancete", value=locale.currency(receitas[0][1], grouping=True, symbol=False))
        col3.metric(label="Diferença encontrada", value=locale.currency(receitas[0][0] - receitas[0][1], grouping=True, symbol=False))
        style_metric_cards(background_color="back", border_left_color="gray")

        if receitas[0][0] == receitas[0][1]:
            st.success("Os valores dos arquivos REC e Contabilizados no Balancete são iguais: ✅")
        else:
            # Exibe os dados da diferença
            st.warning("Os valores dos arquivos REC e Contabilizados no Balancete são diferentes: ⚠️")

            receita = []
            fonteRecurso = []
            saldo_REC_AM = []
            saldo_Final_BAL = []
            diferenca = []

            valores = buscaDiferencaValoresReceitas(st.experimental_user, st.session_state.ano)
            with st.expander("Dados com diferença nos saldos finais:"):
                for linha in valores:
                    receita.append(linha[0])
                    fonteRecurso.append(linha[1])
                    saldo_REC_AM.append(locale.currency(linha[2], grouping=True, symbol=False))
                    saldo_Final_BAL.append(locale.currency(linha[3], grouping=True, symbol=False))
                    diferenca.append(locale.currency(linha[2] - linha[3], grouping=True, symbol=False))

                    df=pd.DataFrame({
                        "Receita":receita,
                        "Fonte Recurso":fonteRecurso,
                        "Total Receita":saldo_REC_AM,
                        "Saldo Final no Balancete":saldo_Final_BAL,
                        "Diferença":diferenca,
                    })
                
                # st.dataframe(df, use_container_width=True)      
                AgGrid(df)
    else:
        st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

    st.divider()
else:
    st.error("Sem Informações a serem processadas e visualizadas")    
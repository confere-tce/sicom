import streamlit as st
import connection
import os
import pandas as pd
import locale
from funcoes import *
from ConsultasSQL import confereSaldoFinalBancos, buscaDiferencaSaldoFinalBancos, confereValoresEmpenhados, buscaDiferencaValoresEmpenhados, confereValoresReceitas, buscaDiferencaValoresReceitas, buscaValoresConciliacaoBancaria
from sqlalchemy import create_engine
from zipfile import ZipFile
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

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

# usuario = 'USER'  # RANZATTI, teste, depois pegar o usuario logado
usuario = 'USER1'  # GUSTAVO, teste, depois pegar o usuario logado
st.session_state.usuario = usuario


st.subheader("Importação dos arquivos Acompanhamento Mensal (AM) e Balancete", divider='rainbow')

# engine = create_engine('postgresql://jsmcfbqq:dzYLD0UV56ksursrQrP4fHMi_f1X116e@silly.db.elephantsql.com/jsmcfbqq') -> Elephant
engine = create_engine('postgresql://uberabpm:SICSADM@34.86.191.201/uberabpm')

if not os.path.exists('uploads'):
    os.makedirs('uploads')

css = '''
    <style>
    [data-testid="stFileUploadDropzone"] div div::before {content:"Arraste aqui seu arquivo ou clique no botão 'Browse Files' "}
    [data-testid="stFileUploadDropzone"] div div span{display:none;}
    [data-testid="stFileUploadDropzone"] div div::after {font-size: .8em; content:"Somente arquivos formato ZIP"}
    [data-testid="stFileUploadDropzone"] div div small{display:none;}
    </style>
    '''
st.markdown(css, unsafe_allow_html=True)

tudoOK = True
ano_arquivo_AM = ano_arquivo_Bal = None
cod_municipio_AM = cod_municipio_BAL = None
cod_orgao_AM = cod_orgao_BAL = None
mes_AM = mes_BAL = None

col1, col2 = st.columns(2)
with col1:
    arquivo_AM = st.file_uploader("Arquivo AM",
                                  type=["zip"],
                                  accept_multiple_files=False)

    if arquivo_AM is not None:
        arquivo = arquivo_AM.name.split('_')

        if arquivo[0] != 'AM':
            st.error('Arquivo não é AM (Acompanhamento Mensal)', icon="🚨")
            tudoOK = False

        # pega o cod Municipio do AM
        cod_municipio_AM = arquivo[1]
        st.session_state.cod_municipio_AM = cod_municipio_AM

        # pega o orgao do AM
        cod_orgao_AM = arquivo[2]
        st.session_state.cod_orgao = cod_orgao_AM

        # pega o Mes do AM
        mes_AM = arquivo[3]
        st.session_state.mes = mes_AM

        # pegar no ano no arquivo AM
        ano_arquivo_AM = int(arquivo[4][0:4])
        st.session_state.ano = ano_arquivo_AM

    else:
        tudoOK = False

with col2:
    arquivo_BAL = st.file_uploader("Arquivo Balancete",
                                   type=["zip"],
                                   accept_multiple_files=False)

    if arquivo_BAL is not None:
        arquivo = arquivo_BAL.name.split('_')

        if arquivo[0] != 'BALANCETE':
            st.error('Arquivo não é Balancete', icon="🚨")
            tudoOK = False

        # pega o Cod Municipio do Balancete
        cod_municipio_BAL = arquivo[1]

        # pega o orgao do BAL
        cod_orgao_BAL = arquivo[2]

        # pega o Mes do BAL
        mes_BAL = arquivo[3]

        # pegar no ano no arquivo Balancete
        ano_arquivo_Bal = int(arquivo[4][0:4])
    else:
        tudoOK = False

# validações entre os dois arquivos
if ano_arquivo_AM is not None and ano_arquivo_Bal is not None and ano_arquivo_AM != ano_arquivo_Bal:
    st.error(
        f"O Ano do arquivo AM ({ano_arquivo_AM}) está diferente do Ano do arquivo Balancete ({ano_arquivo_Bal}) ", icon="🚨")
    tudoOK = False

if cod_municipio_AM is not None and cod_municipio_BAL is not None and cod_municipio_AM != cod_municipio_BAL:
    st.error(
        f"O Código do Municipio do arquivo AM ({cod_municipio_AM}) está diferente do Código do Municipio do arquivo Balancete ({cod_municipio_BAL}) ", icon="🚨")
    tudoOK = False

if cod_orgao_AM is not None and cod_orgao_BAL is not None and cod_orgao_AM != cod_orgao_BAL:
    st.error(
        f"O Código do Orgão do arquivo AM ({cod_orgao_AM}) está diferente do Código do Orgão do arquivo Balancete ({cod_orgao_BAL}) ", icon="🚨")
    tudoOK = False

if mes_AM is not None and mes_BAL is not None and mes_AM != mes_BAL:
    st.error(
        f"O Mês de geração do arquivo AM ({mes_AM}) está diferente do Mês de geração do arquivo Balancete ({mes_BAL}) ", icon="🚨")
    tudoOK = False

st.divider()

if tudoOK:
    if st.button("Processar os arquivos", type="primary"):

        # deletando informaçoes da tabela
        connection.delete(usuario)

        # criando pasta temporaria e mandando o arquivo zip pra pasta
        pasta_temp = criar_pasta_temporaria()

        pasta_AM = criar_pasta_tipo_arquivo(pasta_temp, "AM")
        pasta_BAL = criar_pasta_tipo_arquivo(pasta_temp, "BAL")

        arquivo_zip_AM = os.path.join(pasta_AM, arquivo_AM.name)
        arquivo_zip_BAL = os.path.join(pasta_BAL, arquivo_BAL.name)

        with open(arquivo_zip_AM, "wb") as f:
            f.write(arquivo_AM.getbuffer())
        f.close()

        with open(arquivo_zip_BAL, "wb") as f:
            f.write(arquivo_BAL.getbuffer())
        f.close()

        # Descompactando o arquivo AM
        with ZipFile(arquivo_zip_AM, 'r') as zip:
            zip.extractall(pasta_AM)

        # Descompactando o arquivo Balancete
        with ZipFile(arquivo_zip_BAL, 'r') as zip:
            zip.extractall(pasta_BAL)

        nomes_colunas = ['seq1', 'seq2', 'seq3', 'seq4', 'seq5', 'seq6', 'seq7', 'seq8', 'seq9', 'seq10', 'seq11', 'seq12', 'seq13', 'seq14', 'seq15', 'seq16', 'seq17', 'seq18', 'seq19', 'seq20',
                         'seq21', 'seq22', 'seq23', 'seq24', 'seq25', 'seq26', 'seq27', 'seq28', 'seq29', 'seq30', 'seq31', 'seq32', 'seq33', 'seq34', 'seq35', 'seq36', 'seq37', 'seq38', 'seq39', 'seq40']
        dtypes = {coluna: str for coluna in range(30)}

        # Carregando os arquivos AM
        my_bar_AM = st.progress(0, text="")
        indice = 1

        quantidade_arquivos = len(os.listdir(pasta_AM))

        for arquivo_csv in os.listdir(pasta_AM):
            if arquivo_csv.upper().endswith('.CSV'):

                my_bar_AM.progress(int(indice / quantidade_arquivos * 100),
                                   text="Processando arquivo Acompanhamento Mensal (AM)... aguarde")
                indice += 1

                # Pegando o nome do arquivo
                x = arquivo_csv.rfind(".")
                nome_arquivo = arquivo_csv[:x].upper()

                processa = False
                if nome_arquivo == 'AEX' or \
                        nome_arquivo == 'ALQ' or \
                        nome_arquivo == 'ANL' or \
                        nome_arquivo == 'AOB' or \
                        nome_arquivo == 'AOC' or \
                        nome_arquivo == 'AOP' or \
                        nome_arquivo == 'ARC' or \
                        nome_arquivo == 'CAIXA' or \
                        nome_arquivo == 'CTB' or \
                        nome_arquivo == 'CONCIBANC' or \
                        nome_arquivo == 'CUTE' or \
                        nome_arquivo == 'EMP' or \
                        nome_arquivo == 'EXT' or \
                        nome_arquivo == 'IDE' or \
                        nome_arquivo == 'IDERP' or \
                        nome_arquivo == 'LQD' or \
                        nome_arquivo == 'OBELAC' or \
                        nome_arquivo == 'OPS' or \
                        nome_arquivo == 'ORGAO' or \
                        nome_arquivo == 'REC' or \
                        nome_arquivo == 'RSP':
                    processa = True

                if processa:

                    arq_completo = os.path.join(pasta_AM, arquivo_csv)

                    # Carregar o arquivo CSV em um DataFrame do Pandas
                    df = pd.read_csv(arq_completo, delimiter=';', encoding='latin-1',
                                     header=None, names=nomes_colunas, dtype=dtypes)

                    # Preencher com None para completar até 30 colunas
                    df = df.reindex(
                        columns=[*df.columns, *range(30 - len(df.columns))])

                    # Manter apenas as 30 primeiras colunas
                    df = df.iloc[:, :30]

                    # Substituir NaN por None
                    df = df.where(pd.notna(df), None)

                    df.insert(0, 'ano', ano_arquivo_AM)
                    df.insert(0, 'arquivo', nome_arquivo)
                    df.insert(0, 'modulo', "AM")
                    df.insert(0, 'usuario', usuario)

                    df.to_sql('tce_sicom', engine,
                              if_exists='append', index=False)
                    

        st.success(
            "Arquivo ACOMPANHAMENTO MENSAL (AM) Importado com Sucesso", icon="✅")
        
        my_bar_AM.empty()

        # Carregando os arquivos Balancete
        my_bar_BAL = st.progress(0, text="")
        indice = 1

        quantidade_arquivos = len(os.listdir(pasta_BAL))

        for arquivo_csv in os.listdir(pasta_BAL):
            if arquivo_csv.upper().endswith('.CSV'):

                my_bar_BAL.progress(int(indice / quantidade_arquivos * 100),
                                    text="Processando arquivo Balancete... aguarde")
                indice += 1

                # Pegando o nome do arquivo
                x = arquivo_csv.rfind(".")
                nome_arquivo = arquivo_csv[:x].upper()

                processa = False
                if nome_arquivo == 'BALANCETE':
                    processa = True

                if processa:

                    arq_completo = os.path.join(pasta_BAL, arquivo_csv)

                    # Carregar o arquivo CSV em um DataFrame do Pandas
                    df = pd.read_csv(arq_completo, delimiter=';', encoding='latin-1',
                                     header=None, names=nomes_colunas, dtype=dtypes)

                    # Preencher com None para completar até 30 colunas
                    df = df.reindex(
                        columns=[*df.columns, *range(30 - len(df.columns))])

                    # Manter apenas as 30 primeiras colunas
                    df = df.iloc[:, :30]

                    # Substituir NaN por None
                    df = df.where(pd.notna(df), None)

                    df.insert(0, 'ano', ano_arquivo_Bal)
                    df.insert(0, 'arquivo', nome_arquivo)
                    df.insert(0, 'modulo', "BAL")
                    df.insert(0, 'usuario', usuario)

                    df.to_sql('tce_sicom', engine,
                              if_exists='append', index=False)
                    

        st.success("Arquivo BALANCETE Importado com Sucesso", icon="✅")

        # Deletando a pasta depois do processamento
        deletando_pasta(pasta_temp)

        my_bar_BAL.empty()

########################################################################################################################################################################################
###################################################################################### RESULTADOS ######################################################################################
########################################################################################################################################################################################

        st.subheader("Resultado da Apuração", divider='rainbow')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        ######## DADOS BANCÁRIOS ############
        st.subheader(":red[Contas Bancárias:]")

        bancos = confereSaldoFinalBancos(st.session_state.usuario, st.session_state.ano)
        if bancos:
            saldo_am_formatado = locale.currency(bancos[0][0], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(bancos[0][1], grouping=True, symbol=False)
            diferenca = abs(bancos[0][0] - bancos[0][1] )

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Saldo Final no CTB", value=saldo_am_formatado)
            col2.metric(label="Saldos Contabilizados no Balancete", value=saldo_bal_formatado)
            if diferenca > 0:
                col3.metric(label="Diferença encontrada", value=locale.currency(diferenca, grouping=True, symbol=False))
            style_metric_cards(background_color="back", border_left_color="gray")


            # with col1:
            #     st.write("Saldo Final no CTB")   
            #     st.write(f"R$ {saldo_am_formatado}")
            # with col2:
            #     st.write("Saldos Contabilizados no Balancete")
            #     st.write(f"R$ {saldo_bal_formatado}")
            # with col3:
            #     if diferenca > 0:
            #         st.write("Diferença encontrada")
            #         st.write(f"R$ {locale.currency(diferenca, grouping=True, symbol=False)}")

            if bancos[0][0] == bancos[0][1]:
                st.success("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são iguais: ✅")
            else:
                # Exibe os dados da diferença
                st.warning("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são diferentes: ⚠️")

                diferenca_bancos = buscaDiferencaSaldoFinalBancos(st.session_state.usuario, st.session_state.ano)
                with st.expander("Dados com diferença nos saldos finais:"):
                    for linha in diferenca_bancos:
                        st.write(f"Ficha: {linha[0]} Fonte de Recurso: {linha[1]} -  Saldo Final no CTB: {locale.currency(linha[2], grouping=True, symbol=False)} - Saldo Final no Balancete: {locale.currency(linha[3], grouping=True, symbol=False)}")
                    
                # Exibe Conciliacao Bancaria
                concilicacao_bancos = buscaValoresConciliacaoBancaria(st.session_state.usuario, st.session_state.ano)
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

        

        st.divider()

        ######## DADOS EMPENHOS ############
        st.subheader(":red[Valores Empenhados:]")

        empenhos = confereValoresEmpenhados(st.session_state.usuario, st.session_state.ano)
        if empenhos:
            saldo_am_formatado = locale.currency(empenhos[0][0], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(empenhos[0][1], grouping=True, symbol=False)
            diferenca = abs(empenhos[0][0] - empenhos[0][1] )
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Valores Empenhados", value=saldo_am_formatado)
            col2.metric(label="Valores Contabilizados no Balancete", value=saldo_bal_formatado)
            if diferenca > 0:
                col3.metric(label="Diferença encontrada", value=locale.currency(diferenca, grouping=True, symbol=False))
            style_metric_cards(background_color="back", border_left_color="gray")

            # with col1:
            #     st.write("Valores Empenhados")
            #     st.write(f"R$ {saldo_am_formatado}")
            # with col2:
            #     st.write("Valores Contabilizados no Balancete")
            #     st.write(f"R$ {saldo_bal_formatado}")
            # with col3:
            #     if diferenca > 0:
            #         st.write("Diferença encontrada")
            #         st.write(f"R$ {locale.currency(diferenca, grouping=True, symbol=False)}")
            
            if empenhos[0][0] == empenhos[0][1]:
                st.success("Os valores dos arquivos EMP e Contabilizados no Balancete são iguais: ✅")
            else:
                # Exibe os dados da diferença
                st.warning("Os valores dos arquivos EMP e Contabilizados no Balancete são diferentes: ⚠️")
                diferenca_empenhos = buscaDiferencaValoresEmpenhados(st.session_state.usuario, st.session_state.ano)
                with st.expander("Dados com diferença nos saldos finais:"):
                    for linha in diferenca_empenhos:
                        st.write(f"Funcional: {linha[0]} {linha[1]} {linha[2]} {linha[3]} {linha[4]} {linha[5]} {linha[6]} {linha[7]} {linha[8]} -  EMP: {locale.currency(linha[9], grouping=True, symbol=False)} - Balancete: {locale.currency(linha[10], grouping=True, symbol=False)}")
        else:
            st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

        st.divider()

        ######## DADOS RECEITAS ############
        st.subheader(":red[Valores de Receitas:]")

        receitas = confereValoresReceitas(st.session_state.usuario, st.session_state.ano)
        if receitas:
            saldo_rec_formatado = locale.currency(receitas[0][0], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(receitas[0][1], grouping=True, symbol=False)
            diferenca = abs(receitas[0][0] - receitas[0][1] )

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Valores Receita", value=saldo_am_formatado)
            col2.metric(label="Valores Contabilizados no Balancete", value=saldo_bal_formatado)
            if diferenca > 0:
                col3.metric(label="Diferença encontrada", value=locale.currency(diferenca, grouping=True, symbol=False))
            style_metric_cards(background_color="back", border_left_color="gray")

            # with col1:
            #     st.write("Valores Receita")
            #     st.write(f"R$: {saldo_rec_formatado}")
            # with col2:
            #     st.write("Valores Contabilizados no Balancete")
            #     st.write(f"R$ {saldo_bal_formatado}")
            # with col3:
            #     if diferenca > 0:
            #         st.write("Diferença encontrada")
            #         st.write(f"R$ {locale.currency(diferenca, grouping=True, symbol=False)}")

            if receitas[0][0] == receitas[0][1]:
                st.success("Os valores dos arquivos REC e Contabilizados no Balancete são iguais: ✅")
            else:
                # Exibe os dados da diferença
                st.warning("Os valores dos arquivos REC e Contabilizados no Balancete são diferentes: ⚠️")
                diferenca_receitas = buscaDiferencaValoresReceitas(st.session_state.usuario, st.session_state.ano)
                with st.expander("Dados com diferença nos saldos finais:"):
                    for linha in diferenca_receitas:
                        st.write(f"Receita: {linha[0]} - Fonte de Recurso: {linha[1]} -  REC: {locale.currency(linha[2], grouping=True, symbol=False)} - Balancete: {locale.currency(linha[3], grouping=True, symbol=False)}")
        else:
            st.error("Não foram encontrados dados para o usuário e ano fornecidos ✅")

        st.divider()
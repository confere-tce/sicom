import streamlit as st
import connection
import os
import pandas as pd
import locale
from funcoes import *
from ConsultasSQL import confereSaldoFinalBancos, buscaDiferencaSaldoFinalBancos, confereValoresEmpenhados, buscaDiferencaValoresEmpenhados, confereValoresReceitas, buscaDiferencaValoresReceitas
from sqlalchemy import create_engine
from zipfile import ZipFile
import VariaveisGlobais



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

st.subheader("Importação dos arquivos Acompanhamento Mensal (AM) e Balancete", divider='rainbow')

tudoOK = True
ano_arquivo_AM = ano_arquivo_Bal = None
cod_municipio_AM = cod_municipio_BAL = None
cod_orgao_AM = cod_orgao_BAL = None
mes_AM = mes_BAL = None
usuario = None

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

        # pega o orgao do AM
        cod_orgao_AM = arquivo[2]

        # pega o Mes do AM
        mes_AM = arquivo[3]

        # pegar no ano no arquivo AM
        ano_arquivo_AM = int(arquivo[4][0:4])
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
    if st.button("Processar o Arquivo", type="primary"):

        usuario = 'USUARIO'  # teste, depois pegar o usuario logado

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
            if arquivo_csv.endswith('.csv'):

                my_bar_AM.progress(int(indice / quantidade_arquivos * 100),
                                   text="Processando arquivo Acompanhamento Mensal (AM)... aguarde")
                indice += 1

                # Pegando o nome do arquivo
                x = arquivo_csv.rfind(".")
                nome_arquivo = arquivo_csv[:x]

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
                    
                    VariaveisGlobais.definir_variaveis_globais(ano_arquivo_AM, usuario)
                    

        st.success(
            "Arquivo 'ACOMPANHAMENTO MENSAL (AM)' Importado com Sucesso", icon="✅")

        # Carregando os arquivos Balancete
        my_bar_BAL = st.progress(0, text="")
        indice = 1

        quantidade_arquivos = len(os.listdir(pasta_BAL))

        for arquivo_csv in os.listdir(pasta_BAL):
            if arquivo_csv.endswith('.csv'):

                my_bar_BAL.progress(int(indice / quantidade_arquivos * 100),
                                    text="Processando arquivo Balancete... aguarde")
                indice += 1

                # Pegando o nome do arquivo
                x = arquivo_csv.rfind(".")
                nome_arquivo = arquivo_csv[:x]

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
                    

        st.success("Arquivo 'BALANCETE' Importado com Sucesso", icon="✅")

        # Deletando a pasta depois do processamento
        deletando_pasta(pasta_temp)

        my_bar_AM.empty()
        my_bar_BAL.empty()

        st.subheader("Resultados", divider='rainbow')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # Exibe os dados bancários

        bancos = confereSaldoFinalBancos(usuario, ano_arquivo_AM)

        st.markdown("**Contas Bancárias:**")
        if bancos:
            saldo_am_formatado = locale.currency(bancos[0][0], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(bancos[0][1], grouping=True, symbol=False)
            st.write(f"Saldo Final no CTB: {saldo_am_formatado}")
            st.write(f"Saldo Final Contas Bancos no Balancete: {saldo_bal_formatado}")
        else:
            st.write("Não foram encontrados dados para o usuário e ano fornecidos.")

        if bancos and bancos[0][0] == bancos[0][1]:
            st.success("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são iguais: ✅")
        else:
            st.error("Os valores dos arquivos CTB e Contas Bancárias do BALANCETE são diferentes: 🚨")
            st.write("Dados com diferença nos saldos finais:")
            diferenca_bancos = buscaDiferencaSaldoFinalBancos(usuario, ano_arquivo_AM)
            # Exibe os dados da diferença
            for linha in diferenca_bancos:
                st.write(f"Ficha: {linha[0]} Fonte de Recurso: {linha[1]} -  Saldo Final no CTB: {locale.currency(linha[2], grouping=True, symbol=False)}, Saldo Final no Balancete: {locale.currency(linha[3], grouping=True, symbol=False)}")

        # Exibe os Empenhos

        st.markdown("**Valores Empenhados:**")
        empenhos = confereValoresEmpenhados(usuario, ano_arquivo_AM)
        if empenhos:
            saldo_am_formatado = locale.currency(empenhos[0][0], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(empenhos[0][1], grouping=True, symbol=False)
            st.write(f"Valores Empenhados: {saldo_am_formatado}")
            st.write(f"Valores Empenhados no Balancete: {saldo_bal_formatado}")
        else:
            st.write("Não foram encontrados dados para o usuário e ano fornecidos.")

        if empenhos and empenhos[0][0] == empenhos[0][1]:
            st.success("Os valores dos arquivos EMP e Contabilizados no Balancete são iguais: ✅")
        else:
            st.error("Os valores dos arquivos EMP e Contabilizados no Balancete são diferentes: 🚨")
            st.write("Dados com diferença nos saldos finais:")
            diferenca_empenhos = buscaDiferencaValoresEmpenhados(usuario, ano_arquivo_AM)
            # Exibe os dados da diferença
            for linha in diferenca_empenhos:
                st.write(f"Funcional: {linha[0]} {linha[1]} {linha[2]} {linha[3]} {linha[4]} {linha[5]} {linha[6]} {linha[7]} {linha[8]} -  EMP: {locale.currency(linha[9], grouping=True, symbol=False)}, Balancete: {locale.currency(linha[10], grouping=True, symbol=False)}")

        # Exibe os Receitas

        st.markdown("**Valores de Receitas:**")
        receitas = confereValoresReceitas(usuario, ano_arquivo_AM)
        if receitas:
            saldo_rec_formatado = locale.currency(receitas[0][0], grouping=True, symbol=False)
            saldo_ctb_formatado = locale.currency(receitas[0][1], grouping=True, symbol=False)
            saldo_bal_formatado = locale.currency(receitas[0][2], grouping=True, symbol=False)
            st.write(f"Valores REC: {saldo_rec_formatado}")
            st.write(f"Valores CTB: {saldo_ctb_formatado}")
            st.write(f"Valores Contabilizados no Balancete: {saldo_bal_formatado}")
        else:
            st.write("Não foram encontrados dados para o usuário e ano fornecidos.")

        if receitas and receitas[0][0] == receitas[0][1] and receitas[0][0] == receitas[0][2] and receitas[0][1] == receitas[0][2]:
            st.success("Os valores dos arquivos REC, CTB e Contabilizados no Balancete são iguais: ✅")
        else:
            st.error("Os valores dos arquivos REC, CTB e Contabilizados no Balancete são diferentes: 🚨")
            st.write("Dados com diferença nos saldos finais:")
            diferenca_receitas = buscaDiferencaValoresReceitas(usuario, ano_arquivo_AM)
            # Exibe os dados da diferença
            for linha in diferenca_receitas:
                st.write(f"Receita: {linha[0]} - Fonte de Recurso: {linha[1]} -  REC: {locale.currency(linha[2], grouping=True, symbol=False)}, CTB: {locale.currency(linha[3], grouping=True, symbol=False)}, Balancete: {locale.currency(linha[4], grouping=True, symbol=False)}")

import streamlit as st
import datetime
import connection 
import os
import pandas as pd 
from funcoes import criar_pasta_usuario, deletando_pasta 
from sqlalchemy import create_engine 
from zipfile import ZipFile


def main():
    ano_corrente = datetime.datetime.now().year

    # engine = create_engine('postgresql://jsmcfbqq:dzYLD0UV56ksursrQrP4fHMi_f1X116e@silly.db.elephantsql.com/jsmcfbqq') -> Elephant
    engine = create_engine('postgresql://uberabpm:SICSADM@34.86.191.201/uberabpm')

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    st.title = "Carregar arquivo AM (Acompanhamento Mensal)"

    menu = ["Home", "Importar Arquivo", "Relatórios"]
    escolha = st.sidebar.selectbox("Menu", menu)

    css = '''
        <style>
        [data-testid="stFileUploadDropzone"] div div::before {content:"Arraste aqui seu arquivo ou clique no botão 'Browse Files' "}
        [data-testid="stFileUploadDropzone"] div div span{display:none;}
        [data-testid="stFileUploadDropzone"] div div::after {font-size: .8em; content:"Somente arquivos formato ZIP"}
        [data-testid="stFileUploadDropzone"] div div small{display:none;}
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    if escolha == "Home":
        st.subheader("Home")
    elif escolha == "Importar Arquivo":
        st.subheader("Importar Arquivo")

        tudoOK = True

        arquivoAM = st.file_uploader("Arquivos AM", 
                                    type=["zip"], 
                                    accept_multiple_files=False, 
                                    label_visibility="hidden",
                                    key="arquivo")
        if arquivoAM is not None:
            nome_arquivo = arquivoAM.name
            arquivo = nome_arquivo.split('_')

            if arquivo[0] != 'AM':
                st.warning("Arquivo não é AM (Acompanhamento Mensal)")
                tudoOK= False

            #pegar no ano no arquivo
            ano_arquivo = int(arquivo[4][0:4])
            if ano_corrente != ano_arquivo:
                st.warning("Ano do Arquivo Inválido")
                tudoOK = False

            if tudoOK:
                if st.button("Processar o Arquivo", type="primary"):

                    usuario = 'USUARIO' #teste, depois pegar o usuario logado

                    # deletando informaçoes da tabela
                    connection.delete(usuario)

                    #criando pasta temporaria e mandando o arquivo zip pra pasta
                    pata_temp = criar_pasta_usuario()
                    arquivo_zip = os.path.join(pata_temp, arquivoAM.name)
                    with open(arquivo_zip, "wb") as f:
                        f.write(arquivoAM.getbuffer())
                    f.close()

                    # Descompactando o arquivo zipado
                    with ZipFile(arquivo_zip, 'r') as zip:
                        zip.extractall(pata_temp) 

                    nomes_colunas = ['seq1', 'seq2', 'seq3', 'seq4', 'seq5', 'seq6', 'seq7', 'seq8', 'seq9', 'seq10', 'seq11', 'seq12', 'seq13', 'seq14', 'seq15', 'seq16', 'seq17', 'seq18', 'seq19', 'seq20', 'seq21', 'seq22', 'seq23', 'seq24', 'seq25', 'seq26', 'seq27', 'seq28', 'seq29', 'seq30', 'seq31', 'seq32', 'seq33', 'seq34', 'seq35', 'seq36', 'seq37', 'seq38', 'seq39', 'seq40']
                    dtypes = {coluna: str for coluna in range(30)}  

                    my_bar = st.progress(0, text="Processando... aguarde")
                    indice = 1

                    # Carregando os arquivos da pasta
                    for arquivo_csv in os.listdir(pata_temp):
                        if arquivo_csv.endswith('.csv'):

                            my_bar.progress(int(indice / 49 * 100), text="Processando... aguarde")
                            indice +=1

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

                                arq_completo = os.path.join(pata_temp, arquivo_csv)

                                # Carregar o arquivo CSV em um DataFrame do Pandas
                                df = pd.read_csv(arq_completo, delimiter=';', encoding='latin-1', header=None, names=nomes_colunas, dtype=dtypes)

                                # Preencher com None para completar até 30 colunas
                                df = df.reindex(columns=[*df.columns, *range(30 - len(df.columns))])

                                # Manter apenas as 30 primeiras colunas
                                df = df.iloc[:, :30]

                                # Substituir NaN por None
                                df = df.where(pd.notna(df), None)

                                df.insert(0, 'ano', ano_arquivo)
                                df.insert(0, 'arquivo', nome_arquivo) 
                                df.insert(0, 'modulo', arquivo[0])  
                                df.insert(0, 'usuario', usuario)  

                                df.to_sql('tce_sicom', engine, if_exists='append', index=False)

                    # Deletando a pasta depois do processamento
                    deletando_pasta(pata_temp)

                    my_bar.empty()

                    st.warning("Arquivo Importado com Sucesso")
    else:
        st.subheader("Relatórios")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Acompanhamento Mensal (AM)")
            arquivoAM = st.file_uploader("Arquivos AM", 
                                    type=["zip"], 
                                    accept_multiple_files=False, 
                                    label_visibility="hidden")

        with col2:
            st.header("Balancete")
            arquivoBAL = st.file_uploader("Arquivos Balancete", 
                                    type=["zip"], 
                                    accept_multiple_files=False, 
                                    label_visibility="hidden")


if __name__ == '__main__':
    main()

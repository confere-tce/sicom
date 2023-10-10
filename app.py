import os 
import connection 
import pandas as pd 
from funcoes import *
from flask import Flask, render_template, request, url_for, redirect
from zipfile import ZipFile
from sqlalchemy import create_engine 
from relatorios import relatorioAnaliticoEmpenho, totalizaMovimentosPorFonte, movimentosEmpenhoPorFonte, diarioDespesa


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# engine = create_engine('postgresql://jsmcfbqq:dzYLD0UV56ksursrQrP4fHMi_f1X116e@silly.db.elephantsql.com/jsmcfbqq')
engine = create_engine('postgresql://uberabpm:SICSADM@34.86.191.201/uberabpm')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/') 
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'arquivo' not in request.files:
        return "Selecione um arquivo"
    
    file = request.files['arquivo']

    if file.filename == '':
        return "Selecione um arquivo"
    
    nome_arquivo, extensao = os.path.splitext(file.filename)

    # dando split no nome do arquivo para validacao
    arquivo_AM = nome_arquivo.split('_')
    if arquivo_AM[0] != 'AM':
         return "Arquivo não é de acompanhamento mensal"
  
    if extensao != '.zip':
        return "Terminação do arquivo '" + file.filename + "' inválido. Tem que ser compactado (zip)"
    
    if file:

        print("entrei")

        usuario = 'USUARIO'
        ano = arquivo_AM[4][0:4]

        # deletando informaçoes da tabela
        connection.delete(usuario)

        pasta_temp = criar_pasta_temporaria()
        print(pasta_temp)
        pasta_AM = criar_pasta_tipo_arquivo(pasta_temp, "AM")
        print(pasta_AM)
        pasta_BAL = criar_pasta_tipo_arquivo(pasta_temp, "BAL")

        arquivo_zip_AM = os.path.join(pasta_AM, file.filename)
        # arquivo_zip_BAL = os.path.join(pasta_BAL, arquivo_BAL.name)

        file.save(arquivo_zip_AM)
        # file.save(arquivo_zip_BAL)

        # Descompactando o arquivo AM zipado
        with ZipFile(arquivo_zip_AM, 'r') as zip:
            zip.extractall(pasta_AM) 

        # Descompactando o arquivo BAL zipado
        # with ZipFile(arquivo_zip_BAL, 'r') as zip:
        #     zip.extractall(pasta_BAL)             

        nomes_colunas = ['seq1', 'seq2', 'seq3', 'seq4', 'seq5', 'seq6', 'seq7', 'seq8', 'seq9', 'seq10', 'seq11', 'seq12', 'seq13', 'seq14', 'seq15', 'seq16', 'seq17', 'seq18', 'seq19', 'seq20', 'seq21', 'seq22', 'seq23', 'seq24', 'seq25', 'seq26', 'seq27', 'seq28', 'seq29', 'seq30', 'seq31', 'seq32', 'seq33', 'seq34', 'seq35', 'seq36', 'seq37', 'seq38', 'seq39', 'seq40']
        dtypes = {coluna: str for coluna in range(30)}  

        # Carregando os arquivos AM
        for arquivo_CSV in os.listdir(pasta_AM):
            if arquivo_CSV.endswith('.csv'):

                # Pegando o nome do arquivo
                x = arquivo_CSV.rfind(".")
                nome_arquivo = arquivo_CSV[:x]

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

                    arq_completo = os.path.join(pasta_AM, arquivo_CSV)

                    # Carregar o arquivo CSV em um DataFrame do Pandas
                    df = pd.read_csv(arq_completo, delimiter=';', encoding='latin-1', header=None, names=nomes_colunas, dtype=dtypes)

                    # Preencher com None para completar até 30 colunas
                    df = df.reindex(columns=[*df.columns, *range(30 - len(df.columns))])

                    # Manter apenas as 30 primeiras colunas
                    df = df.iloc[:, :30]

                    # Substituir NaN por None
                    df = df.where(pd.notna(df), None)

                    df.insert(0, 'ano', ano)
                    df.insert(0, 'arquivo', nome_arquivo) 
                    df.insert(0, 'modulo', "AM")  
                    df.insert(0, 'usuario', usuario)  

                    df.to_sql('tce_sicom', engine, if_exists='append', index=False)


        # Deletando a pasta depois do processamento
        deletando_pasta(pasta_temp)

        return redirect(url_for("resultado", usuario=usuario, ano=ano))
    
@app.route('//resultado/<usuario>/<ano>')
def resultado(usuario,ano):
    # Obtém os dados da função de consulta
    dados = relatorioAnaliticoEmpenho(usuario, ano)
    fontes = totalizaMovimentosPorFonte(usuario, ano)
    empenhos = movimentosEmpenhoPorFonte(usuario, ano)
    diarios = diarioDespesa(usuario, ano)

    return render_template('resultado.html', dados=dados, fontes=fontes, empenhos=empenhos, diarios = diarios)    

if __name__ == '__main__':
    app.run(debug=True)
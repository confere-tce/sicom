import os
import csv
from funcoes import criar_pasta_usuario, deletando_pasta
from flask import Flask, render_template, request, url_for, redirect
from zipfile import ZipFile
import connection

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
    arquivo = nome_arquivo.split('_')
    if arquivo[0] != 'AM':
         return "Arquivo não é de acompanhamento mensal"
  
    if extensao != '.zip':
        return "Terminação do arquivo '" + file.filename + "' inválido. Tem que ser compactado (zip)"

    if file:

        usuario = 'USUARIO'

        # deletando informaçoes da tabela
        connection.delete(usuario)

        pasta_usuario = criar_pasta_usuario()
        filename = os.path.join(pasta_usuario, file.filename)
        file.save(filename)

        # Descompactando o arquivo zipado
        with ZipFile(filename, 'r') as zip:
            zip.extractall(pasta_usuario) 

        # Carregando os arquivos da pasta
        for arq in os.listdir(pasta_usuario):
            if arq.endswith('.csv'):

                # Pegando o nome do arquivo
                x = arq.rfind(".")
                nome_arquivo = arq[:x]

                processa = False
                # if nome_arquivo == 'AEX' or \
                #     nome_arquivo == 'ALQ' or \
                #     nome_arquivo == 'ANL' or \
                #     nome_arquivo == 'AOB' or \
                #     nome_arquivo == 'AOC' or \
                #     nome_arquivo == 'AOP' or \
                #     nome_arquivo == 'ARC' or \
                #     nome_arquivo == 'CAIXA' or \
                #     nome_arquivo == 'CTB' or \
                #     nome_arquivo == 'CUTE' or \
                #     nome_arquivo == 'EMP' or \
                #     nome_arquivo == 'EXT' or \
                #     nome_arquivo == 'IDE' or \
                #     nome_arquivo == 'IDERP' or \
                #     nome_arquivo == 'LQD' or \
                #     nome_arquivo == 'OBELAC' or \
                #     nome_arquivo == 'OPS' or \
                #     nome_arquivo == 'ORGAO' or \
                #     nome_arquivo == 'REC':
                if nome_arquivo == 'ALQ' :
                    processa = True

                if processa:

                    arq_completo = os.path.join(pasta_usuario, arq)

                    with open(arq_completo, mode='r') as arq_csv:
                        linha = csv.reader(arq_csv, delimiter=';')
                        for colunas in linha:

                            colunas.extend([None] * (30 - len(colunas)))
                            print(colunas)

                            connection.insere('USUARIO', 'AM', nome_arquivo, colunas)

        # Deletando a pasta depois do processamento
        deletando_pasta(pasta_usuario)

        return "Arquivo " + file.filename + " importado com Sucesso"

if __name__ == '__main__':
    app.run(debug=True)
import os
import csv
from funcoes import criar_pasta_usuario, deletando_pasta
from flask import Flask, render_template, request, url_for, redirect
from zipfile import ZipFile
import psycopg2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

conn = psycopg2.connect(
    dbname="jsmcfbqq",
    user="jsmcfbqq",
    password="dzYLD0UV56ksursrQrP4fHMi_f1X116e",
    host="silly.db.elephantsql.com"
)

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

        cursor = conn.cursor()
        cursor.execute("DELETE from tce_sicom where usuario = %s ", (usuario,))
        conn.commit()
        cursor.close()

        pasta_usuario = criar_pasta_usuario()
        filename = os.path.join(pasta_usuario, file.filename)
        file.save(filename)

        # Descompactando o arquivo zipado
        with ZipFile(filename, 'r') as zip:
            zip.extractall(pasta_usuario) 

        # Carregando os arquivos da pasta
        for arq in os.listdir(pasta_usuario):
            if arq.endswith('.csv'):
                # print(arq)

                # Pegando o nome do arquivo
                x = arq.rfind(".")
                nome_arquivo = arq[:x]

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
                    nome_arquivo == 'REC':
                    processa = True

                if processa:

                    arq_completo = os.path.join(pasta_usuario, arq)

                    with open(arq_completo, mode='r') as arq_csv:
                        linha = csv.reader(arq_csv, delimiter=';')
                        for colunas in linha:

                            colunas.extend([None] * (30 - len(colunas)))
                            print(colunas)

                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO tce_sicom \
                                           (USUARIO, MODULO, ARQUIVO, SEQ1, SEQ2, SEQ3, SEQ4, SEQ5, SEQ6, SEQ7, SEQ8, SEQ9, SEQ10, SEQ11, SEQ12, SEQ13, SEQ14, SEQ15, SEQ16, SEQ17, SEQ18, SEQ19, SEQ20, SEQ21, SEQ22, SEQ23, SEQ24, SEQ25, SEQ26, SEQ27, SEQ28, SEQ29, SEQ30) \
                                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                                           ('USUARIO','AM', nome_arquivo, colunas[0], colunas[1], colunas[2], colunas[3], colunas[4], colunas[5], colunas[6], colunas[7], colunas[8], colunas[9], colunas[10], colunas[11], colunas[12], colunas[13], colunas[14], colunas[15], colunas[16], colunas[17], colunas[18], colunas[19], colunas[20], colunas[21], colunas[22], colunas[23], colunas[24], colunas[25], colunas[26], colunas[27], colunas[28], colunas[29]))
                            conn.commit()
                            cursor.close()

        # Deletando a pasta depois do processamento
        deletando_pasta(pasta_usuario)

        return "Arquivo " + file.filename + " importado com Sucesso"

if __name__ == '__main__':
    app.run(debug=True)
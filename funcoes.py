import random
import os
import string
import shutil

def criar_pasta_temporaria():

    comprimento = 15
    pasta_temporaria = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(comprimento))
    # nome_nova_pasta = '12345678910'
    # nome_nova_pasta = '69162913620'

    pasta_temporaria = os.path.join('uploads', pasta_temporaria)
    os.mkdir(pasta_temporaria)

    return pasta_temporaria

def criar_pasta_tipo_arquivo(pasta_temp, tipo_arquivo):

    pasta_temporaria = os.path.join(pasta_temp, tipo_arquivo)
    os.mkdir(pasta_temporaria)

    return pasta_temporaria

def deletando_pasta(pasta):
    try:
        shutil.rmtree(pasta)
    except OSError as e:
        print(f"Error:{ e.strerror}")
import random
import os
import string
import shutil

def criar_pasta_usuario():

    comprimento = 15
    nome_nova_pasta = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(comprimento))
    # nome_nova_pasta = '12345678910'
    # nome_nova_pasta = '69162913620'
    caminho_nova_pasta = os.path.join('uploads', nome_nova_pasta)

    # Deletando a pasta antes de criar novamente
    deletando_pasta(caminho_nova_pasta)

    os.mkdir(caminho_nova_pasta)

    return caminho_nova_pasta

def deletando_pasta(pasta):
    try:
        shutil.rmtree(pasta)
    except OSError as e:
        print(f"Error:{ e.strerror}")
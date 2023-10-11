anoGlobal = None
usuarioGlobal = None


def definir_variaveis_globais(novo_ano, novo_usuario):
    global anoGlobal  # Indica que estamos modificando a variável global
    global usuarioGlobal  # Indica que estamos modificando a variável global
    
    anoGlobal = novo_ano
    usuarioGlobal = novo_usuario
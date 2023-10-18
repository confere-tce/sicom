import connection


def relatorioAnaliticoEmpenho(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT 
            EMPENHO, 
            FONTERECURSO, 
            CO, 
            EMPENHADO, 
            ANULEMPENHADO, 
            LIQUIDADO, 
            ANULIQUIDADO, 
            PAGO, 
            ANULPAGO
            FROM VW_RELATORIOANALITICOEMPENHO_2023
            WHERE 1=1
            AND USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def totalizaMovimentosPorFonte(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT 
            FONTERECURSO, 
            RECEITA, 
            ANURECEITA, 
            ENTRADABANCO, 
            SAIDABANCO, 
            ENTRADACAIXA, 
            SAIDACAIXA, 
            ENTRADACUTE, 
            SAIDACUTE, 
            EMPENHO, 
            REFORCOEMPENHO, 
            ANULEMPENHO, 
            LIQUIDACAO, 
            RETENCAO, 
            ANULIQUIDACAO, 
            ANURETENCAO, 
            PAGAMENTOEXT, 
            ANULPAGTOEXT, 
            PAGAMENTO, 
            ANULPAGAMENTO, 
            OUTRASBAIXAS, 
            ANULOUTRASBAIXAS, 
            INSCRICAORESTOS 
            FROM 
            VW_RELATORIOMOVIMENTOSPORFONTE_2023
            WHERE USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def movimentosEmpenhoPorFonte(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT X.SEQ4 AS FONTERECURSO, 
        X.SEQ5 AS CO, 
        SUM(EMPENHOS) AS EMPENHADO, 
        SUM(ANULAEMPENHO) AS ANULEMPENHO, 
        SUM(LIQUIDACAO) AS LIQUIDADO, 
        SUM(ANULIQUIDACAO) AS ANULIQUIDADO, 
        SUM(PAGAMENTO) AS PAGAMENTO, 
        SUM(ANUPAGAMENTO) AS ANULPAGAMENTO
        FROM (

        SELECT A.USUARIO AS USUARIO, A.ANO AS ANO, B.SEQ4, B.SEQ5, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHOS, 0 AS ANULAEMPENHO, 0 AS LIQUIDACAO, 0 AS ANULIQUIDACAO, 0 AS PAGAMENTO, 0 AS ANUPAGAMENTO
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ11 = B.SEQ3 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, B.SEQ4, B.SEQ5

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ5, A.SEQ6, 0, SUM(CAST(REPLACE(A.SEQ7, ',', '.') AS NUMERIC)) AS ANULAEMPENHO, 0, 0, 0, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ5, A.SEQ6

        UNION ALL

        SELECT A.USUARIO, A.ANO, B.SEQ3, B.SEQ4,  0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDACAO, 0, 0, 0
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, B.SEQ3, B.SEQ4

        UNION ALL

        SELECT A.USUARIO, A.ANO, B.SEQ3, B.SEQ4, 0, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDACAO, 0, 0
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO)
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, B.SEQ3, B.SEQ4

        UNION ALL

        SELECT A.USUARIO, A.ANO, A.SEQ11, A.SEQ12, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS PAGAMENTO, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ11, A.SEQ12

        UNION ALL

        SELECT A.USUARIO, A.ANO, A.SEQ14, A.SEQ15, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS ANUPAGAMENTO
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ14, A.SEQ15) X
        WHERE 1=1
        AND X.USUARIO = %s
        AND X.ANO = %s
        GROUP BY X.SEQ4, X.SEQ5
        ORDER BY X.SEQ4, X.SEQ5
    """

    cursor.execute(consulta, (usuario, ano,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def diarioDespesa(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT 
            DATAMOVIMENTO , 
            DOCUMENTO , 
            DETALHE, 
            TIPOMOVIMENTO ,
            HISTORICO, 
            FONTERECURSO , 
            VLRMOVIMENTO  
            FROM VW_RELATORIODIARIODESPESA_2023
            WHERE X.USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

# Conferencias


def confereSaldoFinalBancos(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                VW_CONFERESALDOFINALBANCOS_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def confereSaldoFinalBancosNaoCompoe(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                vw_ConfereSaldoFinalBancosNaoCompoe_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def confereSaldoFinalBancosRestituiveis(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                vw_ConfereSaldoFinalBancosRestituiveis_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def buscaDiferencaSaldoFinalBancos(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                FICHA,
                FONTERECURSO,
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                VW_BUSCADIFERENCASALDOFINALBANCOS_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def buscaDiferencaSaldoFinalBancosNaoCompoe(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                FICHA,
                FONTERECURSO,
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                vw_BuscaDiferencaSaldoFinalBancosNaoCompoe_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def vw_BuscaDiferencaSaldoFinalBancosRestituiveis(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT
                FICHA,
                FONTERECURSO,
                SALDOFINALCTB,
                SALDOFINALBAL
            FROM
                vw_BuscaDiferencaSaldoFinalBancosRestituiveis_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def confereValoresEmpenhados(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano >= 2023:
        consulta = """
            SELECT
                AM,
                BALANCETE
            FROM
                VW_CONFEREVALORESEMPENHADOS_2023
            WHERE
                USUARIO = %s
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def buscaDiferencaValoresEmpenhados(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT
            SEQ4, SEQ5, SEQ6, SEQ7, SEQ8, SEQ9, SEQ10, SEQ11, SEQ13, AM, BALANCETE
        FROM
            VW_BUSCADIFERENCAVALORESEMPENHADOS_2023
        WHERE
            USUARIO = %s
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def confereValoresReceitas(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano >= 2023:
        consulta = """
            SELECT
                REALREC, 
                REALBALANCETE
            FROM
                VW_CONFEREVALORESRECEITAS_2023
            WHERE
                USUARIO = %s
        """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def buscaDiferencaValoresReceitas(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT
            RECEITA,
            FONTERECURSO,
            REALREC,
            REALBALANCETE
        FROM
            VW_BUSCADIFERENCAVALORESRECEITAS_2023
        WHERE
            USUARIO = %s;
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def buscaValoresConciliacaoBancaria(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT CAST(SEQ3 AS DECIMAL(20,0)) AS FICHA, SEQ4 AS TIPOCONCBANC, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS VALOR
        FROM TCE_SICOM
        WHERE MODULO = 'AM'
        AND ARQUIVO = 'CONCIBANC'
        AND SEQ1 = '11'
        AND USUARIO = %s
        AND ANO = %s
        GROUP BY CAST(SEQ3 AS DECIMAL(20,0)), SEQ4
        ORDER BY CAST(SEQ3 AS DECIMAL(20,0)), SEQ4
    """

    cursor.execute(consulta, (usuario, ano,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def graficoEmpenhoReceita(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano == 2023:
        consulta = """
            SELECT SUM(X.EMP) as EMP, SUM(X.REC) as REC
            FROM (
            SELECT
                AM AS EMP, 0 AS REC
            FROM
                VW_CONFEREVALORESEMPENHADOS_2023
            WHERE
                USUARIO = %s
                
            UNION ALL
                
            SELECT
                0, REALREC
            FROM
                VW_CONFEREVALORESRECEITAS_2023
            WHERE
                USUARIO = %s
            ) X 
        """

    cursor.execute(consulta, (usuario, usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

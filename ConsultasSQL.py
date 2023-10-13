import connection


def relatorioAnaliticoEmpenho(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT 
        CAST(X.EMPENHO AS INT) AS EMPENHO, 
        X.FONTERECURSO, 
        X.CO, 
        SUM(X.EMPENHADO) AS EMPENHADO, 
        SUM(X.ANULEMPENHADO) AS ANULEMPENHADO, 
        SUM(X.LIQUIDADO) AS LIQUIDADO, 
        SUM(X.ANULIQUIDADO) AS ANULIQUIDADO, 
        SUM(X.PAGO) AS PAGO, 
        SUM(X.ANULPAGO) AS ANULPAGO
        FROM (

        SELECT  A.USUARIO AS USUARIO, A.ANO, A.SEQ3 AS EMPENHO, A.SEQ4 AS FONTERECURSO, A.SEQ5 AS CO, SUM(CAST(REPLACE(A.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHADO, 0 AS ANULEMPENHADO, 0 AS LIQUIDADO, 0 AS ANULIQUIDADO, 0 AS PAGO, 0 AS ANULPAGO
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ3, A.SEQ4, A.SEQ5

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ3, A.SEQ5, A.SEQ6, 0, SUM(CAST(REPLACE(A.SEQ7, ',', '.') AS NUMERIC)) AS ANULEMPENHADO, 0, 0, 0, 0 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ3, A.SEQ5, A.SEQ6

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ6, B.SEQ3, B.SEQ4, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDADO, 0, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        AND A.SEQ5 = '1'
        GROUP BY A.USUARIO, A.ANO, A.SEQ6, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ5, B.SEQ3, B.SEQ4, 0, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDADO, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, A.SEQ5, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ7, A.SEQ11, A.SEQ12, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS PAGO, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '11'
        AND A.SEQ6 IN ('1','2')
        GROUP BY A.USUARIO, A.ANO, A.SEQ7, A.SEQ11, A.SEQ12

        UNION ALL 

        SELECT A.USUARIO, A.ANO, A.SEQ10, A.SEQ14, A.SEQ15, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ16, ',', '.') AS NUMERIC)) AS ANULPAGO 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.ANO, A.SEQ10, A.SEQ14, A.SEQ15) X
        WHERE 1=1
        AND X.USUARIO = %s
        AND X.ANO = %s
        GROUP BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
        ORDER BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
    """

    cursor.execute(consulta, (usuario, ano,))
    dados = cursor.fetchall()

    cursor.close()

    return dados


def totalizaMovimentosPorFonte(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    consulta = """
        SELECT CAST(SEQ3 AS INT) AS FONTERECURSO, 
        SUM(X.RECEITA) AS RECEITA, 
        SUM(X.ANURECEITA) AS ANURECEITA, 
        SUM(X.ENTRADABANCO) AS ENTRADABANCO, 
        SUM(X.SAIDABANCO) AS SAIDABANCO, 
        SUM(X.ENTRADACAIXA) AS ENTRADACAIXA, 
        SUM(X.SAIDACAIXA) AS SAIDACAIXA, 
        SUM(X.ENTRADACUTE) AS ENTRADACUTE, 
        SUM(X.SAIDACUTE) AS SAIDACUTE, 
        SUM(X.EMPENHO) AS EMPENHO, 
        SUM(X.REFORCOEMPENHO) AS REFORCOEMPENHO, 
        SUM(X.ANULEMPENHO) AS ANULEMPENHO, 
        SUM(X.LIQUIDACAO) AS LIQUIDACAO, 
        SUM(X.RETENCAO) AS RETENCAO, 
        SUM(X.ANULIQUIDACAO) AS ANULIQUIDACAO, 
        SUM(X.ANURETENCAO) AS ANURETENCAO, 
        SUM(X.PAGAMENTOEXT) AS PAGAMENTOEXT, 
        SUM(X.ANULPAGTOEXT) AS ANULPAGTOEXT, 
        SUM(X.PAGAMENTO) AS PAGAMENTO, 
        SUM(X.ANULPAGAMENTO) AS ANULPAGAMENTO, 
        SUM(X.OUTRASBAIXAS) AS OUTRASBAIXAS, 
        SUM(X.ANULOUTRASBAIXAS) AS ANULOUTRASBAIXAS, 
        SUM(X.INSCRICAORESTOS) AS INSCRICAORESTOS 
        FROM (
        SELECT USUARIO, ANO, SEQ3, SUM(CAST(REPLACE(SEQ11, ',', '.') AS NUMERIC)) AS RECEITA, 0 AS ANURECEITA, 0 AS ENTRADABANCO, 0 AS SAIDABANCO, 0 AS ENTRADACAIXA, 0 AS SAIDACAIXA, 0 AS ENTRADACUTE, 0 AS SAIDACUTE, 0 AS EMPENHO, 0 AS REFORCOEMPENHO, 0 AS ANULEMPENHO, 0 AS LIQUIDACAO, 0 AS RETENCAO, 0 AS ANULIQUIDACAO, 0 AS ANURETENCAO, 0 AS PAGAMENTOEXT, 0 AS ANULPAGTOEXT, 0 AS PAGAMENTO, 0 AS ANULPAGAMENTO, 0 AS OUTRASBAIXAS, 0 AS ANULOUTRASBAIXAS, 0 AS INSCRICAORESTOS 
        FROM TCE_SICOM
        WHERE ARQUIVO = 'REC' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, SUM(CAST(REPLACE(SEQ11, ',', '.') AS NUMERIC)) AS ANURECEITA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ARC' 
        AND SEQ1 = '21'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ENTRADABANCO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CTB' 
        AND SEQ1 = '21'
        AND SEQ5 = '1'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS SAIDABANCO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CTB' 
        AND SEQ1 = '21'
        AND SEQ5 = '2'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0,SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ENTRADACAIXA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CAIXA' 
        AND SEQ1 = '12'
        AND SEQ4 = '1'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS SAIDACAIXA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CAIXA' 
        AND SEQ1 = '12'
        AND SEQ4 = '2'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0,SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS ENTRADACUTE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CUTE' 
        AND SEQ1 = '21'
        AND SEQ4 = '1'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS SAIDACUTE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CUTE' 
        AND SEQ1 = '21'
        AND SEQ4 = '2'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ4, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS EMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EMP' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ4

        UNION ALL

        SELECT USUARIO, ANO, SEQ8, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ10, ',', '.') AS NUMERIC)) AS REFORCOEMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EMP' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, ANO, SEQ8

        UNION ALL

        SELECT USUARIO, ANO, SEQ5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ANULEMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ANL' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ5

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDACAO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'LQD' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS RETENCAO, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'LQD' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDACAO, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ALQ' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ANURETENCAO, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ALQ' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ10, ',', '.') AS NUMERIC)) AS PAGAMENTOEXT, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EXT' 
        AND SEQ1 = '30'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ANULPAGTOEXT, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AEX' 
        AND SEQ1 = '10'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS PAGAMENTO, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'OPS' 
        AND SEQ1 = '12'
        GROUP BY USUARIO, ANO, SEQ6

        UNION ALL

        SELECT USUARIO, ANO, SEQ6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ANULPAGAMENTO, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AOP' 
        AND SEQ1 = '12'
        GROUP BY USUARIO, ANO, SEQ6

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS OUTRASBAIXAS, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'OBELAC' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS ANULOUTRASBAIXAS, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AOB' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3

        UNION ALL

        SELECT USUARIO, ANO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS INSCRICAORESTOS
        FROM TCE_SICOM
        WHERE ARQUIVO = 'IDERP' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, ANO, SEQ3) X
        WHERE 1=1
        AND X.USUARIO = %s
        AND X.ANO = %s
        GROUP BY CAST(SEQ3 AS INT)
        ORDER BY CAST(SEQ3 AS INT)
    """

    cursor.execute(consulta, (usuario, ano,))
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
    consulta = """
        SELECT 
        X.DATAMOVIMENTO AS DATAMOVIMENTO , 
        X.DOCUMENTO AS DOCUMENTO , 
        X.DETALHE AS DETALHE, 
        X.TIPOMOVIMENTO AS TIPOMOVIMENTO ,
        UPPER(X.HISTORICO) AS HISTORICO, 
        X.FONTERECURSO AS FONTERECURSO , 
        X.VLRMOVIMENTO AS VLRMOVIMENTO  
        FROM (
        SELECT A.USUARIO AS USUARIO, A.ANO AS ANO, TO_DATE(SUBSTRING(A.SEQ12, 1, 2) || '-' || SUBSTRING(A.SEQ12, 3, 2) || '-' || SUBSTRING(A.SEQ12, 5, 4), 'DD-MM-YYYY') AS DATAMOVIMENTO, A.SEQ11 AS DOCUMENTO, '' AS DETALHE, 'EMPENHO' AS TIPOMOVIMENTO, A.SEQ16 AS HISTORICO, B.SEQ4 AS FONTERECURSO, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC)) AS VLRMOVIMENTO
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ11 = B.SEQ3 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ12, 1, 2) || '-' || SUBSTRING(A.SEQ12, 3, 2) || '-' || SUBSTRING(A.SEQ12, 5, 4), 'DD-MM-YYYY') ,A.SEQ11,A.SEQ16, B.SEQ4

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'),A.SEQ4, '', 'REFORCOEMPENHO', 'REFORÇO DE EMPENHO', A.SEQ8, SUM(CAST(REPLACE(A.SEQ10, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '20'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'),A.SEQ4 , A.SEQ8 

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ4, A.SEQ7, 'ANULACAOEMP', A.SEQ9, B.SEQ5, SUM(CAST(REPLACE(B.SEQ7, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ4 = B.SEQ3 AND A.SEQ7 = B.SEQ4 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ4, A.SEQ7, A.SEQ9, B.SEQ5

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPPCANCELA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '1'
        AND A.SEQ10 = '1'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPPENCAMP', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '1'
        AND A.SEQ10 = '2'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'),A.SEQ6, A.SEQ7, 'RSPPCATRIB', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '1'
        AND A.SEQ10 = '3'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPPRECLASSENTRADA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '1'
        AND A.SEQ10 = '5'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPPRECLASSAIDA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '1'
        AND A.SEQ10 = '6'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'),A.SEQ6, A.SEQ7, 'RSPNPCANCELA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '2'
        AND A.SEQ10 = '1'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPNPENCAMP', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '2'
        AND A.SEQ10 = '2'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPNPATRIB', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '2'
        AND A.SEQ10 = '3'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'),A.SEQ6, A.SEQ7, 'RSPNPCRECLASSENTRADA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '2'
        AND A.SEQ10 = '5'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'),A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, 'RSPNPCRECLASSAIDA', A.SEQ16, B.SEQ3, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '21' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'RSP' 
        AND A.SEQ1 = '20'
        AND A.SEQ9 = '2'
        AND A.SEQ10 = '6'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ11, 1, 2) || '-' || SUBSTRING(A.SEQ11, 3, 2) || '-' || SUBSTRING(A.SEQ11, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ7, A.SEQ16, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ9, 'LIQUIDARESTONP', 'LIQUIDAÇÃO DE RESTOS NÃO PROCESSADO', B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        AND A.SEQ5 = '2'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ9, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'),A.SEQ6, A.SEQ9, 'LIQUIDARESTONP', 'LIQUIDAÇÃO DE DESPESAS DO EXERCÍCIO', B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        AND A.SEQ5 = '1'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ9, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ9, 1, 2) || '-' || SUBSTRING(A.SEQ9, 3, 2) || '-' || SUBSTRING(A.SEQ9, 5, 4), 'DD-MM-YYYY'),A.SEQ5, A.SEQ10, 'ANULIQRSPNP', A.SEQ12, B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        AND A.SEQ11 = '2'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ9, 1, 2) || '-' || SUBSTRING(A.SEQ9, 3, 2) || '-' || SUBSTRING(A.SEQ9, 5, 4), 'DD-MM-YYYY'), A.SEQ5, A.SEQ10, A.SEQ12, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ9, 1, 2) || '-' || SUBSTRING(A.SEQ9, 3, 2) || '-' || SUBSTRING(A.SEQ9, 5, 4), 'DD-MM-YYYY'), A.SEQ5, A.SEQ10, 'ANULIQUIDACAO', A.SEQ12, B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        AND A.SEQ11 = '1'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ9, 1, 2) || '-' || SUBSTRING(A.SEQ9, 3, 2) || '-' || SUBSTRING(A.SEQ9, 5, 4), 'DD-MM-YYYY'),A.SEQ5, A.SEQ10, A.SEQ12, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'), A.SEQ5, '', 'PAGAMENTOEXT', A.SEQ11, B.SEQ6, SUM(CAST(REPLACE(B.SEQ9, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '31' AND A.SEQ4 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'EXT' 
        AND A.SEQ1 = '30'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'), A.SEQ5, A.SEQ11, B.SEQ6

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'), A.SEQ4, A.SEQ7, 'ANULPAGEXT', 'ANULAÇÃO DE PAGAMENTO DE EXTRAORÇAMENTÁRIAS', A.SEQ3, SUM(CAST(REPLACE(A.SEQ9, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AEX' 
        AND A.SEQ1 = '20'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ8, 1, 2) || '-' || SUBSTRING(A.SEQ8, 3, 2) || '-' || SUBSTRING(A.SEQ8, 5, 4), 'DD-MM-YYYY'), A.SEQ4, A.SEQ7, A.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ5, 1, 2) || '-' || SUBSTRING(A.SEQ5, 3, 2) || '-' || SUBSTRING(A.SEQ5, 5, 4), 'DD-MM-YYYY'), A.SEQ4, '', 'PAGAMENTOS', A.SEQ7, B.SEQ11, SUM(CAST(REPLACE(B.SEQ13, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ4 = B.SEQ4 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ5, 1, 2) || '-' || SUBSTRING(A.SEQ5, 3, 2) || '-' || SUBSTRING(A.SEQ5, 5, 4), 'DD-MM-YYYY'), A.SEQ4, A.SEQ7, B.SEQ11

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ4, 'PAGAMENTOS', A.SEQ8, B.SEQ14, SUM(CAST(REPLACE(B.SEQ16, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ4 = B.SEQ5 AND A.SEQ6 = B.SEQ4 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ7, 1, 2) || '-' || SUBSTRING(A.SEQ7, 3, 2) || '-' || SUBSTRING(A.SEQ7, 5, 4), 'DD-MM-YYYY'), A.SEQ6, A.SEQ4, A.SEQ8, B.SEQ14

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ5, '', 'OUTRASBAIXAS', A.SEQ12, B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'OBELAC' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ5, A.SEQ12, B.SEQ3

        UNION ALL

        SELECT A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ5, '', 'ANULOUTRASBAIXAS', 'ANULAÇÃO OUTRAS BAIXAS', B.SEQ3, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC))
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'AOB' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.ANO, TO_DATE(SUBSTRING(A.SEQ6, 1, 2) || '-' || SUBSTRING(A.SEQ6, 3, 2) || '-' || SUBSTRING(A.SEQ6, 5, 4), 'DD-MM-YYYY'), A.SEQ5, A.SEQ12, B.SEQ3) X
        WHERE 1=1
        AND X.USUARIO = %s
        AND X.ANO = %s
        ORDER BY X.DATAMOVIMENTO, X.TIPOMOVIMENTO
    """

    cursor.execute(consulta, (usuario, ano,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

# Conferencias


def confereSaldoFinalBancos(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano >= 2023:
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


def buscaDiferencaSaldoFinalBancos(usuario, ano):

    cursor = connection.conn.cursor()

    # Consulta SQL
    if ano >= 2023:
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
        SELECT X.SEQ4, X.SEQ5, X.SEQ6, X.SEQ7, X.SEQ8, X.SEQ9, X.SEQ10, X.SEQ11, X.SEQ13, SUM(X.EMPENHOS) AS AM, SUM(X.EMPENHADO) AS BALANCETE
        FROM (
        SELECT ANO, USUARIO, SEQ4, SEQ5, SEQ6, SEQ7, SEQ8, SEQ9, SEQ10, SEQ11, SEQ13, SUM(CAST(REPLACE(SEQ18, ',', '.') AS NUMERIC)) AS EMPENHADO, 0 AS EMPENHOS
        FROM TCE_SICOM 
        WHERE ARQUIVO = 'BALANCETE'
        AND SEQ1 = '30'
        AND SUBSTRING(SEQ2,1,7) LIKE '6221301'
        GROUP BY ANO, USUARIO, SEQ4, SEQ5, SEQ6, SEQ7, SEQ8, SEQ9, SEQ10, SEQ11, SEQ13

        UNION ALL

        SELECT A.ANO, A.USUARIO, A.SEQ2, A.SEQ3, A.SEQ4, A.SEQ5, A.SEQ6, A.SEQ7, A.SEQ8, A.SEQ9, B.SEQ4, 0, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHOS
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON (A.USUARIO = B.USUARIO AND A.ANO  = B.ANO AND A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ11 = B.SEQ3)
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '10'
        GROUP BY A.ANO, A.USUARIO, A.SEQ2, A.SEQ3, A.SEQ4, A.SEQ5, A.SEQ6, A.SEQ7, A.SEQ8, A.SEQ9, B.SEQ4) X
        WHERE 1=1
        AND X.USUARIO = %s
        AND X.ANO = %s
        GROUP BY X.SEQ4, X.SEQ5, X.SEQ6, X.SEQ7, X.SEQ8, X.SEQ9, X.SEQ10, X.SEQ11, X.SEQ13
        HAVING SUM(X.EMPENHADO) != SUM(X.EMPENHOS)
    """

    cursor.execute(consulta, (usuario, ano,))
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

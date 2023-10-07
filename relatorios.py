import connection

def relatorioAnaliticoEmpenho(usuario):

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

        SELECT  A.USUARIO AS USUARIO, A.SEQ3 AS EMPENHO, A.SEQ4 AS FONTERECURSO, A.SEQ5 AS CO, SUM(CAST(REPLACE(A.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHADO, 0 AS ANULEMPENHADO, 0 AS LIQUIDADO, 0 AS ANULIQUIDADO, 0 AS PAGO, 0 AS ANULPAGO
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ3, A.SEQ4, A.SEQ5

        UNION ALL 

        SELECT A.USUARIO, A.SEQ3, A.SEQ5, A.SEQ6, 0, SUM(CAST(REPLACE(A.SEQ7, ',', '.') AS NUMERIC)) AS ANULEMPENHADO, 0, 0, 0, 0 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ3, A.SEQ5, A.SEQ6

        UNION ALL 

        SELECT A.USUARIO, A.SEQ6, B.SEQ3, B.SEQ4, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDADO, 0, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        AND A.SEQ5 = '1'
        GROUP BY A.USUARIO, A.SEQ6, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.USUARIO, A.SEQ5, B.SEQ3, B.SEQ4, 0, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDADO, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, A.SEQ5, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.USUARIO, A.SEQ7, A.SEQ11, A.SEQ12, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS PAGO, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '11'
        AND A.SEQ6 IN ('1','2')
        GROUP BY A.USUARIO, A.SEQ7, A.SEQ11, A.SEQ12

        UNION ALL 

        SELECT A.USUARIO, A.SEQ10, A.SEQ14, A.SEQ15, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ16, ',', '.') AS NUMERIC)) AS ANULPAGO 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ10, A.SEQ14, A.SEQ15) X
        WHERE 1=1
        AND X.USUARIO = %s
        GROUP BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
        ORDER BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def totalizaMovimentosPorFonte(usuario):

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
        SELECT USUARIO, SEQ3, SUM(CAST(REPLACE(SEQ11, ',', '.') AS NUMERIC)) AS RECEITA, 0 AS ANURECEITA, 0 AS ENTRADABANCO, 0 AS SAIDABANCO, 0 AS ENTRADACAIXA, 0 AS SAIDACAIXA, 0 AS ENTRADACUTE, 0 AS SAIDACUTE, 0 AS EMPENHO, 0 AS REFORCOEMPENHO, 0 AS ANULEMPENHO, 0 AS LIQUIDACAO, 0 AS RETENCAO, 0 AS ANULIQUIDACAO, 0 AS ANURETENCAO, 0 AS PAGAMENTOEXT, 0 AS ANULPAGTOEXT, 0 AS PAGAMENTO, 0 AS ANULPAGAMENTO, 0 AS OUTRASBAIXAS, 0 AS ANULOUTRASBAIXAS, 0 AS INSCRICAORESTOS 
        FROM TCE_SICOM
        WHERE ARQUIVO = 'REC' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, SUM(CAST(REPLACE(SEQ11, ',', '.') AS NUMERIC)) AS ANURECEITA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ARC' 
        AND SEQ1 = '21'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ENTRADABANCO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CTB' 
        AND SEQ1 = '21'
        AND SEQ5 = '1'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS SAIDABANCO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CTB' 
        AND SEQ1 = '21'
        AND SEQ5 = '2'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0,SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ENTRADACAIXA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CAIXA' 
        AND SEQ1 = '12'
        AND SEQ4 = '1'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS SAIDACAIXA, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CAIXA' 
        AND SEQ1 = '12'
        AND SEQ4 = '2'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0,SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS ENTRADACUTE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CUTE' 
        AND SEQ1 = '21'
        AND SEQ4 = '1'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS SAIDACUTE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'CUTE' 
        AND SEQ1 = '21'
        AND SEQ4 = '2'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ4, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS EMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EMP' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ4

        UNION ALL

        SELECT USUARIO, SEQ8, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ10, ',', '.') AS NUMERIC)) AS REFORCOEMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EMP' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, SEQ8

        UNION ALL

        SELECT USUARIO, SEQ5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ANULEMPENHO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ANL' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ5

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDACAO, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'LQD' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS RETENCAO, 0, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'LQD' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDACAO, 0, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ALQ' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ7, ',', '.') AS NUMERIC)) AS ANURETENCAO, 0, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'ALQ' 
        AND SEQ1 = '20'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ10, ',', '.') AS NUMERIC)) AS PAGAMENTOEXT, 0, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'EXT' 
        AND SEQ1 = '30'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ANULPAGTOEXT, 0, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AEX' 
        AND SEQ1 = '10'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS PAGAMENTO, 0, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'OPS' 
        AND SEQ1 = '12'
        GROUP BY USUARIO, SEQ6

        UNION ALL

        SELECT USUARIO, SEQ6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ9, ',', '.') AS NUMERIC)) AS ANULPAGAMENTO, 0, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AOP' 
        AND SEQ1 = '12'
        GROUP BY USUARIO, SEQ6

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS OUTRASBAIXAS, 0, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'OBELAC' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ5, ',', '.') AS NUMERIC)) AS ANULOUTRASBAIXAS, 0
        FROM TCE_SICOM
        WHERE ARQUIVO = 'AOB' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3

        UNION ALL

        SELECT USUARIO, SEQ3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(SEQ6, ',', '.') AS NUMERIC)) AS INSCRICAORESTOS
        FROM TCE_SICOM
        WHERE ARQUIVO = 'IDERP' 
        AND SEQ1 = '11'
        GROUP BY USUARIO, SEQ3) X
        WHERE 1=1
        AND X.USUARIO = %s
        GROUP BY CAST(SEQ3 AS INT)
        ORDER BY CAST(SEQ3 AS INT)
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados

def movimentosEmpenhoPorFonte(usuario):

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

        SELECT A.USUARIO AS USUARIO, B.SEQ4, B.SEQ5, SUM(CAST(REPLACE(B.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHOS, 0 AS ANULAEMPENHO, 0 AS LIQUIDACAO, 0 AS ANULIQUIDACAO, 0 AS PAGAMENTO, 0 AS ANUPAGAMENTO
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ11 = B.SEQ3 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, B.SEQ4, B.SEQ5

        UNION ALL 

        SELECT A.USUARIO, A.SEQ5, A.SEQ6, 0, SUM(CAST(REPLACE(A.SEQ7, ',', '.') AS NUMERIC)) AS ANULAEMPENHO, 0, 0, 0, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ5, A.SEQ6

        UNION ALL

        SELECT A.USUARIO, B.SEQ3, B.SEQ4,  0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDACAO, 0, 0, 0
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, B.SEQ3, B.SEQ4

        UNION ALL

        SELECT A.USUARIO, B.SEQ3, B.SEQ4, 0, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDACAO, 0, 0
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.MODULO = B.MODULO AND A.ARQUIVO = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 AND A.USUARIO = B.USUARIO)
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        GROUP BY A.USUARIO, B.SEQ3, B.SEQ4

        UNION ALL

        SELECT A.USUARIO, A.SEQ11, A.SEQ12, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS PAGAMENTO, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ11, A.SEQ12

        UNION ALL

        SELECT A.USUARIO, A.SEQ14, A.SEQ15, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS ANUPAGAMENTO
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '11'
        GROUP BY A.USUARIO, A.SEQ14, A.SEQ15) X
        WHERE 1=1
        AND X.USUARIO = %s
        GROUP BY X.SEQ4, X.SEQ5
        ORDER BY X.SEQ4, X.SEQ5
    """

    cursor.execute(consulta, (usuario,))
    dados = cursor.fetchall()

    cursor.close()

    return dados
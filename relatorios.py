import connection

def RelatorioAnaliticoEmpenho():

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

        SELECT  A.SEQ3 AS EMPENHO, A.SEQ4 AS FONTERECURSO, A.SEQ5 AS CO, SUM(CAST(REPLACE(A.SEQ6, ',', '.') AS NUMERIC)) AS EMPENHADO, 0 AS ANULEMPENHADO, 0 AS LIQUIDADO, 0 AS ANULIQUIDADO, 0 AS PAGO, 0 AS ANULPAGO
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'EMP' 
        AND A.SEQ1 = '11'
        GROUP BY A.SEQ3, A.SEQ4, A.SEQ5

        UNION ALL 

        SELECT A.SEQ3, A.SEQ5, A.SEQ6, 0, SUM(CAST(REPLACE(A.SEQ7, ',', '.') AS NUMERIC)) AS ANULEMPENHADO, 0, 0, 0, 0 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'ANL' 
        AND A.SEQ1 = '11'
        GROUP BY A.SEQ3, A.SEQ5, A.SEQ6

        UNION ALL 

        SELECT A.SEQ6, B.SEQ3, B.SEQ4, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS LIQUIDADO, 0, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 )
        WHERE A.ARQUIVO = 'LQD' 
        AND A.SEQ1 = '10'
        AND A.SEQ5 = '1'
        GROUP BY A.SEQ6, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.SEQ5, B.SEQ3, B.SEQ4, 0, 0, 0, SUM(CAST(REPLACE(B.SEQ5, ',', '.') AS NUMERIC)) AS ANULIQUIDADO, 0, 0 
        FROM TCE_SICOM A
        JOIN TCE_SICOM B ON ( A.ARQUIVO  = B.ARQUIVO AND B.SEQ1 = '11' AND A.SEQ2 = B.SEQ2 )
        WHERE A.ARQUIVO = 'ALQ' 
        AND A.SEQ1 = '10'
        GROUP BY A.SEQ5, B.SEQ3, B.SEQ4

        UNION ALL 

        SELECT A.SEQ7, A.SEQ11, A.SEQ12, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ13, ',', '.') AS NUMERIC)) AS PAGO, 0
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'OPS' 
        AND A.SEQ1 = '11'
        AND A.SEQ6 IN ('1','2')
        GROUP BY A.SEQ7, A.SEQ11, A.SEQ12

        UNION ALL 

        SELECT A.SEQ10, A.SEQ14, A.SEQ15, 0, 0, 0, 0, 0, SUM(CAST(REPLACE(A.SEQ16, ',', '.') AS NUMERIC)) AS ANULPAGO 
        FROM TCE_SICOM A
        WHERE A.ARQUIVO = 'AOP' 
        AND A.SEQ1 = '11'
        GROUP BY A.SEQ10, A.SEQ14, A.SEQ15) X
        GROUP BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
        ORDER BY CAST(X.EMPENHO AS INT), X.FONTERECURSO, X.CO
    """

    cursor.execute(consulta)
    dados = cursor.fetchall()

    cursor.close()

    return dados
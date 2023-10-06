import psycopg2

conn = psycopg2.connect(
    dbname="uberabpm",
    user="uberabpm",
    password="SICSADM",
    host="34.86.191.201"
    # dbname="jsmcfbqq",
    # user="jsmcfbqq",
    # password="dzYLD0UV56ksursrQrP4fHMi_f1X116e",
    # host="silly.db.elephantsql.com"
)

def delete(usuario):
        cursor = conn.cursor()
        cursor.execute("DELETE from tce_sicom where usuario = %s ", (usuario,))
        conn.commit()
        cursor.close()

# def insere(usuario, arquivo, nome_arquivo, colunas):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO tce_sicom \
#             (USUARIO, MODULO, ARQUIVO, SEQ1, SEQ2, SEQ3, SEQ4, SEQ5, SEQ6, SEQ7, SEQ8, SEQ9, SEQ10, SEQ11, SEQ12, SEQ13, SEQ14, SEQ15, SEQ16, SEQ17, SEQ18, SEQ19, SEQ20, SEQ21, SEQ22, SEQ23, SEQ24, SEQ25, SEQ26, SEQ27, SEQ28, SEQ29, SEQ30) \
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
#             (usuario, arquivo, nome_arquivo, colunas[0], colunas[1], colunas[2], colunas[3], colunas[4], colunas[5], colunas[6], colunas[7], colunas[8], colunas[9], colunas[10], colunas[11], colunas[12], colunas[13], colunas[14], colunas[15], colunas[16], colunas[17], colunas[18], colunas[19], colunas[20], colunas[21], colunas[22], colunas[23], colunas[24], colunas[25], colunas[26], colunas[27], colunas[28], colunas[29]))
#     conn.commit()
#     cursor.close()
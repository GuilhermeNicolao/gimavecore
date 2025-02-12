import mysql.connector

# Configuração do banco de dados
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="guilherme",
    )

    if conn.is_connected():
        print("Conexão bem-sucedida!")

    # Fecha a conexão
    conn.close()

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")

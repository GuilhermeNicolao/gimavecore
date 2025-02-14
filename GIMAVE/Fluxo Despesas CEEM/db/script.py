import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PW"),
    "database": os.getenv("DB")
}

# Conectar ao MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Ler JSON
json_path = (r"C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Fluxo Despesas CEEM\db\Book1.json")
df = pd.read_json(json_path)

# Substituir valores NaN por None
df = df.where(pd.notnull(df), None)

# Criar query de inserção dinâmica (ajuste os nomes das colunas conforme necessário)
query = """
INSERT INTO pedidos_diarios (cod_pedido, cod_cliente, razao_social, produto, dt_pedido, dt_credito, tipo_pedido, 
fase_pedido, vlr_pedido, vlr_taxa, vlr_desconto, vlr_estorno, vlr_emissaocrt, vlr_outros, faturas, grupo) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Transformar DataFrame em Lista de Tuplas
data = [tuple(row) for row in df.to_numpy()]

# Inserir em lotes para evitar sobrecarga no MySQL
cursor.executemany(query, data)

# Commit e fechamento da conexão
conn.commit()
cursor.close()
conn.close()

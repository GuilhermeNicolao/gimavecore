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
json_path = (r"C:\Users\Guilherme.Silva\Desktop\gimavecore\GIMAVE\Fluxo Despesas CEEM\db\importarcadastro.json")
df = pd.read_json(json_path)

# Substituir valores NaN por None
df = df.where(pd.notnull(df), None)

# Criar query de inserção dinâmica (ajuste os nomes das colunas conforme necessário)
query = """
INSERT INTO cadastro (cod,cnpj,razao_social,produto,dt_inicio,dt_fim,status_ctt,taxa,vlr_taxa,tp_desconto,vlr_desconto,cond_pgto,
vlr_emissaocrt,vlr_novavia,cobranca,dt_fechamento,dt_apuracao,freq_apuracao,replica_limite,reposicao_automatica,tp_cartao,
dados_bancarios,calculo_venc,logradouro,numero,complemento,bairro,cidade,estado) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Transformar DataFrame em Lista de Tuplas
data = [tuple(row) for row in df.to_numpy()]

# Inserir em lotes para evitar sobrecarga no MySQL
cursor.executemany(query, data)

# Commit e fechamento da conexão
conn.commit()
cursor.close()
conn.close()

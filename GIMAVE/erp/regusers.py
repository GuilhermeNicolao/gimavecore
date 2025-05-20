import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

#---------UTILIZAR ESTE CÓDIGO APENAS PARA CADASTRO DE ADMINS-------------#

load_dotenv()

db_config = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PW"),
    "database": os.getenv("DB")
}

conexao = mysql.connector.connect(**db_config)
cursor = conexao.cursor()

nome = input("Nome: ")
username = input("Username: ")
senha = input("Senha: ")
nivel = input("Nível (USER ou ADMIN): ").upper()

senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

sql = "INSERT INTO usuarios_com (nome, username, senha_hash, nivel) VALUES (%s, %s, %s, %s)"
cursor.execute(sql, (nome, username, senha_hash, nivel))

conexao.commit()
cursor.close()
conexao.close()

print("Usuário cadastrado com sucesso!")

from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session
from functools import wraps
import os
import re
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SK")  # Necessária pro flash funcionar

#Configuração do DB
db_config = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PW"),
    "database": os.getenv("DB")
}


#Menu principal
@app.route('/system')
def menu_principal():
    return render_template('system.html')

# Homepage
@app.route('/home_com')
def homecomercial():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('home_com.html')

# Parâmetros
@app.route('/parametros')
def parametros():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    # Verifica se o usuário tem permissão de ADMIN
    if session.get('nivel') != 'ADMIN':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('homecomercial'))  # Redireciona para a home comercial

    return render_template('parametros_com.html')

# Registrar-se
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        senha = request.form['senha']
        nivel = request.form['nivel'].upper()

        # Conectar ao banco usando db_config
        conn = mysql.connector.connect(**db_config)  # Usando **db_config para passar os parâmetros de conexão
        cursor = conn.cursor()

        # Verificar se o usuário já existe
        cursor.execute("SELECT COUNT(*) FROM usuarios_com WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Se o usuário já existir, exibe mensagem e não tenta cadastrar
        if result[0] > 0:
            flash('Este usuário já existe!', 'danger')
            cursor.close()
            conn.close()
            return render_template('registrar_com.html')

        # Criptografa a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute(
                "INSERT INTO usuarios_com (nome, username, senha_hash, nivel) VALUES (%s, %s, %s, %s)",
                (nome, username, senha_hash, nivel)
            )
            conn.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
        except mysql.connector.Error as err:
            flash(f'Erro ao cadastrar: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('registrar'))

    return render_template('registrar_com.html')

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        try:
            conexao = mysql.connector.connect(**db_config)
            cursor = conexao.cursor()
            cursor.execute("SELECT senha_hash, nivel FROM usuarios_com WHERE username = %s", (username,))
            resultado = cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

        if resultado:
            senha_hash, nivel = resultado
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8') if isinstance(senha_hash, str) else senha_hash):
                session['username'] = username
                session['nivel'] = nivel
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('homecomercial'))

        flash('Credenciais inválidas', 'danger')

    return render_template('login_com.html')

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    # Limpar a sessão para deslogar o usuário
    session.clear()

    # Adicionar uma mensagem de sucesso ao flash
    flash('Sessão encerrada', 'success')

    # Redirecionar para a página de login
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
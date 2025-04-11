from flask import Flask, render_template, request, redirect, flash
import os
import sys
import subprocess
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import locale
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro_form():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        # Coletar dados do formulário
        data = request.form['data']
        produto = request.form['produto'].strip()
        fornecedor = request.form['fornecedor'].strip()
        valor = request.form['valor'].strip()
        observacao = request.form['observacao'].strip()

        # Validação simples
        if not data or not produto or not fornecedor or not valor:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/cadastro')

        # Formatando data para padrão MySQL
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()

        # Inserindo no banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO cadastro_orc_teste (dt, produto, fornecedor, vlr_orcamento, observacao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (data_formatada, produto, fornecedor, valor, observacao))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect('/cadastro')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/cadastro')

if __name__ == '__main__':
    app.run(debug=True)
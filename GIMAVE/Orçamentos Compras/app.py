from flask import Flask, render_template, request, redirect, flash, jsonify
import os
import re
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

#Rota de cadastro de orçamentos
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


#Rota de cadastro de fornecedores
@app.route('/fornecedores')
def fornecedores_form():
    return render_template('fornecedores.html')

@app.route('/cadastrar_fornecedor', methods=['POST'])
def cadastrar_fornecedor():
    try:
        # Coleta de dados do formulário
        cnpj = request.form['cnpj'].strip()
        razao_social = request.form['razao_social'].strip()
        rua = request.form['rua'].strip()
        numero = request.form['numero'].strip()
        cep = request.form['cep'].strip()

        # Validação simples
        if not cnpj or not razao_social or not rua or not numero or not cep:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/fornecedores')

        cnpj = re.sub(r'\D', '', request.form['cnpj'].strip())  # Remove tudo que não é dígito
        cep = re.sub(r'\D', '', request.form['cep'].strip())  # Remove tudo que não é número

        # Inserção no banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO fornecedores_orc (cnpj, razao_social, rua, numero, cep)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cnpj, razao_social, rua, numero, cep))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Fornecedor cadastrado com sucesso!', 'sucesso')
        return redirect('/fornecedores')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/fornecedores')

@app.route('/fornecedores_sugestoes')
def fornecedores_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT razao_social FROM fornecedores_orc WHERE razao_social LIKE %s LIMIT 10"
    cursor.execute(query, (f'%{termo}%',))
    resultados = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)
  

#Rota de cadastro de produtos
@app.route('/produtos')
def produtos_form():
    return render_template('produtos.html')

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    try:
        nome = request.form['nome'].strip()
        categoria = request.form['categoria'].strip()
        preco = request.form['preco'].strip()
        fornecedor = request.form['fornecedor'].strip()
        descricao = request.form['descricao'].strip()

        if not nome or not categoria or not preco or not fornecedor:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/produtos')

        # Converte valor para formato aceito pelo MySQL
        preco = preco.replace('.', '').replace(',', '.')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO produtos_orc (nome, categoria, preco, fornecedor, descricao)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, categoria, preco, fornecedor, descricao))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Produto cadastrado com sucesso!', 'sucesso')
        return redirect('/produtos')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/produtos')

@app.route('/fornecedores_autocomplete')
def fornecedores_autocomplete():
    termo = request.args.get('termo', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT razao_social FROM fornecedores_orc WHERE razao_social LIKE %s LIMIT 10"
    cursor.execute(query, (f"%{termo}%",))
    resultados = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
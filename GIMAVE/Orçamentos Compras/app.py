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

#Rotas de cadastro de orçamentos
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

        # Formatando data e valor para padrão MySQL
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
        vlr_formatado = float(valor.replace(',', '.'))

        # Abrindo conexão com o banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o produto existe
        cursor.execute("SELECT COUNT(*) FROM produtos_orc WHERE nome = %s", (produto,))
        produto_existe = cursor.fetchone()[0]
  
        if not produto_existe:
            flash("Produto não encontrado. Por favor, selecione um produto válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastro')  

        # Verifica se o fornecedor existe
        cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE razao_social = %s", (fornecedor,))
        fornecedor_existe = cursor.fetchone()[0] 

        if not fornecedor_existe:
            flash("Fornecedor não encontrado. Por favor, selecione uma válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastro')   

        query = "INSERT INTO cadastro_orc_teste (dt, produto, fornecedor, vlr_orcamento, observacao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (data_formatada, produto, fornecedor, vlr_formatado, observacao))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect('/cadastro')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/cadastro')


#Rotas de cadastro de fornecedores
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



#Rota para pesquisa de fornecedores 
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
  
# Rota para pesquisa de categorias
@app.route('/categorias_sugestoes')
def categorias_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT descricao FROM categoria_orc WHERE descricao LIKE %s LIMIT 10"
    cursor.execute(query, (f'%{termo}%',))
    resultados = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)

# Rota para pesquisa de produtos
@app.route('/produtos_sugestoes')
def produtos_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT nome FROM produtos_orc WHERE nome LIKE %s LIMIT 10"
    cursor.execute(query, (f'%{termo}%',))
    resultados = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)


#Rotas de cadastro de produtos
@app.route('/produtos')
def produtos_form():
    return render_template('produtos.html')

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    try:
        nome = request.form['nome'].strip()
        categoria = request.form['categoria'].strip()
        fornecedor = request.form['fornecedor'].strip()
        descricao = request.form['descricao'].strip()

        if not nome or not categoria or not fornecedor:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/produtos')
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se a categoria existe
        cursor.execute("SELECT COUNT(*) FROM categoria_orc WHERE descricao = %s", (categoria,))
        categoria_existe = cursor.fetchone()[0]
  
        if not categoria_existe:
            flash("Categoria não encontrada. Por favor, selecione uma válida.", "erro")
            cursor.close()
            conn.close()
            return redirect('/produtos')        


        # Verifica se o fornecedor existe
        cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE razao_social = %s", (fornecedor,))
        fornecedor_existe = cursor.fetchone()[0] 

        if not fornecedor_existe:
            flash("Fornecedor não encontrado. Por favor, selecione uma válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/produtos')   

        # Se existem...
        query = """
            INSERT INTO produtos_orc (nome, categoria, fornecedor, descricao)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nome, categoria, fornecedor, descricao))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Produto cadastrado com sucesso!', 'sucesso')
        return redirect('/produtos')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/produtos')


#Rotas para cadastro de categorias
@app.route('/categorias')
def categorias_form():
    return render_template('categoria.html')

@app.route('/cadastrar_categoria', methods=['POST'])
def cadastrar_categoria():
    try:
        descricao = request.form['descricao'].strip()

        if not descricao:
            flash('Preencha o campo de descrição!', 'erro')
            return redirect('/categorias')

        # Inserção no banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO categoria_orc (descricao) VALUES (%s)"
        cursor.execute(query, (descricao,))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Categoria cadastrada com sucesso!', 'sucesso')
        return redirect('/categorias')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/categorias')



if __name__ == '__main__':
    app.run(debug=True)
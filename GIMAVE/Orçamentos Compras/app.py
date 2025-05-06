from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
import os
import re
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

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



# Homepage | Orçamento Compras
@app.route('/home')
def home():
    return render_template('home_fin.html')

# Homepage | Viabilidade cartão Elo
@app.route('/home_com')
def homecomercial():
    return render_template('home_com.html')

# Parâmetros
@app.route('/parametros')
def parametros():
    return render_template('parametros_com.html')



#Rotas de cadastro de fornecedores
@app.route('/fornecedores')
def fornecedores_form():
    return render_template('fornecedores_fin.html')

@app.route('/api/fornecedores')
def listar_fornecedores():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT cnpj, razao_social FROM fornecedores_orc ORDER BY razao_social")
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(fornecedores)

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

@app.route('/api/fornecedores/<int:id>', methods=['PUT'])
def editar_fornecedores(id):
    novo_nome = request.json.get('nome', '').strip()

    if not novo_nome:
        return jsonify({'erro': 'Nome não pode estar vazio'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE fornecedores_orc SET razao_social = %s WHERE cnpj = %s", (novo_nome, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/api/fornecedores/<int:id>', methods=['DELETE'])
def excluir_fornecedores(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fornecedores_orc WHERE cnpj = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

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



#Rotas Produtos
@app.route('/produtos')
def produtos_form():
    return render_template('produtos_fin.html')

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

@app.route('/api/produtos')
def listar_produtos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_produto, nome FROM produtos_orc ORDER BY nome")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(produtos)

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def editar_produtos(id):
    novo_nome = request.json.get('nome', '').strip()

    if not novo_nome:
        return jsonify({'erro': 'Nome não pode estar vazio'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos_orc SET nome = %s WHERE id_produto = %s", (novo_nome, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def excluir_produtos(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos_orc WHERE id_produto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

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



#Rotas Categorias
@app.route('/categorias')
def categorias_form():
    return render_template('categoria_fin.html')

@app.route('/cadastrar_categoria', methods=['POST'])
def cadastrar_categoria():
    try:
        descricao = request.form['descricao'].strip()

        if not descricao:
            flash('Preencha o campo de descrição!', 'erro')
            return redirect('/categorias')

        # Conexão com o banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        # Verifica se a categoria já existe (ignorando maiúsculas/minúsculas)
        query_verifica = "SELECT COUNT(*) FROM categoria_orc WHERE LOWER(TRIM(descricao)) = LOWER(%s)"
        cursor.execute(query_verifica, (descricao,))
        (existe,) = cursor.fetchone()

        if existe > 0:
            flash('Categoria já cadastrada!', 'erro')
            cursor.close()
            conn.close()
            return redirect('/categorias')


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

@app.route('/api/categorias')
def listar_categorias():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_categoria, descricao FROM categoria_orc ORDER BY descricao")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categorias)

@app.route('/api/categorias/<int:id>', methods=['PUT'])
def editar_categoria(id):
    nova_descricao = request.json.get('descricao', '').strip()

    if not nova_descricao:
        return jsonify({'erro': 'Descrição não pode estar vazia'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE categoria_orc SET descricao = %s WHERE id_categoria = %s", (nova_descricao, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/api/categorias/<int:id>', methods=['DELETE'])
def excluir_categoria(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categoria_orc WHERE id_categoria = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})


#Rotas Orçamentos
@app.route('/cadastro')
def cadastro_form():
    return render_template('cadastro_fin.html')

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
        vlr_formatado = float(valor.replace('.', '').replace(',', '.')) 

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

@app.route('/validar', methods=['GET', 'POST'])
def validar():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    filtro = request.args.get('filtro')
    valor = request.args.get('valor')

    query_base = """
        SELECT cod, dt, produto, fornecedor, vlr_orcamento, observacao, status 
        FROM cadastro_orc_teste 
        WHERE 1=1
    """
    params = []

    filtros_sql = {
        "produto": " AND produto LIKE %s",
        "fornecedor": " AND fornecedor LIKE %s",
        "data": " AND DATE(dt) = %s",
        "status": " AND status LIKE %s"
    }

    if filtro in filtros_sql and valor:
        query_base += filtros_sql[filtro]
        
        if filtro in ['produto', 'fornecedor', 'status']:
            params.append(f"%{valor}%")
        
        elif filtro == 'data':
            try:
                # Converte de "DD/MM/YY" para "YYYY-MM-DD"
                data_formatada = datetime.strptime(valor, '%d/%m/%y').strftime('%Y-%m-%d')
                params.append(data_formatada)
            except ValueError:
                # Data inválida: força a query a não retornar nada
                query_base += " AND 1=0"

    query_base += " ORDER BY dt DESC"

    cursor.execute(query_base, params)
    orcamentos = cursor.fetchall()

    if request.method == 'POST':
        ids_selecionados = request.form.getlist('orcamento_ids')
        acao = request.form.get('acao')
        if ids_selecionados:
            status = 'Aprovado' if acao == 'aprovar' else 'Reprovado'
            format_strings = ','.join(['%s'] * len(ids_selecionados))
            update_query = f"UPDATE cadastro_orc_teste SET status = %s WHERE cod IN ({format_strings})"
            cursor.execute(update_query, [status] + ids_selecionados)
            conn.commit()

    cursor.close()
    conn.close()

    return render_template('validar.html', orcamentos=orcamentos, filtro=filtro, valor=valor)

@app.route('/autocomplete')
def autocomplete():
    termo = request.args.get('term', '')
    filtro = request.args.get('filtro', '')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    colunas_permitidas = {
        'produto': 'produto',
        'fornecedor': 'fornecedor'
    }

    if filtro in colunas_permitidas:
        coluna = colunas_permitidas[filtro]
        query = f"SELECT DISTINCT {coluna} FROM cadastro_orc_teste WHERE {coluna} LIKE %s LIMIT 10"
        cursor.execute(query, (f"%{termo}%",))
        resultados = [row[0] for row in cursor.fetchall()]
    else:
        resultados = []

    cursor.close()
    conn.close()

    return jsonify(resultados)

@app.route('/visualizar', methods=['GET'])
def visualizar():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    filtro = request.args.get('filtro')
    valor = request.args.get('valor')

    query_base = "SELECT cod, dt, produto, fornecedor, vlr_orcamento, observacao, status FROM cadastro_orc_teste WHERE 1=1"
    params = []

    filtros_sql = {
        "produto": " AND produto LIKE %s",
        "fornecedor": " AND fornecedor LIKE %s",
        "data": " AND DATE_FORMAT(dt, '%%d/%%m/%%y') = %s",
        "status": " AND status LIKE %s"
    }

    if filtro in filtros_sql and valor:
        query_base += filtros_sql[filtro]
        if filtro in ['produto', 'fornecedor', 'status']:
            params.append(f"%{valor}%")
        elif filtro == 'data':
            try:
                data_formatada = datetime.strptime(valor, '%d/%m/%y').strftime('%Y-%m-%d')
                params.append(data_formatada)
            except ValueError:
                params.append('0000-00-00')

    query_base += " ORDER BY dt DESC"

    cursor.execute(query_base, params)
    orcamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('visualizar.html', orcamentos=orcamentos, filtro=filtro, valor=valor)

@app.route('/editar_orcamento/<int:cod>', methods=['POST'])
def editar_orcamento(cod):
    produto = request.form['produto']
    fornecedor = request.form['fornecedor']
    vlr_orcamento = request.form['vlr_orcamento']
    observacao = request.form['observacao']
    dt = request.form['dt']

    # Validar os dados
    try:
        vlr_orcamento = float(vlr_orcamento)
        dt_formatada = datetime.strptime(dt, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        flash('Dados inválidos! Verifique o valor e a data.', 'danger')
        return redirect(url_for('visualizar'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cadastro_orc_teste 
        SET produto = %s, fornecedor = %s, vlr_orcamento = %s, observacao = %s, dt = %s 
        WHERE cod = %s
    """, (produto, fornecedor, vlr_orcamento, observacao, dt_formatada, cod))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash('Orçamento atualizado com sucesso!', 'success')
    return redirect(url_for('visualizar'))

@app.route('/remover_orcamento/<int:cod>', methods=['GET'])
def remover_orcamento(cod):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Excluir o orçamento com base no cod
    cursor.execute("DELETE FROM cadastro_orc_teste WHERE cod = %s", (cod,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Orçamento removido com sucesso!', 'success')
    return redirect(url_for('visualizar'))


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session, send_file
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import lightgrey
from collections import defaultdict
from reportlab.pdfgen import canvas
from mysql.connector import Error
from datetime import timedelta
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal
from functools import wraps
from io import BytesIO
import mysql.connector
import locale
import bcrypt
import uuid
import os
import re

# Load nas credenciais, parâmetros e no DB
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SK")
app.permanent_session_lifetime = timedelta(minutes=15) #Tempo máximo de inatividade
locale.setlocale(locale.LC_ALL, '')
try:
    db_config = {
        "host": os.getenv("HOST"),
        "user": os.getenv("USER"),
        "password": os.getenv("PW"),
        "database": os.getenv("DB")
    }

except Error as e:
    print("Erro de conexão com o banco:")
    print(3)
    raise

def modulo_requerido(*modulos_necessarios):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            modulos_usuario = session.get('modulos', [])
            if not any(mod in modulos_usuario for mod in modulos_necessarios):
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('menu_principal'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_parametros_calculos():
    # Exemplo simples para pegar parâmetro consumo_credenciado do banco
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT consumo_credenciado, confeccao_cartoes, custos_operacionais, custos_operacionais_qtde, " \
    "custo_tag, custo_tag_qtde, custo_eus, custo_eus_qtde, despesatag_envio, despesatag_tagfisica, despesatag_greenpass," \
    "despesaeus_epharma, despesaeus_telemedicina, despesaeus_enviounico, investimento_cartao, negociacao_aprovada," \
    "negociacao_pendente, rentabilidade_ideal FROM parametros_com LIMIT 1;")

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    # Monta um dicionário com os nomes e valores
    if row:
        parametros = {
            "consumo_credenciado": row['consumo_credenciado'],
            "confeccao_cartoes": row['confeccao_cartoes'],
            "custos_operacionais": row['custos_operacionais'],
            "custos_operacionais_qtde": row['custos_operacionais_qtde'],
            "custo_tag": row['custo_tag'],
            "custo_tag_qtde": row['custo_tag_qtde'],
            "custo_eus": row['custo_eus'],
            "custo_eus_qtde": row['custo_eus_qtde'],
            "despesatag_envio": row['despesatag_envio'],
            "despesatag_tagfisica": row['despesatag_tagfisica'],
            "despesatag_greenpass": row['despesatag_greenpass'],
            "despesaeus_epharma": row['despesaeus_epharma'],
            "despesaeus_telemedicina": row['despesaeus_telemedicina'],
            "despesaeus_enviounico": row['despesaeus_enviounico'],
            "investimento_cartao": row['investimento_cartao'],
            "negociacao_aprovada": row['negociacao_aprovada'],
            "negociacao_pendente": row['negociacao_pendente'],
            "rentabilidade_ideal": row['rentabilidade_ideal']
        }
    else:
        parametros = {}

    return parametros





#---------------LOGIN E TELAS INICIAIS----------------#
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        try:
            conexao = mysql.connector.connect(**db_config)
            cursor = conexao.cursor()
            
            # Verifica se o usuário existe
            cursor.execute("SELECT user_id, senha_hash, nivel FROM usuarios WHERE username = %s", (username,))
            resultado = cursor.fetchone()

            if resultado:
                user_id, senha_hash, nivel = resultado

                if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8') if isinstance(senha_hash, str) else senha_hash):
                    session.permanent = True
                    session['user_id'] = user_id
                    session['username'] = username
                    session['nivel'] = nivel

                    if nivel == 'USER':
                        cursor.execute("SELECT modulo FROM modulos WHERE user_id = %s", (user_id,))
                        modulos = [row[0] for row in cursor.fetchall()]
                    else:
                        modulos = ['COMPRAS', 'COMERCIALGESTOR' , 'COMERCIAL']

                    session['modulos'] = modulos
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('menu_principal'))

        except mysql.connector.Error as err:
            flash(f"Erro ao conectar ao banco: {err}", 'danger')

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexao' in locals():
                conexao.close()

        flash('Credenciais inválidas', 'danger')

    return render_template('login.html')

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    # Limpar a sessão para deslogar o usuário
    session.clear()

    # Adicionar uma mensagem de sucesso ao flash
    flash('Sessão encerrada', 'success')

    # Redirecionar para a página de login
    return redirect(url_for('login'))



# Registrar novos usuários
@app.route('/usuarios', methods=['GET', 'POST'])
def reg_usuarios():
    if session.get('nivel') != 'ADMIN':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('menu_principal'))  # Redireciona para a home comercial
    
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        senha = request.form['senha']
        nivel = request.form['nivel']

        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            conexao = mysql.connector.connect(**db_config)
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, username, senha_hash, nivel) VALUES (%s, %s, %s, %s)",
                           (nome, username, senha_hash, nivel))
            conexao.commit()
            flash('Usuário cadastrado com sucesso.', 'success')
        except mysql.connector.IntegrityError:
            flash('Usuário já existe.', 'danger')
        finally:
            cursor.close()
            conexao.close()

    # Listar todos os usuários
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()
    cursor.execute("SELECT user_id, nome, username, nivel FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('reg_users.html', usuarios=usuarios)

# Excluir usuários
@app.route('/usuarios/excluir/<int:user_id>', methods=['POST'])
def excluir_usuario(user_id):
    if session.get('nivel') != 'ADMIN':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('menu_principal'))  # Redireciona para a home comercial
    
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE user_id = %s", (user_id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    flash('Usuário excluído com sucesso.', 'success')
    return redirect(url_for('reg_usuarios'))

# Lista de usuários
@app.route('/modulos')
def listar_usuarios_acessos():
    if session.get('nivel') != 'ADMIN':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('menu_principal'))  # Redireciona para a home comercial
    
    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT user_id, nome, username, nivel FROM usuarios")
        usuarios = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return render_template('usuarios_modulos.html', usuarios=usuarios)

# Gerenciar acesso aos módulos
@app.route('/modulos/<int:user_id>', methods=['GET', 'POST'])
def gerenciar_modulos(user_id):
    if session.get('nivel') != 'ADMIN':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('menu_principal'))  

    modulos_disponiveis = ['COMPRAS', 'COMERCIALGESTOR' , 'COMERCIAL']

    try:
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        if request.method == 'POST':
            modulos_selecionados = request.form.getlist('modulos')

            # Apaga os acessos antigos
            cursor.execute("DELETE FROM modulos WHERE user_id = %s", (user_id,))

            # Insere os novos acessos
            for modulo in modulos_selecionados:
                cursor.execute("INSERT INTO modulos (user_id, modulo) VALUES (%s, %s)", (user_id, modulo))

            conexao.commit()
            flash('Acessos atualizados com sucesso.', 'success')
            return redirect(url_for('listar_usuarios_acessos'))

        # Para GET: busca os acessos atuais do usuário
        cursor.execute("SELECT modulo FROM modulos WHERE user_id = %s", (user_id,))
        modulos_atuais = [row[0] for row in cursor.fetchall()]

    finally:
        cursor.close()
        conexao.close()

    return render_template('modulos.html', user_id=user_id, modulos_disponiveis=modulos_disponiveis, modulos_atuais=modulos_atuais)



# Tela inicial ERP
@app.route('/system')
def menu_principal():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('homepage.html')
#-------------------------------------------------------#





# ----------ROTAS ORÇAMENTO COMPRAS---------------------#
#Rotas de cadastro de fornecedores
@app.route('/fornecedoresCMP')
@modulo_requerido('COMPRAS')
def fornecedoresCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('fornecedoresCMP.html')

@app.route('/api/fornecedoresCMP')
@modulo_requerido('COMPRAS')
def listar_fornecedoresCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT cnpj, razao_social FROM fornecedores_cmp ORDER BY razao_social")
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(fornecedores)

@app.route('/cadastrar_fornecedorCMP', methods=['POST'])
@modulo_requerido('COMPRAS')
def cadastrar_fornecedorCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Coleta de dados do formulário
        cnpj = re.sub(r'\D', '', request.form['cnpj'].strip())
        razao_social = request.form['razao_social'].strip()
        rua = request.form['rua'].strip()
        numero = request.form['numero'].strip()
        cep = re.sub(r'\D', '', request.form['cep'].strip())

        # Validação simples
        if not cnpj or not razao_social or not rua or not numero or not cep:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/fornecedoresCMP')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verifica duplicidade de CNPJ
        cursor.execute("SELECT COUNT(*) AS total FROM fornecedores_cmp WHERE cnpj = %s", (cnpj,))
        if int(cursor.fetchone()['total']) > 0:
            flash("Já existe um fornecedor com esse CNPJ.", "erro")
            return redirect('/fornecedoresCMP')

        # Verifica duplicidade de razão social
        cursor.execute("SELECT COUNT(*) AS total FROM fornecedores_cmp WHERE LOWER(TRIM(razao_social)) = LOWER(%s)", (razao_social,))
        if cursor.fetchone()['total'] > 0:
            flash("Já existe um fornecedor com essa razão social.", "erro")
            return redirect('/fornecedoresCMP')

        # Inserção
        query = """
            INSERT INTO fornecedores_cmp (cnpj, razao_social, rua, numero, cep)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (cnpj, razao_social, rua, numero, cep))
        conn.commit()

        flash('Fornecedor cadastrado com sucesso!', 'sucesso')
        return redirect('/fornecedoresCMP')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/fornecedoresCMP')
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/fornecedoresCMP/<int:id>', methods=['PUT'])
@modulo_requerido('COMPRAS')
def editar_fornecedoresCMP(id):
    novo_nome = request.json.get('nome', '').strip()

    if not novo_nome:
        return jsonify({'erro': 'Nome não pode estar vazio'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verifica se razão social já está sendo usada por outro fornecedor
        cursor.execute("""
            SELECT COUNT(*) AS total FROM fornecedores_cmp 
            WHERE LOWER(TRIM(razao_social)) = LOWER(%s) AND cnpj != %s
        """, (novo_nome, id))
        if cursor.fetchone()['total'] > 0:
            return jsonify({'erro': 'Já existe outro fornecedor com essa razão social.'}), 400

        # Atualiza a razão social
        cursor.execute("UPDATE fornecedores_cmp SET razao_social = %s WHERE cnpj = %s", (novo_nome, id))
        conn.commit()

        return jsonify({'sucesso': True})

    except mysql.connector.Error as err:
        return jsonify({'erro': str(err)}), 500

@app.route('/api/fornecedoresCMP/<int:id>', methods=['DELETE'])
@modulo_requerido('COMPRAS')
def excluir_fornecedoresCMP(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fornecedores_cmp WHERE cnpj = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/fornecedoresCMP_sugestoes')
@modulo_requerido('COMPRAS')
def fornecedoresCMP_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, razao_social FROM fornecedores_cmp WHERE razao_social LIKE %s LIMIT 10", (f'%{termo}%',))
    resultados = [{'cnpj': row[0], 'razao_social': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)


#Rotas Produtos
@app.route('/produtosCMP')
@modulo_requerido('COMPRAS')
def produtosCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('produtosCMP.html')

@app.route('/cadastrar_produtoCMP', methods=['POST'])
@modulo_requerido('COMPRAS')
def cadastrar_produtoCMP():
    try:
        nome = request.form['nome'].strip()
        categoria_id = request.form['categoria_id'].strip()
        descricao = request.form['descricao'].strip()

        if not nome or not categoria_id:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/produtosCMP')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Verifica se a categoria existe
        cursor.execute("SELECT COUNT(*) AS total FROM categorias_cmp WHERE id_categoria = %s", (categoria_id,))
        if int(cursor.fetchone()['total']) == 0:
            flash("Categoria não encontrada. Por favor, selecione uma válida.", "erro")
            return redirect('/produtosCMP')

        # Verifica se já existe produto com o mesmo nome, categoria e fornecedor
        query_verifica = """
            SELECT COUNT(*) AS total FROM produtos_cmp 
            WHERE LOWER(TRIM(nome)) = LOWER(%s)
            AND categoria_id = %s
        """
        cursor.execute(query_verifica, (nome, categoria_id))

        if int(cursor.fetchone()['total']) > 0:
            flash("Produto já cadastrado com esses dados!", "erro")
            return redirect('/produtosCMP')

        # Inserção
        query = """
            INSERT INTO produtos_cmp (nome, categoria_id, descricao)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (nome, categoria_id, descricao))
        conn.commit()

        flash('Produto cadastrado com sucesso!', 'sucesso')
        return redirect('/produtosCMP')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/produtosCMP')
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/produtosCMP')
@modulo_requerido('COMPRAS')
def listar_produtosCMP():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_produto, nome FROM produtos_cmp ORDER BY nome")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(produtos)

@app.route('/api/produtosCMP/<int:id>', methods=['PUT'])
@modulo_requerido('COMPRAS')
def editar_produtosCMP(id):
    novo_nome = request.json.get('nome', '').strip()

    if not novo_nome:
        return jsonify({'erro': 'Nome não pode estar vazio'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Obtém os dados atuais do produto
        cursor.execute("SELECT categoria_id FROM produtos_cmp WHERE id_produto = %s", (id,))
        produto = cursor.fetchone()

        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        categoria_id = produto['categoria_id']

        # Verifica se já existe outro produto com o mesmo nome/categoria/fornecedor
        query_verifica = """
            SELECT COUNT(*) FROM produtos_cmp
            WHERE LOWER(TRIM(nome)) = LOWER(%s)
            AND categoria_id = %s
            AND id_produto != %s
        """
        cursor.execute(query_verifica, (novo_nome, categoria_id, id))
        (existe,) = cursor.fetchone().values()

        if existe > 0:
            return jsonify({'erro': 'Já existe outro produto com esse nome, categoria e fornecedor.'}), 400

        cursor.execute("UPDATE produtos_cmp SET nome = %s WHERE id_produto = %s", (novo_nome, id))
        conn.commit()

        return jsonify({'sucesso': True})

    except mysql.connector.Error as err:
        return jsonify({'erro': str(err)}), 500

@app.route('/api/produtosCMP/<int:id>', methods=['DELETE'])
@modulo_requerido('COMPRAS')
def excluir_produtosCMP(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos_cmp WHERE id_produto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/produtosCMP_sugestoes')
@modulo_requerido('COMPRAS')
def produtosCMP_sugestoes():
    termo = request.args.get('q', '').strip()
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_produto, nome FROM produtos_cmp
        WHERE nome LIKE %s
        ORDER BY nome
        LIMIT 10
    """, (f"%{termo}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)


#Rotas Categorias
@app.route('/categoriasCMP')
@modulo_requerido('COMPRAS')
def categoriasCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('categoriasCMP.html')

@app.route('/cadastrar_categoriaCMP', methods=['POST'])
@modulo_requerido('COMPRAS')
def cadastrar_categoriaCMP():
    try:
        descricao = request.form['descricao'].strip()

        if not descricao:
            flash('Preencha o campo de descrição!', 'erro')
            return redirect('/categoriasCMP')

        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        # Verifica se a categoria já existe (ignorando maiúsculas/minúsculas)
        query_verifica = "SELECT COUNT(*) FROM categorias_cmp WHERE LOWER(TRIM(descricao)) = LOWER(%s)"
        cursor.execute(query_verifica, (descricao,))
        (existe,) = cursor.fetchone()

        if existe > 0:
            flash('Categoria já cadastrada!', 'erro')
            cursor.close()
            conn.close()
            return redirect('/categoriasCMP')


        query = "INSERT INTO categorias_cmp (descricao) VALUES (%s)"
        cursor.execute(query, (descricao,))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Categoria cadastrada com sucesso!', 'sucesso')
        return redirect('/categoriasCMP')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/categoriasCMP')

@app.route('/api/categoriasCMP')
@modulo_requerido('COMPRAS')
def listar_categoriasCMP():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_categoria, descricao FROM categorias_cmp ORDER BY descricao")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categorias)

@app.route('/api/categoriasCMP/<int:id>', methods=['PUT'])
@modulo_requerido('COMPRAS')
def editar_categoriaCMP(id):
    nova_descricao = request.json.get('descricao', '').strip()

    if not nova_descricao:
        return jsonify({'erro': 'Descrição não pode estar vazia'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE categorias_cmp SET descricao = %s WHERE id_categoria = %s", (nova_descricao, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/api/categoriasCMP/<int:id>', methods=['DELETE'])
@modulo_requerido('COMPRAS')
def excluir_categoriaCMP(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias_cmp WHERE id_categoria = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/categoriasCMP_sugestoes')
@modulo_requerido('COMPRAS')
def categoriasCMP_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, descricao FROM categorias_cmp WHERE descricao LIKE %s LIMIT 10", (f'%{termo}%',))
    resultados = [{'id_categoria': row[0], 'descricao': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)


#Rotas Orçamentos
@app.route('/cadastroCMP')
@modulo_requerido('COMPRAS')
def cadastroCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('cadastroCMP.html')

@app.route('/cadastrarCMP', methods=['POST'])
@modulo_requerido('COMPRAS')
def cadastrarCMP():
    try:
        # Coletar dados do formulário
        data = request.form['data']
        produto_id = request.form['produto_id']
        fornecedor_cnpj = request.form['fornecedor_cnpj']
        valor = request.form['valor'].strip()
        observacao = request.form['observacao'].strip()
        user_id = session.get('user_id')

        # Validação simples
        if not data or not produto_id or not fornecedor_cnpj or not valor:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/cadastroCMP')

        # Formatando data e valor para padrão MySQL
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
        vlr_formatado = float(valor.replace('R$', '').replace('.', '').replace(',', '.').strip())


        # Abrindo conexão com o banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o produto existe
        cursor.execute("SELECT COUNT(*) FROM produtos_cmp WHERE id_produto = %s", (produto_id,))
        produto_existe = cursor.fetchone()[0]
  
        if not produto_existe:
            flash("Produto não encontrado. Por favor, selecione um produto válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastroCMP')  

        # Verifica se o fornecedor existe
        cursor.execute("SELECT COUNT(*) FROM fornecedores_cmp WHERE cnpj = %s", (fornecedor_cnpj,))
        fornecedor_existe = cursor.fetchone()[0] 

        if not fornecedor_existe:
            flash("Fornecedor não encontrado. Por favor, selecione uma válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastroCMP')   

        # Inserção
        query = """
            INSERT INTO cadorc_cmp 
            (dt, vlr_orcamento, observacao, status, produto_id, fornecedor_cnpj, user_id)
            VALUES (%s, %s, %s, 'Pendente', %s, %s, %s)
        """
        cursor.execute(query, (data_formatada, vlr_formatado, observacao, produto_id, fornecedor_cnpj, user_id))
        conn.commit()

        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect('/cadastroCMP')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/cadastroCMP')

@app.route('/validarCMP', methods=['GET', 'POST'])
@modulo_requerido('COMPRAS')
def validarCMP():
    if request.method == 'POST':
        id_orcamento = request.form.get('id_orcamento')
        produto_id = request.form.get('produto_id')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        acao = request.form.get('acao')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        if acao == 'validar':
            # Aprova o orçamento selecionado
            cursor.execute("UPDATE cadorc_cmp SET status = 'Aprovado' WHERE id_orcamento = %s", (id_orcamento,))

            # Reprova os demais do mesmo produto
            cursor.execute("""
                UPDATE cadorc_cmp
                SET status = 'Reprovado'
                WHERE produto_id = %s AND id_orcamento != %s
            """, (produto_id, id_orcamento))

            flash('Orçamento aprovado com sucesso', 'success')


        elif acao == 'excluir':
            cursor.execute("DELETE FROM cadorc_cmp WHERE id_orcamento = %s", (id_orcamento,))
            flash('Orçamento excluído com sucesso', 'success')

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('validarCMP', data_inicio=data_inicio, data_fim=data_fim))

    # GET – parte do filtro por data
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    orcamentos = []
    if data_inicio and data_fim:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT c.id_orcamento, c.produto_id, c.vlr_orcamento, c.status, c.dt, c.observacao,
                   p.nome AS nome_produto, f.razao_social AS nome_fornecedor
            FROM cadorc_cmp c
            JOIN produtos_cmp p ON c.produto_id = p.id_produto
            JOIN fornecedores_cmp f ON c.fornecedor_cnpj = f.cnpj
            WHERE c.dt BETWEEN %s AND %s
            ORDER BY c.produto_id, c.dt
        """
        cur.execute(query, (data_inicio, data_fim))
        orcamentos = cur.fetchall()

        for o in orcamentos:
            if isinstance(o['dt'], str):
                o['dt'] = datetime.strptime(o['dt'], '%Y-%m-%d').date()
        cur.close()
        conn.close()

    return render_template('validarCMP.html', orcamentos=orcamentos, datetime=datetime)

@app.route('/autocomplete')
@modulo_requerido('COMPRAS')
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
        query = f"SELECT DISTINCT {coluna} FROM cadorc_cmp WHERE {coluna} LIKE %s LIMIT 10"
        cursor.execute(query, (f"%{termo}%",))
        resultados = [row[0] for row in cursor.fetchall()]
    else:
        resultados = []

    cursor.close()
    conn.close()

    return jsonify(resultados)

@app.route('/visualizarCMP', methods=['GET'])
@modulo_requerido('COMPRAS')
def visualizarCMP():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    filtro = request.args.get('filtro')
    valor = request.args.get('valor')

    query_base = """
        SELECT o.id_orcamento, o.dt, o.vlr_orcamento, o.observacao, o.status,
               p.nome AS produto, f.razao_social AS fornecedor
        FROM cadorc_cmp o
        JOIN produtos_cmp p ON o.produto_id = p.id_produto
        JOIN fornecedores_cmp f ON o.fornecedor_cnpj = f.cnpj
        WHERE 1=1
    """
    params = []

    filtros_sql = {
        "produto": " AND p.nome LIKE %s",
        "fornecedor": " AND f.razao_social LIKE %s",
        "data": " AND o.dt = %s",
        "status": " AND o.status LIKE %s"
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
                params.append('0000-00-00')  # Valor inválido, não retorna nada

    query_base += " ORDER BY o.dt DESC"

    cursor.execute(query_base, params)
    orcamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('visualizarCMP.html', orcamentos=orcamentos, filtro=filtro, valor=valor)

@app.route('/editar_orcamentoCMP/<int:cod>', methods=['POST'])
@modulo_requerido('COMPRAS')
def editar_orcamentoCMP(cod):
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
        UPDATE cadorc_cmp 
        SET produto = %s, fornecedor = %s, vlr_orcamento = %s, observacao = %s, dt = %s 
        WHERE cod = %s
    """, (produto, fornecedor, vlr_orcamento, observacao, dt_formatada, cod))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash('Orçamento atualizado com sucesso!', 'success')
    return redirect(url_for('visualizar'))

@app.route('/remover_orcamentoCMP/<int:cod>', methods=['GET'])
@modulo_requerido('COMPRAS')
def remover_orcamentoCMP(cod):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Excluir o orçamento com base no cod
    cursor.execute("DELETE FROM cadorc_cmp WHERE cod = %s", (cod,))
    conn.commit()

    cursor.close()
    conn.close()

    flash('Orçamento removido com sucesso!', 'success')
    return redirect(url_for('visualizar'))

@app.route('/dashboardCMP')
@modulo_requerido('COMPRAS')
def dashboardCMP():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    produto_id = request.args.get('produto_id')

    relatorio = []
    produtos = []

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)

    # Buscar produtos para o select
    cur.execute("SELECT id_produto, nome FROM produtos_cmp ORDER BY nome")
    produtos = cur.fetchall()

    total_economia = Decimal('0.00')  # Inicializa totalizador

    if data_inicio and data_fim:
        if produto_id:
            query = """
                SELECT 
                    c.produto_id, p.nome AS nome_produto, c.dt,
                    c.vlr_orcamento, c.status, f.razao_social AS fornecedor
                FROM cadorc_cmp c
                JOIN produtos_cmp p ON c.produto_id = p.id_produto
                JOIN fornecedores_cmp f ON c.fornecedor_cnpj = f.cnpj
                WHERE c.dt BETWEEN %s AND %s
                  AND c.produto_id = %s
                ORDER BY c.produto_id, c.dt
            """
            cur.execute(query, (data_inicio, data_fim, produto_id))
        else:
            query = """
                SELECT 
                    c.produto_id, p.nome AS nome_produto, c.dt,
                    c.vlr_orcamento, c.status, f.razao_social AS fornecedor
                FROM cadorc_cmp c
                JOIN produtos_cmp p ON c.produto_id = p.id_produto
                JOIN fornecedores_cmp f ON c.fornecedor_cnpj = f.cnpj
                WHERE c.dt BETWEEN %s AND %s
                ORDER BY c.produto_id, c.dt
            """
            cur.execute(query, (data_inicio, data_fim))

        orcamentos = cur.fetchall()

        # Agrupar por produto e data para calcular os dados
        agrupado = defaultdict(lambda: {
            'nome_produto': '',
            'dt': None,
            'aprovado': None,
            'fornecedor_aprovado': None,
            'maior_reprovado': Decimal('0.00'),
            'fornecedor_reprovado': None
        })

        for o in orcamentos:
            chave = (o['produto_id'], o['dt'])
            valor = Decimal(str(o['vlr_orcamento']))
            agr = agrupado[chave]

            agr['nome_produto'] = o['nome_produto']
            agr['dt'] = o['dt']

            if o['status'] == 'Aprovado':
                agr['aprovado'] = valor
                agr['fornecedor_aprovado'] = o['fornecedor']
            elif o['status'] == 'Reprovado':
                if valor > agr['maior_reprovado']:
                    agr['maior_reprovado'] = valor
                    agr['fornecedor_reprovado'] = o['fornecedor']

        # Montar a lista para o template, incluindo a economia e somando o total
        for dados in agrupado.values():
            if dados['aprovado'] is not None:
                economia = dados['maior_reprovado'] - dados['aprovado']
                if economia > 0:
                    total_economia += economia
                relatorio.append({
                    'data': dados['dt'],
                    'nome_produto': dados['nome_produto'],
                    'fornecedor_aprovado': dados['fornecedor_aprovado'],
                    'valor_aprovado': float(dados['aprovado']),
                    'fornecedor_reprovado': dados['fornecedor_reprovado'],
                    'maior_reprovado': float(dados['maior_reprovado']),
                    'economia': float(economia) if economia > 0 else 0,
                })

    cur.close()
    conn.close()

    return render_template('dashboardCMP.html', 
                           relatorio=relatorio, 
                           produtos=produtos, 
                           total_economia=float(total_economia))
#-----------------------------------------------------------------#





#----------ROTAS VIABILIDADE COMERCIAL ELO------------------------#
@app.route('/simulacaoCOM')
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def simulacaoCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('simulacaoCOM.html')

@app.route('/parametrosCOM')
@modulo_requerido('COMERCIALGESTOR')
def parametrosCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    return render_template('parametrosCOM.html')

@app.route('/get_parametros')
@modulo_requerido('COMERCIALGESTOR')
def get_parametros():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT * FROM parametros_com LIMIT 1")
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(resultado)

@app.route('/salvar_parametros', methods=['POST'])
@modulo_requerido('COMERCIALGESTOR')
def salvar_parametros():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    dados = request.json

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Aqui você pode decidir se quer sobrescrever (DELETE e INSERT) ou usar UPDATE com WHERE
    cursor.execute("DELETE FROM parametros_com")  # Mantém só 1 registro
    query = """
        INSERT INTO parametros_com (
            consumo_credenciado, confeccao_cartoes, custos_operacionais, custos_operacionais_qtde,
            custo_tag, custo_tag_qtde, custo_eus, custo_eus_qtde,
            despesatag_envio, despesatag_tagfisica, despesatag_greenpass,
            despesaeus_epharma, despesaeus_telemedicina, despesaeus_enviounico,
            investimento_cartao, negociacao_aprovada, negociacao_pendente, rentabilidade_ideal
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        dados['consumo_credenciado'],
        dados['confeccao_cartoes'],
        dados['custos_operacionais'],
        dados['custos_operacionais_qtde'],
        dados['custo_tag'],
        dados['custo_tag_qtde'],
        dados['custo_eus'],
        dados['custo_eus_qtde'],
        dados['despesatag_envio'],
        dados['despesatag_tagfisica'],
        dados['despesatag_greenpass'],
        dados['despesaeus_epharma'],
        dados['despesaeus_telemedicina'],
        dados['despesaeus_enviounico'],
        dados['investimento_cartao'],
        dados['negociacao_aprovada'],
        dados['negociacao_pendente'],
        dados['rentabilidade_ideal'],
    )
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()

    return jsonify({"status": "ok"})

@app.route('/calcular_simulacao', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def calcular_simulacao():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    dados_form = request.json  # dicionário com os dados do formulário
    parametros = get_parametros_calculos()  # dicionário com os parâmetros do banco

    # Formulário simulacaoCOM.html
    qtde_cartoes = float(dados_form.get('qtde_cartoes') or 0)
    valor_credito = float(dados_form.get('valor_credito') or 0)
    qtde_meses = int(dados_form.get('meses') or 0)
    taxa_adm = float(dados_form.get('taxa_adm') or 0)
    venda_cartoes = float(dados_form.get('venda_cartoes') or 0)
    qtde_cartoes_tag = int(dados_form.get('qtde_cartoes_tag') or 0)
    rec_tags = float(dados_form.get('rec_tags') or 0)
    qtde_cartoes_eus = int(dados_form.get('qtde_cartoes_eus') or 0)
    rec_saude = float(dados_form.get('rec_saude') or 0)

    # Tabela banco de dados
    consumo_credenciado = float(parametros.get('consumo_credenciado', 0))
    confeccao_cartoes = float(parametros.get('confeccao_cartoes', 0))
    custos_operacionais = float(parametros.get('custos_operacionais', 0))
    custos_operacionais_qtde = float(parametros.get('custos_operacionais_qtde', 0))
    custo_tag = float(parametros.get('custo_tag', 0))
    custo_tag_qtde = float(parametros.get('custo_tag_qtde', 0))
    custo_eus = float(parametros.get('custo_eus', 0))
    custo_eus_qtde = float(parametros.get('custo_eus_qtde', 0))
    despesatag_envio = float(parametros.get('despesatag_envio', 0))
    despesatag_tagfisica = float(parametros.get('despesatag_tagfisica', 0))
    despesatag_greeenpass = float(parametros.get('despesatag_greenpass', 0))
    despesaeus_epharma = float(parametros.get('despesaeus_epharma', 0))
    despesaeus_telemedicina = float(parametros.get('despesaeus_telemedicina', 0))
    despesaeus_enviounico = float(parametros.get('despesaeus_enviounico', 0))
    investimento_cartao = float(parametros.get('investimento_cartao', 0))
    negociacao_aprovada = float(parametros.get('negociacao_aprovada', 0))
    negociacao_pendente = float(parametros.get('negociacao_pendente', 0))
    rentabilidade_ideal = float(parametros.get('rentabilidade_ideal', 0))

    # Volumetria
    volumeMensal = qtde_cartoes * valor_credito
    volumeAnual = volumeMensal * 12
    volumeContrato = volumeMensal * qtde_meses

    # Receitas Previstas - Cartão Elo
    consumoCredenciadoMensal = volumeMensal * (consumo_credenciado / 100)
    consumoCredenciadoAnual = volumeAnual * (consumo_credenciado / 100)
    consumoCredenciadoContrato = volumeContrato * (consumo_credenciado / 100)

    taxaAdmMensal = volumeMensal * (taxa_adm / 100)
    taxaAdmAnual = volumeAnual * (taxa_adm / 100)
    taxaAdmContrato = volumeContrato * (taxa_adm / 100)

    vendaCartoesContrato = venda_cartoes * qtde_cartoes
    vendaCartoesAnual = vendaCartoesContrato / (qtde_meses / 12)
    vendaCartoesMensal = vendaCartoesAnual / 12

    totalReceitasPrevistasMensal = vendaCartoesMensal + taxaAdmMensal + consumoCredenciadoMensal
    totalReceitasPrevistasAnual = vendaCartoesAnual + taxaAdmAnual + consumoCredenciadoAnual
    totalReceitasPrevistasContrato = vendaCartoesContrato + taxaAdmContrato + consumoCredenciadoContrato

    # Despesas Previstas - Cartão Elo
    confeccaoCartoesContrato = confeccao_cartoes * qtde_cartoes
    custosOperacionaisContrato = (custos_operacionais * custos_operacionais_qtde * qtde_cartoes) * qtde_meses
    custoTagContrato = (custo_tag * custo_tag_qtde * qtde_cartoes) * qtde_meses
    custoEusContrato = (custo_eus * custo_eus_qtde * qtde_cartoes) * qtde_meses
    custoInvestimentoContrato = investimento_cartao * qtde_cartoes
    totalDespesasPrevistasContrato = custoInvestimentoContrato + custoEusContrato + custoTagContrato + custosOperacionaisContrato + confeccaoCartoesContrato
    
    # Outros Produtos
    receitaTagContrato = rec_tags * qtde_cartoes_tag * qtde_meses
    despesaTagEnvioContrato = despesatag_envio * qtde_cartoes_tag
    despesaTagFisicaContrato = despesatag_tagfisica * qtde_cartoes_tag
    despesaTagGreenpassContrato = (despesatag_greeenpass * qtde_cartoes_tag) * qtde_meses
    totalDespesasTagContrato = despesaTagGreenpassContrato + despesaTagFisicaContrato + despesaTagEnvioContrato

    receitaEusContrato = rec_saude * qtde_cartoes_eus * qtde_meses
    despesaEusEpharma = despesaeus_epharma * qtde_cartoes_eus * qtde_meses
    despesaEusTelemedicina = despesaeus_telemedicina * qtde_cartoes_eus
    despesaEusEnvio = despesaeus_enviounico * qtde_cartoes_eus

    totalDespesasEusContrato = despesaEusEnvio + despesaEusTelemedicina + despesaEusEpharma

    # Resultados
    resultReceitas = totalReceitasPrevistasContrato + receitaTagContrato + receitaEusContrato
    resultDespesas = custoInvestimentoContrato + totalDespesasTagContrato + totalDespesasEusContrato
    rentabilidadeIdeal = rentabilidade_ideal
    statusAprovado = negociacao_aprovada
    statusPendente = negociacao_pendente
    lucroOperacao = resultReceitas - resultDespesas
    lucroOperacaoMensal = lucroOperacao / qtde_meses
    rentabilidadeAtual = (lucroOperacao / volumeContrato) * 100

    resultado = {
        "volumeMensal": volumeMensal,
        "volumeAnual": volumeAnual,
        "volumeContrato": volumeContrato,
        "consumoCredenciadoMensal": consumoCredenciadoMensal,
        "consumoCredenciadoAnual": consumoCredenciadoMensal,
        "consumoCredenciadoContrato": consumoCredenciadoContrato,
        "taxaAdmMensal": taxaAdmMensal,
        "taxaAdmAnual": taxaAdmAnual,
        "taxaAdmContrato": taxaAdmContrato,
        "vendaCartoesContrato": vendaCartoesContrato,
        "vendaCartoesAnual": vendaCartoesAnual,
        "vendaCartoesMensal": vendaCartoesMensal,
        "totalReceitasPrevistasMensal": totalReceitasPrevistasMensal,
        "totalReceitasPrevistasAnual": totalReceitasPrevistasAnual,
        "totalReceitasPrevistasContrato": totalReceitasPrevistasContrato,
        "confeccaoCartoesContrato": confeccaoCartoesContrato,
        "custosOperacionaisContrato": custosOperacionaisContrato,
        "custoTagContrato": custoTagContrato,
        "custoEusContrato": custoEusContrato,  
        "custoInvestimentoContrato": custoInvestimentoContrato,
        "totalDespesasPrevistasContrato": totalDespesasPrevistasContrato,
        "receitaTagContrato": receitaTagContrato,
        "despesaTagEnvioContrato": despesaTagEnvioContrato,
        "despesaTagFisicaContrato": despesaTagFisicaContrato,
        "despesaTagGreenpassContrato": despesaTagGreenpassContrato,
        "totalDespesasTagContrato": totalDespesasTagContrato,
        "receitaEusContrato": receitaEusContrato,
        "despesaEusEpharma": despesaEusEpharma,
        "despesaEusTelemedicina": despesaEusTelemedicina,
        "despesaEusEnvio": despesaEusEnvio,
        "totalDespesasEusContrato": totalDespesasEusContrato,
        "resultReceitas": resultReceitas,
        "resultDespesas": resultDespesas,
        "rentabilidadeIdeal": rentabilidadeIdeal,
        "statusAprovado": statusAprovado,
        "statusPendente": statusPendente,
        "lucroOperacao": lucroOperacao,
        "lucroOperacaoMensal": lucroOperacaoMensal,
        "rentabilidadeAtual": rentabilidadeAtual     
    }

    return jsonify(resultado)

@app.route('/gravar_propostaCOM', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def gravar_propostaCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    data = request.get_json()
    user_id = session.get('user_id')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Buscar os parâmetros vigentes
        cursor.execute("SELECT * FROM parametros_com ORDER BY id DESC LIMIT 1")
        parametros = cursor.fetchone()


        if not parametros:
            return jsonify({"message": "Nenhum parâmetro cadastrado!"}), 400

        parametros = list(parametros)[1:]  # Ignora o ID da linha

        # Certifique-se de que os dados do formulário estejam no formato certo
        def tratar_valor(valor):
            return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())

        valores = (
            int(data['qtde_cartoes']),
            tratar_valor(data['valor_credito']),
            int(data['meses']),
            float(data['taxa_adm']),
            tratar_valor(data['venda_cartoes']),
            int(data['qtde_cartoes_tag']),
            tratar_valor(data['rec_tags']),
            int(data['qtde_cartoes_eus']),
            tratar_valor(data['rec_saude']),
            *parametros,
            int(data['total_receitas']),
            int(data['total_despesas']),
            float(data['lucroOperacao']),
            float(data['lucroOperacaoMensal']),
            float(data['rentabilidadeAtual']),
            float(data['volumeMensal']),      
            float(data['volumeAnual']),       
            float(data['volumeContrato']),    
            user_id
        )

        sql = """
            INSERT INTO simulacao_com (
                qtde_cartoes, valor_credito, qtde_meses, taxa_adm, venda_cartoes,
                qtde_cartoes_tag, rec_tags, qtde_cartoes_eus, rec_saude,
                consumo_credenciado, confeccao_cartoes, custos_operacionais, custos_operacionais_qtde,
                custo_tag, custo_tag_qtde, custo_eus, custo_eus_qtde,
                despesatag_envio, despesatag_tagfisica, despesatag_greenpass,
                despesaeus_epharma, despesaeus_telemedicina, despesaeus_enviounico,
                investimento_cartao, negociacao_aprovada, negociacao_pendente, rentabilidade_ideal,
                total_receitas, total_despesas, lucro_operacao, lucro_operacao_mensal, rentabilidade_atual,
                volume_mensal, volume_anual, volume_contrato, user_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        cursor.execute(sql, valores)
        conn.commit()

        return jsonify({"message": "Proposta gravada com sucesso!"})

    except Exception as e:
        print("Erro ao gravar proposta:", e)
        return jsonify({"message": "Erro ao gravar proposta."}), 500

    finally:
        cursor.close()
        conn.close()



#Rotas dos relatórios
@app.route('/relatorio1COM', methods=['GET', 'POST'])
@modulo_requerido('COMERCIALGESTOR')
def relatorio1COM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        user_id = request.form['user_id']
        data_inicial = request.form['data_inicial']
        data_final = request.form['data_final']

        query = """
            SELECT * FROM simulacao_com
            WHERE criado_em BETWEEN %s AND %s
        """
        params = [data_inicial, data_final]

        if user_id != 'todos' and user_id != '':
            query += " AND user_id = %s"
            params.append(user_id)

        query += " ORDER BY criado_em"
        cursor.execute(query, tuple(params))
        simulacoes = cursor.fetchall()

        user_ids = list(set(sim['user_id'] for sim in simulacoes))
        if user_ids:
            format_strings = ','.join(['%s'] * len(user_ids))
            cursor.execute(f"""
                SELECT u.user_id, u.username
                FROM usuarios u
                JOIN modulos m ON u.user_id = m.user_id
                WHERE u.user_id IN ({format_strings})
                AND m.modulo IN ('COMERCIAL', 'COMERCIALGESTOR')
            """, tuple(user_ids))
            nomes_usuarios = {u['user_id']: u['username'] for u in cursor.fetchall()}
        else:
            nomes_usuarios = {}


        # Criar PDF com ReportLab
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Cabeçalho
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(180, height - 40, "Relatório analítico por usuário")

        pdf.setFont("Helvetica", 10)

        # Converter as strings de data para objetos datetime e depois formatar
        data_ini_formatada = datetime.strptime(data_inicial, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_fim_formatada = datetime.strptime(data_final, "%Y-%m-%d").strftime("%d/%m/%Y")
        pdf.drawString(50, height - 80, f"Período: {data_ini_formatada} a {data_fim_formatada}")

        pdf.drawString(50, height - 95, f"Total de simulações: {len(simulacoes)}")

        # Definir colunas e pesos
        colunas = [
            ("Simulação", 1.5), ("Usuário", 2.5), ("Qtde Cartões", 2), ("Crédito", 1.5),
            ("Meses", 1), ("Tx. Adm", 1), ("Venda Cartões", 2),
            ("TAGs", 1), ("Rec. TAG", 1.5), ("Eu+ Saúde", 1.5),
            ("Rec. Saúde", 1.5), ("Data Criação", 2)
        ]

        total_peso = sum(peso for _, peso in colunas)
        margem_esquerda = 40
        margem_direita = 20
        usable_width = width - margem_esquerda - margem_direita

        espacamento_colunas = []
        x_atual = margem_esquerda
        for _, peso in colunas:
            largura_coluna = (peso / total_peso) * usable_width
            espacamento_colunas.append(x_atual)
            x_atual += largura_coluna

        # Tabela - Cabeçalho
        y = height - 130
        pdf.setFont("Helvetica-Bold", 9)
        pdf.line(margem_esquerda, y + 10, width - margem_direita, y + 10)
        for (titulo, _), x in zip(colunas, espacamento_colunas):
            pdf.drawString(x, y, titulo)

        # Conteúdo
        pdf.setFont("Helvetica", 8)
        y -= 15
        for sim in simulacoes:
            if y < 50:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica-Bold", 9)
                for (titulo, _), x in zip(colunas, espacamento_colunas):
                    pdf.drawString(x, y, titulo)
                    pdf.line(margem_esquerda, y + 10, width - margem_direita, y + 10)
                pdf.setFont("Helvetica", 8)
                y -= 15

            #Linhas Zebradas
            if simulacoes.index(sim) % 2 == 0:
                pdf.setFillColor(lightgrey)
                pdf.rect(margem_esquerda, y - 2, usable_width, 12, stroke=0, fill=1)
                pdf.setFillColor("black")

            dados = [
                str(sim['id']),
                nomes_usuarios.get(sim['user_id'], f"ID {sim['user_id']}"),
                str(sim['qtde_cartoes']),
                f"R$ {sim['valor_credito']:.2f}",
                str(sim['qtde_meses']),
                str(sim['taxa_adm']),
                str(sim['venda_cartoes']),
                str(sim['qtde_cartoes_tag']),
                f"R$ {sim['rec_tags']:.2f}",
                str(sim['qtde_cartoes_eus']),
                f"R$ {sim['rec_saude']:.2f}",
                sim['criado_em'].strftime("%d/%m/%Y %H:%M")
            ]

            for texto, x in zip(dados, espacamento_colunas):
                pdf.drawString(x, y, texto)

            y -= 12

        pdf.setFont("Helvetica-Oblique", 7)
        pdf.drawString(margem_esquerda, 20, f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        pdf.save()
        buffer.seek(0)

        return send_file(buffer, download_name='relatorio_simulacoes.pdf', as_attachment=True)

    # GET: renderizar formulário
    cursor.execute("""
        SELECT u.user_id AS id, u.username AS nome
        FROM usuarios u
        JOIN modulos m ON u.user_id = m.user_id
        WHERE m.modulo IN ('COMERCIAL', 'COMERCIALGESTOR')
    """)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('relatoriosimulacoesCOM.html', usuarios=usuarios)

@app.route('/relatorio2COM', methods=['GET', 'POST'])
@modulo_requerido('COMERCIALGESTOR')
def relatorio2COM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_sim = request.form['id_sim']
        data_inicial = request.form['data_inicial']
        data_final = request.form['data_final']
        
        query = """
            SELECT * FROM simulacao_com
            WHERE criado_em BETWEEN %s AND %s
        """
        params = [data_inicial, data_final]

        if id_sim != 'todos' and id_sim != '':
            query += " AND id = %s"
            params.append(id_sim)

        query += " ORDER BY criado_em"
        cursor.execute(query, tuple(params))
        simulacoes = cursor.fetchall()

        # Criar PDF com ReportLab
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Cabeçalho
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(180, height - 40, "Relatório analítico por simulação")

        pdf.setFont("Helvetica", 10)

        # Converter as strings de data para objetos datetime e depois formatar
        data_ini_formatada = datetime.strptime(data_inicial, "%Y-%m-%d").strftime("%d/%m/%Y")
        data_fim_formatada = datetime.strptime(data_final, "%Y-%m-%d").strftime("%d/%m/%Y")
        pdf.drawString(50, height - 80, f"Período: {data_ini_formatada} a {data_fim_formatada}")

        pdf.drawString(50, height - 95, f"Total de simulações: {len(simulacoes)}")


        margem_esquerda = 40
        margem_direita = 20

        # Tabela - Cabeçalho
        y = height - 130
        pdf.setFont("Helvetica-Bold", 9)
        pdf.line(margem_esquerda, y + 10, width - margem_direita, y + 10)

        # Conteúdo
        pdf.setFont("Helvetica", 8)
        y -= 10

        for sim in simulacoes:
            if y < 80:
                pdf.showPage()
                pdf.setFont("Helvetica", 8)
                y = height - 50

            # Cabeçalho de cada simulação
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(margem_esquerda, y, f"Simulação ID: {sim['id']}")
            y -= 12

            pdf.setFont("Helvetica", 8)
            pdf.drawString(margem_esquerda, y, f"Volume Mensal: {locale.currency(sim['volume_mensal'], grouping=True)}")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Volume Anual: {locale.currency(sim['volume_anual'], grouping=True)}")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Volume Contrato: {locale.currency(sim['volume_contrato'], grouping=True)}")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Lucro Operação: {locale.currency(sim['lucro_operacao'], grouping=True)}")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Lucro Operação p/ Mês: {locale.currency(sim['lucro_operacao_mensal'], grouping=True)}")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Rentabilidade Atual: {sim['rentabilidade_atual']}%")
            y -= 12
            pdf.drawString(margem_esquerda, y, f"Data Criação: {sim['criado_em'].strftime('%d/%m/%Y %H:%M')}")
            y -= 20  # Espaço entre blocos

        pdf.setFont("Helvetica-Oblique", 7)
        pdf.drawString(margem_esquerda, 20, f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        pdf.save()
        buffer.seek(0)

        return send_file(buffer, download_name='relatorio_simulacoes.pdf', as_attachment=True)

    # GET: renderizar formulário
    cursor.execute("""
        SELECT id FROM simulacao_com
        ORDER BY criado_em DESC
    """)
    simulacao_com = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('relatoriosimulacoes2COM.html', simulacao_com=simulacao_com)



#Rotas de aprovação / reprovação de simulações com status 'PENDENTE'
propostas_pendentes = [] # Lista temporária de propostas pendentes (em memória)

@app.route('/aprovacoesCOM')
@modulo_requerido('COMERCIALGESTOR')
def aprovacoesCOM():
    return render_template('aprovacoesCOM.html')

@app.route('/enviar_para_aprovacaoCOM', methods=['POST'])
def enviar_para_aprovacaoCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))


    dados = request.get_json()
    usuario = session.get('username')
    dados["id"] = dados.get("id") or str(uuid.uuid4())
    dados['usuario'] = usuario

    propostas_pendentes.append(dados)
    return jsonify({"message": "Proposta enviada para aprovação do gestor."})

@app.route('/listar_aprovacoesCOM', methods=['GET'])
def listar_aprovacoesCOM():
    return jsonify(propostas_pendentes)

@app.route("/reprovar_propostaCOM", methods=["POST"])
@modulo_requerido('COMERCIALGESTOR')
def reprovar_propostaCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    data = request.get_json()
    proposta_id = data.get("id")

    if not proposta_id:
        return jsonify({"message": "ID da proposta não informado."}), 400

    try:
        # Remover a proposta da lista em memória
        for i, p in enumerate(propostas_pendentes):
            if str(p.get("id")) == str(proposta_id):
                propostas_pendentes.pop(i)
                return jsonify({"message": "Proposta reprovada com sucesso."})

        return jsonify({"message": "Proposta não encontrada."}), 404

    except Exception as e:
        return jsonify({"message": f"Erro ao reprovar proposta: {str(e)}"}), 500

@app.route('/remover_aprovacaoCOM', methods=['POST'])
def remover_aprovacaoCOM():
    data = request.get_json()
    id_proposta = data.get("id")

    try:
        for i, p in enumerate(propostas_pendentes):
            if str(p.get("id")) == str(id_proposta):
                propostas_pendentes.pop(i)
                return jsonify({"message": "Proposta removida da lista de pendentes."})

        return jsonify({"message": "Proposta não encontrada."}), 404

    except Exception as e:
        return jsonify({"message": f"Erro ao remover proposta: {str(e)}"}), 500
#------------------------------------------------------------------#





#-----------ROTAS VIABILIDADE COMERCIAL ELO (PARCERIAS)------------#
#Rotas de cadastro de parcerias
@app.route('/parceriasCOM')
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def parceriasCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template('cadastroparceiroCOM.html')

@app.route('/api/parceriasCOM')
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def listar_parceriasCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT codigo_parceiro, nome, comissao FROM cadprc_com ORDER BY nome")
    parcerias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(parcerias)

@app.route('/cadastrar_parceriaCOM', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def cadastrar_parceriaCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    conn = None
    cursor = None
    
    try:
        # Coleta de dados do formulário (CORRIGIDO o nome da variável)
        codigo_parceiro = ''.join(filter(str.isdigit, request.form['codigo_parceiro'].strip()))
        nome = request.form['nome'].strip()
        uf = request.form['uf'].strip()
        comissao = request.form['comissao'].strip()

        # Validação simples
        if not codigo_parceiro or not nome or not uf or not comissao:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/parceriasCOM')

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verifica duplicidade de CNPJ
        cursor.execute("SELECT COUNT(*) AS total FROM cadprc_com WHERE codigo_parceiro = %s", (codigo_parceiro,))
        if int(cursor.fetchone()['total']) > 0:
            flash("Já existe um parceiro com esse CNPJ.", "erro")
            return redirect('/parceriasCOM')

        # Verifica duplicidade de razão social
        cursor.execute("SELECT COUNT(*) AS total FROM cadprc_com WHERE LOWER(TRIM(nome)) = LOWER(%s)", (nome,))
        if cursor.fetchone()['total'] > 0:
            flash("Já existe um parceiro com essa razão social.", "erro")
            return redirect('/parceriasCOM')

        # Inserção
        query = """
            INSERT INTO cadprc_com (codigo_parceiro, nome, uf, comissao)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (codigo_parceiro, nome, uf, comissao))
        conn.commit()

        flash('Parceiro cadastrado com sucesso!', 'sucesso')
        return redirect('/parceriasCOM')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/parceriasCOM')
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/parceriasCOM/<codigo>', methods=['PUT'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def atualizar_parceriaCOM(codigo):
    if 'username' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401

    dados = request.get_json()
    novo_nome = dados.get('nome', '').strip()
    nova_comissao = dados.get('comissao', '').strip()

    if not novo_nome or not nova_comissao:
        return jsonify({'erro': 'Nome e comissão são obrigatórios.'}), 400

    try:
        nova_comissao = nova_comissao.replace(',', '.')
        nova_comissao_float = float(nova_comissao)
    except ValueError:
        return jsonify({'erro': 'Comissão inválida.'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cadprc_com 
        SET nome = %s, comissao = %s 
        WHERE codigo_parceiro = %s
    """, (novo_nome, nova_comissao_float, codigo))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'mensagem': 'Parceria atualizada com sucesso'}), 200

@app.route('/api/parceriasCOM/<codigo>', methods=['DELETE'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def excluir_parceriaCOM(codigo):
    if 'username' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cadprc_com WHERE codigo_parceiro = %s", (codigo,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'mensagem': 'Parceria excluída com sucesso'}), 200



#Rotas de parâmetros e simulações
@app.route('/simulacaoprcCOM', methods=['GET'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def simulacaoprcCOM():  
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    id_parceiro = request.args.get('id_parceiro')

    if session.get('parceiro_confirmado') != id_parceiro:
        flash('Você precisa selecionar a parceria antes de continuar.')
        return redirect('/parceriasCOM')  # ou o nome correto

    # Buscar dados do parceiro
    parceiro = None
    if id_parceiro:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nome, comissao FROM cadprc_com WHERE codigo_parceiro = %s", (id_parceiro,))
        parceiro = cursor.fetchone()
    
    return render_template('simulacaoprcCOM.html', parceiro=parceiro, id_parceiro=id_parceiro, nome_parceiro=parceiro['nome'])

@app.route('/parametrosprcCOM')
@modulo_requerido('COMERCIALGESTOR')
def parametrosprcCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    return render_template('parametrosprcCOM.html')

@app.route('/get_parametrosprc')
@modulo_requerido('COMERCIALGESTOR')
def get_parametrosprc():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM parametrosprc_com LIMIT 1")
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(resultado)

@app.route('/salvar_parametrosprc', methods=['POST'])
@modulo_requerido('COMERCIALGESTOR')
def salvar_parametrosprc():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    dados = request.json

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Aqui você pode decidir se quer sobrescrever (DELETE e INSERT) ou usar UPDATE com WHERE
    cursor.execute("DELETE FROM parametrosprc_com")  # Mantém só 1 registro
    query = """
        INSERT INTO parametrosprc_com (
            consumo_credenciado, confeccao_cartoes, custos_operacionais, custos_operacionais_qtde,
            custo_tag, custo_tag_qtde, custo_eus, custo_eus_qtde,
            despesatag_envio, despesatag_tagfisica, despesatag_greenpass,
            despesaeus_epharma, despesaeus_telemedicina, despesaeus_enviounico,
            investimento_cartao, negociacao_aprovada, negociacao_pendente, rentabilidade_ideal
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        dados['consumo_credenciado'],
        dados['confeccao_cartoes'],
        dados['custos_operacionais'],
        dados['custos_operacionais_qtde'],
        dados['custo_tag'],
        dados['custo_tag_qtde'],
        dados['custo_eus'],
        dados['custo_eus_qtde'],
        dados['despesatag_envio'],
        dados['despesatag_tagfisica'],
        dados['despesatag_greenpass'],
        dados['despesaeus_epharma'],
        dados['despesaeus_telemedicina'],
        dados['despesaeus_enviounico'],
        dados['investimento_cartao'],
        dados['negociacao_aprovada'],
        dados['negociacao_pendente'],
        dados['rentabilidade_ideal'],
    )
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()

    return jsonify({"status": "ok"})

@app.route('/calcular_simulacaoprc', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def calcular_simulacaoprc():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    #Capturar o id do parceiro enviado pelo formulário de cadastro
    dados_form = request.json  # dicionário com os dados do formulário
    parametros = get_parametros_calculos()  # dicionário com os parâmetros do banco
    id_parceiro = dados_form.get('id_parceiro')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, comissao FROM cadprc_com WHERE codigo_parceiro = %s", (id_parceiro,))
    parceiro = cursor.fetchone() #Nome e comissão do parceiro armazenados


    # Formulário simulacaoprcCOM.html
    qtde_cartoes = float(dados_form.get('qtde_cartoes') or 0)
    valor_credito = float(dados_form.get('valor_credito') or 0)
    qtde_meses = int(dados_form.get('meses') or 0)
    taxa_adm = float(dados_form.get('taxa_adm') or 0)
    venda_cartoes = float(dados_form.get('venda_cartoes') or 0)
    qtde_cartoes_tag = int(dados_form.get('qtde_cartoes_tag') or 0)
    rec_tags = float(dados_form.get('rec_tags') or 0)
    qtde_cartoes_eus = int(dados_form.get('qtde_cartoes_eus') or 0)
    rec_saude = float(dados_form.get('rec_saude') or 0)

    # Tabela banco de dados
    consumo_credenciado = float(parametros.get('consumo_credenciado', 0))
    confeccao_cartoes = float(parametros.get('confeccao_cartoes', 0))
    custos_operacionais = float(parametros.get('custos_operacionais', 0))
    custos_operacionais_qtde = float(parametros.get('custos_operacionais_qtde', 0))
    custo_tag = float(parametros.get('custo_tag', 0))
    custo_tag_qtde = float(parametros.get('custo_tag_qtde', 0))
    custo_eus = float(parametros.get('custo_eus', 0))
    custo_eus_qtde = float(parametros.get('custo_eus_qtde', 0))
    despesatag_envio = float(parametros.get('despesatag_envio', 0))
    despesatag_tagfisica = float(parametros.get('despesatag_tagfisica', 0))
    despesatag_greeenpass = float(parametros.get('despesatag_greenpass', 0))
    despesaeus_epharma = float(parametros.get('despesaeus_epharma', 0))
    despesaeus_telemedicina = float(parametros.get('despesaeus_telemedicina', 0))
    despesaeus_enviounico = float(parametros.get('despesaeus_enviounico', 0))
    investimento_cartao = float(parametros.get('investimento_cartao', 0))
    negociacao_aprovada = float(parametros.get('negociacao_aprovada', 0))
    negociacao_pendente = float(parametros.get('negociacao_pendente', 0))
    rentabilidade_ideal = float(parametros.get('rentabilidade_ideal', 0))

    # Volumetria
    volumeMensal = qtde_cartoes * valor_credito
    volumeAnual = volumeMensal * 12
    volumeContrato = volumeMensal * qtde_meses

    # Receitas Previstas - Cartão Elo
    consumoCredenciadoMensal = volumeMensal * (consumo_credenciado / 100)
    consumoCredenciadoAnual = volumeAnual * (consumo_credenciado / 100)
    consumoCredenciadoContrato = volumeContrato * (consumo_credenciado / 100)

    taxaAdmMensal = volumeMensal * (taxa_adm / 100)
    taxaAdmAnual = volumeAnual * (taxa_adm / 100)
    taxaAdmContrato = volumeContrato * (taxa_adm / 100)

    vendaCartoesContrato = venda_cartoes * qtde_cartoes
    vendaCartoesAnual = vendaCartoesContrato / (qtde_meses / 12)
    vendaCartoesMensal = vendaCartoesAnual / 12

    totalReceitasPrevistasMensal = vendaCartoesMensal + taxaAdmMensal + consumoCredenciadoMensal
    totalReceitasPrevistasAnual = vendaCartoesAnual + taxaAdmAnual + consumoCredenciadoAnual
    totalReceitasPrevistasContrato = vendaCartoesContrato + taxaAdmContrato + consumoCredenciadoContrato

    # Despesas Previstas - Cartão Elo
    confeccaoCartoesContrato = confeccao_cartoes * qtde_cartoes
    custosOperacionaisContrato = (custos_operacionais * custos_operacionais_qtde * qtde_cartoes) * qtde_meses
    custoTagContrato = (custo_tag * custo_tag_qtde * qtde_cartoes) * qtde_meses
    custoEusContrato = (custo_eus * custo_eus_qtde * qtde_cartoes) * qtde_meses
    custoInvestimentoContrato = investimento_cartao * qtde_cartoes
    totalDespesasPrevistasContrato = custoInvestimentoContrato + custoEusContrato + custoTagContrato + custosOperacionaisContrato + confeccaoCartoesContrato
    
    # Outros Produtos
    receitaTagContrato = rec_tags * qtde_cartoes_tag * qtde_meses
    despesaTagEnvioContrato = despesatag_envio * qtde_cartoes_tag
    despesaTagFisicaContrato = despesatag_tagfisica * qtde_cartoes_tag
    despesaTagGreenpassContrato = (despesatag_greeenpass * qtde_cartoes_tag) * qtde_meses
    totalDespesasTagContrato = despesaTagGreenpassContrato + despesaTagFisicaContrato + despesaTagEnvioContrato

    receitaEusContrato = rec_saude * qtde_cartoes_eus * qtde_meses
    despesaEusEpharma = despesaeus_epharma * qtde_cartoes_eus * qtde_meses
    despesaEusTelemedicina = despesaeus_telemedicina * qtde_cartoes_eus
    despesaEusEnvio = despesaeus_enviounico * qtde_cartoes_eus

    comissao_valor = float(parceiro[1])
    comissao = (comissao_valor / 100) * volumeContrato

    totalDespesasEusContrato = despesaEusEnvio + despesaEusTelemedicina + despesaEusEpharma + comissao

    # Resultados
    resultReceitas = totalReceitasPrevistasContrato + receitaTagContrato + receitaEusContrato
    resultDespesas = custoInvestimentoContrato + totalDespesasTagContrato + totalDespesasEusContrato
    rentabilidadeIdeal = rentabilidade_ideal
    statusAprovado = negociacao_aprovada
    statusPendente = negociacao_pendente
    lucroOperacao = resultReceitas - resultDespesas
    lucroOperacaoMensal = lucroOperacao / qtde_meses
    rentabilidadeAtual = (lucroOperacao / volumeContrato) * 100

    resultado = {
        "volumeMensal": volumeMensal,
        "volumeAnual": volumeAnual,
        "volumeContrato": volumeContrato,
        "consumoCredenciadoMensal": consumoCredenciadoMensal,
        "consumoCredenciadoAnual": consumoCredenciadoMensal,
        "consumoCredenciadoContrato": consumoCredenciadoContrato,
        "taxaAdmMensal": taxaAdmMensal,
        "taxaAdmAnual": taxaAdmAnual,
        "taxaAdmContrato": taxaAdmContrato,
        "vendaCartoesContrato": vendaCartoesContrato,
        "vendaCartoesAnual": vendaCartoesAnual,
        "vendaCartoesMensal": vendaCartoesMensal,
        "totalReceitasPrevistasMensal": totalReceitasPrevistasMensal,
        "totalReceitasPrevistasAnual": totalReceitasPrevistasAnual,
        "totalReceitasPrevistasContrato": totalReceitasPrevistasContrato,
        "confeccaoCartoesContrato": confeccaoCartoesContrato,
        "custosOperacionaisContrato": custosOperacionaisContrato,
        "custoTagContrato": custoTagContrato,
        "custoEusContrato": custoEusContrato,  
        "custoInvestimentoContrato": custoInvestimentoContrato,
        "totalDespesasPrevistasContrato": totalDespesasPrevistasContrato,
        "receitaTagContrato": receitaTagContrato,
        "despesaTagEnvioContrato": despesaTagEnvioContrato,
        "despesaTagFisicaContrato": despesaTagFisicaContrato,
        "despesaTagGreenpassContrato": despesaTagGreenpassContrato,
        "totalDespesasTagContrato": totalDespesasTagContrato,
        "receitaEusContrato": receitaEusContrato,
        "despesaEusEpharma": despesaEusEpharma,
        "despesaEusTelemedicina": despesaEusTelemedicina,
        "despesaEusEnvio": despesaEusEnvio,
        "comissao": comissao,
        "totalDespesasEusContrato": totalDespesasEusContrato,
        "resultReceitas": resultReceitas,
        "resultDespesas": resultDespesas,
        "rentabilidadeIdeal": rentabilidadeIdeal,
        "statusAprovado": statusAprovado,
        "statusPendente": statusPendente,
        "lucroOperacao": lucroOperacao,
        "lucroOperacaoMensal": lucroOperacaoMensal,
        "rentabilidadeAtual": rentabilidadeAtual     
    }

    return jsonify(resultado)

@app.route('/gravar_propostaprcCOM', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def gravar_propostaprcCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    data = request.get_json()
    comissao = float(data['comissao'])
    user_id = session.get('user_id')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Buscar os parâmetros vigentes
        cursor.execute("SELECT * FROM parametrosprc_com ORDER BY id DESC LIMIT 1")
        parametros = cursor.fetchone()


        if not parametros:
            return jsonify({"message": "Nenhum parâmetro cadastrado!"}), 400

        parametros = list(parametros)[1:]  # Ignora o ID da linha

        # Certifique-se de que os dados do formulário estejam no formato certo
        def tratar_valor(valor):
            return float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())

        valores = (
            int(data['qtde_cartoes']),
            tratar_valor(data['valor_credito']),
            int(data['meses']),
            float(data['taxa_adm']),
            tratar_valor(data['venda_cartoes']),
            int(data['qtde_cartoes_tag']),
            tratar_valor(data['rec_tags']),
            int(data['qtde_cartoes_eus']),
            tratar_valor(data['rec_saude']),
            *parametros[:15], #até investimento_cartao
            comissao,
            *parametros[15:18], #resto
            int(data['total_receitas']),
            int(data['total_despesas']),
            float(data['lucroOperacao']),
            float(data['lucroOperacaoMensal']),
            float(data['rentabilidadeAtual']),
            float(data['volumeMensal']),      
            float(data['volumeAnual']),       
            float(data['volumeContrato']),    
            user_id
        )

        sql = """
            INSERT INTO simulacaoprc_com (
                qtde_cartoes, valor_credito, qtde_meses, taxa_adm, venda_cartoes,
                qtde_cartoes_tag, rec_tags, qtde_cartoes_eus, rec_saude,
                consumo_credenciado, confeccao_cartoes, custos_operacionais, custos_operacionais_qtde,
                custo_tag, custo_tag_qtde, custo_eus, custo_eus_qtde,
                despesatag_envio, despesatag_tagfisica, despesatag_greenpass,
                despesaeus_epharma, despesaeus_telemedicina, despesaeus_enviounico,
                investimento_cartao, comissao, negociacao_aprovada, negociacao_pendente, rentabilidade_ideal,
                total_receitas, total_despesas, lucro_operacao, lucro_operacao_mensal, rentabilidade_atual,
                volume_mensal, volume_anual, volume_contrato, user_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        cursor.execute(sql, valores)
        conn.commit()

        return jsonify({"message": "Proposta gravada com sucesso!"})

    except Exception as e:
        print("Erro ao gravar proposta:", e)
        return jsonify({"message": "Erro ao gravar proposta."}), 500

    finally:
        cursor.close()
        conn.close()



#Rotas de aprovação / reprovação de simulações com status 'PENDENTE'
propostas_pendentes_prc = [] # Lista temporária de propostas pendentes (em memória)

@app.route('/aprovacoesprcCOM')
@modulo_requerido('COMERCIALGESTOR')
def aprovacoesprcCOM():
    return render_template('aprovacoesprcCOM.html')

@app.route('/enviar_para_aprovacaoprcCOM', methods=['POST'])
def enviar_para_aprovacaoprcCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))


    dados = request.get_json()
    usuario = session.get('username')
    dados["id"] = dados.get("id") or str(uuid.uuid4())
    dados['usuario'] = usuario

    propostas_pendentes_prc.append(dados)
    return jsonify({"message": "Proposta enviada para aprovação do gestor."})

@app.route('/listar_aprovacoesprcCOM', methods=['GET'])
def listar_aprovacoesprcCOM():
    return jsonify(propostas_pendentes_prc)

@app.route("/reprovar_propostaprcCOM", methods=["POST"])
@modulo_requerido('COMERCIALGESTOR')
def reprovar_propostaprcCOM():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    data = request.get_json()
    proposta_id = data.get("id")

    if not proposta_id:
        return jsonify({"message": "ID da proposta não informado."}), 400

    try:
        # Remover a proposta da lista em memória
        for i, p in enumerate(propostas_pendentes_prc):
            if str(p.get("id")) == str(proposta_id):
                propostas_pendentes_prc.pop(i)
                return jsonify({"message": "Proposta reprovada com sucesso."})

        return jsonify({"message": "Proposta não encontrada."}), 404

    except Exception as e:
        return jsonify({"message": f"Erro ao reprovar proposta: {str(e)}"}), 500

@app.route('/remover_aprovacaoprcCOM', methods=['POST'])
def remover_aprovacaoprcCOM():
    data = request.get_json()
    id_proposta = data.get("id")

    try:
        for i, p in enumerate(propostas_pendentes_prc):
            if str(p.get("id")) == str(id_proposta):
                propostas_pendentes_prc.pop(i)
                return jsonify({"message": "Proposta removida da lista de pendentes."})

        return jsonify({"message": "Proposta não encontrada."}), 404

    except Exception as e:
        return jsonify({"message": f"Erro ao remover proposta: {str(e)}"}), 500

@app.route('/parceriasCOM_sugestoes')
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def parceriasCOM_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_parceiro, nome, comissao FROM cadprc_com WHERE nome LIKE %s LIMIT 10", (f'%{termo}%',))
    resultados = [{'codigo_parceiro': row[0], 'nome': row[1], 'comissao': row[2]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)

@app.route('/confirmar_selecao_parceiro', methods=['POST'])
@modulo_requerido('COMERCIAL','COMERCIALGESTOR')
def confirmar_selecao_parceiro():
    data = request.get_json()
    session['parceiro_confirmado'] = data.get('id_parceiro')
    return jsonify({'status': 'ok'})

#------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True) 
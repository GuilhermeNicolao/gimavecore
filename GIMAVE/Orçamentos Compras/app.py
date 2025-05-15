from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
import os
import re
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
from decimal import Decimal

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


# Homepage 
@app.route('/home')
def home():
    return render_template('home_fin.html')

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
        cnpj = re.sub(r'\D', '', request.form['cnpj'].strip())
        razao_social = request.form['razao_social'].strip()
        rua = request.form['rua'].strip()
        numero = request.form['numero'].strip()
        cep = re.sub(r'\D', '', request.form['cep'].strip())

        # Validação simples
        if not cnpj or not razao_social or not rua or not numero or not cep:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/fornecedores')

        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Verifica duplicidade de CNPJ
                cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE cnpj = %s", (cnpj,))
                if cursor.fetchone()[0] > 0:
                    flash("Já existe um fornecedor com esse CNPJ.", "erro")
                    return redirect('/fornecedores')

                # Verifica duplicidade de razão social
                cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE LOWER(TRIM(razao_social)) = LOWER(%s)", (razao_social,))
                if cursor.fetchone()[0] > 0:
                    flash("Já existe um fornecedor com essa razão social.", "erro")
                    return redirect('/fornecedores')

                # Inserção
                query = """
                    INSERT INTO fornecedores_orc (cnpj, razao_social, rua, numero, cep)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (cnpj, razao_social, rua, numero, cep))
                conn.commit()

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

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Verifica se razão social já está sendo usada por outro fornecedor
                cursor.execute("""
                    SELECT COUNT(*) FROM fornecedores_orc 
                    WHERE LOWER(TRIM(razao_social)) = LOWER(%s) AND cnpj != %s
                """, (novo_nome, id))
                if cursor.fetchone()[0] > 0:
                    return jsonify({'erro': 'Já existe outro fornecedor com essa razão social.'}), 400

                # Atualiza a razão social
                cursor.execute("UPDATE fornecedores_orc SET razao_social = %s WHERE cnpj = %s", (novo_nome, id))
                conn.commit()

        return jsonify({'sucesso': True})

    except mysql.connector.Error as err:
        return jsonify({'erro': str(err)}), 500

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
    cursor.execute("SELECT cnpj, razao_social FROM fornecedores_orc WHERE razao_social LIKE %s LIMIT 10", (f'%{termo}%',))
    resultados = [{'cnpj': row[0], 'razao_social': row[1]} for row in cursor.fetchall()]
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
        categoria_id = request.form['categoria_id'].strip()
        fornecedor_cnpj = request.form['fornecedor_cnpj'].strip()
        descricao = request.form['descricao'].strip()

        if not nome or not categoria_id or not fornecedor_cnpj:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/produtos')

        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Verifica se a categoria existe
                cursor.execute("SELECT COUNT(*) FROM categoria_orc WHERE id_categoria = %s", (categoria_id,))
                if cursor.fetchone()[0] == 0:
                    flash("Categoria não encontrada. Por favor, selecione uma válida.", "erro")
                    return redirect('/produtos')

                # Verifica se o fornecedor existe
                cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE cnpj = %s", (fornecedor_cnpj,))
                if cursor.fetchone()[0] == 0:
                    flash("Fornecedor não encontrado. Por favor, selecione um válido.", "erro")
                    return redirect('/produtos')

                # Verifica se já existe produto com o mesmo nome, categoria e fornecedor
                query_verifica = """
                    SELECT COUNT(*) FROM produtos_orc 
                    WHERE LOWER(TRIM(nome)) = LOWER(%s)
                    AND categoria_id = %s
                    AND fornecedor_cnpj = %s
                """
                cursor.execute(query_verifica, (nome, categoria_id, fornecedor_cnpj))
                (existe,) = cursor.fetchone()

                if existe > 0:
                    flash("Produto já cadastrado com esses dados!", "erro")
                    return redirect('/produtos')

                # Inserção
                query = """
                    INSERT INTO produtos_orc (nome, categoria_id, fornecedor_cnpj, descricao)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (nome, categoria_id, fornecedor_cnpj, descricao))
                conn.commit()

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

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Obtém os dados atuais do produto
                cursor.execute("SELECT categoria_id, fornecedor_cnpj FROM produtos_orc WHERE id_produto = %s", (id,))
                produto = cursor.fetchone()

                if not produto:
                    return jsonify({'erro': 'Produto não encontrado'}), 404

                categoria_id = produto['categoria_id']
                fornecedor_cnpj = produto['fornecedor_cnpj']

                # Verifica se já existe outro produto com o mesmo nome/categoria/fornecedor
                query_verifica = """
                    SELECT COUNT(*) FROM produtos_orc
                    WHERE LOWER(TRIM(nome)) = LOWER(%s)
                    AND categoria_id = %s
                    AND fornecedor_cnpj = %s
                    AND id_produto != %s
                """
                cursor.execute(query_verifica, (novo_nome, categoria_id, fornecedor_cnpj, id))
                (existe,) = cursor.fetchone().values()

                if existe > 0:
                    return jsonify({'erro': 'Já existe outro produto com esse nome, categoria e fornecedor.'}), 400

                cursor.execute("UPDATE produtos_orc SET nome = %s WHERE id_produto = %s", (novo_nome, id))
                conn.commit()

        return jsonify({'sucesso': True})

    except mysql.connector.Error as err:
        return jsonify({'erro': str(err)}), 500

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
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_produto, nome FROM produtos_orc
        WHERE nome LIKE %s
        ORDER BY nome
        LIMIT 10
    """, (f"%{termo}%",))
    resultados = cursor.fetchall()
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

@app.route('/categorias_sugestoes')
def categorias_sugestoes():
    termo = request.args.get('q', '').strip()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id_categoria, descricao FROM categoria_orc WHERE descricao LIKE %s LIMIT 10", (f'%{termo}%',))
    resultados = [{'id_categoria': row[0], 'descricao': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(resultados)



#Rotas Orçamentos
@app.route('/cadastro')
def cadastro_form():
    return render_template('cadastro_fin.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        # Coletar dados do formulário
        data = request.form['data']
        produto_id = request.form['produto_id']
        fornecedor_cnpj = request.form['fornecedor_cnpj']
        valor = request.form['valor'].strip()
        observacao = request.form['observacao'].strip()

        # Validação simples
        if not data or not produto_id or not fornecedor_cnpj or not valor:
            flash('Preencha todos os campos obrigatórios!', 'erro')
            return redirect('/cadastro')

        # Formatando data e valor para padrão MySQL
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
        vlr_formatado = float(valor.replace('R$', '').replace('.', '').replace(',', '.').strip())


        # Abrindo conexão com o banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verifica se o produto existe
        cursor.execute("SELECT COUNT(*) FROM produtos_orc WHERE id_produto = %s", (produto_id,))
        produto_existe = cursor.fetchone()[0]
  
        if not produto_existe:
            flash("Produto não encontrado. Por favor, selecione um produto válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastro')  

        # Verifica se o fornecedor existe
        cursor.execute("SELECT COUNT(*) FROM fornecedores_orc WHERE cnpj = %s", (fornecedor_cnpj,))
        fornecedor_existe = cursor.fetchone()[0] 

        if not fornecedor_existe:
            flash("Fornecedor não encontrado. Por favor, selecione uma válido.", "erro")
            cursor.close()
            conn.close()
            return redirect('/cadastro')   

        # Inserção
        query = """
            INSERT INTO cadastro_orc_teste 
            (dt, vlr_orcamento, observacao, status, produto_id, fornecedor_cnpj)
            VALUES (%s, %s, %s, 'Pendente', %s, %s)
        """
        cursor.execute(query, (data_formatada, vlr_formatado, observacao, produto_id, fornecedor_cnpj))
        conn.commit()

        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect('/cadastro')

    except mysql.connector.Error as err:
        flash(f'Erro ao inserir os dados: {err}', 'erro')
        return redirect('/cadastro')

@app.route('/validar', methods=['GET', 'POST'])
def validar():
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
            cursor.execute("UPDATE cadastro_orc_teste SET status = 'Aprovado' WHERE id_orcamento = %s", (id_orcamento,))

            # Reprova os demais do mesmo produto
            cursor.execute("""
                UPDATE cadastro_orc_teste
                SET status = 'Reprovado'
                WHERE produto_id = %s AND id_orcamento != %s
            """, (produto_id, id_orcamento))

            flash('Orçamento aprovado com sucesso', 'success')


        elif acao == 'excluir':
            cursor.execute("DELETE FROM cadastro_orc_teste WHERE id_orcamento = %s", (id_orcamento,))
            flash('Orçamento excluído com sucesso', 'success')

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('validar', data_inicio=data_inicio, data_fim=data_fim))

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
            FROM cadastro_orc_teste c
            JOIN produtos_orc p ON c.produto_id = p.id_produto
            JOIN fornecedores_orc f ON c.fornecedor_cnpj = f.cnpj
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

    return render_template('validar_fin.html', orcamentos=orcamentos, datetime=datetime)

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

    query_base = """
        SELECT o.id_orcamento, o.dt, o.vlr_orcamento, o.observacao, o.status,
               p.nome AS produto, f.razao_social AS fornecedor
        FROM cadastro_orc_teste o
        JOIN produtos_orc p ON o.produto_id = p.id_produto
        JOIN fornecedores_orc f ON o.fornecedor_cnpj = f.cnpj
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


# Rota Dashboard
@app.route('/dashboard')
def dashboard():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    produto_id = request.args.get('produto_id')

    relatorio = []
    produtos = []

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)

    # Buscar produtos para o select
    cur.execute("SELECT id_produto, nome FROM produtos_orc ORDER BY nome")
    produtos = cur.fetchall()

    total_economia = Decimal('0.00')  # Inicializa totalizador

    if data_inicio and data_fim:
        if produto_id:
            query = """
                SELECT 
                    c.produto_id, p.nome AS nome_produto, c.dt,
                    c.vlr_orcamento, c.status, f.razao_social AS fornecedor
                FROM cadastro_orc_teste c
                JOIN produtos_orc p ON c.produto_id = p.id_produto
                JOIN fornecedores_orc f ON c.fornecedor_cnpj = f.cnpj
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
                FROM cadastro_orc_teste c
                JOIN produtos_orc p ON c.produto_id = p.id_produto
                JOIN fornecedores_orc f ON c.fornecedor_cnpj = f.cnpj
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

    return render_template('dashboard_fin.html', 
                           relatorio=relatorio, 
                           produtos=produtos, 
                           total_economia=float(total_economia))



if __name__ == '__main__':
    app.run(debug=True)
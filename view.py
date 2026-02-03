from flask import Flask, jsonify, request
from main import app, con

@app.route('/livro', methods=['GET'])
def livro():
    try:
        cur = con.cursor()
        cur.execute("SELECT id_livro, titulo, autor,ano_publicacao FROM livro ")
        livros = cur.fetchall()
        livros_list = []
        for livro in livros:
            livros_list.append({
                'id_livro': livro[0]
                , 'titulo': livro[1]
                , 'autor': livro[2]
                , 'ano_publicacao': livro[3]
            })
        return jsonify(mensagem='lista de livros', livros=livros_list)
    except Exception as e:
        return jsonify(mensagem=f"Erro ao consultar banco de dados: {e}"), 500
    finally:
        cur.close()


@app.route('/criar_livro', methods=['POST'])
def criar_livro():
    dados = request.get_json()

    titulo = dados.get('titulo')
    autor = dados.get('autor')
    ano_publicacao = dados.get('ano_publicacao')
    try:
        cur = con.cursor()
        cur.execute("select 1 from livro where titulo = ?", (titulo,))
        if cur.fetchone():
            return jsonify({"erro": "livro ja existe"}), 400
        cur.execute("""INSERT INTO livro (titulo, autor, ano_publicacao) values (?, ?, ?)""", (titulo, autor, ano_publicacao))
        con.commit()
        return jsonify({
            'mensagem': "Livro cadastrado com sucesso!",
            'livro': {
                'titulo': titulo,
                'autor': autor,
                'ano_publicacao': ano_publicacao
            }
        }), 201
    except Exception as e:
        return jsonify(mensagem=f"Erro ao cadastrar livro: {e}"), 500
    finally:
        cur.close()
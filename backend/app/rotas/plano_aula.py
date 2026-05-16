from flask import Blueprint, request, jsonify
from ..models import db, PlanoAula, Tag
from datetime import date
from sqlalchemy import asc, desc
 
plano_aula_bp = Blueprint('plano_aula', __name__)

#funcao para nao repitir tags
def converter_data(valor):
    if not valor:
        return None
    try:
        return date.fromisoformat(str(valor))
    except(ValueError, TypeError):
        return None
    
def get_or_create_tag(nome_tag):
    nome = nome_tag.strip().lower()
    with db.session.no_autoflush:
        tag = Tag.query.filter_by(nome=nome).first()
        if not tag:
            tag = Tag(nome=nome)
            db.session.add(tag)
        return tag

#CRIAR
@plano_aula_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json()

    if not dados or not dados.get('titulo') or not dados.get('disciplina'):
        return jsonify({"erro": "titulo e disciplina são obrigatórios"}), 400
    
    try:
        novo = PlanoAula(
            titulo = dados['titulo'],
            disciplina = dados['disciplina'],
            objetivo = dados.get('objetivo', ''),
            ementa = dados.get('ementa',''),
            conteudos = dados.get('conteudos',''),
            recursos = dados.get('recursos',''),
            data_prevista = converter_data(dados.get('data_prevista')) 
        )

        for t in dados.get('tags', []):
            novo.tags.append(get_or_create_tag(t))
        
        db.session.add(novo)
        db.session.commit()
        return jsonify(novo.to_dict()), 201
    
    except Exception as e:
        db.session.rollback() #se algo der errado, ele cancela tudo
        print("ERRO AO SALVAR:")
        print(str(e))
        return jsonify({"erro": str(e)}), 400
    
#LISTAR
@plano_aula_bp.route('', methods=['GET'])
def listar():
    disciplina = request.args.get('disciplina')
    tag = request.args.get('tag')
    busca = request.args.get('busca')
    data_prevista = request.args.get('data_prevista')       
    order_by = request.args.get('order_by', 'data_criacao') 
    order_dir = request.args.get('order_dir', 'desc')        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = PlanoAula.query

    #filtros
    if disciplina:
        query = query.filter(PlanoAula.disciplina.ilike(f'%{disciplina}%'))
    if busca:
        query = query.filter(PlanoAula.titulo.ilike(f'%{busca}%'))
    if tag:
        query = query.join(PlanoAula.tags).filter(Tag.nome.ilike(f'%{tag}%'))
    if data_prevista:
        data_convertida = converter_data(data_prevista)
        query = query.filter(PlanoAula.data_prevista == data_convertida)
    
    #ordenar
    colunas_permitidas ={
        'titulo':PlanoAula.titulo,
        'data_criacao': PlanoAula.data_criacao,
        'data_prevista': PlanoAula.data_prevista,
    }
    coluna = colunas_permitidas.get(order_by, PlanoAula.data_criacao)
    ordem = asc(coluna) if order_dir == 'asc' else desc(coluna)
    query = query.order_by(ordem)

    paginado = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "dados": [p.to_dict() for p in paginado.items],
        "total": paginado.total,
        "pagina": paginado.page,
        "total_paginas": paginado.pages
    }), 200

#BUSCAR
@plano_aula_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    plano = PlanoAula.query.get_or_404(id)
    return jsonify(plano.to_dict()),200

#EDITAR
@plano_aula_bp.route('/<int:id>', methods=['PUT'])
def editar(id):
    plano = PlanoAula.query.get_or_404(id)
    dados = request.json

    plano.titulo = dados.get('titulo', plano.titulo)
    plano.disciplina =  dados.get('disciplina', plano.disciplina)
    plano.objetivo = dados.get('objetivo', plano.objetivo)
    plano.ementa = dados.get('ementa',plano.ementa)
    plano.conteudos = dados.get('conteudos', plano.conteudos)
    plano.recursos = dados.get('recursos', plano.recursos)
    plano.data_prevista = converter_data(dados.get('data_prevista'))

    if 'tags' in dados:
        plano.tags = []
        for t in dados['tags']:
            plano.tags.append(get_or_create_tag(t))
    db.session.commit()
    return jsonify(plano.to_dict()), 200

#DELETAR

@plano_aula_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    plano = PlanoAula.query.get_or_404(id)
    db.session.delete(plano)
    db.session.commit()
    return '', 204

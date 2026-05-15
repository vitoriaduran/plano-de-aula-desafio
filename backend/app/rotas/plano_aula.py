
from flask import Blueprint, request, jsonify
from ..models import db, PlanoAula, Tag

plano_aula_bp = Blueprint('plano_aula', __name__)

#funcao para nao repitir tags

def get_or_create_tag(nome_tag):
    nome = nome_tag.strip().lower()
    tag = Tag.query.filter_by(nome=nome).first()
    if not tag:
        tag = Tag(nome=nome)
        db.session.add(tag)
    return tag

#CRIAR
@plano_aula_bp.route('', methods=['POST'])
def criar():
    dados = request.json
    try:
        novo = PlanoAula(
            titulo = dados['titulo'],
            disciplina = dados['disciplina'],
            objetivo = dados.get('objetivo', ''),
            ementa = dados.get('ementa',''),
            conteudos = dados.get('conteudos',''),
            recursos = dados.get('recursos',''),
            data_prevista = dados.get('data_prevista','')
        )

        for t in dados.get('tags', []):
            novo.tags.append(get_or_create_tag(t))
        
        db.session.add(novo)
        db.session.commit()
        return jsonify(novo.to_dict()), 201
    
    except Exception as e:
        db.session.rollback() #se algo der errado, ele cancela tudo
        return jsonify({"erro": str(e)}), 400
    
#LISTAR
@plano_aula_bp.route('', methods=['GET'])
def listar():
    planos = PlanoAula.query.all()
    return jsonify([p.to_dict() for p in planos]), 200

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
    plano.conteudos = dados.get('conteudo', plano.conteudos)
    plano.recursos = dados.get('recursos', plano.recursos)
    plano.data_prevista = dados.get('data_prevista', plano.data_prevista)

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
    return jsonify({"mensagem":"Removido com sucesso"}), 200

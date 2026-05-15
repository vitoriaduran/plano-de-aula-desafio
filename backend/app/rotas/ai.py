from flask import Blueprint,request, jsonify
from ..servicos.ia_servicos import IAServico

ai_bp = Blueprint('ai', __name__)
ia_servico = IAServico()

@ai_bp.route('/gerar', methods=['POST'])
def gerar():
    dados = request.get_json()
    titulo = dados.get('titulo')
    disciplina = dados.get('disciplina')
    ementa = dados.get('ementa', '')

    if not titulo or not disciplina:
        return jsonify({"erro": "Titulo e disciplina são necessários"})
    
    resultado = ia_servico.gerar_sugestao_aula(titulo, disciplina, ementa)
    return jsonify({"sugestao": resultado}), 200
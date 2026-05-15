#teste
from flask import Blueprint, request, jsonify
from ..models import db, PlanoAula, Tag

plano_aula_bp = Blueprint('plano_aula', __name__)

@plano_aula_bp.route('/teste', methods=['GET'])
def teste():
    return jsonify({"mensagem": "Rodando!"})
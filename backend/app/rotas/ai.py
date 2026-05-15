#teste

from flask import Blueprint, jsonify

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/teste', methods=['GET'])
def teste_ai():
    return jsonify({"mensagem": "IA offline por enquanto"})
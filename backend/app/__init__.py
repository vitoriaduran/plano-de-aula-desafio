from flask import Flask
from flask_cors import CORS
from .models import db
from .rotas import plano_aula_bp
from .rotas.ai import ai_bp

def crate_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)

    #registrar as rotas blueprint
    app.register_blueprint(plano_aula_bp, url_prefix='/api/planos')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    return app
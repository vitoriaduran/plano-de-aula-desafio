from flask import Flask, render_template, jsonify
from flask_cors import CORS
from .models import db
from .rotas import plano_aula_bp
from .rotas.ai import ai_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)

    #registrar as rotas blueprint
    app.register_blueprint(plano_aula_bp, url_prefix='/api')
    app.register_blueprint(ai_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return render_template('index.html')
    

    #health check 
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "planoedu-api"}), 200

    with app.app_context():
        db.create_all()

    return app

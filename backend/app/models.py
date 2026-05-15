from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#tabela de ligaçao
plano_tags = db.Table('planos_tags', db.Column('plano_id', db.Integer, db.ForeignKey('plano_aula.id'), primary_key = True),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'),primary_key  = True ))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

class PlanoAula(db.Model):
    __tablename__ = 'plano_aula'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable = False)
    disciplina = db.Column(db.String(50), nullable = False)
    objetivo = db.Column(db.Text, nullable = False)
    ementa = db.Column(db.Text, nullable = False)
    conteudos = db.Column(db.Text)
    recursos = db.Column(db.Text)
    data_prevista = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    #cria a conexao entre as tabelas
    tags = db.relationship('Tag', secondary=plano_tags, backref=db.backref('planos', lazy='dynamic'))

    #método de conversao json
    def to_dict(self):
        return{
            "id": self.id,
            "titulo": self.titulo,
            "disciplina": self.disciplina,
            "objetivo": self.objetivo,
            "ementa": self.ementa,
            "conteudos": self.conteudos,
            "recursos": self.conteudos,
            "data_prevista": self.data_prevista,
            "tags":[t.nome for t in self.tags]
        }
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seubanco.db'  # Nome do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Importando as rotas após a criação da aplicação e db
from app import routes

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import User

# Página principal
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza a página index.html

# Registro de novo usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Verificando se o usuário já existe
        user = User.query.filter_by(email=email).first()
        if user:
            return "Usuário já existe!", 400
        
        # Criando um novo usuário
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))  # Redireciona para a página de login
    
    return render_template('register.html')  # Renderiza a página de registro

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verificando se o usuário existe
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return "Login bem-sucedido!", 200  # Caso o login seja bem-sucedido
        else:
            return "Credenciais inválidas!", 400  # Caso as credenciais sejam inválidas
    
    return render_template('login.html')  # Renderiza a página de login

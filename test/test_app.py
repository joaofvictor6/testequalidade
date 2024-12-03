import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    # Criar uma instância do aplicativo para o teste
    app = create_app()
    
    # Configuração do banco de dados para testes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Estabelecer o contexto de aplicativo para criar as tabelas e usar o banco de dados
    with app.app_context():
        db.create_all()  # Criação do banco de dados para testes
    
    # Criar e retornar o cliente de teste
    with app.test_client() as client:
        yield client
    
    # Limpeza após os testes
    with app.app_context():
        db.drop_all()  # Remover as tabelas após os testes

def test_register(client):
    # Teste de cadastro de usuário
    response = client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 302  # Espera um redirecionamento após o cadastro bem-sucedido

    # Verificando se o usuário foi realmente criado no banco
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None  # Usuário deve ser encontrado no banco

def test_register_duplicate_email(client):
    # Teste de cadastro com e-mail duplicado
    client.post('/register', data={'name': 'Test User 1', 'email': 'test@example.com', 'password': 'password'})
    response = client.post('/register', data={'name': 'Test User 2', 'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 400  # Espera erro 400 para e-mail duplicado

def test_register_short_password(client):
    # Teste de cadastro com senha curta (menor que 8 caracteres)
    response = client.post('/register', data={'name': 'Test User', 'email': 'shortpass@example.com', 'password': 'short'})
    assert response.status_code == 400  # Espera erro 400 devido à senha curta

def test_login(client):
    # Teste de login bem-sucedido
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'})
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200  # Espera resposta 200 para login bem-sucedido

def test_login_invalid_credentials(client):
    # Teste de login com credenciais inválidas
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'password'})
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 400  # Espera erro 400 para credenciais inválidas

def test_login_non_existent_user(client):
    # Teste de login com e-mail não cadastrado
    response = client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'password'})
    assert response.status_code == 400  # Espera erro 400 para usuário não encontrado

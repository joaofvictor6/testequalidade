from app import app, db

# Cria as tabelas no banco de dados automaticamente
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

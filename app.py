from flask import Flask, render_template, redirect, url_for
from database import db
import os #Biblioteca para ler arquivos como se fosse um "Sistema Operacional".
from flask_migrate import Migrate
from usuario import Usuario


app = Flask(__name__)
#implementando "senha". Necessário para banco de dados; {
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#}

#Importando os dados do falskenv(Arquivo privado){ 
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
mydb = os.getenv("DB_DATABASE")
#}

#Criando a conexão o caminho da conexão com o banco de dados {
conexao = f"mysql+pymysql://{username}:{password}@{host}/{mydb}"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao
db.init_app(app)
migrate = Migrate(app, db)
#}

#rotas {
@app.route("/") #Página raíz.
def inicio():
    return render_template("inicio.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/buscar")
def buscar():
    return render_template("buscar.html")

@app.route("/cadastrar-se")
def cadastrar_usuario():
    #add_new_user() ESSA FUNÇÃO ADICIONA O USUARIO. DA MANEIRA COMO ESTÁ ELE APENAS ADICIONA O USUARIO QUANDO A PÁGINA É EXIBIDA.
    return render_template("cadastro_usuario.html")

#Função de cadastrar usuario no banco de dados. {}
def add_new_user():
    novo_usuario = Usuario("Usuario de teste", "email@teste.com","Senha#123")
    db.session.add(novo_usuario)
    db.session.commit()
    return("Usuário cadastrado com sucesso!")
#}

@app.route("/cadastrar-animal")
def cadastrar_animal():
    return render_template("cadastro_animal.html")
#}
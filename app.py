from flask import Flask, render_template, redirect, url_for
from database import db
import os #Biblioteca para ler arquivos como se fosse um "Sistema Operacional".

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
#}

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
    return render_template("cadastro_usuario.html")

@app.route("/cadastrar-animal")
def cadastrar_animal():
    return render_template("cadastro_animal.html")
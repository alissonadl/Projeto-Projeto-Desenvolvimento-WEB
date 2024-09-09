from flask import Flask, request, render_template, redirect, url_for
from database import db
import os #Biblioteca para ler arquivos como se fosse um "Sistema Operacional".
from flask_migrate import Migrate
from usuario import Usuario
from animal import Animal
from models.diario import Diario
from controllers.diario import bp_diario

app = Flask(__name__) #BluePrints
app.register_blueprint(bp_diario,url_prefix = "/diario")
#}

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

@app.route("/cadastro-animal")
def cadastrar_animal():
    return render_template("cadastro_animal.html")

@app.route("/cadastro-usuario")
def cadastrar_usuario():
    return render_template("cadastro_usuario.html")

#Função de cadastrar usuario no banco de dados. {
#IMPORTANTE: ISSO SERIA O "C" DO C.R.U.D. Ou seja, Create.
@app.route("/efetuar_cadastro", methods=["POST"])
def add_new_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    """
    if not username or not email or not password:
        return "Todos os campos são obrigatórios!"

    if password != confirm_password:
        return "Senhas não coincidem!" """
    
        #ADICIONAR OS CAMPOS ACIMA COMO UM POP-UP/MENSAGEM NA TELA, SEM REDIRECINAR
    
    new_user = Usuario(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/cadastro_confirmado")

    #Se essa função der erro ao executar, é porque já tem um usuário criado igual. Acesse a rota /teste_delete e tente novamente esta.
#}

#Função para cadastrar animal
@app.route("/efetuar_cadastro_animal", methods=["POST"])
def add_new_animal():
    animalname = request.form.get("animalname")
    animallocalization = request.form.get("animallocalization")
    animaltype = request.form.get("animaltype")

    new_animal = Animal(animalname = animalname, animallocalization = animallocalization, animaltype = animaltype)
    db.session.add(new_animal)
    db.session.commit()
    return redirect("/cadastro_animal_confirmado")

#Função para receber/recuprar dados do banco. {
#IMPORTANTE: ISSO SERIA O "R" DO C.R.U.D. Ou seja, Recovery
@app.route("/teste_recovery")
def recovery_user():
    user = Usuario.query.get("email@teste.com")#Precisa informar a primary key da tupla. Isso recebe os dados da tupla para essa variável.
    teste_msg = f"{user.username}, {user.email}"
    return teste_msg
#}

#Função para atualizar informações do banco. {
#IMPORTANTE: ISSO SERIA O "U" DO C.R.U.D. Ou seja, Update
@app.route("/teste_update")
def update_user():
    user = Usuario.query.get("email@teste.com")#Precisa informar a primary key da tupla. Isso recebe os dados da tupla para essa variável.
    user.username = "Update Sucessful"
    db.session.add(user) #Adiciona as informações atualizadas no banco
    db.session.commit() #Dá commit no banco, efetivando as modificações
    teste_msg = f"{user.username}, {user.email}"
    return teste_msg
#}

#Função para deletar informações do banco. {
#IMPORTANTE: ISSO SERIA O "D" DO C.R.U.D. Ou seja, Delete
@app.route("/teste_delete")
def user_delete():
    user = Usuario.query.get("Alisson")#Precisa informar a primary key da tupla. Isso recebe os dados da tupla para essa variável.
    db.session.delete(user) #Remove a tupla do banco
    db.session.commit() #Dá commit no banco, efetivando as modificações
    teste_msg = Usuario.query.all()
    return teste_msg
#}

@app.route("/cadastro_confirmado")
def cadastro_confirmado():
    return render_template("cadastro_confirmado.html")

@app.route("/cadastro_animal_confirmado")
def cadastro_animal_confirmado():
    return render_template("cadastro_animal_confirmado.html")
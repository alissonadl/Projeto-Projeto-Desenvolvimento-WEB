from flask import Flask, request, render_template, redirect, url_for, flash
from utilidades import db, lm #Importando bando de dados e login manager.
import os #Biblioteca para ler arquivos como se fosse um "Sistema Operacional".
from flask_migrate import Migrate
from models.usuarios import Usuario
from models.animais import Animal
from controllers.diario import bp_diario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__) #BluePrints{
app.register_blueprint(bp_diario,url_prefix = "/diario")
#}

#implementando "senha". Necessário para banco de dados; {
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#}

#"Importando" os dados do falskenv(Arquivo privado){ 
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
mydb = os.getenv("DB_DATABASE")
#}

#Criando a conexão o caminho da conexão com o banco de dados {
conexao = f"mysql+pymysql://{username}:{password}@{host}/{mydb}"
app.config["SQLALCHEMY_DATABASE_URI"] = conexao
db.init_app(app) #Sinalizando que o banco será gerenciado pelo app.
lm.init_app(app) #Sinalizando que o login manager será gerenciado pelo app.
migrate = Migrate(app, db)
#}

#TESTE {
@lm.user_loader
def load_user(username):
    return Usuario.query.filter_by(username=username).first()
#}

#rotas
@app.route("/") #Página raíz.
def inicio():
    return render_template("inicio.html")

@app.route("/inicio_logado")
@login_required
def inicio_logado():
    return render_template("inicio_logado.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verificar se o usuário existe no banco de dados
        user = Usuario.query.filter_by(username=username).first()

        if user and (user.password, password):
            login_user(user)

            return redirect(url_for("inicio_logado"))
        else:
            return ("Dados incorretos, tente novamente.")

    return render_template("login.html")

#Função de logout/logoff {
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
#}

#Pagina do error 401 (Não autorizado, login não feito){
@app.errorhandler(401)
def erro401(error):
    return render_template('erro401.html'), 401
#}

@app.route("/buscar")
@login_required
def buscar():
    animais = Animal.query.all()
    return render_template('buscar.html', animais=animais)

@app.route("/cadastro-usuario")
def cadastrar_usuario():
    return render_template("cadastro_usuario.html")

@app.route("/cadastro_usuario_confirmado")
def cadastro_confirmado():
    return render_template("cadastro_usuario_confirmado.html")

@app.route("/cadastro-animal")
@login_required
def cadastrar_animal():
    return render_template("cadastro_animal.html")

@app.route("/cadastro_animal_confirmado")
@login_required
def cadastro_animal_confirmado():
    return render_template("cadastro_animal_confirmado.html")

#Função de cadastrar usuario no banco de dados. {
#IMPORTANTE: ISSO SERIA O "C" DO C.R.U.D. Ou seja, Create.
@app.route("/efetuar_cadastro_usuario", methods=["POST"])
def add_new_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if(password == confirm_password):
        new_user = Usuario(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit() 
        return redirect("/cadastro_usuario_confirmado")
    else:
        return render_template("falha_cadastro.html")

    #Se essa função der erro ao executar, é porque já tem um usuário criado igual. Acesse a rota /teste_delete e tente novamente esta.
#}

#Função para cadastrar animal
@app.route("/efetuar_cadastro_animal", methods=["POST"])
@login_required
def add_new_animal():
    animalname = request.form.get("animalname")
    animallocalization = request.form.get("animallocalization")
    animaltype = request.form.get("animaltype")

    new_animal = Animal(animalname = animalname, animallocalization = animallocalization, animaltype = animaltype)
    db.session.add(new_animal)
    db.session.commit()
    return redirect("/cadastro_animal_confirmado")

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

#Função para receber/recuprar dados do banco. {
#IMPORTANTE: ISSO SERIA O "R" DO C.R.U.D. Ou seja, Recovery
@app.route("/alterar_senha", methods=["GET", "POST"])
@login_required
def alterar_senha():
    if request.method == "POST":
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = Usuario.query.get(current_user.username) #Busca o usuário atual no banco de dados
        
        if user and user.password == current_password:
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                msg = ("Senha alterada com sucesso!")
                return render_template("aviso_alterar_senha.html", msg = msg)
            else:
                msg = ("A nova senha e a confirmação não coincidem!")
                return render_template("aviso_alterar_senha.html", msg = msg)
        else:
            msg = ("Senha atual incorreta!")
            return render_template("aviso_alterar_senha.html", msg = msg)

    return render_template("alterar_senha.html")

#Função para deletar informações do banco. {
#IMPORTANTE: ISSO SERIA O "D" DO C.R.U.D. Ou seja, Delete
@app.route("/excluir_animal/<string:animalname>")
@login_required
def excluir_animal(animalname):
    animal = Animal.query.get(animalname)
    if animal:
        db.session.delete(animal)
        db.session.commit()
        flash('Animal excluído com sucesso!')
    else:
        flash('Animal não encontrado!')
    return redirect(url_for('buscar'))
#}
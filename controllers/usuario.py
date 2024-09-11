from flask import render_template, request, redirect, flash, url_for
from utilidades import db, lm
from models.usuarios import Usuario
from flask import Blueprint
from flask_login import login_user

bp_usuario = Blueprint("usuario", __name__, template_folder='templates')

@bp_usuario.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=="GET":
        return render_template('usuario_create.html')

    if request.method=="POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        u = Usuario(nome, email, senha)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('usuario.recovery'))
    
@lm.user_loader
def load_user(id):
    usuario = Usuario.query.get(id)
    return usuario

@bp_usuario.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form['email'] 
    senha = request.form['senha']
    usuario = Usuario.query.filter_by(email=email).first()

    print(usuario)
    if (usuario and usuario.senha == senha):
        login_user(usuario)
        return redirect('recovery')
    else:
        flash('Login ou senha incorretos')
        return redirect('/login')
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
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

#Rotas de cadastrar novo animal e listar animais já cadastrados.
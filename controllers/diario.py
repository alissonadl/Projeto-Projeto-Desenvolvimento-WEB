from flask import render_template, request, redirect, flash
from utilidades import db, lm
from flask import Blueprint #permite criar rotas neste arquivo aparte, fora do app.py

bp_diario = Blueprint("diario", __name__, template_folder='templates')


@lm.user_loader
def load_user(username):
    usuario = Usuario.query.get(username)

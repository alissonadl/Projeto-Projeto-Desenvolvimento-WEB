from flask import render_template, request, redirect, flash
from database import db
from models.diario import Diario
from flask import Blueprint #permite criar rotas neste arquivo aparte, fora do app.py

bp_diario = Blueprint("diario", __name__, template_folder='templates')

@bp_diario.route('/recovery')
def recovery():
    dados = Diario.query.all()
    return render_template('diario_recovery.html',dados=dados)

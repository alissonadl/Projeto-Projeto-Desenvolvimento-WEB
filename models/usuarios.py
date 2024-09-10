from utilidades import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__="usuarios"
    username = db.Column(db.String(35),primary_key = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

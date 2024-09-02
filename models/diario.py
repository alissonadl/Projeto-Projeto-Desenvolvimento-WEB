from database import db # É necessário importar a variável DB.

class Diario(db.Model):
  __tablename__= "diario"
  id = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.String(100))
  disciplina = db.Column(db.String(100))

  def __init__(self, titulo, disciplina):
    self.titulo = titulo
    self.disciplina = disciplina
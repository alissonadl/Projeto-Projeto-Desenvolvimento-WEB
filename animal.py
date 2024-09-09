from database import db

class Animal(db.Model):
    __tablename__="animais"
    animalname = db.Column(db.String(35),primary_key = True)
    animallocalization = db.Column(db.String(50))
    animaltype = db.Column(db.String(8))

    def __init__(self, animalname, animallocalization, animaltype):
        self.animalname = animalname
        self.animallocalization = animallocalization
        self.animaltype = animaltype
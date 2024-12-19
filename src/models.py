from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Persons(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet": self.planet_id,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    persons = db.relationship('Persons', backref=('planet'))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "persons": [person.serialize() for person in self.persons] if self.persons else None
        }   


class Favourites(db.Model):
    __tablename__ = 'favourites'
    id = db.Column(db.Integer, primary_key=True)
    base_type = db.Column(db.String(250), nullable=False)
    base_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
         return '<Favourites base_type=%r base_id=%r>' % (self.base_type, self.base_id)

    def serialize(self):
        return {
            "id": db.self.id,
            "base_type": db.self.base_type,
            "base_id": db.self.base_id
    }
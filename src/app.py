"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Persons, Planets, Favourite_persons, Users
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# gets de cada tabla

@app.route('/persons', methods=['GET'])
def get_persons():
    data = Persons.query.all()
    data = [person.serialize() for person in data]
    return jsonify({"msg": "OK", "data": data}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    data = Planets.query.all()
    data = [planet.serialize() for planet in data]
    return jsonify({"msg": "OK", "data": data}), 200

@app.route('/favourites_person', methods=['GET'])
def get_favs():
    data = Favourite_persons.query.all()
    data = [fav.serialize() for fav in data]
    return jsonify({"msg": "OK", "data": data}), 200

# gets de cada tabla por id

@app.route('/persons/<int:id>', methods=['GET'])
def one_person(id):
    data = Persons.query.get(id)
    return jsonify({"msg": "one person with id: " + str(id), "person": data.serialize()})

@app.route('/planets/<int:id>', methods=['GET'])
def one_planet(id):
    data = Planets.query.get(id)
    return jsonify({"msg": "one planet with id: " + str(id), "person": data.serialize()})

@app.route('/favourites_person/<int:id>', methods=['GET'])
def one_fav_person(id):
    data = Favourite_persons.query.get(id)
    return jsonify({"msg": "one person with id: " + str(id), "person": data.serialize()})

# post de cada tabla por 

@app.route('/persons', methods=['POST'])
def create_person():
    
    name = request.json.get('name', None)
    planet_id = request.json.get('planet_id', None)
    if not name or not planet_id:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400 
    check = Persons.query.filter_by(name=name).first()
    if check:
        return jsonify({"msg": 'este personaje ya existe'}), 400

    new_person = Persons(name=name, planet_id=planet_id)
    db.session.add(new_person)
    db.session.commit()

    return jsonify({"msg": "OK", "data": new_person.serialize()}), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    
    name = request.json.get('name', None)
    if not name:
        return jsonify({"msg": 'el nombre es necesario'}), 400 
    check = Planets.query.filter_by(name=name).first()
    if check:
        return jsonify({"msg": 'este planeta ya existe'}), 400

    new_planet = Planets(name=name)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "OK", "data": new_planet.serialize()}), 200


@app.route('/favourites_person', methods=['POST'])
def create_fav_person():
    
    user_id = request.json.get('user_id', None)
    person_id = request.json.get('person_id', None)

    exists = Favourite_persons.query.filter_by(user_id= user_id, person_id=person_id).first()
    if exists: 
        return jsonify({"msg": "este personaje ya es favorito de este user"}), 400

    user_exists = Users.query.filter_by(id=user_id).first()
    if not user_exists: 
        return jsonify({"msg": "este usuario no existe"}), 400

    person_exists = Persons.query.filter_by(id=person_id).first()
    if not person_exists: 
        return jsonify({"msg": "este personaje no existe"}), 400
    
    new_fav_person = Favourite_persons(user_id= user_id, person_id=person_id)

    db.session.add(new_fav_person)
    db.session.commit()

    return jsonify({"msg": "OK", "data": new_fav_person.serialize()}), 200

# delete de cada tabla por id

@app.route('/persons/<int:id>', methods=['DELETE'])
def delete_person(id):
    data = Persons.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return jsonify({"msg": "person deleted with id" + str(id)}), 200

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    data = Planets.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return jsonify({"msg": "planet deleted with id: " + str(id)}), 200

@app.route('/favourites_person/<int:id>', methods=['DELETE'])
def delete_fav_person(id):
    data = Favourite_persons.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return jsonify({"msg": "planet deleted with id: " + str(id)}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

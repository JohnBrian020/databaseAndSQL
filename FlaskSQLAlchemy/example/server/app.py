from flask import Flask, jsonify
from flask_migrate import Migrate
from server.models import db, Pet

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return jsonify({"message": "Pet Management API is running"})


@app.route("/pets")
def get_pets():
    pets = Pet.query.all()
    return jsonify([
        {"id": pet.id, "name": pet.name, "species": pet.species}
        for pet in pets
    ])

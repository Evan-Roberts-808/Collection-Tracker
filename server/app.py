#!/usr/bin/env python3

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite://{os.path.join(BASE_DIR, 'instance/card_tracker.db')}"
# )

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, Set, Card
import json
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance/card_tracker.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Sets(Resource):

    def get(self):
        try:
            sets_data = [set.to_dict(only=('id', 'name', 'icon_url', 'description')) for set in Set.query.all()]
            response_data = json.dumps(sets_data)
            return make_response(response_data, 200)
        except:
            return {"error": "404 Sets not found"}, 404

api.add_resource(Sets, "/sets")

class SetById(Resource):
    def get(self, id):
        try:
            set = Set.query.filter_by(id=id).first()
            if set:
                set_data = set.to_dict()
                response_data = json.dumps(set_data)  # Serialize OrderedDict to JSON
                return make_response(response_data, 200)
            else:
                return make_response({"error": "404 Set not found"}, 404)
        except:
            return make_response({"error": "500 Internal Server Error"}, 500)


api.add_resource(SetById, "/sets/<int:id>")

class Cards(Resource):

    def get(self):
        try:
            cards_data = [card.to_dict() for card in Card.query.all()]
            response_data = json.dumps(cards_data)
            return make_response(response_data, 200)
        except:
            return {"error": "404 Cards not found"}, 404

api.add_resource(Cards, "/cards")

class CardsById(Resource):

    def get(self, id):
        try:
            card = Card.query.filter_by(id=id).first()
            if card:
                card_data = card.to_dict()
                response_data = json.dumps(card_data)
                return make_response(response_data, 200)
            else:
                return make_response({"error": "404 card not found"}, 404)
        except:
            return make_response({"error": "500 Internal Server Error"}, 500)

api.add_resource(CardsById, '/cards/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
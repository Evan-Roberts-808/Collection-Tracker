#!/usr/bin/env python3
import datetime
import json
from models import db, Set, Card, User, Collection
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite://{os.path.join(BASE_DIR, 'instance/card_tracker.db')}"
# )

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASE_DIR, "instance/card_tracker.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

api = Api(app)

app.secret_key = secrets.token_hex(16)  # Set the secret key

class Sets(Resource):

    def get(self):
        try:
            sets_data = [set.to_dict(only=(
                'id', 'name', 'icon_url', 'description', 'set_img')) for set in Set.query.all()]
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
                # Serialize OrderedDict to JSON
                response_data = json.dumps(set_data)
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

# User Sign Up route
@app.route('/signup', methods=['POST'])
def signup():
    name = request.json.get('name')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # Validate if the required fields are present
    if not name or not username or not email or not password:
        return make_response({"error": "Missing required fields"}, 400)

    # Check if the username or email already exists
    if User.query.filter_by(username=username).first() is not None:
        return make_response({"error": "Username already exists"}, 409)
    if User.query.filter_by(email=email).first() is not None:
        return make_response({"error": "Email already exists"}, 409)

    # Hash the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    user = User(name=name, username=username, email=email, password_hash=password_hash)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response({"error": "Database error"}, 500)

    return make_response({"message": "User created successfully"}, 201)

# User Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Validate if the required fields are present
    if not username or not password:
        return make_response({"error": "Missing required fields"}, 400)

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response({"error": "Invalid username or password"}, 401)

    # Check if the password is correct
    if not bcrypt.check_password_hash(user.password_hash, password):
        return make_response({"error": "Invalid username or password"}, 401)

    # Log in the user
    login_user(user)

    return make_response({"message": "Login successful"}, 200)

# User Logout route
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return make_response({"message": "Logout successful"}, 200)

# User Profile route
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user_data = {
        'id': current_user.id,
        'name': current_user.name,
        'username': current_user.username,
        'email': current_user.email
    }
    response_data = json.dumps(user_data)
    return make_response(response_data, 200)

# User Collection route
@app.route('/collection', methods=['GET'])
@login_required
def collection():
    collection_data = [card.to_dict() for card in current_user.collections]
    response_data = json.dumps(collection_data)
    return make_response(response_data, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

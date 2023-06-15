from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Set(db.Model, SerializerMixin):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    icon_url = db.Column(db.String())
    editions = db.Column(db.String())
    cards = db.relationship('Card', backref='set', lazy=True)

    def __repr__(self):
        return f'<Set {self.name}>'
    
class Card(db.Model, SerializerMixin):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String())
    position = db.Column(db.String())
    element = db.Column(db.String())
    rune_type = db.Column(db.String())
    effect = db.Column(db.Text())
    artist = db.Column(db.String())
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.name}>'
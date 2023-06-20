from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from collections import OrderedDict

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Set(db.Model, SerializerMixin):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    set_img = db.Column(db.String())
    icon_url = db.Column(db.String())
    description = db.Column(db.String())
    cards = db.relationship('Card', back_populates='set')

    def __repr__(self):
        return f'<Set {self.name}>'
    
    def to_dict(self, only=None):
        if only:
            data = OrderedDict([
                ('id', self.id),
                ('name', self.name),
                ('description', self.description),
                ('icon_url', self.icon_url)
            ])
            for field in only:
                if field == 'cards':
                    data[field] = [card.to_dict() for card in self.cards]
                elif hasattr(self, field):
                    data[field] = getattr(self, field)
        else:
            data = OrderedDict([
                ('id', self.id),
                ('name', self.name),
                ('description', self.description),
                ('icon_url', self.icon_url),
                ('cards', [card.to_dict() for card in self.cards])
            ])
        return data
    
class Card(db.Model, SerializerMixin):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String())
    position = db.Column(db.String())
    element = db.Column(db.String())
    rune_type = db.Column(db.String())
    subclass1 = db.Column(db.String())
    subclass2 = db.Column(db.String())
    attack_defense = db.Column(db.String())
    description = db.Column(db.Text())
    rarity = db.Column(db.String())
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'), nullable=False)
    set = db.relationship('Set', back_populates='cards')

    serialize_rules = ("-cards.set", '-set')

    def __repr__(self):
        return f'<Card {self.name}>'
    
    def to_dict(self):
        return OrderedDict([
            ('id', self.id),
            ('name', self.name),
            ('description', self.description),
            ('image_url', self.image_url),
            ('element', self.element),
            ('rune_type', self.rune_type),
            ('subclass1', self.subclass1),
            ('subclass2', self.subclass2),
            ('attack_defense', self.attack_defense),
            ('set_id', self.set_id),
            ('position', self.position),
            ('rarity', self.rarity)
        ])
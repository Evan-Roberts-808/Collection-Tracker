from app import app
from models import db, Set, Card
import pickle
import os
import ipdb

def clear_tables():
    db.session.query(Set).delete()
    db.session.query(Card).delete()
    db.session.commit()

def seed_data():
    data_dir = "data_backup"

    # Load sets data
    sets_file_path = os.path.join(data_dir, "set_backup.pkl")
    with open(sets_file_path, "rb") as sets_file:
        sets_data = pickle.load(sets_file)

    # Load cards data
    cards_file_path = os.path.join(data_dir, "card_backup.pkl")
    with open(cards_file_path, "rb") as cards_file:
        cards_data = pickle.load(cards_file)

    # Clear tables
    clear_tables()

    # Seed sets table
    for set_data in sets_data:
        set = Set(**set_data)
        db.session.add(set)

    # Seed cards table
    for card_data in cards_data:
        card = Card(**card_data)
        db.session.add(card)

    db.session.commit()

def update_sets(id):
    set = Set.query.filter(Set.id == id).first()
    # What do you want to do
    db.session.add(set)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # update_sets()
        # seed_data()
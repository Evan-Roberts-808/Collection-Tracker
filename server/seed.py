from app import app
from models import db, Set, Card

set_data_list = [
    {
        'name': 'Base Set',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/BaseSet.png',
        'description': "The initial Elestrals trading card set featuring 125 cards. Prints include Founder, 1st Edition, and 2nd Edition."
    },
    {
        'name': 'Base Set Promo Cards',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/BaseSetPromoCards.png',
        'description': "Promo Cards released during the Base Set era (2023)"
    },
    {
        'name': 'Artist Collection',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/ArtistCollection.png',
        'description': "The Artist Collection is a Kickstarter exclusive set and starts with 10 Cards. All of these beautifully designed cards are made in our artist's distinct style!"
    },
    {
        'name': 'Centaurbor Starter Deck',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/CentaurborStarterDeck.png',
        'description': "Delve into the heart of the Foloi Forest, where dryads hold court for Demeter, Queen of the Harvest. Only the bravest and most cunning can discover the mystic potential of the Centaurbor Starter Deck! With Tectaurus and Equilynx as your guides, none can stand before your rock-solid resolve."
    },
    {
        'name': 'Trifernal Starter Deck',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/TrifernalStarterDeck.png',
        'description': "Kindle the flames of victory as you vanquish your foes in the heat of Volcanic Forge with the Trifernal Starter Deck! Scorch the battlefield with Eruption and a blazing cast of Elestrals including Volcaries, Leonite and Flarachne!"
    },
    {
        'name': 'Majesea Starter Deck',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/MajeseaStarterDeck.png',
        'description': "Command the endless power of the oceans and sink your opponents to the bottom of the sea with water’s might! From the deepest depths, the Majesea Starter Deck rises like a Tsunami to crash against the competition! Rediscover the glory of Atlantis as you ride the waves alongside Krakatuga and Capregal!"
    },
    {
        'name': 'Ohmperial Starter Deck',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/OhmperialStarterDeck.png',
        'description': "Thunder shakes the heavens and lightning splits the skies as an electrifying current strikes from the heights of Mount Olympus! Join forces with almighty Zeus and shocking allies such as Lycavolt, Cygnetric, and Boombatt to smite all who oppose you."
    },
    {
        'name': 'Penterror Starter Deck',
        'icon_url': 'https://raw.githubusercontent.com/evan-roberts-808/Collection-tracker/main/.github/images/sets/PenterrorStarterDeck.png',
        'description': "From howling gales and darkening skies, a tempest emerges! Soar into the heart of the storm on the triumphant wings of Exaltair, Fowlicane, and Glydesdale and blow away your rivals with the Penterror Starter Deck!"
    }
]

def seed_sets():
    for set_data in set_data_list:
        set_obj = Set(**set_data)
        db.session.add(set_obj)
    db.session.commit()
    print('seeding complete')

def clear_cards_table():
    with app.app_context():
        db.session.query(Card).delete()
        db.session.commit()

def update_value():
    pass

def new_set():
    set_obj = Set(
        name = "",
        icon_url = "",
        description = ""
    )
    db.session.add(set_obj)
    db.session.commit()

with app.app_context():
    db.create_all()
    # new_set()
    # clear_cards_table()
    # seed_sets()
    # update_value()
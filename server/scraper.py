from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from models import db, Card
from app import app
import os
import urllib.parse
import urllib.request
import ipdb
import base64
import requests


class Scraper:
    def __init__(self, chrome_driver_path, base_url):
        self.chrome_driver_path = chrome_driver_path
        self.base_url = base_url
        self.cards = []
        self.image_directory = ""
        self.script_directory = os.path.dirname(os.path.abspath(__file__))

    def get_page(self, url):
        options = Options()
        options.add_argument("--headless")
        service = Service(self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        return page_source

    def download_image(self, url, filename):
        filepath = os.path.join(self.script_directory,
                                self.image_directory, filename)
        response = requests.get(url)
        response.raise_for_status()

        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Image saved: {filename}")

    def get_cards(self, urls):

        # Define the image_directory variable
        image_directory = ""
        with app.app_context():
            base_raw_url = 'https://raw.githubusercontent.com/Evan-Roberts-808/Collection-Tracker/main/.github/images/cards/'
            for url in urls:
                try:
                    card_html = self.get_page(url)
                    soup = BeautifulSoup(card_html, 'html.parser')

                    # Title
                    try:
                        title = soup.find('h1').text.strip()
                    except AttributeError:
                        title = None

                    # Description
                    try:
                        description = soup.find(
                            'dd', class_='load-external-scripts image-post_description').p.text.strip()
                    except AttributeError:
                        description = None

                    # Element(s)
                    try:
                        element_title = soup.find(
                            'dt', string='Element(s):').find_next('img')['title']
                    except AttributeError:
                        element_title = None

                    # Subclass(es)
                    subclass1 = None
                    subclass2 = None
                    try:
                        subclass_container = soup.find(
                            'dt', string='Subclass(es):').find_next('dd')
                        subclass_imgs = subclass_container.find_all('img')
                        if subclass_imgs:
                            subclass1 = subclass_imgs[0]['title'].strip()
                        if len(subclass_imgs) > 1:
                            subclass2 = subclass_imgs[1]['title'].strip()
                    except AttributeError:
                        pass

                    # Attack / Defense
                    try:
                        attack_defense = soup.find(
                            'dt', string='Attack / Defense:').find_next('dd').text.strip()
                    except AttributeError:
                        attack_defense = None

                    # Set Name
                    try:
                        set_name = soup.find(
                            'dt', string='Set Name:').find_next('a').text.strip()
                    except AttributeError:
                        set_name = None

                    # Set #
                    try:
                        set_number = soup.find(
                            'dt', string='Set #:').find_next('dd').text.strip()
                    except AttributeError:
                        set_number = None

                    # Rarity
                    try:
                        rarity = soup.find('dt', string='Rarity:').find_next(
                            'dd').text.strip()
                    except AttributeError:
                        rarity = None

                    # Rune Type
                    try:
                        rune_type_element = soup.find(
                            'dt', string='Rune Type:')
                        if rune_type_element:
                            rune_type_img = rune_type_element.find_next('img')
                            rune_type = rune_type_img['title'].strip()
                        else:
                            rune_type = None
                    except AttributeError:
                        rune_type = None

                    # Image
                    try:
                        image_element = soup.select(
                            'div.relative.aspect-\\[\\.733\\] span img')[0]
                        image_url = image_element['src']
                        image_url = urllib.parse.unquote(
                            image_url).replace("amp;", "")
                        full_image_url = f"{self.base_url}{image_url}"

                        # Generate the image filename based on the card title
                        image_filename = set_number.replace(" ", "") + ".png"
                        image_path = os.path.join(
                            self.script_directory, self.image_directory, image_filename)

                        # Download and save the image
                        self.download_image(full_image_url, image_path)

                        # Create the raw GitHubusercontent URL
                        raw_image_url = f"{base_raw_url}{image_filename}"
                    except Exception as e:
                        raw_image_url = None
                        print(
                            f"An error occurred while processing URL: {url}\nError: {str(e)}")

                    # ...

                    card = Card(
                        name=title,
                        description=description,
                        element=element_title,
                        subclass1=subclass1,
                        subclass2=subclass2,
                        position=set_number,
                        attack_defense=attack_defense,
                        rarity=rarity,
                        rune_type=rune_type,
                        set_id=3,  # Set the set_id directly
                        image_url=raw_image_url  # Use the raw image URL
                    )

                    # Save the card to the database
                    db.session.add(card)
                    db.session.commit()

                    self.cards.append(card)

                except Exception as e:
                    print(
                        f"An error occurred while processing URL: {url}\nError: {str(e)}")
                    continue

            return self.cards


urls = []

scraper = Scraper("drivers/chromedriver", "https://www.elestrals.com")
artist_collection_list = scraper.get_cards(urls)

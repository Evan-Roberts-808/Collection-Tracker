import requests
from bs4 import BeautifulSoup
from server.models import db, Set, Card
import ipdb
import base64

class Scraper:

    def __init__(self):
        self.cards = []

    def get_page(self, url):
        doc = BeautifulSoup(requests.get(url).text, 'html.parser')
        return doc
    
    def get_cards(self, urls):
        for url in urls:
            card_html = self.get_page(url)
            
            name = card_html.select('div.w-full.flex-1.px-5 h1.mt-4.mb-3')[0].text.strip()
            image_element = card_html.select('div.relative.aspect-\\[\\.733\\] span img')[0]
            image_url = image_element['src']
            base64_image_data = image_url.split(',')[1]  # Extract the Base64-encoded data

            
            ipdb.set_trace()

artist_collection_urls = [
    'https://www.elestrals.com/image/image__817a413f-a1dc-4e5a-8440-d11e59e492fb',
    'https://www.elestrals.com/image/image__3cb9f3ea-5806-402f-95b2-24df4048f15a',
    'https://www.elestrals.com/image/image__09a95e29-6a7d-477a-8d9c-c803b2be1893',
    'https://www.elestrals.com/image/image__9bb965b7-87e1-41ba-9c72-11b56dff5c6b',
    'https://www.elestrals.com/image/image__b3af6e5f-c865-4294-a661-095d46502689',
    'https://www.elestrals.com/image/image__33e05b3f-603c-45bb-94f2-d602c516ce13',
    'https://www.elestrals.com/image/image__6ebc0615-4c2e-4aec-9890-8b61f66accec',
    'https://www.elestrals.com/image/image__16455dd9-4cae-45bf-8b4f-25360c7220f3',
    'https://www.elestrals.com/image/image__7f31ed04-e447-4648-9a51-defa87c13fee',
    'https://www.elestrals.com/image/image__d686ac57-645c-48db-a6a2-f6c5c687e003',
    'https://www.elestrals.com/image/image__22430c88-6aba-419f-a708-22970a4a69b9',
    'https://www.elestrals.com/image/image__22ad8b7f-50e8-457f-99a4-b9682dc57331',
    'https://www.elestrals.com/image/image__f40e8164-b797-4bde-90fb-151c9e24cb25',
    'https://www.elestrals.com/image/image__65f0404d-3f3c-4eb4-851a-1d04ed21068b',
    'https://www.elestrals.com/image/image__3d9f4277-c1e7-4bc1-b181-9482e9499c6d',
    'https://www.elestrals.com/image/image__3ad9546a-b4ac-46d0-8594-69cdb073c4ad',
    'https://www.elestrals.com/image/image__2bacef95-973a-4dfa-aafc-7eb535fd4910',
    'https://www.elestrals.com/image/image__3faea582-a379-42c0-bce9-14b412495118',
    'https://www.elestrals.com/image/image__f33f9c0a-6e26-45da-bbf0-24be5480a90e',
    'https://www.elestrals.com/image/image__0dea96a3-57e0-490f-b4bf-104b0551f173',
    'https://www.elestrals.com/image/image__545f2dd4-0761-4f76-9042-5a2c23834ed3',
    'https://www.elestrals.com/image/image__24b61d2e-e29a-450c-b822-3f1b4b7ae21e',
    'https://www.elestrals.com/image/image__ed6103a6-df69-4657-813d-507561615544',
    'https://www.elestrals.com/image/image__782d98b4-746c-49c8-a1ce-c75ebfab2e3a',
    'https://www.elestrals.com/image/image__8ed18ec9-c893-4a6e-b9d1-9a6b22f3d1ab'
]

scraper = Scraper()
artist_collection_list = scraper.get_cards(artist_collection_urls)
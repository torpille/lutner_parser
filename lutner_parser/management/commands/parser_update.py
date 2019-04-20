from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand, CommandError
from .config import querystring, payload, headers
from ._utils import find_item_links, find_category_links, find_page_links, get_or_none
from lutner_parser.models import Product, Statistics

class Command(BaseCommand):
    def handle(self, *args, **options):
        session = requests.Session()
        category_links = find_category_links('https://lutner.ru/catalog/')
        # page_links = set()
        # for link in category_links:
        #     page_links.update(find_page_links(link))
        page_links = ['https://lutner.ru/catalog/klassicheskie_gitary//?PAGEN_1=1']
        for url in page_links:
            url = url+'&cat_type=line'

            response = session.post( url, data=payload, headers=headers, params=querystring)

            soup = BeautifulSoup(response.text, 'html5lib')


            h = open("test.txt", "w")
            data = h.write(soup.prettify())
            h.close()
            
         
            items = soup.find(id='tech_char_table').find_all('tr')[1:]
            
            for item in items:
                count = item.find_all('td')[2].text.strip()
                price = item.find_all('td')[3].text.strip()
                product_link = 'https://lutner.ru' + item.find_all('td')[0].find('a', href=True).get('href')
                
                product = get_or_none(Product, link=product_link)
                if product:
                    print('statistics', product.name)
                    statistics = Statistics(product = product)
                    statistics.count = count
                    statistics.price = price
                    statistics.save()

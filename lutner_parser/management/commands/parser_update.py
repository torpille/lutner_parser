from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from .config import querystring, payload, headers
from ._utils import  update_product, get_or_none, get_soup
from lutner_parser.models import Product, Statistics, Pagelink

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        pagelinks = []
        for link in Pagelink.objects.all():
            pagelinks.append(link.link)
        with Pool(30) as p:
            p.map(get_statistics, pagelinks)

def get_statistics(pagelink):
    session = requests.Session()
    url = pagelink +'&cat_type=line'
    soup = get_soup(url, session)
    while True:
        try:
            items = soup.find(id='tech_char_table').find_all('tr')[1:]
            break
        except AttributeError:
            soup = get_soup(url, session)
            print('retry')

    
    for item in items:
        count = item.find_all('td')[2].text.strip()
        price = item.find_all('td')[3].text.strip()
        if price == '""':
            price = 0
        product_link = 'https://lutner.ru' + item.find_all('td')[0].find('a', href=True).get('href')
        product = get_or_none(Product, link=product_link)
        if not product:
            product = Product(link=product_link)
            update_product(product)
      
        print('statistics', product.name)
        statistics = Statistics(product = product)
        statistics.count = count
        statistics.price = price
        try:    
            statistics.save()
        except ValueError:
            statistics.price = 0
            statistics.count = 0
            statistics.save()



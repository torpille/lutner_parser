# from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from ._utils import update_product
from ._utils import save_links
from ._utils import find_category_links
from lutner_parser.models import Pagelink, Product



class Command(BaseCommand):
    def handle(self, *args, **options):
        category_links = find_category_links('https://lutner.ru/catalog/')

        with Pool(30) as p:
            p.map(save_links, category_links)
        
        products = Product.objects.filter(article=None, name=None)
            
        with Pool(20) as p:
            p.map(update_product, products)
      
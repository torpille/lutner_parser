from bs4 import BeautifulSoup
import requests
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from .config import querystring, payload, headers
from ._utils import  update_product, get_or_none, get_soup, get_statistics
from lutner_parser.models import Product, Statistics, Pagelink

class Command(BaseCommand):
    def handle(self, *args, **options):        
        pagelinks = Pagelink.objects.all()
        # pagelinks = ['https://lutner.ru/catalog/kazu/?set_filter=Y&PAGEN_1=1']
        with Pool(20) as p:
            p.map(get_statistics, pagelinks)





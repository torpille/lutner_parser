from multiprocess import Pool
from lutner_parser.models import Pagelink, Product
from ._utils import  update_product, get_statistics, save_links
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = '/catalog/balalayki_aksessuary/'
        #with Pool(30) as p:
        #    p.map(save_links, url)
        save_links(url)
        products = Product.objects.filter(article=None, name=None)

        with Pool(20) as p:
            p.map(update_product, products)

        pagelinks = Pagelink.objects.filter(link__startswith = 'https://lutner.ru/catalog/balalayki_aksessuary/')
        with Pool(20) as p:
            p.map(get_statistics, pagelinks)


from django.core.management.base import BaseCommand, CommandError
from ._utils import create_product, find_item_links, find_category_links, find_page_links



class Command(BaseCommand):
    def handle(self, *args, **options):
        category_links = find_category_links('https://lutner.ru/catalog/')
        page_links = set()
        item_links = set()
        unparsed_links = []
        for link in category_links:
            page_links.update(find_page_links(link))
            print('cl', link)
        for page in page_links:
            item_links.update(find_item_links(page))
            print('pl', page)
        # item_links = ['https://lutner.ru/catalog/blok_fleyty_aksessuary/1094_prima_blokfleyta_soprano_bezhevyy_plastik_derevo_barochnaya_sistema_mollenhauer/']
        for url in item_links:
            print(url)
            create_product(url, unparsed_links)
        for url in unparsed_links:
            print('try', url)
            create_product(url, unparsed_links)

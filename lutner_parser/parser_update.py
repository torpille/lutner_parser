# from bs4 import BeautifulSoup
# import requests
# from django.core.management.base import BaseCommand, CommandError
# from config import querystring, payload, headers
# from ._utils import find_item_links, find_category_links, find_page_links

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         session = requests.Session()
#         category_links = find_category_links('https://lutner.ru/catalog/')
#         page_links = set()
#         for link in category_links:
#             page_links.update(find_page_links(link))
#         for url in page_links:
#             url = url+'&cat_type=line'
#             response = session.post( url, data=payload, headers=headers, params=querystring)

#         # def get_html(url):
#         #     r = session.get(url, timeout = (100, 100))
#         #     return r.text

#         soup = BeautifulSoup(response.text, 'lxml')
#         f = open('text666.txt', 'w')
#         f.write(soup.prettify())
#         f.close()

from django.core.management.base import BaseCommand, CommandError
from ._utils import create_product, find_item_links, find_category_links, find_page_links



class Command(BaseCommand):
    def handle(self, *args, **options):
        category_links = find_category_links('https://lutner.ru/catalog/')
        page_links = set()
        item_links = set()
        for link in category_links[:2]:
            page_links.update(find_page_links(link))
            print('cl', link)
        for page in page_links:
            item_links.update(find_item_links(page))
            print('pl', page)
        for url in item_links:
            create_product(url)




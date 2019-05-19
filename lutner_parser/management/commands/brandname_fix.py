# from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from ._utils import  find_all_item_links, find_category_links
from lutner_parser.models import Brandname
# import requests
# import time
# import traceback
# from lutner_parser.models import Product, Section, Category, Brandname, Pagelink
# from .config import querystring, payload, headers



class Command(BaseCommand):
    def handle(self, *args, **options):
        brandnames = Brandname.objects.all()
        brandnames_list = []
        doublers = []
        for bn in brandnames:
            b_info = [bn.name , bn.id]
            brandnames_list.append(b_info)
        for i in range(len(brandnames_list)):
            for j in range(i,len(brandnames_list)):
                if brandnames_list[i][0] == brandnames_list[j][0]:
                    d = [brandnames_list[i][1], brandnames_list[j][1]]
                    doublers.append(d)
        print(doublers)


        # category_links = find_category_links('https://lutner.ru/catalog/')
        # h = open("test11.txt", "w")
        # data = h.write('\n'.join(category_links))
        # h.close()
        # item_links = []
        # # h = open("test.txt", "r")
        # # data = h.read()
        # # d = data.split('\n')
        # # item_links.extend(d)
        # # h.close()
        # for link in category_links:
        #     item_links.extend(find_all_item_links(link))
        #     print('cl', link)
        # h = open("test.txt", "w")
        # data = h.write('\n'.join(item_links))
        # h.close()

        # with Pool(20) as p:
        #     p.map(create_product, item_links)
        # for link in item_links:
        #     create_product(link)

# def create_product(url):
#     print(url)   
#     product = get_or_none(Product, link=url)
#     if product:
#         return
#     else:  
#         broken_links = open("broken links.txt", "w")
#         soup = get_soup(url)
#         if soup:
#             table = soup.find(class_='product-features-table')
#             article = table_find('Артикул:', table)
            

#             product = get_or_none(Product, article=article)
#             if product:
#                 return
#             else:
#                 product = Product(link=url)
#                 product.name = soup.find('h1').text
#                 product.article = article
#                 if article == None:
#                     data = broken_links.write(url)
#                     return
#                 section_category = soup.find(class_ = 'breadcrumb').text.split('>')
#                 section_text = section_category[-2].strip()
#                 category_text = section_category[-1].strip()
#                 section = get_or_none(Section, name=section_text)
#                 if not section:
#                     section = Section(name=section_text)
#                     section.save()
#                 category = get_or_none(Category, name=category_text)
#                 if not category:
#                     category = Category(name=category_text, section=section)
#                     category.save()
#                 product.category=category
#                 brandname_text = soup.find(class_='product-features-table').find_all('tr')[0].find_all('td')[1].text
#                 brandname = get_or_none(Brandname, name=brandname_text)
#                 if not brandname:
#                     brandname = Brandname(name=brandname_text)
#                     brandname.save()
#                 product.brandname = brandname
#                 product.save()
                
#                 print(product.name)
#                 print('done')
#             return product
#         else:
#             data = broken_links.write(url)
#         broken_links.close()
        
# def get_soup(url, session=None):
#     for i in range(10):
#         try:
#             if session:
#                 html = session.post( url, data=payload, headers=headers, params=querystring).text
#             else:
#                 html = requests.get(url, timeout = (200, 200)).text
#             soup = BeautifulSoup(html, 'html5lib')
#             if soup:
#                 return soup
#         except Exception as e:
#             print('Ошибка:\n')
#             print('----waiting----')
#             print(url)
#             time.sleep(1)
#         if i == 9:
#             broken_links = open("broken links.txt", "w")
#             data = broken_links.write(url)
#             broken_links.close()
        
    


# def get_or_none(classmodel, **kwargs):
#     try:
#         return classmodel.objects.get(**kwargs)
#     except classmodel.DoesNotExist:
#         return None
#     except classmodel.MultipleObjectsReturned:
#         return classmodel.objects.filter(**kwargs).first()
# def table_find(header, table):
#     result = table.find(text=header)
#     if result:
#         result = result.next.next.text
#     return result

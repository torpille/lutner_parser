# from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from ._utils import get_or_none
from lutner_parser.models import Brandname, Product
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
            for j in range(i+1,len(brandnames_list)):
                if brandnames_list[i][0] == brandnames_list[j][0]:
                    print(brandnames_list[i][0])
                    d = [brandnames_list[i][1], brandnames_list[j][1]]
                    doublers.append(d)
        print(doublers)


        for i in range(len(doublers)):
            doubled = get_or_none(Product, brandname=doublers[i][1])
            if doubled:
                doubled.brandname = get_or_none(Brandname, name=doublers[i][0])
                
            else:
                b = get_or_none(Brandname, id=doublers[i][1])
                b.name = '---'
                print('done')
               

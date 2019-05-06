from bs4 import BeautifulSoup
import requests
import time
import traceback
from django.core.management.base import BaseCommand, CommandError
from multiprocess import Pool
from lutner_parser.models import Product, Section, Category, Brandname, Pagelink, Statistics
from .config import querystring, payload, headers


def get_soup(url, session=None):
    for i in range(10):
        try:
            if session:
                html = session.post( url, data=payload, headers=headers, params=querystring).text
            else:
                html = requests.get(url, timeout = (100, 100)).text
            soup = BeautifulSoup(html, 'lxml')
            if soup:
                return soup
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
            print('----waiting----')
            print(url)
            time.sleep(1)
        if i == 9:
            broken_links = open("broken links.txt", "w")
            data = broken_links.write(url)
            broken_links.close()
 

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    except classmodel.MultipleObjectsReturned:
        return classmodel.objects.filter(**kwargs).first()

def get_category(soup):
    def get_url(soup):
        url = soup.find(class_ = 'breadcrumb').find_all('a', href=True)[-1]['href']
        print('cat url', url)
        return(url)
    section_category = soup.find(class_ = 'breadcrumb').text.split('>')
    section_text = section_category[-2].strip()
    category_text = section_category[-1].strip()
    section = get_or_none(Section, name=section_text)
    if not section:
        section = Section(name=section_text)
        section.save()
    category = get_or_none(Category, name=category_text)
    if not category:
        category = Category(name=category_text, section=section)
        category.url = get_url(soup)
        category.save()
    if category.url == None:
        category.url = get_url(soup)
        category.save()
    return(category)

def update_product(product):
    url = product.link  
    soup = get_soup(url)
    table = soup.find(class_='product-features-table')
    if not table:
        return
    article = table_find('Артикул:', table)
    # same_article_product = get_or_none(Product, article=article)
    # if same_article_product:
    #     h = open("duplicate_articles.txt", "a")
    #     data = h.write(product.link + '\n' + same_article_product.link + '\n \n')
    #     h.close()
    product.name = soup.find('h1').text
    product.article = article
    # if article == None:
    #     return
    # section_category = soup.find(class_ = 'breadcrumb').text.split('>')
    # section_text = section_category[-2].strip()
    # category_text = section_category[-1].strip()
    # section = get_or_none(Section, name=section_text)
    # if not section:
    #     section = Section(name=section_text)
    #     section.save()
    # category = get_or_none(Category, name=category_text)
    # if not category:
    #     category = Category(name=category_text, section=section)
    #     category.save()

    product.category = get_category(soup)
    brandname_text = table_find('Производитель:', table)
    if brandname_text:
        brandname = get_or_none(Brandname, name=brandname_text)
        if not brandname:
            brandname = Brandname(name=brandname_text)
            brandname.save()
        product.brandname = brandname
    product.save()
    print(product.name)
    print('done')


def find_category_links(url):
    category_links = []
    soup = get_soup(url)
    for third in  soup.findAll('ul', 'third ie'):
        third.extract()
    for a in  soup.findAll('ul', 'second'):
        for href in a.find_all('a', href=True):
            category_links.append( href['href'])
    return category_links

    
def save_links(link): 
    category_url = 'https://lutner.ru' + link
    i=1
    while True:      
        url = category_url + '?set_filter=Y&PAGEN_1=' + str(i)
        print(url)
        soup = get_soup(url)
        if soup:
            save_links_to_db(soup)

        category = get_category(soup)    
        pagelink = get_or_none(Pagelink, link=url, category=category)
        if not pagelink:
            # section_category = soup.find(class_ = 'breadcrumb').text.split('>')
            # section_text = section_category[-2].strip()
            # category_text = section_category[-1].strip()
            # section = get_or_none(Section, name=section_text)
            # if not section:
            #     section = Section(name=section_text)
            #     section.save()
            # category = get_or_none(Category, name=category_text)
            # if not category:
            #     category = Category(name=category_text, section=section)
            #     category.save()
            old_pagelink = get_or_none(Pagelink, link=url)
            if old_pagelink:
                old_pagelink.category = category
                old_pagelink.save()
            else:
                pagelink = Pagelink(link=url, category=category)
                pagelink.save()
        i+=1
        next_url = link + '?set_filter=Y&PAGEN_1=' + str(i)
        if not soup.find('a', href=next_url):
            break


def save_links_to_db(soup):
    items = soup.find_all( class_='product-item-title')
    for item in items:
        href = item.find('a', href=True).get('href')
        link='https://lutner.ru'+href
        product = get_or_none(Product, link=link)
        if not product:
            product = Product(link=link)
            print('link ' + link)
            product.save()



def table_find(header, table):
    result = table.find(text=header)
    if result:
        result = result.next.next.text
    return result

def get_statistics(pagelink):
    session = requests.Session()
    url = pagelink.link +'&cat_type=line'
    # url = pagelink +'&cat_type=line'
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
        if not count:
            count = 0
        price = item.find_all('td')[3].text.strip()
        if not price:
            price = 0
        product_link = 'https://lutner.ru' + item.find_all('td')[0].find('a', href=True).get('href')
        product = get_or_none(Product, link=product_link)
        if not product:
            product = Product(link=product_link)
            update_product(product)
      
        print('statistics', product.name)
        print(product_link)
        # statistics = get_or_none(Statistics, product=product)
        # if not statistics:
        product.count = count
        product.price = price
        product.save()
        statistics = Statistics(product = product)
        statistics.count = count
        statistics.price = price
        try:    
            statistics.save()
        except ValueError:
            statistics.price = 0
            statistics.count = 0
            statistics.save()
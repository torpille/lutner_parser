from bs4 import BeautifulSoup
import requests
import time
import traceback
from multiprocess import Pool
from lutner_parser.models import Product, Section, Category, Brandname, Pagelink
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

def update_product(product):
    url = product.link  
    soup = get_soup(url)
    table = soup.find(class_='product-features-table')
    article = table_find('Артикул:', table)
    # same_article_product = get_or_none(Product, article=article)
    # if same_article_product:
    #     h = open("duplicate_articles.txt", "a")
    #     data = h.write(product.link + '\n' + same_article_product.link + '\n \n')
    #     h.close()
    product.name = soup.find('h1').text
    product.article = article
    if article == None:
        return
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
        category.save()
    product.category=category
    brandname_text = soup.find(class_='product-features-table').find_all('tr')[0].find_all('td')[1].text
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
            
        pagelink = get_or_none(Pagelink, link=url)
        if not pagelink:
            pagelink = Pagelink(link=url)
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

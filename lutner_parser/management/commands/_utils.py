from bs4 import BeautifulSoup
import requests
import time
from lutner_parser.models import Product, Section, Category, Brandname


def get_soup(url):

    for i in range(10):
        try:
            html = requests.get(url, timeout = (100, 100)).text
            soup = BeautifulSoup(html, 'html5lib')
            break
        except requests.exceptions.ConnectionError:
            print('----waiting----')
            time.sleep(1)
    if soup:
        return soup
    else:
        return

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    except classmodel.MultipleObjectsReturned:
        return classmodel.objects.filter(**kwargs).first()

def create_product(url):
    
        
    soup = get_soup(url)
    if soup:
        product = get_or_none(Product, link=url)
        if product:
            return
        else:
            product = Product(link=url)
            product.name = soup.find('h1').text
            product.article = product.name.split(' ')[0]
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
        






def find_category_links(url):
    category_links = []
    soup = get_soup(url)
    for a in  soup.find_all( class_ = 'second'):
        for href in a.find_all('a', href=True):
            category_links.append( href['href'])
    return category_links

    
    
def find_page_links(link):
    page_links = set()
    url = 'https://lutner.ru' + link
    page_links.add(url + '?PAGEN_1=1')
    soup = get_soup(url)
    pages = soup.find_all( class_='pl')
    for page in pages:
        elems = str(page).split('"')
        for elem in elems:
            if elem.find(link) != -1:
                page_links.add('https://lutner.ru' + elem)

    
    return page_links

def find_item_links(url):
    item_links = set()
    soup = get_soup(url)
    items = soup.find_all( class_='product-item-title')
    for item in items:
        href = item.find('a', href=True).get('href')
        item_links.add('https://lutner.ru'+href)
        

            # if elem.find(url.split('?')[0]) != -1:
                # item_links.add('https://lutner.ru' + elem)
                # print('https://lutner.ru' + elem)
    return item_links



  
from bs4 import BeautifulSoup
import requests
from lutner_parser.models import Product, Section, Category, Brandname


def get_html(url):
    r = requests.get(url, timeout = (1000, 1000))
    return r.text

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    except classmodel.MultipleObjectsReturned:
        return classmodel.objects.filter(**kwargs).first()

def create_product(url, unparsed_links):
    for i in range(10):
        try:
            html = get_html(url)
            break
        except requests.exceptions.ConnectionError:
            print('----waiting----')
            time.sleep(1)
        
    if html:
        soup = BeautifulSoup(html, 'html5lib')
        product = get_or_none(Product, link=url)
        if product:
            return
        else:
            product = Product(link=url)
            try:
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
            except AttributeError as error:
                unparsed_links.append(url)







def find_category_links(page):
    category_links = []
    URL = page
    current_page = requests.get(URL)
    soup = BeautifulSoup(current_page.content, 'html.parser')
    for a in  soup.find_all( class_ = 'second'):
        for href in a.find_all('a', href=True):
            category_links.append( href['href'])
    return category_links

    
    
def find_page_links(link):
    page_links = set()
    URL = 'https://lutner.ru' + link
    page_links.add(URL + '?PAGEN_1=1')
    current_page = requests.get(URL)
    soup = BeautifulSoup(current_page.content, 'html.parser')
    pages = soup.find_all( class_='pl')
    for page in pages:
        elems = str(page).split('"')
        for elem in elems:
            if elem.find(link) != -1:
                page_links.add('https://lutner.ru' + elem)

    
    return page_links

def find_item_links(url):
    item_links = set()
    current_page = requests.get(url)
    soup = BeautifulSoup(current_page.content, 'html.parser')
    items = soup.find_all( class_='product-item-title')
    for item in items:
        href = item.find('a', href=True).get('href')
        item_links.add('https://lutner.ru'+href)
        

            # if elem.find(url.split('?')[0]) != -1:
                # item_links.add('https://lutner.ru' + elem)
                # print('https://lutner.ru' + elem)
    return item_links



  
import load_django, requests, fake_useragent, openpyxl, math
from parser_app import models
from concurrent import futures
from bs4 import BeautifulSoup


ua = fake_useragent.FakeUserAgent()
HEADERS = {'User-Agent': ua.chrome}
ITEMS_PER_PAGE = 12
CATEGORIES = (
    {'name': 'MEN', 'url': 'https://www.namebrandsperfume.com/men-perfume'}, 
    {'name': 'WOMEN', 'url': 'https://www.namebrandsperfume.com/women-perfume'}, 
    {'name': 'CHILDREN', 'url': 'https://www.namebrandsperfume.com/kids-perfume'}, 
    {'name': 'GIFT SETS', 'url': 'https://www.namebrandsperfume.com/perfume-gift-set'}, 
    {'name': 'TESTERS', 'url': 'https://www.namebrandsperfume.com/perfume-testers'}, 
    {'name': 'MINIS', 'url': 'https://www.namebrandsperfume.com/mini-perfume'}, 
    {'name': 'NEW ARRIVALS', 'url': 'https://www.namebrandsperfume.com/new-arrivals'}, 
    {'name': 'DAILY ARRIVALS', 'url': 'https://www.namebrandsperfume.com/daily-arrivals'}, 
    {'name': 'HOT SELLINGS', 'url': 'https://www.namebrandsperfume.com/best-selling-perfumes'}, 
)


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_item_info(item: models.Item) -> tuple:
    url = item.url
    soup = get_soup(url)

    header = soup.find('div', attrs={'class': 'prodetail'})

    name = header.find('h3').text
    description = header.select_one('span.sku').text

    try:
        sku = soup.find('div', attrs={'class': 'qtybox'}).find('input', attrs={'name': 'product[]'}).get('value').split('#')[1]
    except AttributeError:
        try:
            sku = soup.find('input', attrs={'name': 'product[]'}).get('value').split('#')[1]
        except AttributeError:
            sku = ''

    if not name:
        print(f'[INFO]: here is no name, check this out {url}')
    elif not description:
        print(f'[INFO]: here is no description, check this out {url}')
    elif not sku:
        print(f'[INFO]: here is no sku, check this out {url}')

    item.name = name
    item.description = description
    item.sku = sku
    item.save()

    return name, description, sku


def get_category_page_items(page_info: dict) -> None:

    category = page_info.get('category')
    url = page_info.get('url')
    soup = get_soup(url)

    list_product = soup.find('div', attrs={'class': 'row listproduct'})
    items_links = [a.get('href') for a in list_product.select('.product-name>a')]

    print(f'{len(items_links)} items on {url}')

    for link in items_links:
        models.Item.objects.create(
            category=category, 
            url=link
        )


def get_category_items(category: dict) -> None:
    name = category.get('name')
    url = category.get('url')

    soup = get_soup(url)

    try:
        items_amount = soup.find('div', attrs={'class': 'toolbar_but clearfix'}).find('span').text.split()[1]
        print(f'[INFO]: {items_amount} items by {name}')
    except AttributeError:
        print(f'[INFO]: category {name} is empty, check this out {url}')
        return []
    
    category_pagenation = math.ceil(int(items_amount) / ITEMS_PER_PAGE) + 1
    category_pages_links = [{'category': name, 'url': f'{url}?sort=alpha_asc&page={i}'} for i in range(1, category_pagenation)]

    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(get_category_page_items, category_pages_links)

    # for item in category_pages_links:
    #     get_category_page_items(item)
        
    print(len(models.Item.objects.filter(category=name)))


def load_to_xlsx():

    categories = ['MEN', 'WOMEN', 'CHILDREN', 'GIFT SETS', 'TESTERS', 'MINIS', 'NEW ARRIVALS', 'DAILY ARRIVALS', 'HOT SELLINGS']
    file = 'brandsperfume_categories.xlsx'
    wb = openpyxl.load_workbook(file)
    for cat in categories:
        sheet_name = cat
        sheet = wb.get_sheet_by_name(sheet_name)
        sheet.append(('NAME', 'DESCRIPTION', 'SKU'))
        items = models.Item.objects.filter(category=cat)
        for item in items:
            sheet.append((item.name, item.description, item.sku))
    wb.save(file)


def clear_database():
    models.Item.objects.all().delete()
    print('[INFO]: database is cleared...')


if __name__ == '__main__':
    
    for cat in CATEGORIES:
        get_category_items(cat)

    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(get_item_info, models.Item.objects.all())

    load_to_xlsx()

    # clear_database()








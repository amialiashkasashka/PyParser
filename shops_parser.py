import requests
from bs4 import BeautifulSoup as BS
import json

HOST = 'https://www.mebelshara.ru/'
URL =  'https://www.mebelshara.ru/contacts/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
JSON = 'shop_addr.json'

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

def get_content(html):
    soup = BS(html, 'html.parser')
    cities = soup.find_all('div', class_='city-item')
    addresses = []

    for city in cities:
        shops = city.find_all('div', class_='shop-list-item')

        for shop in shops:
            addresses.append(
                {
                    'address': [str(city.find('div', class_='expand-block-header').find('h4').get_text(strip=True) + ', ' + shop.find('div', class_='shop-address').get_text(strip=True))],
                    'latlon': [float(shop.get('data-shop-latitude')), float(shop.get('data-shop-longitude'))],
                    'name': shop.get('data-shop-name'),
                    'phones': [shop.find('div', class_='shop-phone').get_text(strip=True)],
                    'working_hours': [shop.get('data-shop-mode1')[:-1] + ' ' + shop.get('data-shop-mode2')],
                }
            )
    return addresses

def save_doc(content, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        json.dump(content, f, ensure_ascii=False, separators=((',', ':')), indent=4)


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        addresses = get_content(html.text)
        save_doc(addresses, JSON)
    else:
        print('Error')

parser()
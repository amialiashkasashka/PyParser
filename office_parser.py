import requests
from bs4 import BeautifulSoup as BS
import json

# разобрав get-запросы сайта, нашел это чудо, джекпот!
URL = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
HOST = 'https://www.tui.ru/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
JSON = 'offices_addr.json'


def get_content(url, params=''):
    r = requests.get(url, params=params)
    r_json = r.json()
    offices = r_json.get('offices')
    content = []


    for office in offices:
        working_hours = office.get('hoursOfOperation')
        wdaysStartTime = working_hours['workdays']['startStr']
        wdaysEndTime = working_hours['workdays']['endStr']
        saturday = working_hours['saturday']
        sunday = working_hours['sunday']

        if (working_hours['saturday']['isDayOff'] == True) and (working_hours['sunday']['isDayOff'] == True):
            whours = 'сб-вск: выходной'
        elif (working_hours['saturday']['isDayOff'] == False) and (working_hours['sunday']['isDayOff'] == True):
            saturdayStart = working_hours['saturday']['startStr']
            saturdayEnd = working_hours['saturday']['endStr']
            whours = f'сб {saturdayStart}-{saturdayEnd}, вск: выходной'
        else:
            saturdayStart = working_hours['saturday']['startStr']
            saturdayEnd = working_hours['saturday']['endStr']
            sundayStart = working_hours['sunday']['startStr']
            sundayEnd = working_hours['sunday']['endStr']
            whours = f'сб {saturdayStart}-{saturdayEnd}, вск {sundayStart}-{sundayEnd}'

        content.append(
            {
                'address': office.get('address'),
                'latlon': [float(office.get('latitude')), float(office.get('longitude'))],
                'name': office.get('name'),
                'phones': [office.get('phone')],
                'working_hours': [f'пн-пт {wdaysStartTime} до {wdaysEndTime}', whours]
            }
        )
    save_doc(content, JSON)

def save_doc(content, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        json.dump(content, f, ensure_ascii=False, separators=((',', ':')), indent=4)

get_content(URL)


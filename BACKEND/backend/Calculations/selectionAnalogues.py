import ast
import time

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from Calculations.LibSB import transliterate
from Calculations.models import FileData, NumStreet

headers = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-Agent": UserAgent().chrome,
}


def AnalogsMirCvartir(id_session):
    Apart = []
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    street = selectApart["location"].split(',')[1]
    base = NumStreet.objects.all()
    for s_index in base:
        if street.lstrip(' ') in s_index.name_street:
            id_street = s_index.id_street
            print(id_street)

    url=f'https://www.mirkvartir.ru/listing/?locationIds=MK_Street|{id_street}&areaKitchenFrom={selectApart["areaKitchen"]*0.5}'
    result = requests.get(url, headers=headers)
    html = BeautifulSoup(result.text, "lxml")
    content = html.find_all('div', class_="content")
    for area in content:
        s_a = area.find('a', class_="offer-title")
        a = area.find('div', class_='address').find_all('a')
        if a[1].text in street:
            url_Apart = f'https://www.mirkvartir.ru{s_a.get("href")}'
            result_Apart = requests.get(url_Apart, headers=headers)
            soup_Apart = BeautifulSoup(result_Apart.text, "lxml")
            rooms = floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse = ' '
            ls = soup_Apart.find_all('div', class_='faDHoQ')
            for character in ls:

                match (character.find('div', class_='bZiYbk').text):
                    case 'комнаты':
                        rooms =character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'комната':
                        rooms = character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'этаж':
                        floor =character.find('div', class_='sc-kjwnom dOPiKV').text.split(' из ')[0]
                        totalfloor =character.find('div', class_='sc-kjwnom dOPiKV').text.split(' из ')[1]
                    case 'Общая площадь':
                        area =character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'площадь кухни':
                        areaKitchen =character.find('div', class_='sc-kjwnom dOPiKV').text

            for character in soup_Apart.find_all('div', class_='sc-1u2rf9n cktnNC'):
                if ('Дом' in character.find('div', class_='sc-1cbra9b hGpLSC').text) & (character.find('a', class_='sc-1uzgru1 iPCOGd') != None):
                    typeHouse = character.find('a', class_='sc-1uzgru1 iPCOGd').text
            desc = soup_Apart.find_all('script')[16].text.split('"description":"')[1].split('","heading"')[0]
            if ('балкон' in desc) or ('лодж' in desc):
                balcony = 'да'
            else:
                balcony = ' '
            if 'ремонт' in desc:
                arr_disc = desc.split(' ')
                for slovo in arr_disc:
                    if 'ремонт' in slovo:
                        repair = arr_disc[arr_disc.index(slovo) -1]+' '+arr_disc[arr_disc.index(slovo)]
            data = {
                "price": soup_Apart.find('div', class_='price m-all').find('strong').text.replace("\u2009", ""),
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area.replace(' м²',''),
                "areaKitchen": areaKitchen.replace(' м²',''),
                "balcony": balcony,
                "repair": repair,
                "typeHouse": typeHouse,
            }
            full = True
            for cell in data:
                if data[cell] == ' ':
                    full = False
            if full:
                Apart.append(data)
    return Apart


def AnalogsMove(id_session):
    Apart = []
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    street = selectApart["location"].split(',')[1].lstrip(' ')
    url = f'https://move.ru/moskva/{transliterate(street)}/kvartiry/'
    req = requests.get(url, headers=headers, stream=True, timeout=100)
    soup_Apart = BeautifulSoup(req.text, 'lxml')
    info = soup_Apart.find_all('div', class_='search-item move-object')
    for Apaer_info in info:
        str = Apaer_info.find('a', class_='search-item__title-link search-item__item-link')
        if street.split('.')[1] in str.text:
            s_a = 'https:' + str.get("href")
            result_area = requests.get(s_a, headers=headers)
            soup_page = BeautifulSoup(result_area.text, 'lxml')
            rooms = floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse =' '
            ls = soup_page.find_all('li', class_='object-info__details-table_property')
            for character in ls:
                match character.find('div', class_='object-info__details-table_property_name').get('title'):
                    case 'Цена':
                        price = character.find('div', class_='object-info__details-table_property_value').text.replace(' ', '').replace('₽', '')
                    case 'Количество комнат':
                        rooms = character.find('div', class_='object-info__details-table_property_value').text
                    case 'Этаж':
                        floor = character.find('div', class_='object-info__details-table_property_value').text.split('/')[0]
                        totalfloor = character.find('div', class_='object-info__details-table_property_value').text.split('/')[1]
                    case 'Общая площадь':
                        area = character.find('div', class_='object-info__details-table_property_value').text.replace(' м²', '')
                    case 'Площадь кухни':
                        areaKitchen = character.find('div', class_='object-info__details-table_property_value').text.replace(' м²', '')
                    case 'Тип балкона':
                        balcony = character.find('div', class_='object-info__details-table_property_value').text
                    case 'Ремонт':
                        repair =  character.find('div', class_='object-info__details-table_property_value').text
                    case 'Тип здания':
                        typeHouse = character.find('div', class_='object-info__details-table_property_value').text

            data = {
                "price": price,
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area,
                "areaKitchen": areaKitchen,
                "balcony": balcony,
                "repair":repair,
                "typeHouse":typeHouse
            }
            full = True
            for cell in data:
                if data[cell] == ' ':
                    full = False
            if full:
                Apart.append(data)
    return Apart

import ast
import json
import time

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from soupsieve.util import lower
from Calculations.LibSB import transliterate
from Calculations.models import FileData, NumStreet

headers = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-Agent": UserAgent().chrome,
}


def AnalogsMirCvartir(id_session):
    Apart = []
    id_street = ''
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    street = selectApart["location"].split(',')[1]
    street_clone = ''
    street = street.replace('проспект', 'пр-кт,').replace('переулок ', 'пер ').replace('улица', 'ул')
    base = NumStreet.objects.all()
    for s_index in base:
        if street.lstrip(' ').replace(',', '').replace('.', '') in s_index.name_street.replace(',', '').replace('.',
                                                                                                                ''):
            id_street = s_index.id_street
            if id_street == '':
                street = street.replace('.', '').replace(',', '')
                street_clone = street.split(' ')[1] + street.split(' ')[0]
                if street_clone.lstrip(' ').replace(',', '').replace('.', '').replace(' ',
                                                                                      '') in s_index.name_street.replace(
                        ',', '').replace('.', '').replace(' ', ''):
                    id_street = s_index.id_street
    for p in range(4):
        time.sleep(0.2)
        if 'панель' in selectApart["materialWall"].lower():
            url_mat = 7
        elif 'кирпич' in selectApart["materialWall"].lower():
            url_mat = 4
        elif 'монолит' in selectApart["materialWall"].lower():
            url_mat = 5
        else:
            url_mat = ''
        url = f'https://www.mirkvartir.ru/listing/?locationIds=MK_Street|{id_street}&areaKitchenFrom={selectApart["areaKitchen"] * 0.5}&p={p}&wallMaterial={url_mat}'
        print(url)
        result = requests.get(url, headers=headers, timeout=120)
        html = BeautifulSoup(result.text, "lxml")
        content = html.find_all('div', class_="content")
        for area in content:
            time.sleep(0.2)
            s_a = area.find('a', class_="offer-title")
            a = area.find('div', class_='address').find_all('a')
            url_Apart = f'https://www.mirkvartir.ru{s_a.get("href")}'
            result_Apart = requests.get(url_Apart, headers=headers, timeout=120)
            soup_Apart = BeautifulSoup(result_Apart.text, "lxml")
            floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse = ' '
            rooms = 1
            ls = soup_Apart.find_all('div', class_='faDHoQ')
            for character in ls:

                match (character.find('div', class_='bZiYbk').text):
                    case 'комнаты':
                        rooms = character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'комната':
                        rooms = character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'этаж':
                        floor = character.find('div', class_='sc-kjwnom dOPiKV').text.split(' из ')[0]
                        totalfloor = character.find('div', class_='sc-kjwnom dOPiKV').text.split(' из ')[1]
                    case 'Общая площадь':
                        area = character.find('div', class_='sc-kjwnom dOPiKV').text
                    case 'площадь кухни':
                        areaKitchen = character.find('div', class_='sc-kjwnom dOPiKV').text

            for character in soup_Apart.find_all('div', class_='sc-1u2rf9n cktnNC'):
                if ('Дом' in character.find('div', class_='sc-1cbra9b hGpLSC').text) & (
                        character.find('a', class_='sc-1uzgru1 iPCOGd') != None):
                    typeHouse = character.find('a', class_='sc-1uzgru1 iPCOGd').text
            desc = soup_Apart.find_all('script')[16].text.split('"description":"')[1].split('","heading"')[0]
            if ('балкон' in desc) or ('лодж' in desc):
                balcony = 'да'
            else:
                balcony = 'нет'
            if 'ремонт' in desc:
                arr_disc = desc.split(' ')
                for slovo in arr_disc:
                    if 'ремонт' in slovo:
                        repair = arr_disc[arr_disc.index(slovo) - 1] + ' ' + arr_disc[arr_disc.index(slovo)]
            data = {
                "price": soup_Apart.find('div', class_='price m-all').find('strong').text.replace("\u2009", ""),
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area.replace(' м²', ''),
                "areaKitchen": areaKitchen.replace(' м²', ''),
                "balcony": balcony,
                "repair": repair,
                "typeHouse": typeHouse,
            }
            print(data)
            Apart.append(data)
    return Apart


def AnalogsMove(id_session):
    Apart = []
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    street = selectApart["location"].split(',')[1].lstrip(' ')
    url = f'https://move.ru/moskva/{transliterate(street)}/kvartiry/'
    req = requests.get(url, headers=headers, stream=True, timeout=120)
    if req.status_code == 404:
        street_clone = (street.split(' ')[1] + ' ' + street.split(' ')[0]).lstrip(' ')
        url = f'https://move.ru/moskva/{transliterate(street_clone)}/kvartiry/'
        req = requests.get(url, headers=headers, stream=True, timeout=120)
        street = street_clone
    soup_Apart = BeautifulSoup(req.text, 'lxml')
    info = soup_Apart.find_all('div', class_='search-item move-object')
    for Apaer_info in info:
        str = Apaer_info.find('a', class_='search-item__title-link search-item__item-link')
        street = lower(street).replace('переулок ', '').replace('проезд ', '').replace('ул. ', '').replace('улица',
                                                                                                           '').replace(
            'ул ', '').replace('б-р', '')
        if street in lower(str.text):
            s_a = 'https:' + str.get("href")
            result_area = requests.get(s_a, headers=headers)
            soup_page = BeautifulSoup(result_area.text, 'lxml')
            rooms = floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse = ' '
            ls = soup_page.find_all('li', class_='object-info__details-table_property')
            for character in ls:
                match character.find('div', class_='object-info__details-table_property_name').get('title'):
                    case 'Цена':
                        price = character.find('div', class_='object-info__details-table_property_value').text.replace(
                            ' ', '').replace('₽', '')
                    case 'Количество комнат':
                        rooms = character.find('div', class_='object-info__details-table_property_value').text
                    case 'Этаж':
                        floor = character.find('div', class_='object-info__details-table_property_value').text.split('/')[0]
                        totalfloor = character.find('div', class_='object-info__details-table_property_value').text.split('/')[1]
                    case 'Общая площадь':
                        area = character.find('div', class_='object-info__details-table_property_value').text.replace(
                            ' м²', '')
                    case 'Площадь кухни':
                        areaKitchen = character.find('div',
                                                     class_='object-info__details-table_property_value').text.replace(
                            ' м²', '')
                    case 'Тип балкона':
                        balcony = 'да'
                    case 'Ремонт':
                        repair = character.find('div', class_='object-info__details-table_property_value').text
                    case 'Тип здания':
                        typeHouse = character.find('div', class_='object-info__details-table_property_value').text
            if balcony == ' ':
                balcony = 'нет'
            data = {
                "price": price,
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area,
                "areaKitchen": areaKitchen,
                "balcony": balcony,
                "repair": repair,
                "typeHouse": typeHouse
            }
            Apart.append(data)
    return Apart


def sortingAnalogs(analogs, id_session):
    list = []
    id = 1
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    for apart in analogs:
        if int(apart['info']['rooms']) == int(selectApart['numRooms']) and (
                int(apart['info']['totalFloor']) == int(selectApart['floorsHouse'])) and apart not in list:
            apart['info']['id'] = id
            id+=1
            list.append(apart)
    return list


def test(id_session):
    Apart = []
    material = [
        'v_kirpichnom_dome/',
        'v_panelnom_dome/',
        'v_monolitnom_dome/',
    ]
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[Apart_Info.id_reference]
    if 'панель' in selectApart["materialWall"].lower():
        url_mat = material[1]
    elif 'кирпич' in selectApart["materialWall"].lower():
        url_mat = material[0]
    elif 'монолит' in selectApart["materialWall"].lower():
        url_mat = material[2]
    else:
        url_mat = ''
    street = selectApart["location"].split(',')[1].lstrip(' ')
    url = f'https://move.ru/moskva/{transliterate(street)}/kvartiry/{url_mat}?floor_max={selectApart["floorsHouse"]}&limit=30'
    req = requests.get(url, headers=headers, stream=True, timeout=120)
    if req.status_code == 404:
        street_clone = (street.split(' ')[1] + ' ' + street.split(' ')[0]).lstrip(' ')
        url = f'https://move.ru/moskva/{transliterate(street_clone)}/kvartiry/{url_mat}?floor_max={selectApart["floorsHouse"]}&limit=100'
        req = requests.get(url, headers=headers, stream=True, timeout=120)
        street = street_clone
    print(url)
    soup_Apart = BeautifulSoup(req.text, 'lxml')
    info = soup_Apart.find_all('div', class_='search-item move-object')
    for Apaer_info in info:
        time.sleep(0.2)
        str = Apaer_info.find('a', class_='search-item__title-link search-item__item-link')
        street = lower(street).replace('переулок ', '').replace('проезд ', '').replace('ул. ', '').replace('улица',
                                                                                                           '').replace(
            'ул ', '').replace('б-р', '')
        s_a = 'https:' + str.get("href")
        result_area = requests.get(s_a, headers=headers)
        soup_page = BeautifulSoup(result_area.text, 'lxml')
        rooms = floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse = address = ' '
        ls = soup_page.find_all('li', class_='object-info__details-table_property')
        for character in ls:
            match character.find('div', class_='object-info__details-table_property_name').get('title'):
                case 'Цена':
                    price = character.find('div', class_='object-info__details-table_property_value').text.replace(
                        ' ', '').replace('₽', '')
                case 'Количество комнат':
                    rooms = character.find('div', class_='object-info__details-table_property_value').text
                case 'Этаж':
                    floor = \
                        character.find('div', class_='object-info__details-table_property_value').text.split('/')[0]
                    totalfloor = \
                        character.find('div', class_='object-info__details-table_property_value').text.split('/')[1]
                case 'Общая площадь':
                    area = character.find('div', class_='object-info__details-table_property_value').text.replace(
                        ' м²', '')
                case 'Площадь кухни':
                    areaKitchen = character.find('div',
                                                 class_='object-info__details-table_property_value').text.replace(
                        ' м²', '')
                case 'Тип балкона':
                    balcony = 'да'
                case 'Ремонт':
                    repair = character.find('div', class_='object-info__details-table_property_value').text
                case 'Тип здания':
                    typeHouse = character.find('div', class_='object-info__details-table_property_value').text
                case 'Адрес':
                    address = character.find('div', class_='object-info__details-table_property_value').text


        if balcony == ' ':
            balcony = 'нет'
        photos = []
        print("Start Photo")
        for photo in soup_page.find_all('div', class_='images-slider'):
            for a in photo.find_all('a'):
                if ('.jpeg' in a.get('href') or '.jpg' in a.get('href')):
                    a_photo = ''
                    if 'https' not in  a.get('href'):
                        a_photo = 'https:'+a.get('href')
                    else:
                        a_photo = a.get('href')
                    if a_photo not in photos:
                        photos.append(a_photo)

        data = {
            "info":{
                "id":0,
                "price": price,
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area,
                "areaKitchen": areaKitchen,
                "balcony": balcony,
                "repair": repair,
                "typeHouse": typeHouse,
                "s": s_a,
                "address": address.replace('\n', ' '),
            },
            "photo": json.dumps(photos),

        }
        Apart.append(data)
    return Apart

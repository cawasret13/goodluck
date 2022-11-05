import ast
import json
import time

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from haversine import haversine
from soupsieve.util import lower
from Calculations.LibSB import transliterate
from Calculations.models import FileData, NumStreet

headers = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "User-Agent": UserAgent().chrome,
}
key_api_yandex = "a737be26-3193-452c-adb3-790a2a85661f"

def AnalogsMirCvartir(id_session, id_reference):
    Apart = []
    id_street = ''
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[id_reference]
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
        if 'панель' in selectApart["materialWall"].lower():
            url_mat = 7
        elif 'кирпич' in selectApart["materialWall"].lower():
            url_mat = 4
        elif 'монолит' in selectApart["materialWall"].lower():
            url_mat = 5
        else:
            url_mat = ''
        url = f'https://www.mirkvartir.ru/listing/?locationIds=MK_Street|{id_street}&areaKitchenFrom={selectApart["areaKitchen"] * 0.5}&p={p}&wallMaterial={url_mat}'
        result = requests.get(url, headers=headers, timeout=120)
        html = BeautifulSoup(result.text, "lxml")
        content = html.find_all('div', class_="content")
        for area in content:
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
                if ('Дом' in character.find('div', class_='sc-1cbra9b hGpLSC').text) & (character.find('a', class_='sc-1uzgru1 iPCOGd') != None):
                    typeHouse = character.find('a', class_='sc-1uzgru1 iPCOGd').text
                if ('Состояние' in character.find('div', class_='sc-1cbra9b hGpLSC').text) & (character.find('a', class_='sc-1uzgru1 iPCOGd') != None):
                    repair = character.find('a', class_='sc-1uzgru1 iPCOGd').text
            desc = soup_Apart.find_all('script')[16].text.split('"description":"')[1].split('","heading"')[0]
            if ('балкон' in desc) or ('лодж' in desc) or ('Лодж' in desc) or ('Балкон' in desc):
                balcony = 'да'
            else:
                balcony = 'нет'
            if 'ремонт' in desc:
                arr_disc = desc.split(' ')
                for slovo in arr_disc:
                    if 'ремонт' in slovo:
                        repair +=' ' + arr_disc[arr_disc.index(slovo) - 1] + ' ' + arr_disc[arr_disc.index(slovo)]
            photos = []
            for photo in soup_Apart.find_all('div', class_='slick-slide'):
                for apart_photo in photo.find_all('img'):
                    if 'https:'+apart_photo.get('data-src') not in photos and len(photos)<9:
                        photos.append('https:'+apart_photo.get('data-src'))
            _address = soup_Apart.find('div', class_='address').find_all('span')
            address = ''
            for address_apart in _address:
                address += address_apart.text

            ls_st_metro = soup_Apart.find('div', class_="l-object-address").find_all('p')[1]
            str = []
            for st_metro in ls_st_metro:
                for name_metro in st_metro:
                    if name_metro != ' ' and name_metro != '\u2002' and name_metro != ',' and name_metro != '\xa0' and name_metro != '.':
                        if name_metro.text != ' ' and name_metro.text != '':
                            str.append(name_metro.text.replace('\xa0', ''))
            try:
                if 'км' in str[1]:
                    metro = str[0]
                    time = round((float(str[1].split(' ')[0]) / 5)*60)
                else:
                    time = str[1]
                    metro = str[0]
            except:
                time = 0
                metro = ''
            data = {
                'info': {
                    "id": 0,
                    "price": soup_Apart.find('div', class_='price m-all').find('strong').text.replace("\u2009", ""),
                    "rooms": rooms,
                    "floor": floor,
                    "totalFloor": totalfloor,
                    "area": area.replace(' м²', ''),
                    "areaKitchen": areaKitchen.replace(' м²', ''),
                    "balcony": balcony,
                    "repair": repair,
                    "typeHouse": typeHouse,
                    "time": time,
                    "metro": metro,
                    "s": url_Apart,
                    "address": address.lower(),
                    "id_reference": id_reference,
                },
                'photo': json.dumps(photos)
            }
            Apart.append(data)
    return Apart
def AnalogsMove(id_session, id_reference):
    Apart = []
    material = ['v_kirpichnom_dome/', 'v_panelnom_dome/', 'v_monolitnom_dome/']
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[id_reference]
    if 'панель' in selectApart["materialWall"].lower():
        url_mat = material[1]
    elif 'кирпич' in selectApart["materialWall"].lower():
        url_mat = material[0]
    elif 'монолит' in selectApart["materialWall"].lower():
        url_mat = material[2]
    else:
        url_mat = ''
    street = selectApart["location"].split(',')[1].lstrip(' ')
    url = f'https://move.ru/moskva/{transliterate(street)}/kvartiry/{url_mat}?floor_max={selectApart["floorsHouse"]}&limit=100'
    req = requests.get(url, headers=headers, stream=True, timeout=120)
    if req.status_code == 404:
        street_clone = (street.split(' ')[1] + ' ' + street.split(' ')[0]).lstrip(' ')
        url = f'https://move.ru/moskva/{transliterate(street_clone)}/kvartiry/{url_mat}?floor_max={selectApart["floorsHouse"]}&limit=100'
        req = requests.get(url, headers=headers, stream=True, timeout=120)
        street = street_clone
    soup_Apart = BeautifulSoup(req.text, 'lxml')
    info = soup_Apart.find_all('div', class_='search-item move-object')
    for Apaer_info in info:
        str = Apaer_info.find('a', class_='search-item__title-link search-item__item-link')
        street = lower(street).replace('переулок ', '').replace('проезд ', '').replace('ул. ', '').replace('улица',
                                                                                                           '').replace(
            'ул ', '').replace('б-р', '')
        s_a = 'https:' + str.get("href")
        ls = []
        try:
            result_apart = requests.get(s_a, headers=headers, timeout=200)
            soup_page = BeautifulSoup(result_apart.text, 'lxml')
            ls = soup_page.find_all('li', class_='object-info__details-table_property')
        except:
            print("Err")
        rooms = floor = totalfloor = area = areaKitchen = balcony = repair = typeHouse = address = ' '
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
        for photo in soup_page.find_all('div', class_='images-slider'):
            for a in photo.find_all('a'):
                if ('.jpeg' in a.get('href') or '.jpg' in a.get('href')):
                    if 'https' not in a.get('href'):
                        a_photo = 'https:' + a.get('href')
                    else:
                        a_photo = a.get('href')
                    if a_photo not in photos and len(photos)<9:
                        photos.append(a_photo)

        min_time = 100
        st_metro = ''
        ls_metro = soup_page.find_all('li', class_="object-info__details-table_property")
        for metro_st in ls_metro:
            metro = metro_st.find('span', class_="route-pedestrian")
            if metro != None:
                for metro_time in metro:
                    time = metro_time.text.split(',')[0].strip().replace('\xa0', ' ').split(' ')[0]
                    if int(time) < min_time:
                        min_time = int(time)
                        st_metro = metro_st.find('div', class_="object-info__details-table_property_name").get('title')
        if min_time == 100:
            min_time = ''
            st_metro = ''

        data = {
            "info": {
                "id": 0,
                "price": price,
                "rooms": rooms,
                "floor": floor,
                "totalFloor": totalfloor,
                "area": area,
                "areaKitchen": areaKitchen,
                "balcony": balcony,
                "repair": repair,
                "typeHouse": typeHouse,
                "time": min_time,
                "metro": st_metro,
                "s": s_a,
                "address": address.replace('\n', ' '),
                "coordinates": '',
                "distance": '',
                "id_reference": id_reference,
            },
            "photo": json.dumps(photos),
        }
        Apart.append(data)
    return Apart

def sortingAnalogs(analogs, id_session, id_reference):
    list = []
    id = 1
    Apart_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Apart_Info.data)
    selectApart = data[id_reference]
    info_api = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={key_api_yandex}&geocode={selectApart["location"]}&format=json')
    pos_select = json.loads(info_api.text)["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    coor_select = (float(pos_select.split(' ')[0]),float(pos_select.split(' ')[1]))
    selectApart['coordinates'] = [float(pos_select.split(' ')[0]),float(pos_select.split(' ')[1])]
    for apart in analogs:
        if apart['info']['rooms'] != ' ':
            if int(apart['info']['rooms']) == int(selectApart['numRooms']) \
                    and (int(apart['info']['totalFloor']) == int(selectApart['floorsHouse'])) and apart not in list and apart["info"]["repair"] != ' ' \
                    and int(apart["info"]["id_reference"]) == int(id_reference):
                apart['info']['id'] = id_reference*10 + id
                id += 1
                if 'евро' in apart["info"]["repair"]:
                    apart["info"]["repair"] = 'с современной отделкой'
                elif 'без' in apart["info"]["repair"]:
                    apart["info"]["repair"] = 'без отделки'
                else:
                    apart["info"]["repair"] = 'муниципальный ремонт'
                info_api_analog = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={key_api_yandex}&geocode={apart["info"]["address"]}&format=json')
                pos_analog = json.loads(info_api_analog.text)["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                coor_analog = (float(pos_analog.split(' ')[0]), float(pos_analog.split(' ')[1]))
                dist = haversine(coor_analog, coor_select)
                if dist <= 1.5:
                    apart["info"]["distance"] = dist
                    apart["info"]["coordinates"] = [float(pos_analog.split(' ')[0]), float(pos_analog.split(' ')[1])]
                    list.append(apart)
    return list

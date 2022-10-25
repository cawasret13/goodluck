import time

import bs4
from fake_useragent import UserAgent
from requests_html import HTMLSession
from django.contrib.sites import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from requests.auth import HTTPBasicAuth
import requests
from bs4 import BeautifulSoup


# Здесь форма
class GetDataForm(APIView):
    def post(self, request, format=None):
        # Здесь пишем переменные которые мы должны получить
        data = {
            'metro': request.data.get('metro'),
            'way_get_metro': request.data.get('way'),
            'timeWay': request.data.get('timeWay'),
            'district': request.data.get('district'),

            'floors': request.data.get('floors'),
            'rooms_floor': request.data.get('rooms'),
            'type_house': request.data.get('typeHouse'),

            'num_rooms': request.data.get('numRoom'),
            'apartment_area': request.data.get('areaRoom'),
            'kitchen_area': request.data.get('areaKitchen'),
            'state_apart': request.data.get('stateApart'),
        }
        return Response(coefficient_calculation(data), status=status.HTTP_201_CREATED)


def coefficient_calculation(data):
    url = 'https://msk.etagi.com/realty/'
    resurce = requests.get(url, headers={"User-Agent": UserAgent().Firefox}, timeout=5)
    soup = BeautifulSoup(resurce.text, 'lxml')
    list_apart = soup.find_all('div', class_="y8VEv templates-object-card etagiSlider__parent")
    # print(list_apart)
    for apart in list_apart:
        price = apart.find('span', class_="eypL8")
        print(price.text)
    return 'dd'

from random import random

from rest_framework.views import APIView

from personal_area.models import PersonalData


# Create your views here.
class createUser(APIView):
    def post(self, request, format=None):
        id_user = ''
        login = request.data.get('login')
        pas = request.data.get('pas')
        name = request.data.get('name')
        lastname = request.data.get('lastname')
        for x in range(16):
            id_user = id_user + random.choice(
                list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_'))
        data = PersonalData({
            "id": id_user,
            "login": login,
            "pas": pas,
            "name": name,
            "lastname": lastname
        })
        data.save()
        return id_user


class GetUser(APIView):
    def post(self, request, format=False):
        login = request.data.get('login')
        pas = request.data.get('pas')
        data = PersonalData.objects.get(login=login, pas=pas)
        id_user = data.id
        return id_user

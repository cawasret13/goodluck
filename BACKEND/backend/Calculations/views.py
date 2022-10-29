from random import random
from rest_framework.response import Response
from rest_framework.views import APIView
from Calculations.models import FileData
import random
import openpyxl
from Calculations.selectionAnalogues import AnalogsMirCvartir, AnalogsMove


class LoadFile(APIView):
    def post(self, request):
        id_session = ''
        for x in range(32):
            id_session = id_session + random.choice(
                list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM/*-+.{}[]|'))
        pr = FileData(
            file=request.data.get('file'),
            id_user=request.data.get('id_user'),
            path='',
            id_session=id_session,
        )
        pr.save()
        obj = FileData.objects.get(id_session=id_session)
        obj.path = pr.file.name
        obj.save()
        return Response({"id_session": id_session, "data": read_open(id_session)})


def read_open(id_session):
    lot = []
    id = 0
    path = FileData.objects.get(id_session=id_session).path
    wookbook = openpyxl.load_workbook(path)
    worksheet = wookbook.active
    start_position_y = 0
    for x in range(1, worksheet.max_row + 1):
        if ((worksheet.cell(row=x, column=1).value != None) &
                (worksheet.cell(row=x, column=1).value == 'Местоположение')):
            start_position_y = x + 1
    for y in range(start_position_y, worksheet.max_row + 1):
        if (worksheet.cell(row=y, column=1).value != None):
            data = {
                "id_Apart": id,
                "location": worksheet.cell(row=y, column=1).value,
                "numRooms": worksheet.cell(row=y, column=2).value,
                "segment": worksheet.cell(row=y, column=3).value,
                "floorsHouse": worksheet.cell(row=y, column=4).value,
                "materialWall": worksheet.cell(row=y, column=5).value,
                "floor": worksheet.cell(row=y, column=6).value,
                "areaApart": worksheet.cell(row=y, column=7).value,
                "areaKitchen": worksheet.cell(row=y, column=8).value,
                "balcony": worksheet.cell(row=y, column=9).value,
                "proxMetro": worksheet.cell(row=y, column=10).value,
                "structure": worksheet.cell(row=y, column=11).value,
            }
            id += 1
            lot.append(data)
    obj = FileData.objects.get(id_session=id_session)
    obj.data = lot
    obj.save()
    return lot


class selectionAnalogs(APIView):

    def post(self, request, format=None):
        id_session = request.data.get('id_session')
        id_user = request.data.get('id_user')
        id_referens = request.data.get('id_ref')
        arrFile = FileData.objects.get(id_user=id_user, id_session=id_session)
        arrFile.id_reference = id_referens
        arrFile.save()
        print(id_session, id_user, id_referens)
        return Response("0")

    def get(self, request, format=None):
        Apart = []
        id_session = self.request.query_params.get('id_session')
        id_session = '3koY4sacdBVbIAZM5WdQBI/7fweItBKg'
        Apart.append({"analog":AnalogsMirCvartir(id_session)})
        Apart.append({"analog":AnalogsMove(id_session)})
        return Response(Apart)

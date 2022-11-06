import ast
import time

from Calculations.LibSB import generateID, createFile
from Calculations.models import FileData


def calculate_price(id_session, id_reference, ids_analogues):
    _report = report = []
    print(ids_analogues)
    Analog_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Analog_Info.data_analogs)
    reference = ast.literal_eval(Analog_Info.data)[id_reference]
    _flag=[]
    for id_analog in ids_analogues:
        for _obj in data:
            for obj in _obj['resualt']['data']:
                if int(obj["info"]["id"]) == int(id_analog) and int(int(obj["info"]["id"]) not in _flag):
                    price = int(int(obj["info"]["price"]) / float(obj["info"]["area"]))
                    _report.append(calc_coeff(price, obj["info"], reference))
                    _flag.append(int(obj["info"]["id"]))
    _weight = 0
    for analogue_weight in _report:
        _weight += (1 / analogue_weight["size"])
    for analogue in _report:
        analogue["weight"] = round((1 / analogue["size"]) / _weight, 2)
    for n_analogue in _report:
        sum = 0
        for coef in _report:
            sum += (1/coef['size'])
        weight = round((1/n_analogue["size"])/sum, 2)
        n_analogue['weight'] = weight
    priceMeter = 0
    for price in _report:
        priceMeter += price['weight'] * price['price']
    report = {
        "id_ref": id_reference,
        "id_a": ids_analogues,
        "report": _report,
        "priceMeter": int(priceMeter),
        "price": int(int(priceMeter) * float(obj["info"]["area"])),
    }
    return report


def calc_coeff(_price, analogue, reference):
    print(analogue)
    price = _price - (4.5 * _price / 100)
    history = []
    history.append({"id": generateID(), "discription": "Корректировка на торг", "price": int(_price), "coef": -4.5})
    coef = 0
    if int(reference["floorsHouse"]) == int(reference["floor"]):
        if analogue["totalFloor"] == 1:
            coef = 3.2
        elif analogue["floor"] == analogue["totalFloor"]:
            coef = 0
        else:
            coef = -4.0
    elif int(reference["floor"]) == 1:
        if analogue["totalFloor"] == 1:
            coef = 0
        elif analogue["floor"] == analogue["totalFloor"]:
            coef = -3.1
        else:
            coef = -7.0
    else:
        if analogue["totalFloor"] == 1:
            coef = 7.5
        elif analogue["floor"] == analogue["totalFloor"]:
            coef = 4.2
        else:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id": generateID(), "discription": "Корректировка на этаж квартиры", "price": int(price), "coef": coef})
    area_ref = float(reference["areaApart"])
    area_ana = float(analogue["area"])
    if area_ref < 30:
        if area_ana < 30:
            coef = 0
        elif area_ana > 30 and area_ana <= 50:
            coef = 6
        elif area_ana > 50 and area_ana <= 65:
            coef = 14
        elif area_ana > 65 and area_ana <= 90:
            coef = 21
        elif area_ana > 90 and area_ana <= 120:
            coef = 28
        elif area_ana > 120:
            coef = 31
    elif area_ref > 30 and area_ref <= 50:
        if area_ana < 30:
            coef = -6
        elif area_ana > 30 and area_ana <= 50:
            coef = 0
        elif area_ana > 50 and area_ana <= 65:
            coef = 7
        elif area_ana > 65 and area_ana <= 90:
            coef = 14
        elif area_ana > 90 and area_ana <= 120:
            coef = 21
        elif area_ana > 120:
            coef = 24
    elif area_ref > 50 and area_ref <= 65:
        if area_ana < 30:
            coef = -12
        elif area_ana > 30 and area_ana <= 50:
            coef = -7
        elif area_ana > 50 and area_ana <= 65:
            coef = 0
        elif area_ana > 65 and area_ana <= 90:
            coef = 6
        elif area_ana > 90 and area_ana <= 120:
            coef = 13
        elif area_ana > 120:
            coef = 16
    elif area_ref > 65 and area_ref <= 90:
        if area_ana < 30:
            coef = -17
        elif area_ana > 30 and area_ana <= 50:
            coef = -12
        elif area_ana > 50 and area_ana <= 65:
            coef = -6
        elif area_ana > 65 and area_ana <= 90:
            coef = 0
        elif area_ana > 90 and area_ana <= 120:
            coef = 6
        elif area_ana > 120:
            coef = 9
    elif area_ref > 90 and area_ref <= 120:
        if area_ana < 30:
            coef = -22
        elif area_ana > 30 and area_ana <= 50:
            coef = -17
        elif area_ana > 50 and area_ana <= 65:
            coef = -11
        elif area_ana > 65 and area_ana <= 90:
            coef = -6
        elif area_ana > 90 and area_ana <= 120:
            coef = 0
        elif area_ana > 120:
            coef = 3
    elif area_ref > 120:
        if area_ana < 30:
            coef = -24
        elif area_ana > 30 and area_ana <= 50:
            coef = -19
        elif area_ana > 50 and area_ana <= 65:
            coef = -13
        elif area_ana > 65 and area_ana <= 90:
            coef = -8
        elif area_ana > 90 and area_ana <= 120:
            coef = -3
        elif area_ana > 120:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id": generateID(), "discription": "Корректировка на площадь", "price": int(price), "coef": coef})
    area_ref = float(reference["areaKitchen"])
    area_ana = float(analogue["areaKitchen"])
    if area_ref < 7:
        if area_ana < 7:
            coef = 0
        elif area_ana > 7 and area_ana <= 10:
            coef = -2.9
        elif area_ana > 10 and area_ana <= 15:
            coef = -8.3
    elif area_ref > 7 and area_ref <= 10:
        if area_ana < 7:
            coef = 3
        elif area_ana > 7 and area_ana <= 10:
            coef = 0
        elif area_ana > 10 and area_ana <= 15:
            coef = -5.5
    elif area_ref > 10 and area_ref <= 15:
        if area_ana < 7:
            coef = 9
        elif area_ana > 7 and area_ana <= 10:
            coef = 5.8
        elif area_ana > 10 and area_ana <= 15:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id": generateID(), "discription": "Корректировка на площадь кухни", "price": int(price), "coef": coef})
    if (reference["balcony"]).lower() == 'да':
        if (analogue["balcony"]).lower() == 'да':
            coef = 0
        else:
            coef = 5.3
    else:
        if (analogue["balcony"]).lower() == 'да':
            coef = -5
        else:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id": generateID(), "discription": "Корректировка на наличие балкона/лоджии", "price": int(price), "coef": coef})
    time = int(analogue["time"])
    if int(reference["proxMetro"]) < 5:
        if time < 5:
            coef = 0
        elif time > 5 and time <= 10:
            coef = 7
        elif time > 10 and time <= 15:
            coef = 12
        elif time > 15 and time <= 30:
            coef = 17
        elif time > 30 and time <= 60:
            coef = 24
        elif time > 60 and time <= 90:
            coef = 29
    elif int(reference["proxMetro"]) > 5 and int(reference["proxMetro"]) <= 10:
        if time < 5:
            coef = -7
        elif time > 5 and time <= 10:
            coef = 0
        elif time > 10 and time <= 15:
            coef = 4
        elif time > 15 and time <= 30:
            coef = 9
        elif time > 30 and time <= 60:
            coef = 15
        elif time > 60 and time <= 90:
            coef = 20
    elif int(reference["proxMetro"]) > 10 and int(reference["proxMetro"]) <= 15:
        if time < 5:
            coef = -11
        elif time > 5 and time <= 10:
            coef = -4
        elif time > 10 and time <= 15:
            coef = 0
        elif time > 15 and time <= 30:
            coef = 5
        elif time > 30 and time <= 60:
            coef = 11
        elif time > 60 and time <= 90:
            coef = 15
    elif int(reference["proxMetro"]) > 15 and int(reference["proxMetro"]) <= 30:
        if time < 5:
            coef = -15
        elif time > 5 and time <= 10:
            coef = -8
        elif time > 10 and time <= 15:
            coef = -5
        elif time > 15 and time <= 30:
            coef = 0
        elif time > 30 and time <= 60:
            coef = 6
        elif time > 60 and time <= 90:
            coef = 10
    elif int(reference["proxMetro"]) > 30 and int(reference["proxMetro"]) <=60:
        if time < 5:
            coef = -19
        elif time > 5 and time <= 10:
            coef = -13
        elif time > 10 and time <= 15:
            coef = -10
        elif time > 15 and time <= 30:
            coef = -6
        elif time > 30 and time <= 60:
            coef = 0
        elif time > 60 and time <= 90:
            coef = 4
    elif int(reference["proxMetro"]) > 60 and int(reference["proxMetro"]) <=90:
        if time < 5:
            coef = -22
        elif time > 5 and time <= 10:
            coef = -17
        elif time > 10 and time <= 15:
            coef = -13
        elif time > 15 and time <= 30:
            coef = -9
        elif time > 30 and time <= 60:
            coef = -4
        elif time > 60 and time <= 90:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id":generateID(), "discription": "Корректировка на удаленность от метро", "price": int(price), "coef": coef})
    if reference["structure"] == "без отделки":
        if analogue["repair"] == "без отделки":
            coef = 0
        elif analogue["repair"] == "муниципальный ремонт":
            coef = -13400
        elif analogue["repair"] == "с современной отделкой":
            coef = -20100
    elif reference["structure"] == "муниципальный ремонт":
        if analogue["repair"] == "без отделки":
            coef = 13400
        elif analogue["repair"] == "муниципальный ремонт":
            coef = 0
        elif analogue["repair"] == "с современной отделкой":
            coef = -6700
    else:
        if analogue["repair"] == "без отделки":
            coef = 20100
        elif analogue["repair"] == "муниципальный ремонт":
            coef = 6700
        elif analogue["repair"] == "с современной отделкой":
            coef = 0
    clone_price = price
    price = price - coef
    clone_coef = round((coef*100)/clone_price, 1)
    history.append({"id":generateID(), "discription": "Корректировка на ремонт", "price": int(price), "coef": clone_coef})
    dif = max = size_coef = 0
    min = 100;
    for coef in history:
        size_coef += abs(coef["coef"])
        if coef["coef"] < min:
            min = float(coef["coef"])
        if coef["coef"] > max:
            max = float(coef["coef"])
    if max != 0:
        dif = max - min
    report = {
        "coefficient": history,
        "price": int(price),
        "size": size_coef,
        "difference": dif,
        "weight": 0,
    }
    return report

def newPrice(id_session, ref, index):
    data = FileData.objects.get(id_session=id_session)
    _rep = []
    for rep in ast.literal_eval(data.report):
        if int(rep['id_ref']) == int(ref):
           price = 0
           for report in rep['report']:
               for coef in report['coefficient']:
                   if report['coefficient'].index(coef) != 0:
                        coef['price'] = (int(report['coefficient'][report['coefficient'].index(coef) -1]["price"]) + int(float(coef["coef"]) *  int(report['coefficient'][report['coefficient'].index(coef) -1]["price"]) / 100))
                        price = coef['price']
               report['price'] = price
        _rep.append(rep)
    min = 1000
    max = 0
    all_w = 0
    price_meter = 0
    for rep in _rep:
        for report in rep['report']:
            size = 0
            for coef in report['coefficient']:
                if float(coef['coef']) > max:
                    max = float(coef['coef'])
                if float(coef['coef']) < min:
                    min = float(coef['coef'])
                size += abs(float(coef['coef']))
            report['size'] = size
            if max != 0:
                dif = max - min
            else:
                dif = 0
            report['difference'] = dif
            all_w+= 1/float(report['size'])
        for report in rep['report']:
            report['weight'] = (round((1/report['size'])/all_w, 2))
            price_meter += report['weight'] * report['price']
        rep['priceMeter'] = int(price_meter)
        refs = ast.literal_eval(data.data)[int(rep['id_ref'])]['areaApart'] * rep['priceMeter']
        rep['price'] = refs
    data.report =_rep
    data.save()
    return _rep

def Pool(id_session):
    data = FileData.objects.get(id_session=id_session)
    _file = ast.literal_eval(data.data)
    Report = ast.literal_eval(data.report)
    _objects =[]
    for object in Report:
        for file in _file:
            if int(file["numRooms"]) == int(_file[object['id_ref']]["numRooms"]):
                file["price"] = int(float(file['areaApart']) * int(object['priceMeter']))
                _objects.append(file)

    data.NewData = _objects
    data.EndPool = createFile(id_session)
    data.save()
    return _objects

import ast
from Calculations.models import FileData


def calculate_price(id_session):
    _report = report = []
    Analog_Info = FileData.objects.filter(id_session=id_session)[0]
    data = ast.literal_eval(Analog_Info.data_analogs)
    reference = ast.literal_eval(Analog_Info.data)[Analog_Info.id_reference]
    for id_analog in ast.literal_eval(Analog_Info.ids_analogs):
        for obj in data:
            if int(obj["info"]["id"]) == int(id_analog):
                price = int(int(obj["info"]["price"]) / float(obj["info"]["area"]))
                _report.append(calc_coeff(price, obj["info"], reference))
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
        "report": _report,
        "priceMeter": priceMeter,
        "price": priceMeter * float(obj["info"]["area"]),
    }
    return report


def calc_coeff(_price, analogue, reference):
    price = _price - (4.5 * _price / 100)
    history = []
    history.append({"id":analogue["id"], "discription": "Корректировка на торг", "price": int(_price), "coef": -4.5})
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
    history.append({"id":analogue["id"], "discription": "Корректировка на этаж квартиры", "price": int(price), "coef": coef})
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
    history.append({"id":analogue["id"], "discription": "Корректировка на площадь", "price": int(price), "coef": coef})
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
    history.append({"id":analogue["id"], "discription": "Корректировка на площадь кухни", "price": int(price), "coef": coef})
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
    history.append({"id":analogue["id"], "discription": "Корректировка на наличие балкона/лоджии", "price": int(price), "coef": coef})

    if reference["proxMetro"] < 5:
        if analogue["time"] < 5:
            coef = 0
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = 7
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = 12
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = 17
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = 24
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 29
    elif reference["proxMetro"] > 5 and reference["proxMetro"] <= 10:
        if analogue["time"] < 5:
            coef = -7
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = 0
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = 4
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = 9
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = 15
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 20
    elif reference["proxMetro"] > 10 and reference["proxMetro"] <= 15:
        if analogue["time"] < 5:
            coef = -11
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = -4
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = 0
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = 5
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = 11
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 15
    elif reference["proxMetro"] > 15 and reference["proxMetro"] <= 30:
        if analogue["time"] < 5:
            coef = -15
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = -8
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = -5
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = 0
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = 6
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 10
    elif reference["proxMetro"] > 30 and reference["proxMetro"] <=60:
        if analogue["time"] < 5:
            coef = -19
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = -13
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = -10
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = -6
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = 0
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 4
    elif reference["proxMetro"] > 60 and reference["proxMetro"] <=90:
        if analogue["time"] < 5:
            coef = -22
        elif analogue["time"] > 5 and analogue["time"] <= 10:
            coef = -17
        elif analogue["time"] > 10 and analogue["time"] <= 15:
            coef = -13
        elif analogue["time"] > 15 and analogue["time"] <= 30:
            coef = -9
        elif analogue["time"] > 30 and analogue["time"] <= 60:
            coef = -4
        elif analogue["time"] > 60 and analogue["time"] <= 90:
            coef = 0
    price = price + (coef * price / 100)
    history.append({"id":analogue["id"], "discription": "Корректировка на удаленность от метро", "price": int(price), "coef": coef})
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
    history.append({"id":analogue["id"], "discription": "Корректировка на ремонт", "price": int(price), "coef": clone_coef})
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

import xlrd
from main.models import Bike, Company


def insert_entries():
    workbook = xlrd.open_workbook('bikedekho.xls')
    sheet = workbook.sheet_by_index(0)
    attrs = ['id', 'company_name_id', 'model_name', 'name', 'mileage', 'price',
             'displacement', 'front_brake', 'back_brake', 'tank_capacity', 'bhp', 'img_src']
    for j in range(1, sheet.nrows):
        d, p = {}, 0
        for k in range(sheet.ncols):
            v = sheet.cell_value(0, k)
            if p < len(attrs) and v == attrs[p]:
                d[v] = sheet.cell_value(j, k)
                if not d[v]:
                    d[v] = None
                p += 1
        process(d)
        print(d)
        Bike.objects.create(**d)


def process(d):
    d['company_name_id'] = Company.objects.get(company_name=d['company_name_id'])
    if d['price'] and not isinstance(d['price'], float):
        s = d['price'][3:]
        p = []
        for x in s:
            if x == '.' or x.isnumeric():
                p.append(x)
        if ''.join(p):
            d['price'] = float(''.join(p))
        else:
            d['price'] = None
        if 'Lakh' in s:
            d['price'] *= 100000
    if d['mileage'] and not isinstance(d['mileage'], float):
        s = d['mileage']
        p = []
        for x in s:
            if x == '.' or x.isnumeric():
                p.append(x)
        if ''.join(p):
            d['mileage'] = float(''.join(p))
        else:
            d['mileage'] = None

    if d['tank_capacity'] and not isinstance(d['tank_capacity'], float):
        s = d['tank_capacity']
        p = []
        for x in s:
            if x == '.' or x.isnumeric():
                p.append(x)
        if ''.join(p):
            d['tank_capacity'] = float(''.join(p))
        else:
            d['tank_capacity'] = None
    if d['displacement'] and not isinstance(d['displacement'], float):
        s = d['displacement']
        p = []
        for x in s:
            if x == '.' or x.isnumeric():
                p.append(x)
        if ''.join(p):
            d['displacement'] = float(''.join(p))
        else:
            d['displacement'] = None

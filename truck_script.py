import xlrd
from main.models import Truck, Company


def insert_entries():
    workbook = xlrd.open_workbook('truck.xls')
    sheet = workbook.sheet_by_index(0)
    attrs = ['company_name_id',   'name', 'img_src', 'price', 'num_tyre', 'fuel_type', 'mileage', 
    'transmission',
             'displacement', 'payload', 'tank_capacity', 'bhp']
    for j in range(1, sheet.nrows):
        d, p = {}, 0
        for k in range(sheet.ncols):
            v = sheet.cell_value(0, k)
            if p < len(attrs) and v == attrs[p]:
                d[v] = sheet.cell_value(j, k)
                if not d[v]:
                    d[v] = None
                p += 1
        print(d)
        process(d)
        Truck.objects.create(**d)


def process(d):
    d['company_name_id'] = Company.objects.get(company_name=d['company_name_id'])
    if d['price'] and not isinstance(d['price'], float):
        s = d['price']
        if '-' in d['price']:
            s = d['price'][d['price'].index('-') + 1:]
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
        elif 'Cr' in s:
            d['price'] *= 10000000
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
    if d['payload'] and not isinstance(d['payload'], float):
        s = d['payload']
        p = []
        for x in s:
            if x == '.' or x.isnumeric():
                p.append(x)
        if ''.join(p):
            d['payload'] = float(''.join(p))
        else:
            d['payload'] = None

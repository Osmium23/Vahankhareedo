from . import models

model = {'bike': models.Bike, 'car': models.Car, 'truck' : models.Truck, 'bus': models.Bus}


def get_model(x):
    return model[x]


def get_titles(x):
    if x == 'bike':
        return {'company_name_id_id': ('Company', ''),
                'name': ('Name', ''), 'model_name': ('Model name', ''), 'displacement' :
                    ('Displacement', 'cc'), 'price': ('Price', ''),
        'mileage': ('Mileage', 'kmpl'), 'front_brake': ('Front Brake', ''), 'back_brake': ('Back Brake', ''),
                'tank_capacity': ('Tank capacity', 'L'), 'bhp': ('BHP', '')}
    elif x == 'car':
        return {'company_name_id_id': ('Company', ''), 'fuel_type': ('Fuel Type', ''),
                'name': ('Name', ''), 'model_name': ('Model name', ''), 'transmission':('Transmission', ''),
                'displacement' :
                    ('Displacement', 'cc'), 'price': ('Price', ''), 'gear_box':('Gear Box', ''),
        'mileage': ('Mileage', 'kmpl'), 'front_brake': ('Front Brake', ''), 'back_brake': ('Back Brake', ''),
                'tank_capacity': ('Tank capacity', 'L'), 'bhp': ('BHP', '')}
    elif x == 'truck':
        return {'company_name_id_id': ('Company', ''),
                'name': ('Name', ''), 'displacement' :
                    ('Displacement', 'cc'), 'price': ('Price', ''),
        'mileage': ('Mileage', 'kmpl'), 'num_tyre': ('Number of tyres', ''), 'payload': ('Payload', 'kgs'),
                'tank_capacity': ('Tank capacity', 'L'), 'bhp': ('BHP', '')}
    else:
        return {'company_name_id_id': ('Company', ''),
                'name': ('Name', ''), 'displacement' :
                    ('Displacement', 'cc'), 'price': ('Price', ''),
        'mileage': ('Mileage', 'kmpl'), 'seating_capacity': ('Seating Capacity', ''),
                'tank_capacity': ('Tank capacity', 'L'), 'bhp': ('BHP', '')}

def get_type(v):
    try:
        return v.bike, 'bike'
    except:
        try :
            return v. car, 'car'
        except:
            try:
                return v.truck, 'truck'
            except:
                return v.bus, 'bus'
from django.contrib.auth import models as auth_models
from django.db import models as db_models
from phonenumber_field import modelfields as phone_models

from . import signals


class Company(db_models.Model):
    company_name = db_models.CharField(max_length=20, primary_key=True)
    website = db_models.CharField(max_length=100)
    address = db_models.CharField(max_length=100)
    contact1 = phone_models.PhoneNumberField()
    contact2 = phone_models.PhoneNumberField()


class Customer(db_models.Model):
    user = db_models.OneToOneField(auth_models.User, on_delete=db_models.CASCADE)
    contact = phone_models.PhoneNumberField(blank=True)


class Vehicle(db_models.Model):
    vehicle_id = db_models.AutoField(primary_key=True)
    company_name_id = db_models.ForeignKey(Company, on_delete=db_models.CASCADE)
    rating = db_models.FloatField(default=0.0)
    nvis = db_models.IntegerField(default=0)
    nrated = db_models.IntegerField(default=0)


class BrakeType(db_models.TextChoices):
    DISC = 'Disc'
    DRUM = 'Drum'


class Bike(Vehicle):
    model_name = db_models.CharField(max_length=75)
    name = db_models.CharField(max_length=100)
    mileage = db_models.IntegerField(null=True, blank=True)
    price = db_models.IntegerField()
    displacement = db_models.FloatField(null=True, blank=True)
    front_brake = db_models.CharField(max_length=4, choices=BrakeType.choices)
    back_brake = db_models.CharField(max_length=4, choices=BrakeType.choices)
    tank_capacity = db_models.FloatField(null=True, blank=True)
    bhp = db_models.CharField(max_length=50, null=True, blank=True)
    img_src = db_models.CharField(max_length=150, null=True, blank=True)


class Car(Vehicle):
    model_name = db_models.CharField(max_length=75)
    name = db_models.CharField(max_length=100)
    price = db_models.IntegerField(null=True, blank=True)
    fuel_type=db_models.CharField(max_length=10)
    mileage = db_models.IntegerField(null=True, blank=True)
    transmission = db_models.CharField(max_length=10)
    displacement = db_models.IntegerField(null=True, blank=True)
    gear_box = db_models.CharField(max_length=10, null=True, blank=True)
    seating_capacity = db_models.IntegerField(null=True, blank=True)
    front_brake = db_models.CharField(max_length=10, null=True, blank=True, default='Drum')
    back_brake = db_models.CharField(max_length=10, null=True, blank=True, default='Drum')
    tank_capacity = db_models.FloatField(null=True, blank=True)
    bhp = db_models.CharField(max_length=50, null=True, blank=True)
    img_src = db_models.CharField(max_length=150, null=True, blank=True)


class Truck(Vehicle):
    name = db_models.CharField(max_length=100)
    price = db_models.IntegerField(null=True, blank=True)
    num_tyre  = db_models.IntegerField(null=True, blank=True)
    fuel_type=db_models.CharField(max_length=10)
    mileage = db_models.IntegerField(null=True, blank=True)
    transmission = db_models.CharField(max_length=10)
    displacement = db_models.IntegerField(null=True, blank=True)
    payload = db_models.FloatField(null=True, blank=True)
    tank_capacity = db_models.FloatField(null=True, blank=True)
    bhp = db_models.CharField(max_length=50, null=True, blank=True)
    img_src = db_models.CharField(max_length=150, null=True, blank=True)

class Bus(Vehicle):
    name = db_models.CharField(max_length=100)
    price = db_models.IntegerField(null=True, blank=True)
    mileage = db_models.IntegerField(default=0, null=True, blank=True)
    bhp = db_models.CharField(max_length=50, null=True, blank=True)
    tank_capacity = db_models.FloatField(null=True, blank=True)
    displacement = db_models.IntegerField(null=True, blank=True)
    seating_capacity = db_models.IntegerField(null=True, blank=True)
    img_src = db_models.CharField(max_length=150, null=True, blank=True)

class Favourite(db_models.Model):
    vehicle_id = db_models.ForeignKey(Vehicle, on_delete=db_models.CASCADE)
    user_id = db_models.ForeignKey(Customer, on_delete=db_models.CASCADE)

    class Meta:
        unique_together = ('vehicle_id', 'user_id')


class Review(db_models.Model):
    vehicle_id = db_models.ForeignKey(Vehicle, on_delete=db_models.CASCADE)
    user_id = db_models.ForeignKey(Customer, on_delete=db_models.CASCADE)
    content = db_models.TextField(null=True, blank=True) 
    rating = db_models.IntegerField(default=0)

    class Meta:
        unique_together = ('vehicle_id', 'user_id')

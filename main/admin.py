from django.contrib import admin

from . import models

admin.site.register(models.Company)
admin.site.register(models.Customer)
admin.site.register(models.Bike)
admin.site.register(models.Car)
admin.site.register(models.Truck)
admin.site.register(models.Bus)
admin.site.register(models.Favourite)
admin.site.register(models.Review)
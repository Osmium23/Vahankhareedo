import random
from main import models

ls = [1, 2, 3, 4, 5]
for x in models.Customer.objects.all():
    v = random.randrange(5, 35)
    for j in range(v):
        y = random.randrange(1, 100)
        try:
            models.Review.objects.create(user_id=x, vehicle_id=models.Vehicle.objects.get(vehicle_id=y), content=None, rating=random.randrange(1, 6))
        except:
            pass
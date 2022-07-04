from django import dispatch
from django.contrib.auth import models as auth_models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals

from . import models


@dispatch.receiver(signals.post_save, sender=auth_models.User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        models.Customer.objects.create(user=instance)
    try:
        instance.customer.save()
    except ObjectDoesNotExist:
        pass

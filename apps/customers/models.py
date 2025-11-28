from django.conf import settings
from django.db import models

from apps.cars.models import Cars
from apps.common.fields import IDField, MoneyField


class Profiles(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=17)
    balance = MoneyField(default=0)
    reserved_balance = MoneyField(default=0)


class Offers(models.Model):
    STATUSES = (
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
        ("COMPLETED", "COMPLETED"),
    )

    id = IDField()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="offers", on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, related_name="offers", on_delete=models.CASCADE)
    max_price = MoneyField()
    status = models.CharField(max_length=32, choices=STATUSES, default="ACTIVE")

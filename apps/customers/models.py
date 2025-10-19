from django.db import models

from apps.common.models import AbstractBaseModel


class Customers(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    email = models.TextField()
    password = models.TextField()


class Profiles(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField()
    balance = models.FloatField()


class Offers(models.Model):
    id = models.UUIDField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    model = models.TextField()
    max_price = models.FloatField()

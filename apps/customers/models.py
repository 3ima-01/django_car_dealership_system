from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import AbstractBaseModel


class Customers(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)


class Profiles(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=17)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])


class Offers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    model = models.CharField(max_length=64)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

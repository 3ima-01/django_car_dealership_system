from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import AbstractBaseModel


class Customers(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField()
    password = models.TextField()


class Profiles(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=17)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])


class Offers(models.Model):
    id = models.UUIDField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

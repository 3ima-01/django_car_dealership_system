from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from apps.accounts.models import Customers


class Profiles(models.Model):
    customer_id = models.OneToOneField(Customers, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=17)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)


class Offers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    model = models.CharField(max_length=64)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

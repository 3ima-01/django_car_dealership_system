from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models


class Profiles(models.Model):
    customer = models.OneToOneField("accounts.Customers", related_name="profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=17)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    reserved_balance = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )


class Offers(models.Model):
    STATUSES = (
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
        ("COMPLETED", "COMPLETED"),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer = models.ForeignKey("accounts.Customers", related_name="offers", on_delete=models.CASCADE)
    model = models.CharField(max_length=64)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=32, choices=STATUSES, default="ACTIVE")

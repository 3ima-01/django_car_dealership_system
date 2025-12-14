from django.db import models

from apps.cars.models import Cars
from apps.common.fields import IDField, MoneyField


class Profiles(models.Model):
    customer = models.OneToOneField("accounts.Customers", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=17)
    balance = MoneyField()
    reserved_balance = MoneyField()

    objects = models.Manager()

    class Meta:
        db_table = "profiles"


class Offers(models.Model):
    STATUSES = (
        ("ACTIVE", "ACTIVE"),
        ("CANCELED", "CANCELED"),
        ("COMPLETED", "COMPLETED"),
    )

    id = IDField()
    customer = models.ForeignKey("accounts.Customers", on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    max_price = MoneyField()
    status = models.CharField(max_length=32, choices=STATUSES, default="ACTIVE")

    objects = models.Manager()

    class Meta:
        db_table = "offers"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(max_price__gt=0),
                name="max_price_positive",
            ),
        ]

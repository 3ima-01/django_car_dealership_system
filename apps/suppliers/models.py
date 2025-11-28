from django.db import models

from apps.autoshows.models import AutoShows
from apps.cars.models import Cars
from apps.common.fields import IDField, MoneyField, PercentField
from apps.common.models import AbstractBaseModel


class Suppliers(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)


class SuppliersStock(AbstractBaseModel):
    id = IDField()
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = MoneyField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["car_id", "supplier_id"], name="unique_car_supplier")]


class SuppliersPromotions(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = PercentField
    cars = models.ForeignKey(SuppliersStock, on_delete=models.CASCADE)
    autoshow = models.ForeignKey(AutoShows, on_delete=models.CASCADE)


class SuppliersSales(models.Model):
    id = IDField()
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    autoshow = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    promotion = models.ForeignKey(SuppliersPromotions, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True)
    total_price = MoneyField()

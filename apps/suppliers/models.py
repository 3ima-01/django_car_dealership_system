from uuid import uuid4

from django.db import models

from apps.autoshows.models import AutoShows
from apps.cars.models import Cars
from apps.common.models import AbstractBaseModel


class Suppliers(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)


class SuppliersStock(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["car_id", "supplier_id"], name="unique_car_supplier")]


class SuppliersPromotions(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = models.IntegerField()
    cars_id = models.ForeignKey(SuppliersStock, on_delete=models.CASCADE)
    autoshow_id = models.UUIDField(null=True)


class SuppliersSales:
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    car_id = models.ForeignKey(SuppliersStock, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(SuppliersPromotions, on_delete=models.CASCADE)
    date = models.DateField()
    total_price = models.FloatField()

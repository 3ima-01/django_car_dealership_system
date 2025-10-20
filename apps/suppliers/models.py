from django.db import models

from apps.autoshows.models import AutoShowsCars
from apps.common.models import AbstractBaseModel, Cars


# Create your models here.
class Suppliers(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class SuppliersCars(models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    suppliers_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


class SuppliersPromotions(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = models.IntegerField()
    cars_id = models.ForeignKey(SuppliersCars, on_delete=models.CASCADE)
    autoshow_id = models.UUIDField(null=True)


class SuppliersSales:
    id = models.UUIDField(primary_key=True)
    supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    autoshow_id = models.ForeignKey(AutoShowsCars, on_delete=models.CASCADE)
    car_id = models.ForeignKey(SuppliersCars, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(SuppliersPromotions, on_delete=models.CASCADE)
    date = models.DateField()
    total_price = models.FloatField()

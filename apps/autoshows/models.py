from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import AbstractBaseModel, Cars
from apps.customers.models import Customers


class AutoShows(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    car_preferences = models.JSONField(null=True, default=dict)


class AutoShowsCars(models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])


class AutoShowsPromotions(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = models.IntegerField(validators=[MinValueValidator(0)])
    cars_id = models.ForeignKey(AutoShowsCars, on_delete=models.CASCADE)
    autoshow_id = models.UUIDField(null=True)


class AutoShowsSales(models.Model):
    id = models.UUIDField(primary_key=True)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    car_id = models.ForeignKey(AutoShowsCars, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(AutoShowsPromotions, on_delete=models.CASCADE)
    date = models.DateField()
    total_price = models.FloatField(validators=[MinValueValidator(0)])

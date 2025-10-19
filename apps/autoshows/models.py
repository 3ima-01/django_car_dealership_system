from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.common.models import AbstractBaseModel, Cars
from apps.customers.models import Customers


class AutoShows(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    geo = models.TextField()
    balance = models.FloatField()
    car_preferences = models.JSONField(null=True, default=dict)


class AutoShowsCars(models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


class AutoShowsPromotions(AbstractBaseModel):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = models.IntegerField()
    cars_id = models.ForeignKey(AutoShowsCars, on_delete=models.CASCADE)
    autoshow_id = models.UUIDField(null=True)


class AutoShowsSales(models.Model):
    id = models.UUIDField(primary_key=True)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    car_id = models.ForeignKey(AutoShowsCars, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(AutoShowsPromotions, on_delete=models.CASCADE)
    date = models.DateField()
    total_price = models.FloatField()

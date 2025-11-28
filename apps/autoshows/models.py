from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.cars.models import Cars
from apps.common.fields import IDField, MoneyField, PercentField
from apps.common.models import AbstractBaseModel


class AutoShows(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    markup_percent = PercentField(default=10)
    balance = MoneyField(default=0)
    car_preferences = models.JSONField(null=True, default=dict)


class AutoShowsStock(AbstractBaseModel):
    id = IDField()
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    autoshow = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = MoneyField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["car_id", "autoshow_id"], name="unique_car_autoshow")]


class AutoShowsPromotions(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = PercentField()
    cars = models.ForeignKey(AutoShowsStock, on_delete=models.CASCADE)
    autoshow = models.ForeignKey(AutoShows, on_delete=models.CASCADE)


class AutoShowsSales(models.Model):
    id = IDField()
    autoshow = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    promotion = models.ForeignKey(AutoShowsPromotions, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True)
    total_price = MoneyField()

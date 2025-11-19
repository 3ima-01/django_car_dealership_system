from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from apps.cars.models import Cars
from apps.common.models import AbstractBaseModel


class AutoShows(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    car_preferences = models.JSONField(null=True, default=dict)


class AutoShowsStock(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["car_id", "autoshow_id"], name="unique_car_autoshow")]


class AutoShowsPromotions(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    percent = models.IntegerField(validators=[MinValueValidator(0)])
    cars_id = models.ForeignKey(AutoShowsStock, on_delete=models.CASCADE)
    autoshow_id = models.UUIDField(null=True)


class AutoShowsSales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    autoshow_id = models.ForeignKey(AutoShows, on_delete=models.CASCADE)
    customer_id = models.ForeignKey("accounts.Customers", on_delete=models.CASCADE)
    car_id = models.ForeignKey(AutoShowsStock, on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(AutoShowsPromotions, on_delete=models.CASCADE)
    date = models.DateField()
    total_price = models.FloatField(validators=[MinValueValidator(0)])

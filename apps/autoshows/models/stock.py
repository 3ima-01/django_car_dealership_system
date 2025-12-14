from django.db import models

from apps.common.fields import IDField, MoneyField
from apps.common.models import AbstractBaseModel


class Stock(AbstractBaseModel):
    id = IDField()
    car = models.ForeignKey("cars.Cars", on_delete=models.CASCADE, related_name="autoshows_stock_car")
    autoshow = models.ForeignKey("autoshows.AutoShow", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = MoneyField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.autoshow.title} | {self.car} | {self.quantity}"

    class Meta:
        db_table = "autoshows_stock"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

        constraints = [models.UniqueConstraint(fields=["car_id", "autoshow_id"], name="unique_car_autoshow")]

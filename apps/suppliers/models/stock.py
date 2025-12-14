from django.db import models

from apps.common.fields import IDField, MoneyField
from apps.common.models import AbstractBaseModel


class Stock(AbstractBaseModel):
    id = IDField()
    car = models.ForeignKey(
        "cars.Cars",
        on_delete=models.CASCADE,
        related_name="suppliers_stock_car",
    )
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.CASCADE,
        related_name="stock",
    )
    quantity = models.PositiveIntegerField()
    price = MoneyField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.supplier.title} - {self.car.brand}-{self.car.model}({self.quantity}) - {self.price}"

    class Meta:
        db_table = "suppliers_stock"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

        constraints = [
            models.UniqueConstraint(
                fields=["car_id", "supplier_id"],
                name="suppliers_stock_car_unique",
            )
        ]

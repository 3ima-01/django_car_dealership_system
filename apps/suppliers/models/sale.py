from django.db import models

from apps.common.fields import IDField, MoneyField
from apps.common.models import AbstractBaseModel


class Sale(AbstractBaseModel):
    id = IDField()
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.CASCADE,
        related_name="suppliers_sales",
    )
    autoshow = models.ForeignKey(
        "autoshows.AutoShow",
        on_delete=models.CASCADE,
        related_name="suppliers_sales",
    )
    car = models.ForeignKey(
        "cars.Cars",
        on_delete=models.CASCADE,
        related_name="suppliers_sales_car",
    )
    discount = models.ForeignKey(
        "suppliers.Discount",
        on_delete=models.CASCADE,
        null=True,
        related_name="sales",
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units sold")
    price_per_unit = MoneyField(help_text="Unit price WITHOUT discount")
    discounted_price_per_unit = MoneyField(help_text="Discounted unit price")
    total_price = MoneyField()

    class Meta:
        db_table = "suppliers_sales"
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

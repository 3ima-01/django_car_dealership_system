from django.db import models

from apps.common.fields import IDField, MoneyField
from apps.common.models import AbstractBaseModel


class Sale(AbstractBaseModel):
    id = IDField()
    autoshow = models.ForeignKey("autoshows.AutoShow", on_delete=models.CASCADE, related_name="autoshows_sales")
    customer = models.ForeignKey("accounts.Customers", on_delete=models.PROTECT)
    car = models.ForeignKey("cars.Cars", on_delete=models.PROTECT, related_name="autoshows_sales_car")
    discount = models.ForeignKey("autoshows.Discount", null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units sold")
    price_per_unit = MoneyField(help_text="Unit price WITHOUT discount")
    discounted_price_per_unit = MoneyField(help_text="Discounted unit price")
    total_price = MoneyField()

    objects = models.Manager()

    class Meta:
        db_table = "autoshows_sales"
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

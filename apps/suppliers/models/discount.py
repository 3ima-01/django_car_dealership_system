from typing import Any
from uuid import UUID

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from apps.common.fields import IDField
from apps.common.models import AbstractBaseModel


class DiscountManager(models.Manager):
    @transaction.atomic()
    def create_discount(self, supplier_id: UUID, data: dict[str, Any]):
        car_ids = data.pop("cars", [])

        discount = self.create(
            supplier_id=supplier_id,
            **data,
        )

        if car_ids:
            discount.cars.set(car_ids)

        return discount


class Discount(AbstractBaseModel):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", _("Percent")
        FIXED = "fixed", _("Fixed")

    id = IDField()
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT,
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.CASCADE,
        related_name="discounts",
    )
    cars = models.ManyToManyField(
        "cars.Cars",
        related_name="suppliers_discount",
    )
    autoshow = models.ForeignKey(
        "autoshows.AutoShow",
        on_delete=models.CASCADE,
        related_name="suppliers_discount",
        blank=True,
        null=True,
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = DiscountManager()

    def __str__(self):
        return f"{self.name} - {self.discount_type}-{self.value} - {self.start_date}-{self.end_date}"

    class Meta:
        db_table = "suppliers_discount"
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

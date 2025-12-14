from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django_countries.fields import CountryField

from apps.common.fields import IDField
from apps.common.models import AbstractBaseModel
from apps.suppliers.models import Sale


class Supplier(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    country = CountryField()
    city = models.CharField(max_length=128)

    objects = models.Manager()

    def __str__(self):
        return f"{self.title} - {self.country} - {self.city}"

    @transaction.atomic
    def sell_to(self, autoshow, car, quantity=1, discount=None):
        """
        Sell car to autoshow
        """
        # 1. search car in self.stock
        stock = self.stock.select_for_update().get(car=car)

        # 2. quantity validation
        if quantity <= 0:
            raise ValidationError("Quantity must be positive")
        if stock.quantity < quantity:
            raise ValidationError(f"Insufficient stock. Available: {stock.quantity}, requested: {quantity}")

        # 2. calculating price with discount
        price_per_unit = stock.price.amount
        discounted_price_per_unit = price_per_unit

        if discount and discount.is_active:
            discounted_price_per_unit = self.calculate_discounted_price(price_per_unit, discount)

        total_price = discounted_price_per_unit * quantity

        # 3. create sale
        sale = Sale.objects.create(
            supplier=self,
            autoshow=autoshow,
            car=car,
            quantity=quantity,
            price_per_unit=price_per_unit,
            discounted_price_per_unit=discounted_price_per_unit,
            total_price=total_price,
            discount=discount,
        )

        # 4. update quantity
        stock.quantity = models.F("quantity") - 1
        stock.save(update_fields=["quantity"])

        return sale

    @staticmethod
    def calculate_discounted_price(price, discount):
        if discount.discount_type == discount.DiscountType.PERCENT:
            return price * (1 - discount.value / Decimal("100"))
        elif discount.discount_type == discount.DiscountType.FIXED:
            return max(price - discount.value, Decimal("0.01"))
        return price

    class Meta:
        db_table = "suppliers"
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

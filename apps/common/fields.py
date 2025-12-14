from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField as BaseMoneyField
from djmoney.money import Money


class IDField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("primary_key", True)
        kwargs.setdefault("default", uuid4)
        kwargs.setdefault("editable", False)
        super().__init__(*args, **kwargs)


class MoneyField(BaseMoneyField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("default", Money(0, "USD"))
        super().__init__(*args, **kwargs)


class PercentField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)
        validators = list(kwargs.get("validators", []))
        validators.append(MinValueValidator(0))
        validators.append(MaxValueValidator(100))
        super().__init__(*args, **kwargs)

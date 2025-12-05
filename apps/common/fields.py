from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class IDField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("primary_key", True)
        kwargs.setdefault("default", uuid4)
        kwargs.setdefault("editable", False)
        super().__init__(*args, **kwargs)


class MoneyField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)
        validators = kwargs.setdefault("validators", [])
        validators.append(MinValueValidator(0))
        super().__init__(*args, **kwargs)


class PercentField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)
        validators = kwargs.setdefault("validators", [])
        validators.append(MinValueValidator(0))
        validators.append(MaxValueValidator(100))
        super().__init__(*args, **kwargs)

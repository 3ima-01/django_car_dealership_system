from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.fields import IDField
from apps.common.models import AbstractBaseModel


class Cars(AbstractBaseModel):
    class EngineType(models.TextChoices):
        GASOLINE = "gasoline", _("Gasoline")
        DIESEL = "diesel", _("Diesel")
        ELECTRIC = "electric", _("Electric")
        HYBRID = "hybrid", _("Hybrid")

    class BodyType(models.TextChoices):
        SEDAN = "sedan", _("Sedan")
        HATCHBACK = "hatchback", _("Hatchback")
        SUV = "suv", _("SUV")
        COUPE = "coupe", _("Coupe")
        CONVERTIBLE = "convertible", _("Convertible")
        PICKUP = "pickup", _("Pickup")
        VAN = "van", _("Van")

    id = IDField()

    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1886, message="The first car was produced in 1886"),
            MaxValueValidator(
                datetime.now().year + 1, message="The year cannot be in the future (except next year for new cars)"
            ),
        ],
    )

    brand = models.CharField(
        max_length=64,
    )

    model = models.CharField(
        max_length=64,
    )

    color = models.CharField(
        max_length=64,
    )

    body_type = models.CharField(
        max_length=32,
        choices=BodyType.choices,
    )

    engine_type = models.CharField(
        max_length=16,
        choices=EngineType.choices,
        default=EngineType.GASOLINE,
    )
    horse_power = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    properties = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return f"{self.brand}-{self.model} {self.body_type} {self.engine_type}-{self.horse_power}HP - {self.year}"

    class Meta:
        db_table = "cars"
        verbose_name = "Car"
        verbose_name_plural = "Cars"
        ordering = ["-year", "brand", "model"]

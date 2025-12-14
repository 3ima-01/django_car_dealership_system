from django.db import models
from django_countries.fields import CountryField

from apps.common.fields import IDField, MoneyField, PercentField
from apps.common.models import AbstractBaseModel


class AutoShow(AbstractBaseModel):
    id = IDField()
    title = models.CharField(max_length=128)
    location = CountryField()
    markup_percent = PercentField()
    balance = MoneyField()

    objects = models.Manager()

    car_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Example: {'brand': ['BMW'], 'engine_type': ['electric'], 'min_year': 2020}",
    )

    def __str__(self):
        return f"{self.title} | {self.location}"

    class Meta:
        db_table = "autoshows"
        verbose_name = "AutoShow"
        verbose_name_plural = "AutoShows"

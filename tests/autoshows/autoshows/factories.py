import factory
from djmoney.money import Money
from faker import Faker

from apps.autoshows.models import AutoShow

fake = Faker()


class AutoShowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AutoShow

    title = factory.Faker("company")
    location = factory.Faker("country_code")
    markup_percent = factory.Faker("pyint", min_value=1, max_value=100)
    balance = factory.LazyFunction(
        lambda: Money(
            fake.pydecimal(left_digits=5, right_digits=2, positive=True),
            "USD",
        )
    )
    car_preferences = {"doors": 5}

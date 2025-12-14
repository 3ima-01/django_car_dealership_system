import factory
from djmoney.money import Money
from faker import Faker

from apps.suppliers.models import Stock
from tests.cars.factories import CarFactory
from tests.suppliers.suppliers.factories import SupplierFactory

fake = Faker()


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    car = factory.SubFactory(CarFactory)
    supplier = factory.SubFactory(SupplierFactory)

    quantity = factory.Faker("pyint", min_value=1, max_value=100)

    price = factory.LazyFunction(
        lambda: Money(
            fake.pydecimal(left_digits=5, right_digits=2, positive=True, max_value=5_000),
            "USD",
        )
    )

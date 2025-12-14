from datetime import timedelta, timezone

import factory
from factory import Faker, LazyAttribute, PostGeneration
from faker import Faker as RealFaker

from apps.suppliers.models import Discount
from tests.autoshows.autoshows.factories import AutoShowFactory
from tests.cars.factories import CarFactory
from tests.suppliers.suppliers.factories import SupplierFactory


class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount
        skip_postgeneration_save = True

    name = Faker("word", ext_word_list=["Summer Sale", "Clearance", "VIP Deal", "New Stock", "Loyalty Bonus"])
    description = Faker("sentence", nb_words=10)
    discount_type = Faker("random_element", elements=["percent", "fixed"])

    # value depends on the type of discount
    @LazyAttribute
    def value(self):
        fake = RealFaker()
        if self.discount_type == "percent":
            return fake.pydecimal(left_digits=2, right_digits=2, min_value=1, max_value=99)
        return fake.pydecimal(left_digits=5, right_digits=2, min_value=10, max_value=2000)

    supplier = factory.SubFactory(SupplierFactory)
    autoshow = factory.Maybe(
        Faker("pybool", truth_probability=50),  # chance that it`s will be AutoShow
        yes_declaration=factory.SubFactory(AutoShowFactory),
        no_declaration=None,
    )
    start_date = Faker("date_time_between", start_date="-30d", end_date="now", tzinfo=timezone.utc)

    @LazyAttribute
    def end_date(self):
        fake = RealFaker()
        days = fake.random_int(min=7, max=30)
        return self.start_date + timedelta(days=days)

    # M2M
    @PostGeneration
    def cars(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.cars.set(extracted)
        else:
            fake = RealFaker()
            car_count = fake.random_int(min=0, max=5)
            cars = CarFactory.create_batch(car_count)
            self.cars.set(cars)

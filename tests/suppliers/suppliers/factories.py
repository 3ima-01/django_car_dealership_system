import factory

from apps.suppliers.models.supplier import Supplier


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    title = factory.Faker("company")
    year = factory.Faker("pyint", min_value=1900, max_value=2025)
    country = factory.Faker("country_code")
    city = factory.Faker("city")

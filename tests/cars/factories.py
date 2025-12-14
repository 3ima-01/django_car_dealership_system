import factory

from apps.cars.models import Cars


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cars

    year = factory.Faker("pyint", min_value=1900, max_value=2025)
    brand = factory.Faker(
        "random_element",
        elements=["Toyota", "Ford", "Honda", "BMW", "Mercedes-Benz", "Audi", "Nissan", "Hyundai", "Kia"],
    )
    model = factory.Faker("lexify", text="??-???")
    color = factory.Faker("color_name")
    body_type = factory.Faker("random_element", elements=[choice[0] for choice in Cars.BodyType.choices])
    engine_type = factory.Faker("random_element", elements=[choice[0] for choice in Cars.EngineType.choices])
    horse_power = factory.Faker("pyint", min_value=100, max_value=800)
    properties = {"doors": 5}

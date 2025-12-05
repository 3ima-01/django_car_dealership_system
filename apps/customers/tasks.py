from apps.customers.services.offers import OffersService
from car_dealership_system.celery import app


@app.task(bind=True)
def buy_car_from_autoshow(self):
    OffersService().buy_car_from_autoshow()

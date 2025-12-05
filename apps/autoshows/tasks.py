from django.db import transaction

from apps.autoshows.services.autoshows import AutoShowsService
from car_dealership_system.celery import app


@app.task(bind=True)
def buy_cars_by_demand(self):
    with transaction.atomic():
        AutoShowsService().buy_cars_from_supplier()

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_dealership_system.settings.settings")

from celery import Celery  # type: ignore
from celery.beat import crontab  # type: ignore

from car_dealership_system.settings.celery import CELERY

app = Celery("car_dealership_system")
app.config_from_object(CELERY)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "autoshow_buy_cars_from_dealers": {
        "task": "apps.autoshows.tasks.buy_cars_by_demand",
        "schedule": crontab(minute="*/1"),
    },
    "customer_buy_car_from_offer": {
        "task": "apps.customers.tasks.buy_car_from_autoshow",
        "schedule": crontab(minute="*/3"),
    },
}

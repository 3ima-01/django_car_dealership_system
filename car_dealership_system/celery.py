import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_dealership_system.settings.settings")

from celery import Celery

from car_dealership_system.settings.celery import CELERY

app = Celery("car_dealership_system")
app.config_from_object(CELERY)

app.autodiscover_tasks()

import sys

from django.conf import settings

from car_dealership_system.settings.config import config

TESTING = "test" in sys.argv
TESTING = TESTING or "test_coverage" in sys.argv or "pytest" in sys.modules

CELERY = {
    "broker_url": config.redis.REDIS_URL,
    "task_always_eager": TESTING,
    "timezone": settings.TIME_ZONE,
    "result_backend": "django-db",
    "result_extended": True,
    "task_track_started": True,
}

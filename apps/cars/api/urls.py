from django.urls import path

from apps.cars.api.views.cars import CarsAPIView

app_name = "cars"

urlpatterns = [
    path("cars/", CarsAPIView.as_view(), name="cars-list"),
    path("cars/<uuid:id>/", CarsAPIView.as_view(), name="cars-detail"),
]

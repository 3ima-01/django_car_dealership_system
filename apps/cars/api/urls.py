from django.urls import path

from apps.cars.api.views.cars import CarsDetailView, CarsListView

app_name = "cars"

urlpatterns = [
    path("cars/", CarsListView.as_view(), name="cars-list"),
    path("cars/<uuid:id>/", CarsDetailView.as_view(), name="cars-detail"),
]

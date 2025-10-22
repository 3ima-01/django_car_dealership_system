from django.urls import path

from apps.autoshows.api.views.autoshows import AutoShowsAPIView
from apps.autoshows.api.views.autoshows_stock import AutoShowsStockAPIView

app_name = "autoshows"

urlpatterns = [
    path("auto-shows/", AutoShowsAPIView.as_view(), name="auto-shows-list"),
    path("auto-shows/<uuid:id>/", AutoShowsAPIView.as_view(), name="auto-shows-detail"),
    path("auto-shows/<uuid:id>/stock", AutoShowsStockAPIView.as_view(), name="auto-show-stock"),
]

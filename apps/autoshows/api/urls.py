from django.urls import path

from apps.autoshows.api.views.autoshows import AutoShowsDetailView, AutoShowsListView
from apps.autoshows.api.views.autoshows_stock import AutoShowsStockAPIView

app_name = "autoshows"

urlpatterns = [
    path("auto-shows/", AutoShowsListView.as_view(), name="auto-shows-list"),
    path("auto-shows/<uuid:id>/", AutoShowsDetailView.as_view(), name="auto-shows-detail"),
    path("auto-shows/<uuid:id>/stock", AutoShowsStockAPIView.as_view(), name="auto-show-stock"),
]

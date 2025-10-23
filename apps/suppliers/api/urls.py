from django.urls import path

from apps.suppliers.api.views.suppliers import SuppliersAPIView
from apps.suppliers.api.views.suppliers_stock import SuppliersStockAPIView

app_name = "suppliers"

urlpatterns = [
    path("suppliers/", SuppliersAPIView.as_view(), name="suppliers-list"),
    path("suppliers/<uuid:id>/", SuppliersAPIView.as_view(), name="suppliers-detail"),
    path("suppliers/<uuid:id>/stock", SuppliersStockAPIView.as_view(), name="suppliers-stock"),
]

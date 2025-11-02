from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.api.views.accounts import AccountsViewSet
from apps.autoshows.api.views.autoshows import AutoShowsViewSet
from apps.autoshows.api.views.autoshows_stock import AutoShowsStockViewSet
from apps.cars.api.views.cars import CarsViewSet
from apps.suppliers.api.views.suppliers import SuppliersViewSet
from apps.suppliers.api.views.suppliers_stock import SuppliersStockViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Car Dealership Sysytem API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"cars", CarsViewSet, basename="cars")
router.register(r"accounts", AccountsViewSet, basename="accounts")
router.register(r"suppliers", SuppliersViewSet, basename="suppliers")
router.register(r"autoshows", AutoShowsViewSet, basename="autoshows")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(router.urls)),
]

nested_urls = [
    path(
        "suppliers/<uuid:supplier_id>/stock/",
        SuppliersStockViewSet.as_view({"get": "list", "post": "create"}),
        name="supplier-stock-list",
    ),
    path(
        "suppliers/<uuid:supplier_id>/stock/<uuid:pk>/",
        SuppliersStockViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="supplier-stock-detail",
    ),
    path(
        "api/v1/autoshows/<uuid:autoshow_id>/stock/",
        AutoShowsStockViewSet.as_view({"get": "list"}),
        name="autoshow-stock-list",
    ),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns += nested_urls

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
